import graphene

from apps.accounts.api.types import UserType


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
    # authenticate the User with its username or email and password to obtain the JSON Web token.
    token_auth = TokenAuth.Field()
