
"""=============== Imports ==============="""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category, Brand, Color, Size, Style, Material, Technology


"""=============== Product List with All Filters ==============="""
def products_list(request):
    products = Product.objects.filter(is_active=True)

    # ===== Get filter values from GET =====
    brand_slug = request.GET.get('brand')
    category_slug = request.GET.get('category')
    color_id = request.GET.get('color')
    size_id = request.GET.get('size')
    style_slug = request.GET.get('style')
    material_id = request.GET.get('material')
    technology_id = request.GET.get('technology')

    """ ===== Apply filters ===== """
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if color_id:
        products = products.filter(colors__id=color_id)
    if size_id:
        products = products.filter(sizes__id=size_id)
    if style_slug:
        products = products.filter(styles__slug=style_slug)
    if material_id:
        products = products.filter(materials__id=material_id)
    if technology_id:
        products = products.filter(technologies__id=technology_id)

    products = products.distinct().order_by('-created_at')

    """ ===== Pagination ===== """
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    """ ===== Context for template ====="""
    context = {
        'products': products,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
        'sizes': Size.objects.all(),
        'styles': Style.objects.all(),
        'materials': Material.objects.all(),
        'technologies': Technology.objects.all(),
        'selected_filters': request.GET,
    }
    return render(request, 'products/products.html', context)


"""=============== Product Detail View ==============="""
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {'product': product}
    return render(request, 'products/product-detail.html', context)
