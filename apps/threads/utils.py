import tweepy
from django.contrib.auth import get_user_model

from django.conf import settings


def send_thread(user: get_user_model(), thread: str):
    # check length of every tweet
    filtered = list(filter(lambda t: len(t) <= 280, thread))
    if len(thread) != len(filtered):
        # if length is incorrect return false
        return None
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
