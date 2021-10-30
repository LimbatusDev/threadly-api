import graphene
from graphene import ObjectType

from apps.accounts.api.mutations import UserMutations
from apps.accounts.api.queries import UserQueries
from apps.accounts.api.types import user_types
from apps.billing.api.mutations import BillingMutations
from apps.threads.api.mutations import ThreadMutations
from apps.threads.api.queries import ThreadQueries

types = user_types


class Query(ObjectType, UserQueries, ThreadQueries):
    pass


class Mutation(UserMutations, ThreadMutations, BillingMutations, ObjectType):
    pass


schema = graphene.Schema(
    types=types,
    query=Query,
    mutation=Mutation
)
