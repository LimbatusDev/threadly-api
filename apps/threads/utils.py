import json
import uuid

import tweepy
from django.conf import settings
from django.contrib.auth import get_user_model
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from .constants import TASKS
from .models import Thread


def send_thread(user: get_user_model(), thread: [str]) -> str:
    """
    Send the thread to twitter and return the url of the first tweet
    """
    # check length of every tweet
    filtered = list(filter(lambda t: len(t) <= 280, thread))
    if len(thread) != len(filtered):
        # if length is incorrect return false
        return ""
    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_KEY_SECRET)
    auth.set_access_token(user.twitter_token, user.twitter_token_secret)
    api = tweepy.API(auth)

    # send the tweets
    reply_status = None
    url = None
    for tweet in thread:
        status = api.update_status(status=tweet, in_reply_to_status_id=reply_status)
        reply_status = status.id
        if not url:
            url = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"
    return url


def schedule_thread(thread: Thread):
    """
    Schedule the thread to the time saved
    """
    schedule, created = ClockedSchedule.objects.get_or_create(
        clocked_time=thread.pub_date
    )
    PeriodicTask.objects.create(
        clocked=schedule,
        name=str(uuid.uuid4()),
        task=TASKS.SEND_ASYNC_THREAD,
        args=json.dumps({
            'thread_id': thread.id,
        }),
        one_off=True,  # If True, the schedule will only run the task a single time
    )
    pass
