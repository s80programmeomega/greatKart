from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "id",
        "email",
        "username",
        "user_type",
    )
    list_filter = ("user_type", "email", "username")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("username",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        # ("Important Dates", {"fields": ("last_login", "date_joined", "last_modified")}),
        ("User Type", {"fields": ("user_type",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "username",
                    "user_type",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)

    def save_model(self, request, obj, form, change):
        # Hash the password if it is being set or updated
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)


# Register the custom user model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = (
        "id",
        "user",
        "profile_picture",
        "thumbnail_preview",
    )
    list_display_links = ("id", "user")
    list_filter = ("user",)
    # fieldsets = (
    #     (None, {"fields": ("user", "profile_picture")}),
    #     ("Thumbnail", {"fields": ("thumbnail",)}),
    # )
    search_fields = ("user",)
    ordering = ("id",)
    
    readonly_fields = ("user", "thumbnail",)
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px;" />', obj.thumbnail.url
            )
        return "No Thumbnail"

    thumbnail_preview.short_description = (
        "Thumbnail Preview"  # Set column header in the admin panel
    )


admin.site.register(UserProfile, UserProfileAdmin)
