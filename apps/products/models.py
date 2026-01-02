from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from apps.utilities.models import BaseModel


""" ========= Brand ========= """
class Brand(BaseModel):
    SIZE_SYSTEM_CHOICES = (
        ('EU', 'EU'),
        ('UK', 'UK'),
        ('KIDS', 'Kids'),
    )

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='products/logos/%Y/%m', blank=True)
    size_system = models.CharField(max_length=10, choices=SIZE_SYSTEM_CHOICES, default='EU')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


""" ============== Color =============== """
class Color(BaseModel):
    name = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.name


""" ============= Size ============== """
class Size(BaseModel):
    value = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=[('men', 'Men'), ('women', 'Women'), ('unisex', 'Unisex')])

    class Meta:
        unique_together = ('value', 'gender')
        ordering = ['gender', 'value']

    def __str__(self):
        return f"{self.value} ({self.gender})"


""" =========== Material ========== """
class Material(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


""" ========== Technology ========== """
class Technology(BaseModel):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name


""" ========== Style ========== """
class Style(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


""" =========== Category =========== """
class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='banners/', null=True, blank=True)

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
        return reverse('products:category_detail', kwargs={'slug': self.slug})


""" ============ Product ============ """
class Product(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)

    colors = models.ManyToManyField(Color, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    materials = models.ManyToManyField(Material, blank=True)
    styles = models.ManyToManyField(Style, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)

    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)

    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.sku:
            self.sku = f"PROD-{self.pk or 'TEMP'}-{slugify(self.title)[:8]}".upper()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_price(self):
        return self.sale_price if self.sale_price else self.price


""" ============ Product Image ============= """
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.title} - Image"
