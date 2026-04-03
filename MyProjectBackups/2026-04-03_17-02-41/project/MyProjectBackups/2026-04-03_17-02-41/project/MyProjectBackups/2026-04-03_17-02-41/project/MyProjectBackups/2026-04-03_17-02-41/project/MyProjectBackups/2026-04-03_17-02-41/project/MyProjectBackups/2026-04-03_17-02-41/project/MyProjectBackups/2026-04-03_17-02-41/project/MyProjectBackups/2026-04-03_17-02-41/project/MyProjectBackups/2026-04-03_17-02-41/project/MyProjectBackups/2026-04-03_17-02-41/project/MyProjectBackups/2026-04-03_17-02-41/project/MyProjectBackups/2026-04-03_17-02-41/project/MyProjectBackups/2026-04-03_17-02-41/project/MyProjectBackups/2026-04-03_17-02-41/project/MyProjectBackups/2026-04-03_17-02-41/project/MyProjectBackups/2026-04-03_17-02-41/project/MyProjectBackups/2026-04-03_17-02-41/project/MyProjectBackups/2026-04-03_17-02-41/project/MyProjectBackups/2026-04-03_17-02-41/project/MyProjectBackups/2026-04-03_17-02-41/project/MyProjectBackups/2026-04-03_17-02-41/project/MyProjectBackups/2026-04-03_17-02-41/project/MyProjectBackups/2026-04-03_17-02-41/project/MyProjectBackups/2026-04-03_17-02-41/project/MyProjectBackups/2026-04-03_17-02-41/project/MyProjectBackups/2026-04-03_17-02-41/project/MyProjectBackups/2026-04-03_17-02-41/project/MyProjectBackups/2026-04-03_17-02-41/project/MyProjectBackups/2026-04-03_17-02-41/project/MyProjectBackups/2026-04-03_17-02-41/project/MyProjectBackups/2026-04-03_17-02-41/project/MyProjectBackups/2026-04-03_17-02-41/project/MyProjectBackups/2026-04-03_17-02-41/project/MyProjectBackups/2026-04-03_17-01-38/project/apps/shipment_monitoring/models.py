"""
================================================================================
            SHIPMENT MONITORING MODELS - Customer Delivery Tracking
================================================================================
Purpose: Track shipments from warehouse to customer (Last Mile Delivery)
Author: Muhammad Nouman
================================================================================
"""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.utilities.models import BaseModel, TimeStampedModel
from apps.order_fulfillment.models import Order
from apps.products.models import ProductVariant
from apps.inventory_tracking.models import InventoryLevel

'''
=============================================================================
     1. SHIPMENT MODEL - Package Tracking to Customer
         Purpose: Track individual shipments from warehouse to customer
         When to use: When order is shipped, create a shipment record
=============================================================================
'''
class Shipment(TimeStampedModel, BaseModel):

    class ShipmentStatus(models.TextChoices):
        PENDING = "pending", _("Pending Dispatch")
        PICKED = "picked", _("Picked Up by Courier")
        IN_TRANSIT = "in_transit", _("In Transit")
        OUT_FOR_DELIVERY = "out_for_delivery", _("Out for Delivery")
        DELIVERED = "delivered", _("Delivered")
        FAILED = "failed", _("Delivery Failed")
        RETURNED = "returned", _("Returned to Sender")

    class CourierCompany(models.TextChoices):
        LEOPARDS = "leopards", _("Leopards Courier")
        TCS = "tcs", _("TCS")
        DHL = "dhl", _("DHL")
        PAKISTAN_POST = "pakistan_post", _("Pakistan Post")
        CALL_COURIER = "call_courier", _("Call Courier")
        OTHER = "other", _("Other")

    shipment_number = models.CharField(
        max_length=50, 
        unique=True, 
        editable=False
    )

    order = models.ForeignKey(
        "order_fulfillment.Order",
        on_delete=models.CASCADE,
        related_name="shipments"
    )

    courier_company = models.CharField(
        max_length=20, 
        choices=CourierCompany.choices
    )
    tracking_number = models.CharField(
        max_length=100
    )
    tracking_url = models.URLField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=ShipmentStatus.choices,
        default=ShipmentStatus.PENDING,
        db_index=True
    )

    estimated_delivery_date = models.DateField(
        null=True, 
        blank=True
    )
    shipped_date = models.DateTimeField(
        null=True, 
        blank=True
    )
    delivered_date = models.DateTimeField(
        null=True, 
        blank=True
    )

    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )

    customer_notified = models.BooleanField(
        default=False
    )
    delivery_attempts = models.PositiveSmallIntegerField(
        default=0
    )
    failure_reason = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["shipment_number"]),
            models.Index(fields=["tracking_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["order"]),
        ]

    def __str__(self):
        return f"Shipment #{self.shipment_number}"

    def save(self, *args, **kwargs):
        if not self.shipment_number:
            year = timezone.now().year
            last = Shipment.objects.filter(
                shipment_number__startswith=f"SHP-{year}-"
            ).order_by('-shipment_number').first()

            num = int(last.shipment_number.split('-')[-1]) + 1 if last else 1
            self.shipment_number = f"SHP-{year}-{num:06d}"

        super().save(*args, **kwargs)

        
'''
=============================================================================
     2. SHIPMENT TRACKING LOG - Detailed Tracking History
        Purpose: Show customer the journey of their package
        Features: Location, timestamp, status updates (like Daraz tracking page)
=============================================================================
'''

class ShipmentTrackingLog(TimeStampedModel):
    """
    Shipment Tracking Log - Daraz Style Tracking Page
    Shows customer: "Your package is in Karachi", "Out for delivery", etc.
    """
    
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="tracking_logs",
        verbose_name=_("Shipment")
    )
    
    status = models.CharField(
        max_length=50,
        verbose_name=_("Status"),
        help_text="e.g., 'Picked Up', 'In Transit', 'Out for Delivery'"
    )
    
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Location"),
        help_text="City or facility name"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text="Detailed status description for customer"
    )
    
    # For API integration with courier services
    api_response = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("API Response"),
        help_text="Raw response from courier API"
    )
    
    class Meta:
        verbose_name = _("Shipment Tracking Log")
        verbose_name_plural = _("Shipment Tracking Logs")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["shipment", "-created_at"], name="tracking_shipment_idx"),
        ]
    
    def __str__(self):
        return f"{self.shipment.shipment_number} - {self.status} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"