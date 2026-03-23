""" ============== Imports =============== """
from django.db import models
from cities_light.models import Country, Region, City
from apps.products.models import Product
from apps.utilities.models import BaseModel
from apps.users.models import User

""" ============== Address Model =============== """

class Address(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.street

""" ============== Cart Model =============== """

class Cart(BaseModel):
    """
    DB-backed cart (for checkout + demo system).
    Current cart page still uses session cart, but we create a Cart row on checkout POST.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")

    def __str__(self):
        return f"Cart #{self.id} ({self.user.email})"

""" ============== Cart Item Model =============== """
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="cart_items")
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)  # unit price

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price

""" ============== Shipping Address Model =============== """
class ShippingAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shipping_addresses")
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    street_address = models.TextField(blank=True)

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="shipping_addresses")
    province = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="shipping_addresses", null=True, blank=True
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="shipping_addresses", null=True, blank=True)

    postal_code = models.CharField(max_length=20, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name or self.user.email} - {self.street_address[:20]}"