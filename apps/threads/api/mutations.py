import json
import logging

import graphene
from django.db.models import Q
from django.utils import timezone
from graphql_jwt.decorators import login_required

from apps.threads.models import Thread
from apps.threads.utils import send_thread, schedule_thread

logger = logging.getLogger(__name__)


class TwitterThread(graphene.Mutation):
    status = graphene.Boolean()
    tweet_url = graphene.String()

    class Arguments:
        thread = graphene.List(graphene.String)

    @staticmethod
    @login_required
    def mutate(root, info, thread: [str]):
        url = send_thread(info.context.user, thread)
        if url:
            user = info.context.user
            user.send_tweets(len(thread))
        return TwitterThread(status=url is not None, tweet_url=url)


class ScheduleThread(graphene.Mutation):
    status = graphene.Boolean()

    class Arguments:
        tweets = graphene.List(graphene.String)
        pub_date = graphene.DateTime()

    @staticmethod
    @login_required
    def mutate(root, info, tweets: [str], pub_date):
        thread = Thread.objects.create(
            tweets=json.dumps(tweets),
            author=info.context.user,
            pub_date=pub_date
        )
        schedule_thread(thread)
        return ScheduleThread(status=True)


class RemoveThread(graphene.Mutation):
    status = graphene.Boolean()

    class Arguments:
        thread_id = graphene.Int()

    @staticmethod
    @login_required
    def mutate(root, info, thread_id):
        try:
            thread = Thread.objects.get(Q(id=thread_id) & Q(pub_date__gte=timezone.now()))
            # check if this thread belongs to author or is admin how remove it
            if thread.author == info.context.user or info.context.user.is_superuser:
                thread.delete()
                return RemoveThread(status=True)
        except Thread.DoesNotExist:
            logger.warning('Future Thread with id {} no exist'.format(thread_id))
        return RemoveThread(status=False)


class ThreadMutations(graphene.ObjectType):
    # post twitter thread
    tweet_post = TwitterThread.Field()
    # schedule threads
    schedule_thread = ScheduleThread.Field()
    # remove scheduled thread
    remove_thread = RemoveThread.Field()
