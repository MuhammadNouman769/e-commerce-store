
""" =========== apps/utilities/models.py ============ """
from django.db import models

""" =========== BaseModel with Soft Delete =========== """
class SoftDeleteQuerySet(models.QuerySet):

    def delete(self):
        return super().update(is_active=False)

    def hard_delete(self):
        return super().delete()

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

""" BaseModel with soft delete functionality """
class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_active=True)

""" BaseModel with common fields and soft delete """
class BaseModel(models.Model):

    id = models.BigAutoField(primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.__class__.__name__} (ID: {self.id})"

    def delete(self, using=None, keep_parents=False):
        """Soft delete"""
        self.is_active = False
        self.save()

    def hard_delete(self):
        """Permanent delete"""
        super().delete()