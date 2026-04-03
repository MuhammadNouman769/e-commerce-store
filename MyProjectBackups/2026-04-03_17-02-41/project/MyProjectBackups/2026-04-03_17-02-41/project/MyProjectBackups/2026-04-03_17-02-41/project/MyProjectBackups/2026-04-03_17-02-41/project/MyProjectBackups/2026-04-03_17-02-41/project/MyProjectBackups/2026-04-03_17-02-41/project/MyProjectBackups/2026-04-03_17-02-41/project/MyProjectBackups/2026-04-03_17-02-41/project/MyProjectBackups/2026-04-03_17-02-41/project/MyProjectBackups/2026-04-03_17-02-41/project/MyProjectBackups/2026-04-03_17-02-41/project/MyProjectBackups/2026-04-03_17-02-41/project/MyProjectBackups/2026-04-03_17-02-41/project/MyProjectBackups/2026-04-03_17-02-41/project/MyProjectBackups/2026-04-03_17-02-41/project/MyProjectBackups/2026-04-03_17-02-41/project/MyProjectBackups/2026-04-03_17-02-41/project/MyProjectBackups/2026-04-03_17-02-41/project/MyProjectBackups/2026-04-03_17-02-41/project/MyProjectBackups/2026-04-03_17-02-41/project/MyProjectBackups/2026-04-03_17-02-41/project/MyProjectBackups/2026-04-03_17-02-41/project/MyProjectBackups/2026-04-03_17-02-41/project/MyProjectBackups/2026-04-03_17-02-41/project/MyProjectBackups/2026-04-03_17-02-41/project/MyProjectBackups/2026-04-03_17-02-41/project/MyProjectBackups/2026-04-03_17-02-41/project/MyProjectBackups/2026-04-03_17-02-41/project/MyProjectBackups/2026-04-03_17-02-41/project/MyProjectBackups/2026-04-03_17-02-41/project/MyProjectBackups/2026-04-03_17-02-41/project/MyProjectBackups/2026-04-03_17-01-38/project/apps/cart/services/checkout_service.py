from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem
from apps.cart.models import ShippingAddress
from apps.cart.services.cart_service import CartService

class CheckoutService:
    """Checkout / Order processing service"""

    @staticmethod
    @transaction.atomic
    def create_order(cart: Cart, user, shipping_address: ShippingAddress,
                     billing_address: ShippingAddress = None,
                     payment_method: str = Order.PaymentMethods.COD):
        """Convert cart to order"""
        if cart.is_empty:
            raise ValidationError("Cart is empty")

        # Calculate totals
        subtotal = cart.subtotal
        discount = cart.discount_amount
        total = cart.total

        order = Order.objects.create(
            user=user,
            cart=cart,
            shipping_address=shipping_address,
            billing_address=billing_address,
            payment_method=payment_method,
            subtotal=subtotal,
            discount=discount,
            total_amount=total,
        )

        # Add order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                product_name=item.product_name,
                variant_name=item.variant_name,
                sku=item.sku,
                quantity=item.quantity,
                price=item.price,
                total_price=item.total_price
            )

        # Mark cart as converted
        cart.status = Cart.CartStatus.CONVERTED
        cart.save()

        return order

    @staticmethod
    @transaction.atomic
    def process_payment(order: Order, transaction_id: str = None, gateway_response: dict = None):
        """Process payment and mark order as paid"""
        if order.is_paid:
            raise ValidationError("Order already paid")

        order.payment_status = Order.PaymentStatus.PAID
        order.transaction_id = transaction_id
        order.payment_gateway_response = gateway_response or {}
        order.paid_at = order.paid_at or order.created_at
        order.save()
        return order

    @staticmethod
    def update_order_status(order: Order, status: str):
        """Update order status"""
        if status not in dict(Order.OrderStatus.choices).keys():
            raise ValidationError("Invalid order status")
        order.order_status = status
        order.save()
        return order

    @staticmethod
    @transaction.atomic
    def refund_order(order: Order, amount: Decimal = None):
        """Process refund for order"""
        if not order.is_paid:
            raise ValidationError("Cannot refund unpaid order")
        refund_amount = amount or order.total_amount
        order.payment_status = Order.PaymentStatus.REFUNDED
        order.save()
        # Refund logic with payment gateway would go here
        return refund_amount