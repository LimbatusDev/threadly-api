import graphene
from django.conf import settings
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from qvapay.v1 import QvaPayClient

from apps.billing.constants import BillingTypes
from apps.billing.models import BillingConfig, Transaction


class CreateInvoice(graphene.Mutation):
    url = graphene.String()

    class Arguments:
        billing_type = graphene.String()

    @staticmethod
    @login_required
    def mutate(root, info, billing_type):
        if billing_type != BillingTypes.YEARLY and billing_type != BillingTypes.MONTHLY:
            return GraphQLError('BillingType should be monthly or yearly')

        client = QvaPayClient(app_id=settings.QVAPAY_APP_ID, app_secret=settings.QVAPAY_APP_SECRET)
        config = BillingConfig.load()
        price_monthly = config.price_monthly
        price_yearly = config.price_yearly

        amount = price_monthly if billing_type == 'monthly' else price_yearly
        days = 30 if billing_type == 'monthly' else 360
        description = 'Threadly App Mensual' if billing_type == 'monthly' else 'Threadly App Anual'

        transaction = Transaction.objects.create(
            user=info.context.user,
            amount=amount,
            days=days
        )

        invoice = client.create_invoice(
            amount=amount,
            description=description,
            remote_id=transaction.number
        )
        return CreateInvoice(url=invoice.url)


class ConfirmTransaction(graphene.Mutation):
    status = graphene.Boolean()

    class Arguments:
        token = graphene.String()
        remote_id = graphene.String()
        transaction_uuid = graphene.String()

    @staticmethod
    @login_required
    def mutate(root, info, token, remote_id, transaction_uuid):
        if token != settings.SECRET_TOKEN:
            return GraphQLError('secret is incorrect!')

        client = QvaPayClient(app_id=settings.QVAPAY_APP_ID, app_secret=settings.QVAPAY_APP_SECRET)
        invoice = client.get_transaction(transaction_uuid)

        try:
            transaction = Transaction.objects.get(number=remote_id)
            if transaction.state == 'confirmed':
                print('Already paid')
                return ConfirmTransaction(status=False)

            transaction.state = 'confirmed'
            transaction.save()
            info.context.user.extend_premium(transaction.days)
            return ConfirmTransaction(status=True)
        except Transaction.DoesNotExist:
            print('remote id incorrect')
            return ConfirmTransaction(status=False)


class CancelTransaction(graphene.Mutation):
    status = graphene.Boolean()

    class Arguments:
        token = graphene.String()
        remote_id = graphene.String()

    @staticmethod
    def mutate(root, info, token, remote_id):
        if token != settings.SECRET_TOKEN:
            return GraphQLError('secret is incorrect!')

        return CancelTransaction(status=True)


class BillingMutations:
    create_invoice = CreateInvoice.Field()
    confirm_transaction = ConfirmTransaction.Field()
    cancel_transaction = CancelTransaction.Field()
