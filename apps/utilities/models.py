""" =========== apps/utilities/models.py ============ """
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SoftDeleteQuerySet(models.QuerySet):
    """Custom queryset with soft delete support"""
    
    def delete(self):
        """Soft delete all items in queryset"""
        return super().update(is_active=False, updated_at=timezone.now())
    
    def hard_delete(self):
        """Permanently delete all items in queryset"""
        return super().delete()
    
    def active(self):
        """Filter only active items"""
        return self.filter(is_active=True)
    
    def inactive(self):
        """Filter only inactive items"""
        return self.filter(is_active=False)
    
    def restore(self):
        """Restore soft deleted items"""
        return super().update(is_active=True, updated_at=timezone.now())


class SoftDeleteManager(models.Manager):
    """Manager that returns only active items by default"""
    
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_active=True)
    
    def active(self):
        """Get active items"""
        return self.get_queryset()
    
    def inactive(self):
        """Get inactive items"""
        return self.all_objects.filter(is_active=False)
    
    def all_with_deleted(self):
        """Get all items including deleted ones"""
        return self.all_objects.all()


class BaseModel(models.Model):
    """Base model with common fields and soft delete functionality"""
    
    id = models.BigAutoField(primary_key=True, verbose_name=_("ID"))
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Soft delete flag")
    )
    
    # Default manager returns only active items
    objects = SoftDeleteManager()
    
    # Manager that returns all items including deleted ones
    all_objects = models.Manager()
    
    class Meta:
        abstract = True
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.__class__.__name__} #{self.id}"
    
    def delete(self, using=None, keep_parents=False):
        """Soft delete - just mark as inactive"""
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])
    
    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete from database"""
        super().delete(using=using, keep_parents=keep_parents)
    
    def restore(self):
        """Restore a soft deleted record"""
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])
    
    @property
    def is_deleted(self):
        """Check if record is soft deleted"""
        return not self.is_active
    
    class Meta:
        abstract = True