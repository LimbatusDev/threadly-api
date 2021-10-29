import graphene

from apps.threads.tasks import my_task


class TestMutate(graphene.Mutation):
    status = graphene.Boolean()

    class Arguments:
        pass

    @staticmethod
    def mutate(root, info):
        my_task.delay(1, 2)
        return TestMutate(status=True)


class ThreadMutations(graphene.ObjectType):
    testing = TestMutate.Field()
