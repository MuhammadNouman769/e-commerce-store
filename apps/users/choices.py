from django.db import models

class UserRoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    CUSTOMER = 'customer', 'Customer'
