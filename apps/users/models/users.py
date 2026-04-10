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
from ..choices.role_choices import UserRoleChoices
from ..choices.status_choices import UserStatusChoices
from ..managers.user_manager import UserManager


class User(AbstractUser, BaseModel):
    username = None

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)

    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.CUSTOMER,
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/%Y/%m/',
        null=True,
        blank=True,
    )

    account_status = models.CharField(
        max_length=20,
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.PENDING,
    )

    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['account_status']),
        ]

    def __str__(self):
        return self.email

    @property
    def is_customer(self):
        return self.role == UserRoleChoices.CUSTOMER

    @property
    def is_seller(self):
        return self.role == UserRoleChoices.SELLER