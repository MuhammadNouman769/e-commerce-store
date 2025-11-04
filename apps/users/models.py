
""" =============== Imports =============== """
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from apps.utilities.models import BaseModel
from apps.users.choices import UserRoleChoices
from apps.users.manager import UserManager

""" =============== Custom User Model =============== """

class User(AbstractUser):
    """Custom User model extending AbstractUser."""
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    role = models.CharField(
        max_length=50,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.CUSTOMER,  
    )

    # Custom manager
    objects = UserManager()   # pyright: ignore[reportAssignmentType]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  

   
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
