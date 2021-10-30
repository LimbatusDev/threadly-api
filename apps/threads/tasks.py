import json

from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from .models import Thread
from .utils import send_thread

logger = get_task_logger(__name__)


@shared_task
def my_task(a, b):
    return a + b


@shared_task
def send_async_thread(thread_id: int) -> str:
    try:
        thread = Thread.objects.get(pk=thread_id)
        user = thread.author
        # process tweets
        tweets = json.loads(thread.tweets)
        return send_thread(user, tweets)
    except Thread.DoesNotExist:
        logger.error(f'No exist Thread with id "{thread_id}"')
    return ""
