from django.db import models

class ProductStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"
    OUT_OF_STOCK = "out_of_stock", "Out of Stock"


