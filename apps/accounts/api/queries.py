import graphene
import tweepy
from django.conf import settings
from django.contrib.auth import get_user_model
from graphql import GraphQLError

from .types import UserType


class UserQueries:
    me = graphene.Field(UserType)

    def resolve_me(self, info, **kwargs):
        return info.context.user
