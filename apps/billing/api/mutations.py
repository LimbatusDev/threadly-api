import logging

import graphene
from django.conf import settings
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from qvapay.v1 import SyncQvaPayClient

from apps.billing.constants import BillingTypes, BILLING
from apps.billing.models import BillingConfig, Transaction

logger = logging.getLogger(__name__)


class CreateInvoice(graphene.Mutation):
    url = graphene.String()

    class Arguments:
        billing_type = graphene.String()

    @staticmethod
    @login_required
    def mutate(root, info, billing_type):
        if billing_type != BillingTypes.YEARLY and billing_type != BillingTypes.MONTHLY:
            return GraphQLError('BillingType should be monthly or yearly')

        client = SyncQvaPayClient(app_id=settings.QVAPAY_APP_ID, app_secret=settings.QVAPAY_APP_SECRET)
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
            logger.warning('secret is incorrect')
            return GraphQLError('secret is incorrect!')

        try:
            # get the Transaction
            transaction = Transaction.objects.get(number=remote_id)
            if transaction.state == BILLING.CONFIRMED:
                logger.info('Already paid')
                return ConfirmTransaction(status=False)
            if transaction.state == BILLING.CANCELLED:
                logger.info('Already cancelled')
                return ConfirmTransaction(status=False)

            # get the invoice
            client = SyncQvaPayClient(app_id=settings.QVAPAY_APP_ID, app_secret=settings.QVAPAY_APP_SECRET)
            invoice = client.get_transaction(transaction_uuid)

            # check if the transaction and invoice amount match
            if invoice.amount != transaction.amount:
                logger.warning(
                    'Invoice ({}) and transaction ({}) amount don\'t match'.format(invoice.amount, transaction.amount)
                )
                return ConfirmTransaction(status=False)
            # check if invoice remote id and transaction number match
            if invoice.remote_id != transaction.number:
                logger.warning(
                    'Paid invoice ({}) no match width transaction id ({})'.format(invoice.remote_id, transaction.number)
                )
                return ConfirmTransaction(status=False)
            # check if the invoice status is paid
            if invoice.status == 'paid':
                transaction.state = BILLING.CONFIRMED
                transaction.save()
                info.context.user.extend_premium(transaction.days)
                return ConfirmTransaction(status=True)
            else:
                logger.info('invoice status isn\'t paid')
                return ConfirmTransaction(status=False)
        # transaction id don't exists
        except Transaction.DoesNotExist:
            logger.info('remote id incorrect')
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
        try:
            transaction = Transaction.objects.get(number=remote_id)
            if transaction.state == BILLING.PENDING:
                transaction.state = BILLING.CANCELLED
                transaction.save()
                return CancelTransaction(status=True)
            else:
                logger.warning('Transaction ({}) already {}'.format(transaction.id, transaction.state))
                return CancelTransaction(status=False)
        except Transaction.DoesNotExist:
            return CancelTransaction(status=False)


class BillingMutations:
    create_invoice = CreateInvoice.Field()
    confirm_transaction = ConfirmTransaction.Field()
    cancel_transaction = CancelTransaction.Field()
