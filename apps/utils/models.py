
'''=================================================================================
  UTILITIES MODELS INFORMATION
  Purpose: Handle automatic warehouse management and inventory synchronization
  Author: Muhammad Nouman
=================================================================================
'''

'''=================== IMPORTS ========================'''
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
from django.conf import settings
from django.utils.translation import gettext_lazy as _


''' 
=================================================================================
  1. SOFT DELETE QUERYSET INFORMATION
  Purpose: Handle automatic deletion of models instead of permanent deletion
  When to use: When you want to delete a model but want to restore it later
  Features: in this model we have 4 methods delete, hard_delete, restore,
  active, inactive
  Author: Muhammad Nouman
=================================================================================
'''
class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_active=False, updated_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return super().update(is_active=True, updated_at=timezone.now())

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_active=True)

'''
=================================================================================
  2. BASE MODEL INFORMATION
  Purpose: Handle automatic fields like id, created_at, updated_at, is_active for
           equil use in models, logs, stock tracking & other purposes
  Author: Muhammad Nouman
=================================================================================
'''
class BaseModel(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        verbose_name = _("ID")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,null=True,blank=True,
        verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,null=True,blank=True,
        verbose_name=_("Updated At")
    )
    is_active = models.BooleanField(
        default=True,null=True,blank=True,
        verbose_name=_("Is Active")
    )
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Includes inactive

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def delete(
        self, 
        using=None, 
        keep_parents=False
        ):
        self.is_active = False
        self.save(
            update_fields=['is_active', 'updated_at']
            )

    def hard_delete(
        self, 
        using=None, 
        keep_parents=False
        ):
        super().delete(
            using=using, 
            keep_parents=keep_parents
            )

    def restore(self):
        self.is_active = True
        self.save(
            update_fields=['is_active', 'updated_at']
            )

    @property
    def is_deleted(self):
        return not self.is_active

'''
=================================================================================
  3. UUID BASE MODEL INFORMATION
  Purpose: Handle secure public IDs for models instead of auto incremented IDs
  & also provide unique IDs for models for security purpose
  Author: Muhammad Nouman
=================================================================================
'''
class UUIDBaseModel(BaseModel):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

'''
=================================================================================
  4. TIME STAMPED MODEL INFORMATION
  Purpose: Handle automatic timestamping of models for logs & analytics 
  Author: Muhammad Nouman
=================================================================================
'''
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
        )
    updated_at = models.DateTimeField(
        auto_now=True
        )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

'''
=================================================================================
  5. ORDERED MODEL INFORMATION
  Purpose: Handle manual ordering of models
  Author: Muhammad Nouman
=================================================================================
'''
class OrderedModel(BaseModel):
    position = models.PositiveSmallIntegerField(
        default=None, 
        null=True, 
        blank=True
        )

    class Meta:
        abstract = True
        ordering = ["position", "-created_at"]

    def save(self, *args, **kwargs):
        if self.position is None and not self.pk:
            max_pos = self.__class__.objects.active
            ().aggregate(
                models.Max('position')
                )['position__max']
            self.position = (
                max_pos or 0
                ) + 1
        super().save(
            *args, 
            **kwargs
            )

'''
=================================================================================
  5. SLUGGED MODEL INFORMATION
  Purpose: Handle automatic slug generation for SEO friendly URLs
  Author: Muhammad Nouman
=================================================================================
'''
class SluggedModel(models.Model):
    slug = models.SlugField(
        max_length=255, 
        blank=True
        )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['slug']),
        ]

    SLUG_FIELD = "name"  # field from which slug will be generated

    def generate_slug(self):
        value = getattr(
            self, 
            self.SLUG_FIELD
            )
        base_slug = slugify(value)
        slug = base_slug
        counter = 1

        while self.__class__.all_objects.filter(
            slug=slug
            ).exclude(
                pk=self.pk
                ).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(
            *args, 
            **kwargs
            )