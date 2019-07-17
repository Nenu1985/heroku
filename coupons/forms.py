from django import forms


# form that we are going to use for the user to enter a
# coupon code
class CouponApplyForm(forms.Form):
    code = forms.CharField()
