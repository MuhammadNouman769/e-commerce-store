from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # What you see in user list table
    list_display = ("email", "phone", "role", "is_active", "is_staff")
    list_filter = ("role", "is_staff", "is_active")

    # Fields shown when editing a user
    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Role Data", {"fields": ("role",)}),
    )

    # Fields shown when creating a new user from admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "phone",
                "role",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )

    search_fields = ("email", "phone")
    ordering = ("email",)
