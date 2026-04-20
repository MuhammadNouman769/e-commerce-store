from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.users import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # ================= LIST PAGE =================
    list_display = (
        "email",
        "phone",
        "role",
        "email_verified",
        "phone_verified",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "email_verified",
        "phone_verified",
    )

    search_fields = ("email", "phone")
    ordering = ("email",)

    # ================= DETAIL PAGE =================
    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),

        ("Personal Info", {
            "fields": ("first_name", "last_name", "profile_picture")
        }),

        ("Verification", {
            "fields": ("email_verified", "phone_verified")
        }),

        ("Role & Status", {
            "fields": ("role", "account_status")
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
            )
        }),

        ("System Info", {
            "fields": ("last_login", "last_login_ip")
        }),
    )

    # ================= ADD USER FORM =================
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