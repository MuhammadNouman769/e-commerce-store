import random
from django.db import models
from django.utils import timezone
from datetime import timedelta


class OTP(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)

        super().save(*args, **kwargs)