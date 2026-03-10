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
        queryset = Product.objects.select_related("shop").prefetch_related("categories", "images").all()
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

    def get_queryset(self):
        """
        Optimize queries by prefetching related data:
        - shop (ForeignKey)
        - categories (ManyToMany)
        - images (ForeignKey)
        - options + option values (inlines)
        - variants
        """
        return Product.objects.select_related("shop").prefetch_related(
            "categories",
            "images",
            "options__values",
            "variants__option1",
            "variants__option2",
            "variants__option3",
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object

        '''prefetch otions with their values'''
        options = product.options.prefetch_related("values").all()
        context["options"] = options

        '''prefetch variants with their options'''
        variants = product.variants.select_related("option1", "option2", "option3").all()
        context["variants"] = variants

        '''prefetch images'''
        images = product.images.all()
        context["images"] = images

        '''prefetch categories'''
        categories = product.categories.all()
        context["categories"] = categories
        
        return context  
