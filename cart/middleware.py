from django.http import HttpRequest
from django.urls import resolve
from .models import Cart


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Check if the request is destined for the 'cart' app
        # resolver_match = resolve(request.path)
        # print(f'=====> {resolver_match.app_name=} <=====')
        # if resolver_match.app_name in {"cart", "store", "admin"}:
        if not request.session.get("cart_id"):
            if request.user.is_authenticated:
                user_cart = Cart.objects.filter(owner=request.user).first()
                if not user_cart:
                    self.create_new_cart(request)
                else:
                    request.session["cart_id"] = user_cart.cart_id
            else:
                self.create_new_cart(request)

        response = self.get_response(request)
        return response

    def create_new_cart(self, request: HttpRequest):
        if not request.session.session_key:
            request.session.create()
        cart_id = request.session.session_key
        Cart.objects.get_or_create(cart_id=cart_id, owner=request.user if request.user.is_authenticated else None)