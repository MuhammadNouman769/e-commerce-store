"""
                 USER MANAGER
Purpose: Custom user manager for email-based authentication
"""
''' ------------ iMPORTS ------------ '''
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

''' ------------ USER MANAGER ------------ '''
class UserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    """
    ''' ------------ CREATE USER ------------ '''
    def create_user(self, email, phone, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and phone
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not phone:
            raise ValueError(_('The Phone field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    ''' ------------ CREATE SUPERUSER ------------ '''
    def create_superuser(self, email, phone, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and phone
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, phone, password, **extra_fields)

    ''' ------------ CREATE CUSTOMER ------------ '''
    def create_customer(self, email, phone, password=None, **extra_fields):
        """Create a customer user"""
        extra_fields.setdefault('role', 'customer')
        return self.create_user(email, phone, password, **extra_fields)

    ''' ------------ CREATE SELLER ------------ '''
    def create_seller(self, email, phone, password=None, **extra_fields):
        """Create a seller user (pending verification)"""
        extra_fields.setdefault('role', 'seller')
        extra_fields.setdefault('is_active', False)  # Needs verification
        return self.create_user(email, phone, password, **extra_fields)