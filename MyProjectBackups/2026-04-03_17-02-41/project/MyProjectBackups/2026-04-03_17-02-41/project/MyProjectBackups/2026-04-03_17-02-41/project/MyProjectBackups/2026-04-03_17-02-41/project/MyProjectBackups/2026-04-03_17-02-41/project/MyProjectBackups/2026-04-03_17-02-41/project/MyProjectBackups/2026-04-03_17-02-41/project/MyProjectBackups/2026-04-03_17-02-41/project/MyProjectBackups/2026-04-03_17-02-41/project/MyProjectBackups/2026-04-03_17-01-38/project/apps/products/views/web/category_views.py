""" ============= imprts ============= """
from django.views.generic import ListView
from apps.products.models import Category


""" ============= Category Views ============= """
class CategoryListView(ListView):
    model = Category
    template_name = "shop/product_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        # Optional shop filter
        shop_id = self.request.GET.get("shop")
        queryset = Category.objects.prefetch_related("children", "products")
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        return queryset
