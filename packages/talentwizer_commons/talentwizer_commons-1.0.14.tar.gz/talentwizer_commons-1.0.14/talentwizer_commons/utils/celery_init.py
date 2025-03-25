import os
import json
from celery import Celery, signals
from celery.states import PENDING, SUCCESS, FAILURE
from kombu import Queue, Exchange
from datetime import datetime
import logging
from typing import Dict, Any
from talentwizer_commons.utils.db import mongo_database
from .core import redis_client, get_redis_url
from .sequence_utils import (
    process_scheduled_email
)

logger = logging.getLogger(__name__)

# Initialize Celery with proper name 
celery_app = Celery('talentwizer_commons.utils.celery_init')

# Configure Celery
celery_app.conf.update(
    broker_url=get_redis_url(),
    result_backend=get_redis_url(),
    broker_connection_retry_on_startup=True,
    imports=['talentwizer_commons.utils.celery_init'],
    task_track_started=True,
    task_ignore_result=False,
    task_routes={
        'send_scheduled_email': {
            'queue': 'email_queue',
            'exchange': 'email'
        }
    }
)

# Define queues
default_exchange = Exchange('default', type='direct')
email_exchange = Exchange('email', type='direct')

celery_app.conf.task_queues = (
    Queue('celery', default_exchange, routing_key='celery'),
    Queue('email_queue', email_exchange, routing_key='email.#'),
)

# MongoDB collections
sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]

@celery_app.task(name='send_scheduled_email')
def send_scheduled_email(email_payload: dict, user_email: str, scheduled_time: str = None):
    """Send a scheduled email."""
    try:
        logger.info(f"Starting scheduled email task at {datetime.now()}")
        logger.info(f"Email payload: {email_payload}")
        
        if scheduled_time:
            scheduled_dt = datetime.fromisoformat(scheduled_time)
            now = datetime.utcnow()
            
            # If it's not time yet, defer the task
            if scheduled_dt > now:
                delay = (scheduled_dt - now).total_seconds()
                logger.info(f"Deferring email for {delay} seconds (scheduled: {scheduled_dt}, now: {now})")
                
                # Re-schedule the task with same arguments
                send_scheduled_email.apply_async(
                    kwargs={
                        'email_payload': email_payload,
                        'user_email': user_email,
                        'scheduled_time': scheduled_time
                    },
                    eta=scheduled_dt
                )
                return {'status': 'deferred', 'scheduled_time': scheduled_time}

        # Process the email if it's time
        result = process_scheduled_email(email_payload, user_email)
        return result

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}", exc_info=True)
        raise

# Use a simpler singleton pattern
_task_restore_complete = False

@celery_app.task(bind=True, name='restore_persisted_tasks')
def restore_persisted_tasks(self):
    """Task to restore persisted tasks on worker startup."""
    global _task_restore_complete
    
    if (_task_restore_complete):
        logger.info("Tasks already restored, skipping...")
        return 0

    try:
        from .sequence_utils import restore_tasks  # Import here to avoid circular imports
        result = restore_tasks()
        _task_restore_complete = True
        return result
    except Exception as e:
        logger.error(f"Task restoration failed: {str(e)}")
        return 0

@signals.worker_ready.connect
def on_worker_ready(sender, **kwargs):
    """Run task restoration exactly once when worker is ready."""
    global _task_restore_complete
    if not _task_restore_complete:
        restore_persisted_tasks.apply_async(countdown=5)

@signals.task_sent.connect
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    """Handle task sent event."""
    task_id = headers.get('id') if headers else None
    if task_id:
        try:
            task_data = {
                'status': PENDING,
                'sent': datetime.utcnow().isoformat()
            }
            redis_client.set(
                f'flower:task:{task_id}',
                json.dumps(task_data),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_sent_handler: {str(e)}")

@signals.task_received.connect
def task_received_handler(sender=None, request=None, **kwargs):
    """Handle task received event."""
    if request and request.id:
        try:
            task_data = {
                'status': PENDING,
                'received': datetime.utcnow().isoformat()
            }
            redis_client.set(  # Now redis_client is properly imported
                f'flower:task:{request.id}',
                json.dumps(task_data),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_received_handler: {str(e)}")

@signals.task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    """Handle task success event."""
    if sender and sender.request.id:
        try:
            task_data = {
                'status': SUCCESS,
                'result': str(result),
                'completed': datetime.utcnow().isoformat()
            }
            redis_client.set(
                f'flower:task:{sender.request.id}',
                json.dumps(task_data),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_success_handler: {str(e)}")

@signals.task_failure.connect
def task_failure_handler(sender=None, exception=None, **kwargs):
    """Handle task failure event."""
    if sender and sender.request.id:
        try:
            task_data = {
                'status': FAILURE,
                'error': str(exception),
                'failed': datetime.utcnow().isoformat()
            }
            redis_client.set(
                f'flower:task:{sender.request.id}',
                json.dumps(task_data),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_failure_handler: {str(e)}")

# Export key components
__all__ = [
    'celery_app',
    'send_scheduled_email',
    'restore_persisted_tasks'
]