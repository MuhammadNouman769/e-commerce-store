
                    ┌─────────────────┐
                    │   models.Model  │  (Django's built-in)
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼─────────┐ ┌─▼─────────────┐ ┌─▼──────────────────┐
    │   TimeStampedModel│ │   BaseModel   │ │                    │
    │  (Only timestamps)│ │ (Soft delete) │ │                    │
    └───────────────────┘ └───────┬───────┘ └────────────────────┘
                                  │
         ┌────────────────────────┼───────────────────────┐
         │                        │                       │
┌────────▼─────────┐    ┌─────────▼─────────┐    ┌────────▼─────────┐
│   OrderedModel   │    │   SluggedModel    │    │   UUIDBaseModel  │
│ (Adds position)  │    │  (Adds name/slug) │    │  (UUID instead   │
│                  │    │                   │    │  of BigAutoField)│
└──────────────────┘    └───────────────────┘    └──────────────────┘        

================================================================================
          BASE MODELS INHERITANCE HIERARCHY - COMPLETE DOCUMENTATION
================================================================================
Django Ecommerce Platform - Base Models Structure
Author: Muhammad Noman
Project: B.Store Ecommerce Platform
================================================================================

This file contains all base models and their complete documentation.
All models in the application should inherit from these base models.


from django.db import models
from django.utils import timezone
import uuid


# =================================================================================
# LEVEL 0: DJANGO'S BUILT-IN MODEL (For Reference Only)
# =================================================================================
# This is Django's built-in model class that all models inherit from
# It provides:
#   - Database connection
#   - QuerySet API
#   - Model validation
#   - Meta class support
#   - Manager support


# =================================================================================
# LEVEL 1: THREE BASE MODELS (Direct Inheritance from models.Model)
# =================================================================================

# --------------------------------------------------------------------------------
# 1. TimeStampedModel - For models that only need timestamps
# --------------------------------------------------------------------------------
class TimeStampedModel(models.Model):
    """
    PURPOSE: For models that only need timestamps without soft delete.
    
    FIELDS:
        - created_at: When record was created
        - updated_at: When record was last modified
    
    WHEN TO USE:
        - Logs (user activity logs, error logs)
        - Analytics data (page views, click tracking)
        - Audit trails (who did what and when)
        - System metrics (performance data)
    
    WHY NOT USE BASEMODEL:
        - Soft delete (is_active) is unnecessary for logs
        - Logs should never be deleted for compliance
        - Keeps database clean (no extra fields)
    
    EXAMPLE USAGE:
        class PageViewLog(TimeStampedModel):
            page_url = models.URLField()
            user_ip = models.GenericIPAddressField()
            session_key = models.CharField(max_length=40)
    """
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Date and time when this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Date and time when this record was last updated"
    )
    
    class Meta:
        abstract = True
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['-created_at'], name='%(class)s_created_at_idx'),
        ]
    
    def __str__(self):
        return f"{self.__class__.__name__} #{self.id}"


