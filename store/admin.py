from django.contrib import admin
from .models import Product, Variation



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = [
        "product_name",
        "price",
        "stock",
        "category",
        "modified_date",
        "is_available",
    ]
    list_filter = [
        "product_name",
        "price",
        "stock",
        "category",
        "modified_date",
        "is_available",
    ]


class VariationAdmin(admin.ModelAdmin):
    list_display = ["variation_category", "variation_value", "product", "is_active"]
    list_editable = ("is_active",)
    list_filter = [
        "variation_category",
        "variation_value",
        "product",
    ]
    list_display_links = [
        "variation_value",
        "variation_category",
        "product",
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
