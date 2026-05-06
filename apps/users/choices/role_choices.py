

''' ------------ iMPORTS ------------ '''
from django.db import models
from django.utils.translation import gettext_lazy as _

''' ------------ CHOICES ------------ '''
class UserRoleChoices(models.TextChoices):
    """User role choices for the platform"""
    CUSTOMER = 'customer', _('Customer')
    SELLER = 'seller', _('Seller')
    ADMIN = 'admin', _('admin')
    STAFF = 'staff', _('Staff')