# --------------------------------------------------------------------------------
# 2. BaseModel - Core model with soft delete and timestamps
# --------------------------------------------------------------------------------
class BaseModel(models.Model):
    """
    PURPOSE: Core base model with soft delete and timestamps.
    This is the foundation for most business models.
    
    FIELDS:
        - id: BigAutoField (supports billions of records)
        - created_at: When record was created
        - updated_at: When record was last modified
        - is_active: Soft delete flag (True=active, False=deleted)
    
    METHODS:
        - delete(): Soft delete (mark as inactive)
        - hard_delete(): Permanently delete from database
        - restore(): Restore soft-deleted record
        - is_deleted: Property to check if record is deleted
    
    WHEN TO USE:
        - Main business models: Product, Order, User, Category
        - Any model where data should be recoverable
        - Models that need audit trail
    
    WHY USE SOFT DELETE:
        - Preserve order history (users can see past orders)
        - Maintain analytics data (sales reports remain accurate)
        - Easy recovery of accidentally deleted items
        - GDPR compliance (can hard delete if needed)
    
    EXAMPLE USAGE:
        class Product(BaseModel):
            name = models.CharField(max_length=255)
            price = models.DecimalField(max_digits=12, decimal_places=2)
            # Inherits: id, created_at, updated_at, is_active
    """
    
    # Primary Key - BigAutoField for scalability (supports billions of records)
    id = models.BigAutoField(
        primary_key=True,
        verbose_name="ID",
        help_text="Unique identifier for this record"
    )
    
    # Timestamp Fields - Automatically managed by Django
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Date and time when this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Date and time when this record was last updated"
    )
    
    # Soft Delete Flag - Instead of permanent deletion
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Soft delete flag: True = active, False = deleted/hidden"
    )
    
    class Meta:
        abstract = True
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['is_active'], name='%(class)s_is_active_idx'),
            models.Index(fields=['-created_at'], name='%(class)s_created_at_idx'),
        ]
    
    def __str__(self):
        """Human-readable representation of the model"""
        return f"{self.__class__.__name__} #{self.id}"
    
    def delete(self, using=None, keep_parents=False):
        """
        SOFT DELETE - Mark as inactive instead of permanent deletion
        This is the default delete behavior for all models
        """
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])
    
    def hard_delete(self, using=None, keep_parents=False):
        """
        PERMANENT DELETE - Actually remove from database
        Use with caution - only when absolutely necessary
        """
        super().delete(using=using, keep_parents=keep_parents)
    
    def restore(self):
        """
        RESTORE - Reactivate a soft-deleted record
        Useful when admin wants to bring back a deleted product
        """
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])
    
    @property
    def is_deleted(self):
        """Check if record is soft-deleted"""
        return not self.is_active
    
    @property
    def age_in_days(self):
        """Calculate how many days old this record is"""
        delta = timezone.now() - self.created_at
        return delta.days


# =================================================================================
# LEVEL 2: SPECIALIZED BASE MODELS (Inherit from BaseModel)
# =================================================================================

# --------------------------------------------------------------------------------
# 3. OrderedModel - Adds manual ordering/positioning
# --------------------------------------------------------------------------------
class OrderedModel(BaseModel):
    """
    PURPOSE: Adds manual ordering/positioning to BaseModel.
    Inherits all BaseModel fields + adds position field.
    
    FIELDS (inherited from BaseModel):
        - id, created_at, updated_at, is_active
    
    ADDITIONAL FIELDS:
        - position: Manual order (lower numbers appear first)
    
    FEATURES:
        - Auto-assigns position if not provided
        - Orders items by position automatically
        - New items go to the end (highest position number)
    
    WHEN TO USE:
        - Categories (homepage order)
        - Product images (gallery order)
        - Menu items (navigation order)
        - Banner slides (carousel order)
        - FAQ items (question order)
    
    WHY INHERIT FROM BASEMODEL:
        - Needs soft delete (categories can be hidden)
        - Needs timestamps (track when order changed)
        - BaseModel provides all core fields
    
    EXAMPLE USAGE:
        class Category(OrderedModel):
            name = models.CharField(max_length=255)
            parent = models.ForeignKey('self', null=True, blank=True)
            # Inherits: id, created_at, updated_at, is_active, position
            # Categories will appear in order of position
    """
    
    position = models.PositiveSmallIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name="Position",
        help_text="Lower numbers appear first (auto-assigned if not provided)"
    )
    
    class Meta:
        abstract = True
        ordering = ["position", "-created_at"]  # First by position, then by date
        indexes = [
            models.Index(fields=['position'], name='%(class)s_position_idx'),
        ]
    
    def save(self, *args, **kwargs):
        """
        Auto-assign position if not set.
        New items get the next highest position number.
        """
        if self.position is None and not self.pk:
            # Get current maximum position
            max_position = self.__class__.objects.filter(
                is_active=True
            ).aggregate(
                models.Max('position')
            )['position__max']
            self.position = (max_position or 0) + 1
        super().save(*args, **kwargs)


