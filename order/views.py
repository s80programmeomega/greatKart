from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from cart.models import Cart, CartItem
from cart.views import get_cart_id
from order.forms import OrderForm

from datetime import datetime


def checkout_order(request: HttpRequest):
    cart = Cart.objects.get(cart_id=get_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    return render(request, "order/place-order.html", {"cart_items": cart_items})


def place_order(request: HttpRequest):
    cart = Cart.objects.get(cart_id=get_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    order_total = sum([item.sub_total() for item in cart_items])
    tax = order_total*2/100
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.ip = request.META.get("REMOTE_ADDR")
            order.order_total = order_total
            order.tax = tax
            order.save()
            messages.success(
                request, "Your order has been placed successfully!", extra_tags="success"
            )
            print(f"====>\n {vars(order)} \n<====")
            print(str(datetime.today().date()).split("-"))
            return redirect("order:place_order")
            # return render(request, "order/order_complete.html", {"form": form, "cart_items": cart_items})
        else:
            messages.error(request, "Error placing order.",
                           extra_tags="danger")
    else:
        form = OrderForm()
        return render(request, "order/place-order.html", {"form": form, "order_total": order_total, "tax": tax, "cart_items": cart_items, "total":order_total+tax})
