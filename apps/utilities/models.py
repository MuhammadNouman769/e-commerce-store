""" ============= Imports ============== """
from django.db import models


""" ============= BaseModel =============== """
class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']  # optional default ordering

    def __str__(self):
        return f"{self.__class__.__name__} (ID: {self.id})"

    def deactivate(self):
        """Soft delete record (optional helper)"""
        self.is_active = False
        self.save()
