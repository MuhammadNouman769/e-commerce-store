"""=============== Imports ==============="""
from django.shortcuts import render
from .models import Product, Category, Brand, Color, Size

"""=============== Product List with All Filters ==============="""
def product_list(request):
    products = Product.objects.filter(is_active=True)

    # ===== Get filter values from GET =====
    brand_slug = request.GET.get('brand')
    category_slug = request.GET.get('category')
    color_id = request.GET.get('color')
    size_id = request.GET.get('size')

    # ===== Apply filters =====
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if color_id:
        products = products.filter(colors__id=color_id)
    if size_id:
        products = products.filter(sizes__id=size_id)

    products = products.distinct().order_by('-created_at')

    # ===== Context for template =====
    context = {
        'products': products,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
        'sizes': Size.objects.all(),
        'selected_filters': request.GET,  # preserve selected filters
    }

    return render(request, 'products/products.html', context)




"""=============== Product Detail View ==============="""
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {
        'product': product
    }
    return render(request, 'products/product-detail.html', context)
