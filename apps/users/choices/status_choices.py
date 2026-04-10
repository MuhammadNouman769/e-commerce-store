from django.db import models
from django.utils.translation import gettext_lazy as _

''' ---------- USER STATUS CHOICES ---------- '''
class UserStatusChoices(models.TextChoices):
    """User account status"""
    ACTIVE = 'active', _('Active')
    INACTIVE = 'inactive', _('Inactive')
    SUSPENDED = 'suspended', _('Suspended')
    PENDING = 'pending', _('Pending Verification')