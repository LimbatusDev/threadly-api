from graphene_django import DjangoObjectType

from apps.threads import models


class ThreadType(DjangoObjectType):
    class Meta:
        model = models.Thread


thread_types = [
    ThreadType
]
