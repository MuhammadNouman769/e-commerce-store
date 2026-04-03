''' 
==================================================
    here we are creating a service for order 
    item fulfillment & order item history, order item 
    cancellation, order item payment, order item 
    shipping, order item delivery
==================================================
'''
from django.db import transaction
from decimal import Decimal
from django.core.exceptions import ValidationError

from apps.orders.models import OrderItem, OrderHistory, Order

''' ====================== ORDER ITEM SERVICE ====================== '''

class OrderItemService:

    def __init__(self, order_item: OrderItem):
        self.item = order_item
        self.order = order_item.order

    # ========================= RETURN ITEM =========================
    @transaction.atomic
    def return_item(self, quantity, refund_amount=None):

        if quantity <= 0:
            raise ValidationError("Quantity must be greater than 0")

        remaining = self.item.quantity - self.item.returned_quantity

        if quantity > remaining:
            raise ValidationError("Cannot return more than available quantity")

        # update returned quantity
        self.item.returned_quantity += quantity

        # update refund
        if refund_amount:
            self.item.refund_amount += Decimal(refund_amount)
        else:
            self.item.refund_amount += Decimal(quantity) * self.item.price

        self.item.save()

        # OPTIONAL: update order payment status
        self._update_order_refund_status()

        # log history
        OrderHistory.objects.create(
            order=self.order,
            status_from=self.order.order_status,
            status_to=self.order.order_status,
            action=OrderHistory.ActionType.REFUND,
            notes=f"{quantity} item(s) returned"
        )

    ''' ========================= UPDATE ORDER TOTAL ========================='''
    def recalculate_order_total(self):
        total = sum(i.total_price for i in self.order.items.all())
        self.order.subtotal = total
        self.order.total_amount = self.order.subtotal + self.order.tax + self.order.shipping_fee - self.order.discount
        self.order.save(update_fields=["subtotal", "total_amount"])

    ''' ========================= REFUND STATUS ========================='''
    def _update_order_refund_status(self):
        total_refund = sum(i.refund_amount for i in self.order.items.all())

        if total_refund > 0:
            if total_refund >= self.order.total_amount:
                self.order.payment_status = Order.PaymentStatus.REFUNDED
            else:
                self.order.payment_status = Order.PaymentStatus.PARTIALLY_REFUNDED

            self.order.save(update_fields=["payment_status"])