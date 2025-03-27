from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "user_type",
    )
    list_filter = ("user_type", "email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
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
                    "first_name",
                    "last_name",
                    "user_type",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def save_model(self, request, obj, form, change):
        # Hash the password if it is being set or updated
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)


# Register the custom user model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
