"""
=================================================================================
    USER MODEL
    Purpose: Custom user for authentication & role-based management
    Author: Muhammad Nouman
=================================================================================
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from apps.utils.models import BaseModel
from .choices import UserRoleChoices, UserStatusChoices
from .manager import UserManager


'''
=================================================================================
    USER MODEL IMPLEMENTATION
    Purpose: Custom user for authentication & role-based management
    Author: Muhammad Nouman
=================================================================================
'''
class User(AbstractUser, BaseModel):
    username = None  # use email as username

    email = models.EmailField(
        unique=True,
        verbose_name=_("Email Address"),
        help_text=_("Used for login and communication")
    )

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+923001234567'. Up to 15 digits allowed.")
    )
    phone = models.CharField(
        validators=[phone_validator],
        max_length=15,
        unique=True,
        verbose_name=_("Phone Number")
    )

    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.CUSTOMER,
        verbose_name=_("User Role")
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_("Profile Picture")
    )

    email_verified = models.BooleanField(default=False, verbose_name=_("Email Verified"))
    phone_verified = models.BooleanField(default=False, verbose_name=_("Phone Verified"))

    account_status = models.CharField(
        max_length=20,
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.PENDING,
        verbose_name=_("Account Status")
    )

    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("Last Login IP"))

    # Authentication settings
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['account_status']),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email

    @property
    def is_customer(self):
        return self.role == UserRoleChoices.CUSTOMER

    @property
    def is_seller(self):
        return self.role == UserRoleChoices.SELLER