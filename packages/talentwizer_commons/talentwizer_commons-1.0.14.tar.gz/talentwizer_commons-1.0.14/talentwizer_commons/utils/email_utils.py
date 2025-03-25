from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import logging
import json
from typing import Dict, Any
import asyncio
import base64
import email  # Add this import
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from talentwizer_commons.utils.db import mongo_database
from .core import celery_app, redis_client, check_redis_queue, get_redis_client
from .test_utils import get_test_delay
import os
import requests
from msal import ConfidentialClientApplication
import time
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)
sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]

MICROSOFT_GRAPH_URL = "https://graph.microsoft.com/v1.0"

class EmailQuotaExceeded(Exception):
    """Raised when email quota is exceeded."""
    pass

class EmailRateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    pass

def create_message(email_payload: dict, thread_id: str = None) -> dict:
    """Create email message with proper threading."""
    try:
        mime_msg = MIMEMultipart('alternative')
        mime_msg['to'] = ', '.join(email_payload['to_email'])
        mime_msg['from'] = email_payload.get('sender')
        
        # Add CC/BCC if present
        if email_payload.get('cc'):
            mime_msg['cc'] = ', '.join(email_payload['cc'])
        if email_payload.get('bcc'):
            mime_msg['bcc'] = ', '.join(email_payload['bcc'])
        
        # Handle threading for follow-up emails
        if not email_payload.get('is_initial') and thread_id:
            message_id = f"{thread_id}@mail.gmail.com"
            mime_msg['References'] = f"<{message_id}>"
            mime_msg['In-Reply-To'] = f"<{message_id}>"
            subject = email_payload.get('subject', '')
            if not subject.startswith('Re:'):
                subject = f"Re: {subject}"
            mime_msg['subject'] = subject
        else:
            mime_msg['subject'] = email_payload.get('subject', '')

        content = email_payload.get('content') or email_payload.get('body')

        # Add unsubscribe URL to content if enabled
        if email_payload.get('unsubscribe') and email_payload.get('sequence_id'):
            frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3001')
            unsubscribe_url = (
                f"{frontend_url}/unsubscribe"
                f"?sequence_id={email_payload['sequence_id']}"
                f"&public_identifier={email_payload['public_identifier']}"
            )
            unsubscribe_html = f"""
                <br><br>
                <div style="color: #666; font-size: 12px; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px;">
                    <p>Don't want to receive these emails? <a href="{unsubscribe_url}" style="color: #556bd8; text-decoration: underline;">Click here to unsubscribe</a></p>
                </div>
            """
            content += unsubscribe_html

        html_part = MIMEText(content, 'html', 'utf-8')
        mime_msg.attach(html_part)

        raw_message = base64.urlsafe_b64encode(mime_msg.as_bytes()).decode()
        
        message = {
            'raw': raw_message,
            'threadId': thread_id if thread_id else None
        }

        return message

    except Exception as e:
        logger.error(f"Error creating message: {str(e)}")
        raise

def build_gmail_service(token_data: dict):
    """Build Gmail service with proper error handling."""
    try:
        if not token_data:
            raise ValueError("Token data is required")

        required_fields = ['accessToken', 'clientId', 'clientSecret']
        missing_fields = [field for field in required_fields if not token_data.get(field)]
        
        if missing_fields:
            raise ValueError(f"Missing required token fields: {', '.join(missing_fields)}")

        scopes = [token_data.get('scope', 'https://www.googleapis.com/auth/gmail.send')]
        
        creds = Credentials(
            token=token_data["accessToken"],
            refresh_token=token_data.get("refreshToken"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=token_data["clientId"],
            client_secret=token_data["clientSecret"],
            scopes=scopes
        )

        return build('gmail', 'v1', credentials=creds)

    except Exception as e:
        logger.error(f"Failed to build Gmail service: {str(e)}", exc_info=True)
        raise

def build_email_service(token_data: dict):
    """Build appropriate email service based on provider."""
    provider = token_data.get('provider', '').lower()
    logger.debug(f"Building email service for provider: {provider}")
    
    if 'google' in provider:
        return build_gmail_service(token_data)
    elif 'microsoft' in provider or 'azure' in provider:
        return build_outlook_service(token_data)
    else:
        raise ValueError(f"Unsupported email provider: {provider}")

def build_outlook_service(token_data: dict):
    """Build Microsoft Graph API service wrapper."""
    return {
        'token': token_data['accessToken'],
        'user_email': token_data['email'],
        'base_url': MICROSOFT_GRAPH_URL
    }

def send_email_from_user_email_sync(token_data: dict, email_payload: dict) -> dict:
    """Send email using appropriate email service."""
    try:
        provider = token_data.get('provider', '').lower()
        logger.info(f"Sending email using provider: {provider}, token data: {token_data}")
        
        if not provider:
            raise ValueError("No provider found in token_data")

        # Build appropriate service
        service = build_email_service(token_data)
        
        # Create message in common format
        message = create_message(email_payload, email_payload.get('thread_id'))
        
        # Send using appropriate provider
        if 'google' in provider:
            logger.info("Using Gmail provider")
            # Fixed: Pass service first, then user_id, then message
            return send_message_gmail(service, 'me', message)
        elif 'microsoft' in provider or 'azure' in provider:
            logger.info("Using Microsoft provider")
            return send_message_outlook(message, service)
        else:
            raise ValueError(f"Unsupported email provider: {provider}")

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}", exc_info=True)
        raise

