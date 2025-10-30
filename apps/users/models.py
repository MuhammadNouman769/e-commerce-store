
""" =============== Imports =============== """
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone
from apps.utilities.models import BaseModel


""" =============== Custom User Manager =============== """
class UserManager(BaseUserManager):
    """Manager for custom User model using email instead of username."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with admin rights."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


""" =============== Custom User Model =============== """
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Main user model using email as the unique identifier."""

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No username or additional required fields

    class Meta(BaseModel.Meta):
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


""" =============== Contact Details =============== """
class ContactDetail(BaseModel):
    """Stores additional contact numbers or alternative emails."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contact_details"
    )
    phone_number = models.CharField(max_length=20)
    alt_phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.phone_number}"


""" =============== Addresses =============== """
class Address(BaseModel):
    """Stores user shipping and billing addresses."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default_shipping = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.city})"


""" =============== Profile =============== """
class Profile(BaseModel):
    """Additional profile information (1-to-1 with User)."""

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )

    def __str__(self):
        return f"Profile of {self.user.email}"
