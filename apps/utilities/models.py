from django.db import models

class BaseModel(models.Model):
    """
    Abstract base model with common fields:
    - id
    - created_at / updated_at
    - is_active (soft delete)
    - Optional shop field for multi-tenant systems
    """

    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # Optional shop field placeholder
    shop = None  # child models can override

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.__class__.__name__} (ID: {self.id})"

    def deactivate(self):
        """Soft delete record"""
        self.is_active = False
        self.save()