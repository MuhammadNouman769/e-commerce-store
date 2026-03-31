# from django.contrib import admin
# from .models import Warehouse, InventoryItem, InventoryLevel



# # ===== Warehouse Admin =====
# class WarehouseAdmin(admin.ModelAdmin):
#     list_display = ("name", "address")
#     search_fields = ("name",)

# admin.site.register(Warehouse, WarehouseAdmin)


# # ===== Inventory Item Admin =====
# class InventoryItemAdmin(admin.ModelAdmin):
#     list_display = ("variant", "tracked", "cost_price")
#     list_filter = ("tracked",)
#     search_fields = ("variant__sku", "variant__barcode")

# admin.site.register(InventoryItem, InventoryItemAdmin)


# # ===== Inventory Level Admin =====
# class InventoryLevelAdmin(admin.ModelAdmin):
#     list_display = ("inventory_item", "warehouse", "available_quantity", "incoming_quantity")
#     list_filter = ("warehouse",)
#     search_fields = ("inventory_item__variant__sku",)

# admin.site.register(InventoryLevel, InventoryLevelAdmin)