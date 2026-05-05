"""
=================================================================================
    UTILITIES BASE MODELS
    Purpose: Reusable base models for soft delete, UUIDs, timestamps, slugging
    Author: Muhammad Nouman
=================================================================================
"""

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
from django.utils.translation import gettext_lazy as _

'''
=================================================================================
  1. SOFT DELETE MODEL IMPLEMENTATION
      Purpose: Reusable base model for soft delete
      Features:
        - Is deleted (BooleanField) - whether the model is deleted
        - Created at (DateTimeField) - the date and time the model was created
        - Updated at (DateTimeField) - the date and time the model was updated
=================================================================================
'''
class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True, updated_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return super().update(is_deleted=False, updated_at=timezone.now())

    def active(self):
        return self.filter(is_deleted=False)

    def inactive(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def active(self):
        return self.get_queryset().filter(is_deleted=False)

    def inactive(self):
        return self.get_queryset().filter(is_deleted=True)

'''
=================================================================================
  2. BASE MODEL IMPLEMENTATION
      Purpose: Reusable base model for all models
      Features:
        - ID (BigAutoField) - the primary key for the model
        - Created at (DateTimeField) - the date and time the model was created
        - Updated at (DateTimeField) - the date and time the model was updated
        - Is deleted (BooleanField) - whether the model is deleted
=================================================================================
'''
class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name=_("ID"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Is Deleted"))

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # includes deleted

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=['is_deleted', 'updated_at'])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=['is_deleted', 'updated_at'])

    @property
    def is_active(self):
        return not self.is_deleted


'''
=================================================================================
  3. UUID BASE MODEL IMPLEMENTATION
      Purpose: Reusable base model for all models that need a UUID
      Features:
        - ID (UUIDField) - the primary key for the model
=================================================================================
'''
class UUIDBaseModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


'''
=================================================================================
  4. ORDERED MODEL IMPLEMENTATION
      Purpose: Reusable base model for all models that need a position
      Features:
        - Position (PositiveSmallIntegerField) - the position of the model
=================================================================================
'''
class OrderedModel(BaseModel):
    position = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["position", "-created_at"]

    def save(self, *args, **kwargs):
        if self.position is None and not self.pk:
            max_pos = self.__class__.objects.active().aggregate(models.Max('position'))['position__max']
            self.position = (max_pos or 0) + 1
        super().save(*args, **kwargs)


'''
=================================================================================
  5. SLUGGED MODEL IMPLEMENTATION
      Purpose: Reusable base model for all models that need a slug
      Features:
        - Slug (SlugField) - the slug of the model
=================================================================================
'''
class SluggedModel(BaseModel):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    SLUG_FIELD = "n"  # override in child model

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['slug']),
        ]

    def generate_slug(self):
        value = getattr(self, self.SLUG_FIELD)
        base_slug = slugify(value)
        slug = base_slug
        counter = 1

        while self.__class__.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)