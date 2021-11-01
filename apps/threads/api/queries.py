import graphene
from django.db.models import Q
from django.utils import timezone
from graphql_jwt.decorators import login_required

from .types import ThreadType
from ..models import Thread


class ThreadQueries:
    queues = graphene.List(ThreadType)

    @login_required
    def resolve_queues(self, info, **kwargs):
        return Thread.objects.filter(Q(author=info.context.user) & Q(pub_date__gt=timezone.now())).order_by('pub_date')
