# apps/banners/admin.py
from django.contrib import admin
from apps.main.models import Banners

@admin.register(Banners)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("image", "is_active")
