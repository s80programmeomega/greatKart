from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = [
        "product_name",
        "price",
        "stock",
        "category",
        "thumbnail_preview",
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

    def thumbnail_preview(self, obj: Product):
        if obj.product_image:
            return format_html(
                f'<a href={obj.product_image.url}><img src="{obj.product_image.url}" style="width: 50px; height: 50px;" /></a>',
            )
        return "No Thumbnail"

    thumbnail_preview.short_description = (
        "Thumbnail Preview"  # Set column header in the admin panel
    )


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
