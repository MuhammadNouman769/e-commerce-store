from django.contrib import admin
from apps.products.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "parent",
        "is_visible",
    )

    search_fields = ("name",)

    list_filter = ("is_visible",)