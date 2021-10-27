import graphene
from graphene import ObjectType

from apps.accounts.api.mutations import UserMutations
from apps.accounts.api.queries import UserQueries
from apps.accounts.api.types import user_types

types = user_types


class Query(ObjectType, UserQueries):
    pass


class Mutation(UserMutations, ObjectType):
    pass


schema = graphene.Schema(
    types=types,
    query=Query,
    mutation=Mutation
)
