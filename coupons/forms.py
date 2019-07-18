from django import forms
from django.utils.translation import gettext_lazy as _


# form that we are going to use for the user to enter a
# coupon code
class CouponApplyForm(forms.Form):
    code = forms.CharField(label=_('Coupon'))
