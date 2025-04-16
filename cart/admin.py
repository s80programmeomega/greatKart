from django.contrib import admin

from cart.models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ["cart_id", "date_added", "owner"]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "cart", "quantity", "is_active"]
    list_display_links = ["id", "product"]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