# --------------------------------------------------------------------------------
# 4. SluggedModel - Adds SEO-friendly URL slugs
# --------------------------------------------------------------------------------
class SluggedModel(BaseModel):
    """
    PURPOSE: Adds SEO-friendly URL slugs to BaseModel.
    Inherits all BaseModel fields + adds name and slug fields.
    
    FIELDS (inherited from BaseModel):
        - id, created_at, updated_at, is_active
    
    ADDITIONAL FIELDS:
        - name: Human-readable display name
        - slug: URL-friendly version (auto-generated)
    
    FEATURES:
        - Auto-generates slug from name
        - Ensures slug uniqueness by adding numbers
        - Indexed for fast database lookups
        - Clean __str__ method returns name
    
    WHEN TO USE:
        - Products (URL: /products/nike-air-max)
        - Categories (URL: /categories/mens-shoes)
        - Blog posts (URL: /blog/how-to-shop)
        - Pages (URL: /about-us)
        - Brands (URL: /brands/nike)
    
    WHY INHERIT FROM BASEMODEL:
        - Needs soft delete (products can be archived)
        - Needs timestamps (track when created)
        - BaseModel provides all core fields
    
    EXAMPLE USAGE:
        class Product(SluggedModel):
            price = models.DecimalField(max_digits=12, decimal_places=2)
            description = models.TextField()
            # Inherits: id, created_at, updated_at, is_active, name, slug
            # URL will be: /products/nike-air-max-shoes
    """
    
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        help_text="Display name (e.g., 'Nike Air Max')"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="URL-friendly version (auto-generated from name)"
    )
    
    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['slug'], name='%(class)s_slug_idx'),
            models.Index(fields=['name'], name='%(class)s_name_idx'),
        ]
    
    def save(self, *args, **kwargs):
        """
        Auto-generate unique slug from name.
        Example: "Nike Air Max" → "nike-air-max"
        If exists: "nike-air-max-1", "nike-air-max-2", etc.
        """
        from django.utils.text import slugify
        
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            # Check uniqueness across all records (including deleted)
            while self.__class__.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# --------------------------------------------------------------------------------
# 5. UUIDBaseModel - Uses UUID instead of sequential integer IDs
# --------------------------------------------------------------------------------
class UUIDBaseModel(BaseModel):
    """
    PURPOSE: Uses UUID instead of sequential integer IDs.
    Inherits all BaseModel fields but overrides id field.
    
    FIELDS (overridden from BaseModel):
        - id: UUIDField instead of BigAutoField
    
    FIELDS (inherited from BaseModel):
        - created_at, updated_at, is_active
    
    BENEFITS OF UUID:
        - Security: IDs are not sequential (can't guess next order number)
        - Privacy: Total record count is hidden
        - Distributed Systems: Unique across multiple databases
        - API Safety: No ID enumeration attacks
    
    WHEN TO USE:
        - Orders (order numbers should be hard to guess)
        - Payments (transaction IDs)
        - API Keys (authentication tokens)
        - Public User Profiles (profile URLs)
        - Any public-facing ID
    
    WHY INHERIT FROM BASEMODEL:
        - Needs soft delete (orders can be cancelled)
        - Needs timestamps (track order dates)
        - BaseModel provides all other fields
    
    EXAMPLE USAGE:
        class Order(UUIDBaseModel):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
            total_amount = models.DecimalField(max_digits=12, decimal_places=2)
            # Inherits: id (UUID), created_at, updated_at, is_active
            # Order ID: 550e8400-e29b-41d4-a716-446655440000
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
        help_text="Unique UUID identifier (not sequential for security)"
    )
    
    class Meta:
        abstract = True
        ordering = ["-created_at"]


# =================================================================================
# MULTIPLE INHERITANCE - COMBINING MULTIPLE BASE MODELS
# =================================================================================

# --------------------------------------------------------------------------------
# Example: Category Model (Ordered + Slugged)
# --------------------------------------------------------------------------------
# This is an example of how to use multiple inheritance
# Uncomment and use in your products app

"""
class Category(OrderedModel, SluggedModel):
    \"""
    Multiple inheritance example.
    Gets features from both OrderedModel and SluggedModel.
    
    FIELDS RECEIVED:
        From OrderedModel:
            - position (manual ordering)
        From SluggedModel:
            - name, slug (SEO URLs)
        From BaseModel (through both):
            - id, created_at, updated_at, is_active (soft delete)
    
    USAGE:
        categories = Category.objects.all()
        # Returns categories ordered by position
        # Each category has SEO-friendly URL
    \"""
    
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    icon = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    
    class Meta:
        ordering = ['position', 'name']
    
    def __str__(self):
        return self.name
    
    def get_full_path(self):
        \"""Get full category path (Parent > Child)\"""
        path = [self.name]
        parent = self.parent
        while parent:
            path.append(parent.name)
            parent = parent.parent
        return " > ".join(reversed(path))
"""


