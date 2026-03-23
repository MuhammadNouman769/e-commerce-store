from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.order_fulfillment.models import BillingDetail
from apps.products.models import Product, ProductVariant, Shop
from apps.users.choices import UserRoleChoices

from .forms import SellerProductForm, ShopForm

@login_required
def seller_dashboard(request):
    if request.user.role != UserRoleChoices.SELLER:
        return redirect("home")

    shop = Shop.objects.filter(owner=request.user).first()
    products_count = 0
    sales_count = 0
    revenue_total = Decimal("0.00")

    if shop:
        products_count = Product.objects.filter(shop=shop).count()

        sales_qs = BillingDetail.objects.filter(cart__items__product__shop=shop).distinct()
        sales_count = sales_qs.count()
        # Sum only items that belong to this seller's shop.
        revenue_total = Decimal("0.00")
        for billing in sales_qs:
            items_qs = billing.cart.items.filter(product__shop=shop).only("price", "quantity")
            revenue_total += sum((i.total_price for i in items_qs), Decimal("0.00"))

    return render(
        request,
        "admin_panel/seller/dashboard.html",
        {
            "shop": shop,
            "products_count": products_count,
            "sales_count": sales_count,
            "revenue_total": revenue_total,
        },
    )


@login_required
def seller_shop_setup(request):
    if request.user.role != UserRoleChoices.SELLER:
        return redirect("home")

    shop = Shop.objects.filter(owner=request.user).first()

    if request.method == "POST":
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            seller_shop = form.save(commit=False)
            # Ensure owner is always set to current seller.
            seller_shop.owner = request.user
            seller_shop.save()
            messages.success(request, "Shop saved successfully!")
            return redirect("admin_panel:seller_dashboard")
    else:
        form = ShopForm(instance=shop)

    return render(
        request,
        "admin_panel/seller/shop_setup.html",
        {"form": form, "shop": shop},
    )


@login_required
def seller_product_list(request):
    if request.user.role != UserRoleChoices.SELLER:
        return redirect("home")

    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        return redirect("admin_panel:seller_shop_setup")

    products = Product.objects.filter(shop=shop).order_by("-id")
    return render(
        request,
        "admin_panel/seller/products/list.html",
        {"shop": shop, "products": products},
    )


@login_required
@transaction.atomic
def seller_product_create(request):
    if request.user.role != UserRoleChoices.SELLER:
        return redirect("home")

    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        return redirect("admin_panel:seller_shop_setup")

    if request.method == "POST":
        form = SellerProductForm(request.POST, shop=shop)
        if form.is_valid():
            cd = form.cleaned_data

            # Create product first, handle auto-generated in model save().
            product = Product.objects.create(
                shop=shop,
                title=cd["title"],
                description_html=cd.get("description_html", ""),
                vendor=cd.get("vendor", ""),
                product_type=cd.get("product_type", ""),
                status=cd["status"],
                published_at=(timezone.now() if cd["status"] == Product.ProductStatus.ACTIVE else None),
            )
            categories = cd.get("categories") or []
            if categories:
                product.categories.set(categories)

            # Minimal variant: one variant with price.
            ProductVariant.objects.create(
                product=product,
                price=cd["price"],
                sku=(cd.get("sku") or None),
                position=0,
            )

            messages.success(request, "Product created successfully!")
            return redirect("admin_panel:seller_product_list")
    else:
        form = SellerProductForm(shop=shop)

    return render(
        request,
        "admin_panel/seller/products/new.html",
        {"shop": shop, "form": form},
    )


@login_required
def seller_sales(request):
    if request.user.role != UserRoleChoices.SELLER:
        return redirect("home")

    shop = Shop.objects.filter(owner=request.user).first()
    if not shop:
        return redirect("admin_panel:seller_shop_setup")

    sales_qs = (
        BillingDetail.objects.filter(cart__items__product__shop=shop)
        .select_related("user", "shipping_address", "cart")
        .order_by("-created_at")
        .distinct()
    )

    # Build a small view model for template rendering.
    sales = []
    for billing in sales_qs:
        items_qs = billing.cart.items.select_related("product").filter(product__shop=shop)
        seller_revenue = sum((i.total_price for i in items_qs), Decimal("0.00"))
        sales.append(
            {
                "billing": billing,
                "items": items_qs,
                "seller_revenue": seller_revenue,
            }
        )

    return render(
        request,
        "admin_panel/seller/sales.html",
        {"shop": shop, "sales": sales},
    )
