from django.db import transaction
from django.utils import timezone
from apps.shipment_monitoring.models import Shipment, ShipmentTrackingLog
from apps.order_fulfillment.services.order_service import OrderService


class ShipmentService:

    def __init__(self, shipment: Shipment):
        self.shipment = shipment

    @transaction.atomic
    def update_status(self, status, location=None, description=None):

        old_status = self.shipment.status
        self.shipment.status = status

        if status == Shipment.ShipmentStatus.PICKED:
            self.shipment.shipped_date = timezone.now()

        if status == Shipment.ShipmentStatus.DELIVERED:
            self.shipment.delivered_date = timezone.now()

        self.shipment.save()

        ShipmentTrackingLog.objects.create(
            shipment=self.shipment,
            status=status,
            location=location or "",
            description=description or ""
        )

    @transaction.atomic
    def mark_as_delivered(self):
        self.update_status(Shipment.ShipmentStatus.DELIVERED)

        # update order via service (clean way)
        OrderService(self.shipment.order).mark_as_delivered()