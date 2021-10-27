import graphene
from graphene import ObjectType

types = None


class Query(ObjectType):
    pass


class Mutation(ObjectType):
    pass


schema = graphene.Schema(
    types=types,
    query=Query,
    mutation=Mutation
)
