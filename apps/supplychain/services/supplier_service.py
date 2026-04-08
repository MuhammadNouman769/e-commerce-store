from apps.supplychain.models import Supplier, SupplierProduct
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

class SupplierService:
    
    @staticmethod
    def create_supplier(name, code, supplier_type, contact_person, email, phone, address):
        supplier = Supplier.objects.create(
            name=name,
            code=code,
            supplier_type=supplier_type,
            contact_person=contact_person,
            email=email,
            phone=phone,
            address=address
        )
        return supplier

    @staticmethod
    def update_supplier(supplier_id, **kwargs):
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            for key, value in kwargs.items():
                setattr(supplier, key, value)
            supplier.save()
            return supplier
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def add_product_to_supplier(supplier_id, product, cost_price, lead_time_days=7, min_order_qty=1, preferred=False):
        supplier = Supplier.objects.get(id=supplier_id)
        sp, created = SupplierProduct.objects.get_or_create(
            supplier=supplier,
            product=product,
            defaults={
                'cost_price': cost_price,
                'lead_time_days': lead_time_days,
                'minimum_order_quantity': min_order_qty,
                'is_preferred': preferred
            }
        )
        if not created:
            sp.cost_price = cost_price
            sp.lead_time_days = lead_time_days
            sp.minimum_order_quantity = min_order_qty
            sp.is_preferred = preferred
            sp.save()
        return sp