from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.manager import UserManager
from apps.users.choices import UserRoleChoices


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)

    role = models.CharField(
        max_length=10,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.CUSTOMER
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"