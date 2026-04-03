''' 
==================================================
    here we are creating a service for order 
  fulfillment & order history, order cancellation, 
  order payment, order shipping, order delivery
==================================================
'''
from django.db import transaction
from django.utils import timezone
from apps.orders.models import Order, OrderHistory


class OrderService:

    def __init__(self, order: Order):
        self.order = order

    ''' ========================= PAYMENT ========================='''
    @transaction.atomic
    def mark_as_paid(self, transaction_id=None, gateway_response=None):
        old_status = self.order.order_status

        self.order.payment_status = Order.PaymentStatus.PAID
        self.order.order_status = Order.OrderStatus.PROCESSING
        self.order.paid_at = timezone.now()

        if transaction_id:
            self.order.transaction_id = transaction_id
        if gateway_response:
            self.order.payment_gateway_response = gateway_response

        self.order.save()

        OrderHistory.objects.create(
            order=self.order,
            status_from=old_status,
            status_to=self.order.order_status,
            action=OrderHistory.ActionType.PAYMENT
        )

    ''' ========================= SHIPPING ========================='''
    @transaction.atomic
    def mark_as_shipped(self, tracking_number=None, courier_company=None):
        old_status = self.order.order_status

        self.order.order_status = Order.OrderStatus.SHIPPED
        self.order.shipped_at = timezone.now()

        if tracking_number:
            self.order.tracking_number = tracking_number
        if courier_company:
            self.order.courier_company = courier_company

        self.order.save()

        OrderHistory.objects.create(
            order=self.order,
            status_from=old_status,
            status_to=self.order.order_status,
            action=OrderHistory.ActionType.SHIPPED
        )

    ''' ========================= DELIVERY ========================='''
    @transaction.atomic
    def mark_as_delivered(self):
        old_status = self.order.order_status

        self.order.order_status = Order.OrderStatus.DELIVERED
        self.order.delivered_at = timezone.now()
        self.order.save()

        OrderHistory.objects.create(
            order=self.order,
            status_from=old_status,
            status_to=self.order.order_status,
            action=OrderHistory.ActionType.DELIVERED
        )

    ''' ========================= CANCEL ========================='''
    @transaction.atomic
    def cancel_order(self, reason=""):
        if not self.order.can_cancel:
            raise ValueError("Order cannot be cancelled")

        old_status = self.order.order_status

        self.order.order_status = Order.OrderStatus.CANCELLED
        self.order.cancelled_at = timezone.now()

        if reason:
            self.order.admin_notes = f"{reason}\n{self.order.admin_notes}"

        self.order.save()

        OrderHistory.objects.create(
            order=self.order,
            status_from=old_status,
            status_to=self.order.order_status,
            action=OrderHistory.ActionType.CANCELLED,
            notes=reason
        )