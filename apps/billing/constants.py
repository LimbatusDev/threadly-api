class BILLING:
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'


BILLING_STATE = (
    (BILLING.PENDING, 'Pending'),
    (BILLING.CONFIRMED, 'Confirmed'),
    (BILLING.CANCELLED, 'Cancelled')
)


class BillingTypes:
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
