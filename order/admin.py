from django.contrib import admin

from .models import Order, Payment, OrderProduct


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "payment_id",
        "user",
        "payment_method",
        "amount_paid",
        "status",
        "date_added",
        "last_modified",
    ]
    list_display_links = [
        "pk",
        "payment_id",
        "user",
    ]
    list_filter = [
        "user__username",
        "payment_method",
        "amount_paid",
        "status",
        "date_added",
        "last_modified",
    ]
    search_fields = [
        "user__username",
        "payment_method",
        "amount_paid",
        "status",
    ]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "order",
        "payment",
        "user",
        "product",
        "quantity",
        "price",
        "is_ordered",
    ]
    list_display_links = [
        "pk",
        "order",
        "payment",
    ]
    list_filter = [
        "user__username",
        "product__product_name",
        "is_ordered",
    ]
    search_fields = [
        "user__username",
        "product__product_name",
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "order_number",
        "user",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "address_line_1",
        "address_line_2",
        "country",
        "state",
        "city",
        "order_total",
        "status",
    ]
    list_display_links = [
        "pk",
        "order_number",
        "first_name",
    ]
    list_filter = [
        "status",
        "user__username",
        "first_name",
        "last_name",
        "email",
        "country",
        "state",
        "city",
        "order_total",
        "date_added",
        "last_modified",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "phone_number",
    ]
