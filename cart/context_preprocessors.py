from django.http import HttpRequest

from cart.models import Cart, CartItem

from .views import get_cart_id


def get_cart_items(request: HttpRequest):
    cart_id = get_cart_id(request)
    print(f'cart_id ===> {cart_id}')
    cart = Cart.objects.filter(cart_id=cart_id)
    cart_items = CartItem.objects.all().filter(cart=cart[:1])
    quantity = 0
    for item in cart_items:
        quantity += item.quantity
    return {'cart_items_count': quantity}
