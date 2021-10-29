import graphene
import tweepy
from django.conf import settings
from django.contrib.auth import get_user_model
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_jwt.signals import token_issued
from graphql_jwt.utils import jwt_payload, jwt_encode

from apps.accounts.api.types import UserType
from apps.threads.utils import send_thread


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


class TwitterAuth(graphene.Mutation):
    """
    Login user
    """
    status = graphene.Boolean()
    token = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        oauth_verifier = graphene.String(required=True)
        request_token = graphene.String(required=True)

    def mutate(self, info, oauth_verifier, request_token):
        auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_KEY_SECRET)
        auth.request_token = {
            'oauth_token': request_token,
            'oauth_token_secret': oauth_verifier
        }
        try:
            # TODO: Check if this returns me the twitter user
            auth.get_access_token(oauth_verifier)
            api = tweepy.API(auth)

            twitter_user = api.verify_credentials()
            try:
                profile_banner_url = twitter_user.profile_banner_url
            except:
                profile_banner_url = ''
            try:
                profile_image_url = twitter_user.profile_image_url
            except:
                profile_image_url = ''

            user, created = get_user_model().objects.get_or_create(
                username=twitter_user.screen_name,
                defaults={
                    'first_name': twitter_user.name,
                    'banner_url': profile_banner_url,
                    'image_url': profile_image_url,
                    'twitter_token': auth.access_token,
                    'twitter_token_secret': auth.access_token_secret,
                }
            )
            payload = jwt_payload(user)
            token = jwt_encode(payload)

            token_issued.send(
                sender='TokenAuth',
                request=info.context,
                user=user
            )
            return TwitterAuth(status=True, token=token, user=user)
        except tweepy.TweepyException as e:
            print(e)
            return GraphQLError('Error! Failed to get access token.')


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


class UserMutations(graphene.ObjectType):
    # authenticate with twitter
    twitter_login = TwitterLoginUrl.Field()

    # authenticate the User with its username or email and password to obtain the JSON Web token.
    token_auth = TwitterAuth.Field()

    # post twitter thread
    tweetPost = TwitterThread.Field()
