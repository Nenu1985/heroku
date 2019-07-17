from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        return redirect('cart:cart-detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart-detail')


def cart_detail(request):
    cart = Cart(request)

    # create an instance of CartAddProductForm for each item in the cart to allow
    # changing product quantities. We initialize the form with the current item quantity
    # and set the update feld to True so that when we submit the form to the cart_add
    # view, the current quantity is replaced with the new one
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})

    coupon_apply_form = CouponApplyForm()

    return render(request, 'cart/detail.html', {'cart': cart,
                                                'coupon_apply_form': coupon_apply_form,
                                                })
