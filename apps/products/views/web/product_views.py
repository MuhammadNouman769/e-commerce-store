""" =========== Importations =========== """
from django.shortcuts import render
from apps.products.models import Product, Category
from django.views.generic import ListView, DetailView

""" =========== Product List View =========== """
class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    '''process the context data to include categories'''
    def get_queryset(self):
        queryset = Product.objects.select_related("shop").prefetch_related("categories").all()
        # Get the category filter from the query parameters
        shop_id = self.request.GET.get("shop")
        vendor = self.request.GET.get("vendor")
        category_id = self.request.GET.get("category")

        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        if vendor:
            queryset = queryset.filter(vendor__iexact=vendor)
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        return queryset


""" =========== Product Detail View =========== """
class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/single-product.html"
    context_object_name = "product"     

    '''process the context data to include categories'''
    def get_queryset(self):
        # Prefetch categories and variants to optimize queries
        return Product.objects.select_related("shop").prefetch_related("categories", "variants")


          