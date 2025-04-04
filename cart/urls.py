from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_cart, name="cart"),
    path("add_cart/<int:product_id>", views.add_cart, name="add_cart"),
    path("remove_cart/<int:product_id>", views.remove_cart, name="remove_cart"),
    path(
        "remove_cart_item/<int:product_id>",
        views.remove_cart_item,
        name="remove_cart_item",
    ),
    path("place_order/", views.place_order, name="place_order"),
]
