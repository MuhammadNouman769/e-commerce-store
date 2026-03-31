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
from apps.inventory_tracking.models import InventoryItem

'''
=============================================================================
     1. SHIPMENT MODEL - Package Tracking to Customer
         Purpose: Track individual shipments from warehouse to customer
         When to use: When order is shipped, create a shipment record
=============================================================================
'''

class Shipment(TimeStampedModel, BaseModel):
    """
    Shipment Model - Track delivery to customers
    """
    
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
    
    # Reference
    shipment_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name=_("Shipment Number")
    )
    
    order = models.ForeignKey(
        "order_fulfillment.Order",
        on_delete=models.CASCADE,
        related_name="shipments",
        verbose_name=_("Order")
    )
    
    # Courier Information
    courier_company = models.CharField(
        max_length=20,
        choices=CourierCompany.choices,
        verbose_name=_("Courier Company")
    )
    
    tracking_number = models.CharField(
        max_length=100,
        verbose_name=_("Tracking Number")
    )
    
    tracking_url = models.URLField(
        blank=True,
        verbose_name=_("Tracking URL")
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=ShipmentStatus.choices,
        default=ShipmentStatus.PENDING,
        verbose_name=_("Shipment Status")
    )
    
    # Important Dates for Customer
    estimated_delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Estimated Delivery Date"),
        help_text="Shown to customer"
    )
    
    shipped_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Shipped Date")
    )
    
    delivered_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Delivered Date")
    )
    
    # Package Details
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Weight (kg)")
    )
    
    # Customer Communication
    customer_notified = models.BooleanField(
        default=False,
        verbose_name=_("Customer Notified"),
        help_text="Has customer been notified of status?"
    )
    
    # Delivery Attempts
    delivery_attempts = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Delivery Attempts")
    )
    
    failure_reason = models.TextField(
        blank=True,
        verbose_name=_("Failure Reason")
    )
    
    class Meta:
        verbose_name = _("Shipment")
        verbose_name_plural = _("Shipments")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["shipment_number"], name="shipment_number_idx"),
            models.Index(fields=["tracking_number"], name="shipment_tracking_idx"),
            models.Index(fields=["status"], name="shipment_status_idx"),
            models.Index(fields=["order"], name="shipment_order_idx"),
        ]
    
    def __str__(self):
        return f"Shipment #{self.shipment_number} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        """Auto-generate shipment number"""
        if not self.shipment_number:
            from django.utils import timezone
            year = timezone.now().year
            last_shipment = Shipment.objects.filter(
                shipment_number__startswith=f"SHP-{year}-"
            ).order_by('-shipment_number').first()
            
            if last_shipment:
                last_number = int(last_shipment.shipment_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.shipment_number = f"SHP-{year}-{new_number:06d}"
        
        # Update dates based on status
        if self.status == self.ShipmentStatus.PICKED and not self.shipped_date:
            self.shipped_date = timezone.now()
        elif self.status == self.ShipmentStatus.DELIVERED and not self.delivered_date:
            self.delivered_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    def update_status(self, status, location=None, description=None):
        """Update shipment status with tracking log"""
        self.status = status
        self.save()
        
        # Add tracking log
        ShipmentTrackingLog.objects.create(
            shipment=self,
            status=status,
            location=location or "",
            description=description or ""
        )
    
    def mark_as_picked(self):
        """Mark as picked by courier"""
        self.update_status(self.ShipmentStatus.PICKED, 
                          description="Picked up by courier")
    
    def mark_as_in_transit(self, location=None):
        """Mark as in transit"""
        self.update_status(self.ShipmentStatus.IN_TRANSIT, 
                          location=location,
                          description="Shipment in transit")
    
    def mark_as_out_for_delivery(self):
        """Mark as out for delivery"""
        self.update_status(self.ShipmentStatus.OUT_FOR_DELIVERY,
                          description="Out for delivery")
    
    def mark_as_delivered(self):
        """Mark as delivered"""
        self.update_status(self.ShipmentStatus.DELIVERED,
                          description="Delivered successfully")
        # Update order status
        self.order.mark_as_delivered()
    
    def mark_as_failed(self, reason):
        """Mark delivery as failed"""
        self.update_status(self.ShipmentStatus.FAILED,
                          description=f"Delivery failed: {reason}")
        self.delivery_attempts += 1
        self.failure_reason = reason
        self.save()

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