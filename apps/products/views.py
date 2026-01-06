from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from .models import (
    Product, Category, Brand,
    Color, Size, Style, Material, Technology
)

"""=============== Product List View ==============="""
class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        products = Product.objects.filter(is_active=True)
        request = self.request

        if request.GET.get('brand'):
            products = products.filter(brand__slug=request.GET.get('brand'))

        if request.GET.get('category'):
            products = products.filter(category__slug=request.GET.get('category'))

        if request.GET.get('color'):
            products = products.filter(colors__id=request.GET.get('color'))

        if request.GET.get('size'):
            products = products.filter(sizes__id=request.GET.get('size'))

        if request.GET.get('style'):
            products = products.filter(styles__slug=request.GET.get('style'))

        if request.GET.get('material'):
            products = products.filter(materials__id=request.GET.get('material'))

        if request.GET.get('technology'):
            products = products.filter(technologies__id=request.GET.get('technology'))

        return products.distinct().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['brand'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        context['colors'] = Color.objects.all()
        context['sizes'] = Size.objects.all()
        context['styles'] = Style.objects.all()
        context['materials'] = Material.objects.all()
        context['technologies'] = Technology.objects.all()
        context['selected_filters'] = self.request.GET

        return context


"""=============== Product Detail View ==============="""
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        context['sizes'] = product.sizes.all()
        context['colors'] = product.colors.all()
        context['styles'] = product.styles.all()
        context['materials'] = product.materials.all()
        context['technologies'] = product.technologies.all()
        context['images'] = product.images.all() if hasattr(product, 'images') else []


        context['reviews'] = []

        return context
