from graphene_django import DjangoObjectType

from .. import models


class UserType(DjangoObjectType):
    class Meta:
        model = models.User


user_types = [
    UserType
]
