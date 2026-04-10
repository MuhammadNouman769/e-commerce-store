from django.db import models

class ProductStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"
    OUT_OF_STOCK = "out_of_stock", "Out of Stock"


class ShopStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending Review'
    UNDER_REVIEW = 'under_review', 'Under Review'
    APPROVED = 'approved', 'Approved'
    SUSPENDED = 'suspended', 'Suspended'
    REJECTED = 'rejected', 'Rejected'