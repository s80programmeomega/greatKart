import re
from django.http import HttpRequest

from cart.models import Cart, CartItem

from .views import get_cart_id


def get_cart_items(request: HttpRequest):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(owner=request.user).first()
    else:
        cart = None
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        quantity = 0
        for item in cart_items:
            quantity += item.quantity
        return {'cart_items_count': quantity}
    else:
        return {'cart_items_count': 0}
    # print(f'User ===> {request.user}')
    # cart = Cart.objects.filter(owner=request.user)
    # cart_items = cart[0].cart_items.all()
    # print(f'cart ===> {cart}')
    # print(f'cart_tems ===> {cart_items}')
    # quantity = 0
    # for item in cart_items:
    #     quantity += item.quantity
    # return {'cart_items_count': quantity}
