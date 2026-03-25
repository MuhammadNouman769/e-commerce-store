""" =========== Importations =========== """
from django.shortcuts import render
from apps.products.models import Product, Category
from django.views.generic import ListView, DetailView
from django.db.models import Count, Min, Q
from urllib.parse import urlencode

""" =========== Product List View =========== """
class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    allowed_per_page = (4, 8, 12)
    allowed_cols = (2, 4, 5, 6)

    
    '''process the context data to include categories'''
    def get_queryset(self):
        queryset = Product.objects.select_related("shop").prefetch_related("categories", "images", "variants").all()

        # search query
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description_html__icontains=q) |
                Q(vendor__icontains=q)
        )

        # Get the category filter from the query parameters
        shop_id = self.request.GET.get("shop")
        vendors = [v for v in self.request.GET.getlist("vendor") if v]
        category_id = self.request.GET.get("category")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        sort = (self.request.GET.get("sort") or "").strip()

            # Price values as integers
        try:
            min_price = int(self.request.GET.get("min_price")) if self.request.GET.get("min_price") else None
            max_price = int(self.request.GET.get("max_price")) if self.request.GET.get("max_price") else None
        except ValueError:
            min_price = max_price = None

        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        if vendors:
            vq = Q()
            for v in vendors:
                vq |= Q(vendor__iexact=v)
            queryset = queryset.filter(vq)
        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        # Filter by price safely
        if min_price is not None:
            queryset = queryset.filter(variants__price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(variants__price__lte=max_price)

        # Sorting (vendor / price)
        if sort in ("price_asc", "price_desc"):
            queryset = queryset.annotate(_min_price=Min("variants__price"))
            queryset = queryset.order_by(("_min_price" if sort == "price_asc" else "-_min_price"), "-id")
        elif sort == "vendor_asc":
            queryset = queryset.order_by("vendor", "-id")
        else:
            # default: newest first
            queryset = queryset.order_by("-id")

        return queryset.distinct()

    def get_paginate_by(self, queryset):
        try:
            per_page = int(self.request.GET.get("per_page") or self.paginate_by)
        except (TypeError, ValueError):
            per_page = self.paginate_by

        if per_page not in self.allowed_per_page:
            per_page = self.paginate_by

        return per_page


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        ''' category for sidebar (multi-level) '''
        categories = (
            Category.objects
            .filter(parent=None)
            .prefetch_related(
                "children",                # level 1
                "children__children",      # level 2
                "children__children__children",  # level 3 (safety)
            )
        )
        context["categories"] = categories
            
            # Correct vendors query
        vendors_qs = (
            Product.objects.exclude(vendor__isnull=True)
            .exclude(vendor__exact="")
            .values("vendor")
            .annotate(count=Count("id"))
            .order_by("vendor")
        )
        vendors = [v["vendor"] for v in vendors_qs]
        context["vendors"] = vendors
        context["vendor_counts"] = {v["vendor"]: v["count"] for v in vendors_qs}
        context["selected_vendors"] = [v for v in self.request.GET.getlist("vendor") if v]

        # Static brand logos (optional)
        known_logos = {
            "apple": "img/brands/apple.svg",
            "samsung": "img/brands/samsung.svg",
            "oppo": "img/brands/oppo.svg",
            "vivo": "img/brands/vivo.svg",
            "xiaomi": "img/brands/xiaomi.svg",
            "infinix": "img/brands/infinix.svg",
            "tecno": "img/brands/tecno.svg",
            "nothing": "img/brands/nothing.svg",
        }
        vendor_items = []
        for name in vendors:
            key = (name or "").strip().lower()
            vendor_items.append(
                {
                    "name": name,
                    "logo": known_logos.get(key),
                }
            )
        context["vendor_items"] = vendor_items

        # Pagination helpers (preserve filters across page/per_page changes)
        context["per_page"] = self.get_paginate_by(self.get_queryset())
        context["allowed_per_page"] = self.allowed_per_page
        context["sort"] = (self.request.GET.get("sort") or "").strip() or "default"

        # View helpers (grid columns / list)
        layout = (self.request.GET.get("layout") or "").strip().lower() or "grid"
        if layout not in ("grid", "list"):
            layout = "grid"
        try:
            cols = int(self.request.GET.get("cols") or 4)
        except (TypeError, ValueError):
            cols = 4
        if cols not in self.allowed_cols:
            cols = 4
        context["layout"] = layout
        context["cols"] = cols
        context["allowed_cols"] = self.allowed_cols

        preserved_filters = [(k, v) for k, v in self.request.GET.items() if k not in ("page", "per_page")]
        context["preserved_filters"] = preserved_filters

        qs_no_page = self.request.GET.copy()
        qs_no_page.pop("page", None)
        context["querystring_without_page"] = qs_no_page.urlencode()

        qs_no_page_per_page = qs_no_page.copy()
        qs_no_page_per_page.pop("per_page", None)
        context["querystring_without_page_and_per_page"] = qs_no_page_per_page.urlencode()

        qs_no_view = qs_no_page.copy()
        qs_no_view.pop("cols", None)
        qs_no_view.pop("layout", None)
        context["querystring_without_page_and_view"] = qs_no_view.urlencode()

        qs_no_price = qs_no_page.copy()
        qs_no_price.pop("min_price", None)
        qs_no_price.pop("max_price", None)
        context["querystring_without_page_and_price"] = qs_no_price.urlencode()

        # Price range buttons (15k to 100k with 10k step + below 10k)
        ranges = [
            {"min": None, "max": 10000, "label": "Below Rs 10,000"},
            {"min": 15000, "max": 25000, "label": "Rs 15,000 - Rs 25,000"},
        ]
        for start in range(15000, 100000, 10000):
            end = min(start + 10000, 100000)
            if start == 15000 and end == 25000:
                continue  # already added above
            ranges.append({"min": start, "max": end, "label": f"Rs {start:,} - Rs {end:,}"})
        context["price_ranges"] = ranges

        return context


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
        product = self.get_object()

        '''prefetch options with their values'''
        options = product.options.prefetch_related("values").all()
        context["options"] = options

        '''prefetch variants with their options'''
        variants = product.variants.select_related("option1", "option2", "option3").order_by("position").all()
        context["variants"] = variants

        '''prefetch images'''
        images = product.images.all()
        context["images"] = images

        '''prefetch categories'''
        categories = product.categories.all()
        context["categories"] = categories

        '''related products (same category, exclude current, limit 6) - for accessories/get yours'''
        category_ids = product.categories.values_list("id", flat=True)
        related = (
            Product.objects.filter(categories__id__in=category_ids, status=Product.ProductStatus.ACTIVE)
            .exclude(pk=product.pk)
            .select_related("shop")
            .prefetch_related("images", "variants")
            .distinct()[:6]
        )
        context["related_products"] = related

        '''discount % for first variant (for display)'''
        first_variant = variants.first()
        discount_pct = 0
        if first_variant and first_variant.compare_at_price and first_variant.compare_at_price > first_variant.price:
            discount_pct = round((1 - float(first_variant.price) / float(first_variant.compare_at_price)) * 100)
        context["discount_pct"] = discount_pct

        return context
