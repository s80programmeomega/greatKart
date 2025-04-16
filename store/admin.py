from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html

from .models import Product, Variation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = [
        "pk",
        "product_name",
        "price",
        "stock",
        "category",
        "thumbnail_preview",
        "last_modified",
        "is_available",
    ]
    list_display_links = [
        "pk",
        "product_name",
    ]
    list_filter = [
        "product_name",
        "price",
        "stock",
        "category",
        "last_modified",
        "is_available",
    ]

    def get_form(self, request: HttpRequest, obj: Product = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Field based permission example
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields["product_name"].disabled = True
            form.base_fields["product_image"].disabled = True
        return form

    def has_change_permission(self, request: HttpRequest, obj: Product = None) -> bool:
        if request.user.has_perm("store.add_product"):
            return True
        else:
            return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request: HttpRequest, obj: Product = None) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_view_permission(self, request: HttpRequest, obj: Product = None) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_module_permission(self, request: HttpRequest) -> bool:
        """
        Determines whether the user has permission to view the module in the admin interface.
        Args:
            request (HttpRequest): The HTTP request object containing user information.
        Returns:
            bool: True if the user is a superuser or a staff member, False otherwise.
        """

        return request.user.is_superuser or request.user.is_staff

    def thumbnail_preview(self, obj: Product):
        if obj.product_image:
            return format_html(
                f'<a href={obj.product_image.url} target="_blank" ><img src="{obj.product_image.url}" style="width: 50px; height: 50px;" /></a>',
            )
        return "No Thumbnail"

    thumbnail_preview.short_description = (
        "Thumbnail Preview"  # Set column header in the admin panel
    )


class VariationAdmin(admin.ModelAdmin):
    list_display = ["variation_category",
                    "variation_value", "product", "is_active"]
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


# admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
