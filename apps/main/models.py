from django.db import models
from apps.utilities.models import BaseModel


# Create your models here.
class Banners(BaseModel):
    CATEGORIES = [
        ('men', 'Men'),
        ('women', 'Women'),
    ]

    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Original price"
    )
    discount_percentage = models.PositiveSmallIntegerField(
        default=0,
        help_text="0 - 100"
    )
    button_text = models.CharField(max_length=100, default='Shop Collection')
    category = models.CharField(max_length=100, choices=CATEGORIES, default='men')
    image = models.ImageField(upload_to='banners/%Y/%m/%d')
    is_active = models.BooleanField(default=True)

    def final_price(self):
        if self.discount_percentage > 0:
            return self.price - (self.price * self.discount_percentage / 100)
        return self.price

    def __str__(self):
        return self.title



