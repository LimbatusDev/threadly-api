import graphene
from graphene_django import DjangoObjectType

from apps.accounts import models


class UserType(DjangoObjectType):
    is_premium = graphene.Boolean()

    class Meta:
        model = models.User
    
    @staticmethod
    def resolve_is_premium(parent, info):
        return parent.is_premium()


user_types = [
    UserType
]
