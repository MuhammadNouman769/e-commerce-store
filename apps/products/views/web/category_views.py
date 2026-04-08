from django.views.generic import ListView
from django.core.cache import cache
from apps.products.models import Category, Product


class CategoryListView(ListView):
    model = Category
    template_name = "shop/product_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        """Return top-level categories with children and products prefetched."""
        queryset = Category.objects.filter(parent=None).prefetch_related(
            "children",
            "children__children",
            "products",
        )

        # Optional shop filter
        shop_id = self.request.GET.get("shop")
        if shop_id:
            queryset = queryset.filter(products__shop_id=shop_id).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Caching categories for 1 hour
        shop_key = self.request.GET.get("shop", "all")
        cache_key = f"categories_list_{shop_key}"
        categories = cache.get(cache_key)
        if categories is None:
            categories = self.get_queryset()
            cache.set(cache_key, categories, 3600)  # cache 1 hour
        context["categories"] = categories

        return context