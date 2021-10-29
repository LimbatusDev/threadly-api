import graphene
from graphql_jwt.decorators import login_required

from apps.threads.utils import send_thread


class TwitterThread(graphene.Mutation):
    status = graphene.Boolean()
    tweet_url = graphene.String()

    class Arguments:
        thread = graphene.List(graphene.String)

    @staticmethod
    @login_required
    def mutate(root, info, thread):
        url = send_thread(info.context.user, thread)
        return TwitterThread(status=url is not None, tweet_url=url)


class ThreadMutations(graphene.ObjectType):
    # post twitter thread
    tweet_post = TwitterThread.Field()
