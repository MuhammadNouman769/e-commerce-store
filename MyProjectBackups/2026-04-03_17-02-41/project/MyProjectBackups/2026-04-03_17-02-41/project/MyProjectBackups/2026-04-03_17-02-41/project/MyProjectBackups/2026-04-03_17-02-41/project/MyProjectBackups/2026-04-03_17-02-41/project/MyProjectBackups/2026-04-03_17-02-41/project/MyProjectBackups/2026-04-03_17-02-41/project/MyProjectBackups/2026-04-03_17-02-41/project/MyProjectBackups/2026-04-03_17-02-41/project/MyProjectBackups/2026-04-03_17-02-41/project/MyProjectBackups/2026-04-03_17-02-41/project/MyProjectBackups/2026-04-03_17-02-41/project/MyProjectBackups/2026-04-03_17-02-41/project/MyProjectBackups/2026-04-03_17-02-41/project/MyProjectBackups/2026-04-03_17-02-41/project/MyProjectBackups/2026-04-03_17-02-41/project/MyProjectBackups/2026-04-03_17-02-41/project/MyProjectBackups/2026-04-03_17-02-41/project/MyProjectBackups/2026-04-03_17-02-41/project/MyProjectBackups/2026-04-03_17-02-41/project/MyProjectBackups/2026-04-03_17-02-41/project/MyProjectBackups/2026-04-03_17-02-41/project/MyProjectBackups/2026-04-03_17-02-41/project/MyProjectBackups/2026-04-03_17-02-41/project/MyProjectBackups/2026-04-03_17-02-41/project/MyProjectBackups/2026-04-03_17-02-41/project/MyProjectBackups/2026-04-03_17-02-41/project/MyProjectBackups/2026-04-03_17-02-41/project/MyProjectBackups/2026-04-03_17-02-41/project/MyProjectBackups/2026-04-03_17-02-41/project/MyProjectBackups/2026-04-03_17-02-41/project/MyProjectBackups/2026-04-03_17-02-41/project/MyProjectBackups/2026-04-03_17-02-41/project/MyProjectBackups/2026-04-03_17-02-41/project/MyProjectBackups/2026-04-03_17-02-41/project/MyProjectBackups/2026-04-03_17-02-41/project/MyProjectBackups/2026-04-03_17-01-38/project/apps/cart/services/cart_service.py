from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.cart.models import Cart, CartItem
from apps.products.models import Product, ProductVariant

class CartService:
    """Cart business logic / service layer"""

    @staticmethod
    def get_cart(user=None, session_key=None):
        """Fetch or create active cart"""
        return Cart.get_or_create_cart(user=user, session_key=session_key)

    @staticmethod
    @transaction.atomic
    def add_item(cart: Cart, product: Product, variant: ProductVariant = None, quantity: int = 1):
        """Add or update cart item"""
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than 0")

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={
                "product_name": product.title,
                "variant_name": variant.get_variant_name() if variant else "",
                "sku": variant.sku if variant else product.sku,
                "quantity": quantity,
                "price": variant.price if variant else product.price,
            }
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item

    @staticmethod
    @transaction.atomic
    def remove_item(cart: Cart, product: Product, variant: ProductVariant = None):
        """Remove item from cart"""
        CartItem.objects.filter(cart=cart, product=product, variant=variant).delete()

    @staticmethod
    @transaction.atomic
    def update_quantity(cart: Cart, product: Product, variant: ProductVariant = None, quantity: int = 1):
        """Update quantity to specific value"""
        try:
            item = CartItem.objects.get(cart=cart, product=product, variant=variant)
            if quantity <= 0:
                item.delete()
            elif quantity <= item.available_stock:
                item.quantity = quantity
                item.save()
            else:
                raise ValidationError(f"Only {item.available_stock} items available")
            return item
        except CartItem.DoesNotExist:
            raise ValidationError("Item not found in cart")

    @staticmethod
    def clear_cart(cart: Cart):
        """Empty the cart"""
        cart.clear()

    @staticmethod
    def apply_coupon(cart: Cart, coupon_code: str, discount_amount: Decimal):
        """Apply coupon"""
        cart.apply_coupon(coupon_code, discount_amount)

    @staticmethod
    def remove_coupon(cart: Cart):
        """Remove coupon"""
        cart.remove_coupon()

    @staticmethod
    @transaction.atomic
    def merge_carts(user_cart: Cart, guest_cart: Cart):
        """Merge guest cart into user cart"""
        if guest_cart and guest_cart != user_cart:
            user_cart.merge_with(guest_cart)