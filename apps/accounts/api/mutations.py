import graphene
import tweepy
from django.conf import settings
from graphql import GraphQLError

from apps.accounts.api.types import UserType


class TwitterLoginUrl(graphene.Mutation):
    """
    Get Twitter login url
    """
    status = graphene.Boolean()
    url = graphene.String()
    oauth_token = graphene.String()

    class Arguments:
        callback_url = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, callback_url):
        auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_KEY_SECRET, callback_url)

        try:
            redirect_url = auth.get_authorization_url()
            return TwitterLoginUrl(status=True, url=redirect_url, oauth_token=auth.request_token['oauth_token'])
        except tweepy.TweepyException as e:
            print(e)
            return GraphQLError('Error fetching Twitter authorization url')


class TokenAuth(graphene.Mutation):
    """
    Login user
    """
    ok = graphene.Boolean()
    token = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        pass


class UserMutations(graphene.ObjectType):
    # authenticate with twitter
    twitter_login = TwitterLoginUrl.Field()

    # authenticate the User with its username or email and password to obtain the JSON Web token.
    token_auth = TokenAuth.Field()
