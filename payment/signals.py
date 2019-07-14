from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from orders.models import Order


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # payment was successful
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        # mark the order as paid
        order.paid = True
        order.save()


# We connect the payment_notification receiver function to the valid_ipn_
# received signal provided by django-paypal. The receiver function works
# as follows:
# 1. We receive the sender object, which is an instance of the PayPalIPN model
# defned in paypal.standard.ipn.models.
# 2. We check the payment_status attribute to make sure it equals the completed
# status of django-paypal. This status indicates that the payment was
# successfully processed.
# 3. Then we use the get_object_or_404() shortcut function to get the order
# whose ID matches the invoice parameter we provided for PayPal.
# 4. We mark the order as paid by setting its paid attribute to True and saving
# the Order object to the database.
valid_ipn_received.connect(payment_notification)