# =================================================================================
# COMPLETE INHERITANCE MATRIX
# =================================================================================
"""
┌─────────────────┬───────────────────┬─────────────────────────────────────────┬──────────────────────────┐
│ Model Name      │ Inherits From     │ Fields Received                         │ Purpose                  │
├─────────────────┼───────────────────┼─────────────────────────────────────────┼──────────────────────────┤
│ TimeStampedModel│ models.Model      │ created_at, updated_at                  │ Logs, analytics          │
│ BaseModel       │ models.Model      │ id, created_at, updated_at, is_active   │ Core business models     │
│ OrderedModel    │ BaseModel         │ + position                              │ Sortable items           │
│ SluggedModel    │ BaseModel         │ + name, slug                            │ SEO-friendly URLs        │
│ UUIDBaseModel   │ BaseModel         │ id (UUID) instead of BigAutoField       │ Secure public IDs        │
└─────────────────┴───────────────────┴─────────────────────────────────────────┴──────────────────────────┘
"""


# =================================================================================
# DECISION TREE - WHICH BASE MODEL TO USE
# =================================================================================
"""
START: Do you need to track when records are created/modified?
    │
    ├── NO → Use models.Model directly
    │
    └── YES → Do you need soft delete (is_active)?
              │
              ├── NO → Use TimeStampedModel
              │
              └── YES → Do you need SEO-friendly URLs (slug)?
                        │
                        ├── YES → Do you need manual ordering?
                        │         │
                        │         ├── YES → Use both OrderedModel + SluggedModel
                        │         │
                        │         └── NO → Use SluggedModel
                        │
                        └── NO → Do you need manual ordering?
                                │
                                ├── YES → Use OrderedModel
                                │
                                └── NO → Do you need UUID for security?
                                        │
                                        ├── YES → Use UUIDBaseModel
                                        │
                                        └── NO → Use BaseModel
"""


# =================================================================================
# BEST PRACTICES SUMMARY
# =================================================================================
"""
1. Always use TimeStampedModel for logs - Never delete logs
2. Use BaseModel for main business models - Products, Users, Orders
3. Use SluggedModel for public URLs - Products, Categories, Blog
4. Use OrderedModel for sortable items - Categories, Images, Menu
5. Use UUIDBaseModel for security - Orders, Payments, API keys
6. Use multiple inheritance when needed - Category needs both order + slug


# =================================================================================
# EXAMPLE: COMPLETE PRODUCT MODEL
# =================================================================================
"""
class Product(SluggedModel):  # Uses SluggedModel (BaseModel features)
    \"""
    Daraz-style product model with:
    - Soft delete (can hide products)
    - Timestamps (track when added)
    - SEO-friendly URL (auto-generated from name)
    \
    
    # Custom fields
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    shop = models.ForeignKey('products.Shop', on_delete=models.CASCADE)
    
    # Inherited fields from SluggedModel → BaseModel:
    # - id (BigAutoField)
    # - created_at, updated_at
    # - is_active (soft delete)
    # - name, slug (auto-generated)
    
    def __str__(self):
        return self.name
    
    @property
    def discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return int(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0



# =================================================================================
# END OF BASE MODELS FILE
# =================================================================================