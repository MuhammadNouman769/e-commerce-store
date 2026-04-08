from apps.supplychain.models import PurchaseOrderItem, PurchaseOrder
from django.db import transaction

class PurchaseOrderItemService:

    @staticmethod
    @transaction.atomic
    def update_quantity(item_id, new_quantity):
        item = PurchaseOrderItem.objects.get(id=item_id)
        item.quantity = new_quantity
        item.total_price = item.quantity * item.unit_price
        item.save()
        # Update PO total
        po = item.purchase_order
        po.total_amount = sum(i.total_price for i in po.items.all())
        po.save()
        return item

    @staticmethod
    @transaction.atomic
    def receive_item(item_id, received_qty):
        item = PurchaseOrderItem.objects.get(id=item_id)
        item.received_quantity += received_qty
        item.save()
        return item