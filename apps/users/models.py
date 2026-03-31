"""
-------------------------------------------------
                 USERS MODELS
Purpose: User authentication and profile management
Author: Muhammad Nouman
-------------------------------------------------
"""

''' ------------ iMPORTS ------------ '''
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.utilities.models import BaseModel
from apps.users.choices import UserRoleChoices, UserStatusChoices
from apps.users.manager import UserManager

''' ----------------- USER MODEL ----------- '''

class User(AbstractUser, BaseModel):
    """
              Custom User Model
    Uses email as username field instead of username
    """
    username = None # Remove username field because we are using email as username
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email Address"),
        help_text=_("Used for login and communication")
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Phone Number")
    )
    # Role Management here so user can be customer, seller, admin, staff
    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.CUSTOMER,
        verbose_name=_("User Role")
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Last Name")
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_("Profile Picture")
    )
    # here we are using boolean fields to check if the user is verified or not not use email again and again  
    email_verified = models.BooleanField(
        default=False,
        verbose_name=_("Email Verified")
    )
    phone_verified = models.BooleanField(
        default=False,
        verbose_name=_("Phone Verified")
    )
    account_status = models.CharField(
        max_length=20,
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.ACTIVE,
        verbose_name=_("Account Status")
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("Last Login IP")
    )
    # here we are using custom manager for user model authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name"]
    objects = UserManager()
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['role']),
            models.Index(fields=['account_status']),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Return full name"""
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email
    
    @property
    def is_customer(self):
        """Check if user is a customer"""
        return self.role == UserRoleChoices.CUSTOMER
    
    @property
    def is_seller(self):
        """Check if user is an approved seller"""
        return self.role == UserRoleChoices.SELLER