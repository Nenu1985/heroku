from django.db import models
from django.db import models
from django.core.validators import MinValueValidator, \
    MaxValueValidator


# Create your models here.

class Coupon(models.Model):

    # The code that users have to enter in order to apply the
    # coupon to their purchase
    code = models.CharField(max_length=50,
                            unique=True)
    # The datetime value that indicates when the coupon
    # becomes valid
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    #  The discount rate to apply in %
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)])

    #  whether the coupon is active
    active = models.BooleanField()

    def __str__(self):
        return self.code