def send_message_gmail(service, user_id: str, message: dict) -> dict:
    """Send an email via Gmail API with proper thread handling."""
    try:
        if message.get('threadId'):
            message['threadId'] = message['threadId']
            logger.info(f"Added threadId to message body: {message['threadId']}")

        response = service.users().messages().send(
            userId=user_id,
            body=message
        ).execute()

        return {
            "status_code": 200,
            "message": "Email sent successfully",
            "threadId": response.get('threadId')
        }

    except Exception as e:
        logger.error(f"Error sending Gmail message: {str(e)}")
        raise

def send_message_outlook(message: dict, service: dict) -> dict:
    """Send message via Microsoft Graph API with rate limiting handling."""
    try:
        logger.info(f"Sending Outlook message with service: {service}")

        # Convert Gmail-style message to Microsoft Graph format
        msg_body = base64.urlsafe_b64decode(message['raw']).decode('utf-8')
        mime_msg = email.message_from_string(msg_body)

        # Extract recipients
        to_recipients = [{"emailAddress": {"address": addr.strip()}} 
                        for addr in mime_msg['to'].split(',') if addr.strip()]
        
        cc_recipients = []
        if mime_msg.get('cc'):
            cc_recipients = [{"emailAddress": {"address": addr.strip()}} 
                           for addr in mime_msg['cc'].split(',') if addr.strip()]
            
        bcc_recipients = []
        if mime_msg.get('bcc'):
            bcc_recipients = [{"emailAddress": {"address": addr.strip()}} 
                            for addr in mime_msg['bcc'].split(',') if addr.strip()]

        # Extract HTML content
        content = ""
        for part in mime_msg.walk():
            if part.get_content_type() == "text/html":
                content = part.get_payload(decode=True).decode()
                break

        # Construct Microsoft Graph API message format - Fix saveToSentItems placement
        graph_message = {
            "message": {
                "subject": mime_msg['subject'],
                "body": {
                    "contentType": "HTML",
                    "content": content
                },
                "toRecipients": to_recipients,
                "ccRecipients": cc_recipients,
                "bccRecipients": bcc_recipients
            },
            "saveToSentItems": True  # Move this outside of message object
        }

        # Add conversation/thread references if available
        if message.get('threadId'):
            graph_message["message"].update({
                "conversationId": message['threadId'],
                "internetMessageHeaders": [
                    {
                        "name": "Thread-Topic",
                        "value": mime_msg.get('subject', '').replace('Re: ', '')
                    },
                    {
                        "name": "Thread-Index",
                        "value": message['threadId']
                    }
                ]
            })

        headers = {
            'Authorization': f'Bearer {service["token"]}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Prefer': 'IdType="ImmutableId"'
        }

        max_retries = 3
        base_delay = 5  # Base delay in seconds
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{service['base_url']}/users/{service['user_email']}/sendMail",
                    headers=headers,
                    json=graph_message
                )

                if response.ok:
                    # Get the message ID and conversation ID
                    message_id = None
                    conversation_id = None

                    # First try to get message details using beta endpoint for more info
                    try:
                        messages_response = requests.get(
                            f"https://graph.microsoft.com/beta/users/{service['user_email']}/messages",
                            headers=headers,
                            params={
                                '$orderby': 'sentDateTime desc',
                                '$select': 'id,conversationId,subject,sentDateTime',
                                '$top': 1
                            }
                        )

                        if messages_response.ok:
                            messages = messages_response.json().get('value', [])
                            if messages:
                                latest_message = messages[0]
                                message_id = latest_message.get('id')
                                conversation_id = latest_message.get('conversationId')
                                logger.info(f"Found conversation ID from beta endpoint: {conversation_id}")
                    except Exception as e:
                        logger.warning(f"Failed to get conversation ID from beta endpoint: {str(e)}")

                    # If beta endpoint failed, try v1.0 endpoint
                    if not conversation_id and message.get('threadId'):
                        conversation_id = message['threadId']
                        logger.info(f"Using existing thread ID: {conversation_id}")

                    return {
                        'status_code': 200,
                        'message': 'Email sent successfully',
                        'threadId': conversation_id or message.get('threadId')
                    }

                error_data = response.json().get('error', {})
                error_code = error_data.get('code', '')
                error_msg = error_data.get('message', '')

                # Handle specific error cases
                if response.status_code == 429 or 'quota' in error_code.lower():
                    if 'ErrorExceededMessageLimit' in error_code:
                        raise EmailQuotaExceeded(
                            f"Daily email quota exceeded for {service['user_email']}: {error_msg}"
                        )
                    
                    # Calculate retry delay with exponential backoff
                    retry_after = int(response.headers.get('Retry-After', base_delay * (2 ** attempt)))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds before retry {attempt + 1}/{max_retries}")
                    time.sleep(retry_after)
                    continue

                # Other errors
                raise RequestException(f"Failed to send message: {response.status_code} - {response.text}")

            except (EmailQuotaExceeded, EmailRateLimitExceeded) as e:
                logger.error(str(e))
                raise

            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(base_delay * (2 ** attempt))

        raise RequestException("Max retries exceeded")

    except Exception as e:
        logger.error(f"Error sending Outlook message: {str(e)}", exc_info=True)
        raise

async def schedule_email(email_payload: dict, scheduled_time: datetime = None, token_data: dict = None) -> str:
    """Schedule an email to be sent at a specific time."""
    try:
        # Schedule task with correct name and metadata
        task = celery_app.send_task(
            'send_scheduled_email',
            kwargs={
                'email_payload': email_payload,
                'user_email': token_data.get('email'),
                'scheduled_time': scheduled_time.isoformat() if scheduled_time else None
            },
            eta=scheduled_time,
            queue='email_queue',
            routing_key='email.send'
        )
        
        return str(task.id)
    except Exception as e:
        logger.error(f"Failed to schedule email: {str(e)}", exc_info=True)
        raise
