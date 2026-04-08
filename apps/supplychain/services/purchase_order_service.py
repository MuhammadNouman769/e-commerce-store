from apps.supplychain.models import PurchaseOrder, PurchaseOrderItem, Supplier
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class PurchaseOrderService:

    @staticmethod
    @transaction.atomic
    def create_purchase_order(supplier_id, expected_delivery_date, notes=""):
        supplier = Supplier.objects.get(id=supplier_id)
        po = PurchaseOrder.objects.create(
            supplier=supplier,
            expected_delivery_date=expected_delivery_date,
            notes=notes
        )
        return po

    @staticmethod
    @transaction.atomic
    def add_item(po_id, product, quantity, unit_price):
        po = PurchaseOrder.objects.get(id=po_id)
        item = PurchaseOrderItem.objects.create(
            purchase_order=po,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            total_price=quantity * unit_price
        )
        # Update total amount of PO
        po.total_amount = sum(i.total_price for i in po.items.all())
        po.save()
        return item

    @staticmethod
    @transaction.atomic
    def update_status(po_id, status):
        po = PurchaseOrder.objects.get(id=po_id)
        po.status = status
        po.save()
        return po

    @staticmethod
    def get_po_by_id(po_id):
        try:
            return PurchaseOrder.objects.get(id=po_id)
        except ObjectDoesNotExist:
            return None