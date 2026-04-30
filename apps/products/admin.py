from django.contrib import admin
from .models.shop import Shop

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner")
    search_fields = ("name", "owner__username") 
    
    
    