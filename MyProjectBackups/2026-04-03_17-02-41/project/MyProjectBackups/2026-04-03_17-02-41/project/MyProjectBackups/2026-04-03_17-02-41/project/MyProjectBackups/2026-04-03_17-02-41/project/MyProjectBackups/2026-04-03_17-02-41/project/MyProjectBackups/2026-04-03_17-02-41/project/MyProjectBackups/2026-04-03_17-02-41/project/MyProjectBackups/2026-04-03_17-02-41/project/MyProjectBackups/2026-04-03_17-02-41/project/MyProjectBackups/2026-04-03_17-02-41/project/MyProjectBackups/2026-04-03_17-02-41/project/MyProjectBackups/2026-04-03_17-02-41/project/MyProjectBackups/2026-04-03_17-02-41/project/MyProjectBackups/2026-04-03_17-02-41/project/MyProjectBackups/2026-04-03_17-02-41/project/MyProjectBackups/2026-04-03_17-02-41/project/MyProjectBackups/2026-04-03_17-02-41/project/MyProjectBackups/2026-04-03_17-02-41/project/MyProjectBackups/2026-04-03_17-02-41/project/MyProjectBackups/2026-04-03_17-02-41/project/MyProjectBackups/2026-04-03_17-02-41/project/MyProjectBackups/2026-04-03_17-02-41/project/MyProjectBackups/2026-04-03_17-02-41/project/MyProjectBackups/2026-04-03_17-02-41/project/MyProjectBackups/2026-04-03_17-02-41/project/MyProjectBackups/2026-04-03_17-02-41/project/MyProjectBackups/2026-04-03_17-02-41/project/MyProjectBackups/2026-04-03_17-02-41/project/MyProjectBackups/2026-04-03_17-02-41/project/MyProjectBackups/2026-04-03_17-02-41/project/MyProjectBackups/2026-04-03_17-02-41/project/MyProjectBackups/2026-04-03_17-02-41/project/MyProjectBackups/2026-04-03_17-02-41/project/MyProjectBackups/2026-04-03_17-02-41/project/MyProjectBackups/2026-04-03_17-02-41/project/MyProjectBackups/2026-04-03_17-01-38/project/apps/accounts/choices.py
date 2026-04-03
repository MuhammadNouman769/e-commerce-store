'''
-------------------------------------------------
                USER CHOICES
Purpose: Define user role choices for the platform
-------------------------------------------------
'''

''' ------------ iMPORTS ------------ '''
from django.db import models
from django.utils.translation import gettext_lazy as _

''' ------------ CHOICES ------------ '''
class UserRoleChoices(models.TextChoices):
    """User role choices for the platform"""
    CUSTOMER = 'customer', _('Customer')
    SELLER = 'seller', _('Seller')
    ADMIN = 'admin', _('Admin')
    STAFF = 'staff', _('Staff')

''' ---------- USER STATUS CHOICES ---------- '''
class UserStatusChoices(models.TextChoices):
    """User account status"""
    ACTIVE = 'active', _('Active')
    INACTIVE = 'inactive', _('Inactive')
    SUSPENDED = 'suspended', _('Suspended')
    PENDING = 'pending', _('Pending Verification')