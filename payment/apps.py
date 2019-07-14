from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'payment'

    # human readable format
    verbose_name = 'Payment'

    #  import the signals module in the ready() method
    # to make sure they are loaded when the application is initialized
    def ready(self):
        # import signal handlers
        import payment.signals
