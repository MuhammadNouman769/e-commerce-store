"""
                 USERS MODELS
Purpose: User authentication and profile management
Author: Muhammad Nouman
"""
''' ------------ iMPORTS ------------ '''
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from apps.utilities.models import BaseModel
from apps.users.choices import UserRoleChoices, UserStatusChoices
from apps.users.manager import UserManager

'''
================================================================================
    1. USER MODEL - User Authentication and Profile Management
    Usage: Manage user accounts, authentication, and profiles
    Features: Email/phone login, role management, verification status
================================================================================
'''

class User(AbstractUser, BaseModel):
    """
              Custom User Model
    Uses email as username field instead of username
    """
    
    ''' ------------ REMOVE USERNAME FIELD ------------ '''
    username = None
    
    ''' ------------ REQUIRED FIELDS ------------ '''
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email Address"),
        help_text=_("Used for login and communication")
    )
    ''' ------------ PHONE FIELD ------------ '''
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Phone Number"),
        help_text=_("Used for OTP verification and contact")
    )
    
    ''' ------------ ROLE MANAGEMENT ------------ '''
    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.CUSTOMER,
        verbose_name=_("User Role"),
        help_text=_("Determines user permissions and access")
    )
    
    ''' ------------ PROFILE INFORMATION ------------ '''
    ''' ------------ FIRST NAME FIELD ------------ '''
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("First Name")
    )
    ''' ------------ LAST NAME FIELD ------------ '''
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Last Name")
    )
    ''' ------------ PROFILE PICTURE FIELD OPTIONAL ------------ '''
    profile_picture = models.ImageField(
        upload_to='profile_pics/%Y/%m/',
        null=True,
        blank=True,
        verbose_name=_("Profile Picture")
    )
    
    ''' ------------ VERIFICATION STATUS ------------ '''
    ''' ------------ EMAIL VERIFIED FIELD ------------ '''
    email_verified = models.BooleanField(
        default=False,
        verbose_name=_("Email Verified")
    )
    ''' ------------ PHONE VERIFIED FIELD ------------ '''
    phone_verified = models.BooleanField(
        default=False,
        verbose_name=_("Phone Verified")
    )
    
    ''' ------------ ACCOUNT STATUS ------------ '''
    account_status = models.CharField(
        max_length=20,
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.ACTIVE,
        verbose_name=_("Account Status")
    )
    
    ''' ------------ SELLER INFORMATION ------------ '''
    ''' ------------ STORE NAME FIELD ------------ '''
    store_name = models.CharField(  
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Store Name"),
        help_text=_("Required if user wants to become a seller")
    )
    ''' ------------ SELLER APPROVED FIELD ------------ '''
    is_seller_approved = models.BooleanField(
        default=False,
        verbose_name=_("Seller Approved"),
        help_text=_("Admin approval required for sellers")
    )
    
    ''' ------------ SECURITY ------------ '''
    ''' ------------ LAST LOGIN IP FIELD ------------ '''
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("Last Login IP")
    )
    
    ''' ------------ CONFIGURE AUTHENTICATION ------------ '''
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name"]
    
    ''' ------------ USE CUSTOM MANAGER ------------ '''
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
        return self.role == UserRoleChoices.SELLER and self.is_seller_approved
    
    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == UserRoleChoices.ADMIN or self.is_superuser
    
    def become_seller(self, store_name=None):
        """Request to become a seller"""
        if store_name:
            self.store_name = store_name
        self.role = UserRoleChoices.SELLER
        self.is_seller_approved = False
        self.is_active = False  # Needs admin approval
        self.save()
    
    def approve_seller(self):
        """Admin approves seller"""
        if self.role == UserRoleChoices.SELLER:
            self.is_seller_approved = True
            self.is_active = True
            self.save()
    
    def get_profile_completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = ['first_name', 'last_name', 'phone', 'profile_picture']
        completed = sum(1 for field in fields if getattr(self, field))
        return int((completed / len(fields)) * 100)