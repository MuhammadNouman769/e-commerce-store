from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from cities_light.models import City, Country, Region

from apps.products.models import Product

def cart(request):
    """
    Simple session-based cart.
    Session shape:
      cart = { "<product_id>": <qty_int>, ... }
    """
    cart_data = request.session.get("cart", {})

    # Actions via query params
    add_id = request.GET.get("add")
    remove_id = request.GET.get("remove")
    clear = request.GET.get("clear")

    if clear:
        request.session["cart"] = {}
        request.session.modified = True
        return redirect("cart")

    if add_id:
        pid = str(add_id)
        cart_data[pid] = int(cart_data.get(pid, 0)) + 1
        request.session["cart"] = cart_data
        request.session.modified = True
        return redirect("cart")

    if remove_id:
        pid = str(remove_id)
        cart_data.pop(pid, None)
        request.session["cart"] = cart_data
        request.session.modified = True
        return redirect("cart")

    # Quantity updates via POST
    if request.method == "POST":
        updated = {}
        for key, value in request.POST.items():
            if not key.startswith("qty_"):
                continue
            pid = key.replace("qty_", "", 1)
            try:
                qty = int(value)
            except (TypeError, ValueError):
                qty = cart_data.get(pid, 1)
            if qty <= 0:
                continue
            updated[pid] = qty
        request.session["cart"] = updated
        request.session.modified = True
        return redirect("cart")

    product_ids = [int(pid) for pid in cart_data.keys() if str(pid).isdigit()]
    products = Product.objects.filter(id__in=product_ids).prefetch_related("images", "variants")
    products_by_id = {p.id: p for p in products}

    cart_items = []
    subtotal = 0

    for pid_str, qty in cart_data.items():
        try:
            pid = int(pid_str)
        except (TypeError, ValueError):
            continue
        product = products_by_id.get(pid)
        if not product:
            continue

        variant = product.variants.first()
        price = variant.price if variant else 0
        line_total = price * qty
        subtotal += line_total

        image = product.images.first()
        image_url = image.images.url if image and image.images else ""

        cart_items.append(
            {
                "product": product,
                "qty": qty,
                "price": price,
                "line_total": line_total,
                "image_url": image_url,
                "remove_url": f"{reverse('cart')}?remove={product.id}",
            }
        )

    countries = Country.objects.all().order_by("name")
    default_country = countries.filter(code2="PK").first() or countries.first()

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "cart_count": sum(int(q) for q in cart_data.values() if isinstance(q, int)),
        "countries": countries,
        "default_country_id": getattr(default_country, "id", None),
    }
    return render(request, "shop/cart.html", context)


def regions_for_country(request):
    """
    Return regions (provinces/states) for a given country.
    GET param: country_id
    """
    country_id = request.GET.get("country_id")
    qs = Region.objects.all()
    if country_id and str(country_id).isdigit():
        qs = qs.filter(country_id=int(country_id))
    else:
        qs = qs.none()

    data = [{"id": r.id, "name": r.name} for r in qs.order_by("name")]
    return JsonResponse({"results": data})


def cities_for_region(request):
    """
    Return cities for a given region.
    GET param: region_id
    """
    region_id = request.GET.get("region_id")
    qs = City.objects.all()
    if region_id and str(region_id).isdigit():
        qs = qs.filter(region_id=int(region_id))
    else:
        qs = qs.none()

    data = [{"id": c.id, "name": c.name} for c in qs.order_by("name")]
    return JsonResponse({"results": data})
