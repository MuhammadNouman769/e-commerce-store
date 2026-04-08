from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q, Min, Max, Count, F
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product, Category, ProductStatus


class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    allowed_per_page = (4, 8, 12, 24, 48)
    allowed_cols = (2, 3, 4, 5, 6)

    def get_queryset(self):
        """Get filtered and sorted products - only active ones"""
        queryset = Product.objects.filter(status=ProductStatus.ACTIVE).select_related(
            "shop"
        ).prefetch_related(
            "categories", "images", "variants"
        )

        # Search query
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description_html__icontains=q) |
                Q(brand__icontains=q)
            )

        # Shop filter
        shop_id = self.request.GET.get("shop")
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)

        # Vendor/Brand filter
        vendors = [v for v in self.request.GET.getlist("vendor") if v]
        if vendors:
            vendor_q = Q()
            for v in vendors:
                vendor_q |= Q(brand__iexact=v)
            queryset = queryset.filter(vendor_q)

        # Category filter
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        # Price filter
        try:
            min_price = int(self.request.GET.get("min_price")) if self.request.GET.get("min_price") else None
            max_price = int(self.request.GET.get("max_price")) if self.request.GET.get("max_price") else None
        except (TypeError, ValueError):
            min_price = max_price = None

        if min_price is not None:
            queryset = queryset.filter(variants__price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(variants__price__lte=max_price)

        # Sorting
        sort = self.request.GET.get("sort", "").strip()
        if sort == "price_asc":
            queryset = queryset.annotate(min_price=Min("variants__price")).order_by("min_price", "-id")
        elif sort == "price_desc":
            queryset = queryset.annotate(min_price=Min("variants__price")).order_by("-min_price", "-id")
        elif sort == "brand_asc":
            queryset = queryset.order_by("brand", "-id")
        elif sort == "newest":
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("-created_at")  # default newest first

        return queryset.distinct()

    def get_paginate_by(self, queryset):
        try:
            per_page = int(self.request.GET.get("per_page", self.paginate_by))
        except (TypeError, ValueError):
            per_page = self.paginate_by
        return per_page if per_page in self.allowed_per_page else self.paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Categories caching
        cache_key = f"categories_list_{self.request.GET.get('shop', 'all')}"
        categories = cache.get(cache_key)
        if categories is None:
            categories = Category.objects.filter(parent=None).prefetch_related(
                "children",
                "children__children",
                "products"
            )
            cache.set(cache_key, categories, 3600)
        context["categories"] = categories

        # Vendors/Brands
        vendors_qs = Product.objects.filter(status=ProductStatus.ACTIVE).exclude(brand__isnull=True).exclude(brand__exact="").values("brand").annotate(count=Count("id")).order_by("brand")
        context["vendors"] = [v["brand"] for v in vendors_qs]
        context["vendor_counts"] = {v["brand"]: v["count"] for v in vendors_qs}
        context["selected_vendors"] = [v for v in self.request.GET.getlist("vendor") if v]

        # Vendor logos (example)
        known_logos = {
            "apple": "img/brands/apple.svg",
            "samsung": "img/brands/samsung.svg",
            "oppo": "img/brands/oppo.svg",
            "vivo": "img/brands/vivo.svg",
            "xiaomi": "img/brands/xiaomi.svg",
        }
        vendor_items = []
        for name in context["vendors"]:
            key = (name or "").strip().lower()
            vendor_items.append({
                "name": name,
                "logo": known_logos.get(key),
                "count": context["vendor_counts"].get(name, 0)
            })
        context["vendor_items"] = vendor_items

        # Price ranges
        price_stats = Product.objects.filter(status=ProductStatus.ACTIVE, variants__price__isnull=False).aggregate(
            min_price=Min("variants__price"),
            max_price=Max("variants__price")
        )
        actual_min = int(price_stats["min_price"] or 0)
        actual_max = int(price_stats["max_price"] or 100000)
        step = 10000
        ranges = [{"min": None, "max": actual_min + step, "label": _("Below Rs {:,}").format(actual_min + step)}]
        start = actual_min + step
        while start < actual_max:
            end = min(start + step, actual_max)
            ranges.append({"min": start, "max": end, "label": f"Rs {start:,} - Rs {end:,}"})
            start += step
        context["price_ranges"] = ranges

        # Pagination & layout
        context["per_page"] = self.get_paginate_by(self.get_queryset())
        context["allowed_per_page"] = self.allowed_per_page
        context["sort"] = self.request.GET.get("sort", "").strip() or "newest"
        layout = self.request.GET.get("layout", "grid").strip().lower()
        context["layout"] = layout if layout in ("grid", "list") else "grid"
        try:
            cols = int(self.request.GET.get("cols", 4))
        except (TypeError, ValueError):
            cols = 4
        context["cols"] = cols if cols in self.allowed_cols else 4
        context["allowed_cols"] = self.allowed_cols

        # Preserved filters
        preserved_filters = [(k, v) for k, v in self.request.GET.items() if k not in ("page", "per_page")]
        context["preserved_filters"] = preserved_filters

        return context


""" =========== Product Detail View =========== """
class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/single-product.html"
    context_object_name = "product"

    def get_queryset(self):
        """Only active products"""
        return Product.objects.filter(
            status=Product.ProductStatus.ACTIVE  # ← IMPORTANT FIX
        ).select_related("shop").prefetch_related(
            "categories",
            "images",
            "options__values",
            "variants__option1__option",
            "variants__option2__option",
            "variants__option3__option",
        )

    def get_object(self, queryset=None):
        """Get product by pk or handle/slug"""
        if queryset is None:
            queryset = self.get_queryset()
        
        pk = self.kwargs.get("pk")
        handle = self.kwargs.get("handle") or self.kwargs.get("slug")
        
        if pk:
            return get_object_or_404(queryset, pk=pk)
        elif handle:
            return get_object_or_404(queryset, handle=handle)
        else:
            return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Options
        context["options"] = product.options.prefetch_related("values").order_by("position")
        
        # Variants
        context["variants"] = product.variants.select_related(
            "option1__option", "option2__option", "option3__option"
        ).order_by("position")
        
        # Images
        context["images"] = product.images.order_by("position")
        
        # Categories
        context["categories"] = product.categories.filter(is_visible=True)
        
        # Related products
        category_ids = context["categories"].values_list("id", flat=True)
        if category_ids:
            related = Product.objects.filter(
                categories__id__in=category_ids,
                status=Product.ProductStatus.ACTIVE
            ).exclude(pk=product.pk).select_related("shop").prefetch_related(
                "images", "variants"
            ).distinct()[:6]
        else:
            related = Product.objects.filter(
                shop=product.shop,
                status=Product.ProductStatus.ACTIVE
            ).exclude(pk=product.pk).select_related("shop").prefetch_related(
                "images", "variants"
            )[:6]
        
        context["related_products"] = related
        
        # Discount
        first_variant = context["variants"].first()
        discount_pct = 0
        if first_variant and first_variant.compare_at_price:
            if first_variant.compare_at_price > first_variant.price:
                discount_pct = round(
                    (1 - float(first_variant.price) / float(first_variant.compare_at_price)) * 100
                )
        context["discount_pct"] = discount_pct
        
        # JSON data for JavaScript
        variants_data = []
        for variant in context["variants"]:
            variant_data = {
                "id": variant.id,
                "price": float(variant.price),
                "compare_at_price": float(variant.compare_at_price) if variant.compare_at_price else None,
                "sku": variant.sku,
                "options": {}
            }
            if variant.option1:
                variant_data["options"][variant.option1.option.name] = variant.option1.value
            if variant.option2:
                variant_data["options"][variant.option2.option.name] = variant.option2.value
            if variant.option3:
                variant_data["options"][variant.option3.option.name] = variant.option3.value
            variants_data.append(variant_data)
        
        context["variants_json"] = variants_data
        
        return context


""" =========== Category Views =========== """
class CategoryListView(ListView):
    model = Category
    template_name = "shop/category_list.html"  # ← Alag template
    context_object_name = "categories"
    paginate_by = 24

    def get_queryset(self):
        shop_id = self.request.GET.get("shop")
        queryset = Category.objects.filter(
            is_visible=True
        ).select_related("shop").prefetch_related(
            "children", "products"
        ).annotate(
            product_count=Count("products", filter=Q(products__status=Product.ProductStatus.ACTIVE))
        )
        
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        
        # Only show categories with products or children
        return queryset.filter(
            Q(product_count__gt=0) | Q(children__isnull=False)
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Product Categories")
        context["root_categories"] = context["categories"].filter(parent=None)
        return context