'''---------- IMPORTS ----------'''
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

'''
==========================================
 Custom QuerySet & Manager for Soft Delete
==========================================
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
==========================================
 BaseModel with Soft Delete & Timestamps
==========================================
'''
class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_created")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_updated")

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Includes inactive

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])

    @property
    def is_deleted(self):
        return not self.is_active

'''
==========================================
 UUIDBaseModel - Secure Public IDs
==========================================
'''
class UUIDBaseModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

'''
==========================================
 TimeStampedModel - For Logs & Analytics
==========================================
'''
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

'''
==========================================
 OrderedModel - Manual Ordering
==========================================
'''
class OrderedModel(BaseModel):
    position = models.PositiveSmallIntegerField(default=None, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["position", "-created_at"]

    def save(self, *args, **kwargs):
        if self.position is None and not self.pk:
            max_pos = self.__class__.objects.active().aggregate(models.Max('position'))['position__max']
            self.position = (max_pos or 0) + 1
        super().save(*args, **kwargs)

'''
==========================================
 SluggedModel - SEO Friendly URLs
==========================================
'''

class SluggedModel(models.Model):
    slug = models.SlugField(max_length=255, blank=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['slug']),
        ]

    SLUG_FIELD = "name"  # jis field se slug banega

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