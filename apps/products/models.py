
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.utilities.models import BaseModel


"""
========== Brand ==========
"""
class Brand(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/logos/%Y/%m/', blank=True, null=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


"""
============== Color ===============
"""
class Color(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True, help_text="e.g., #FF0000")

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"
        ordering = ['name']

    def __str__(self):
        return self.name


"""
============== Size ================
"""
class Size(BaseModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex'),
    )
    size = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    class Meta:
        unique_together = ('size', 'gender')
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
        ordering = ['gender', 'size']

    def __str__(self):
        return f"{self.size} ({self.get_gender_display()})"


"""
=========== Material ===========
"""
class Material(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"
        ordering = ['name']

    def __str__(self):
        return self.name


"""
========== Technology ==========
"""
class Technology(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        ordering = ['name']

    def __str__(self):
        return self.name


"""
=========== Style ===========
"""
class Style(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Style"
        verbose_name_plural = "Styles"
        ordering = ['name']

    def __str__(self):
        return self.name


"""
============ Category =============
"""
class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    image = models.ImageField(upload_to='categories/%Y/%m/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='categories/banners/%Y/%m/', blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        path = [self.name]
        p = self.parent
        while p:
            path.insert(0, p.name)
            p = p.parent
        return ' → '.join(path)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:products_list', kwargs={'slug': self.slug})


"""
============ Product ============
"""
class Product(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    # ManyToMany Relations
    colors = models.ManyToManyField(Color, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    materials = models.ManyToManyField(Material, blank=True)
    styles = models.ManyToManyField(Style, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)

    # Flags
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)

    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['brand']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if not self.sku:
            self.sku = f"PROD-{self.pk or 'NEW'}-{slugify(self.title)[:10].upper()}"

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    def get_price(self):
        return self.sale_price if self.sale_price and self.is_on_sale else self.price

    def get_primary_image(self):
        return self.images.filter(is_primary=True).first() or self.images.first()


"""
=========== Product Image ============
"""
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/%Y/%m/%d/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['-is_primary', 'id']

    def __str__(self):
        return f"{self.product.title} - {self.alt_text or 'Image'}"

    def save(self, *args, **kwargs):

        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)