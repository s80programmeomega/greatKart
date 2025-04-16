from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path("checkout/", views.checkout_order, name="checkout_order"),
    path("place_order/", views.place_order, name="place_order"),
    # path("order_complete/", views.order_complete, name="order_complete"),
    # path("payment/", views.payment, name="payment"),
    # path("order_history/", views.order_history, name="order_history"),
]
