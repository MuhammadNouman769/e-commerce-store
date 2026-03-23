from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from cities_light.models import City, Country, Region

from apps.products.models import Product

""" ============== Cart View =============== """
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

    """ ============== Clear Cart =============== """
    if clear:
        request.session["cart"] = {}
        request.session.modified = True
        return redirect("cart")

    """ ============== Add to Cart =============== """
    if add_id:
        pid = str(add_id)
        cart_data[pid] = int(cart_data.get(pid, 0)) + 1
        request.session["cart"] = cart_data
        request.session.modified = True
        return redirect("cart")

    """ ============== Remove from Cart =============== """
    if remove_id:
        pid = str(remove_id)
        cart_data.pop(pid, None)
        request.session["cart"] = cart_data
        request.session.modified = True
        return redirect("cart")

    """ ============== Quantity Updates =============== """
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

    """ ============== Get Cart Items =============== """
    product_ids = [int(pid) for pid in cart_data.keys() if str(pid).isdigit()]
    products = Product.objects.filter(id__in=product_ids).prefetch_related("images", "variants")
    products_by_id = {p.id: p for p in products}

    cart_items = []
    """ ============== Calculate Subtotal =============== """
    subtotal = 0

    """ ============== Loop through Cart Data =============== """
    for pid_str, qty in cart_data.items():
        try:
            pid = int(pid_str)
        except (TypeError, ValueError):
            continue
        """ ============== Get Product =============== """
        product = products_by_id.get(pid)
        if not product:
            continue

        """ ============== Get Variant =============== """
        variant = product.variants.first()
        """ ============== Calculate Line Total =============== """
        price = variant.price if variant else 0
        line_total = price * qty
        subtotal += line_total

        """ ============== Get Image =============== """
        image = product.images.first()
        image_url = image.images.url if image and image.images else ""

        """ ============== Add to Cart Items =============== """
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

    """ ============== Get Countries =============== """
    countries = Country.objects.all().order_by("name")
    """ ============== Get Default Country =============== """
    default_country = countries.filter(code2="PK").first() or countries.first()

    """ ============== Get Context =============== """
    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "cart_count": sum(int(q) for q in cart_data.values() if isinstance(q, int)),
        "countries": countries,
        "default_country_id": getattr(default_country, "id", None),
    }
    return render(request, "shop/cart.html", context)

""" ============== Regions for Country View =============== """
def regions_for_country(request):
    """
    Return regions (provinces/states) for a given country.
    GET param: country_id
    """
    country_id = request.GET.get("country_id")
    """ ============== Get Regions =============== """
    qs = Region.objects.all()
    """ ============== Filter Regions by Country ID =============== """
    if country_id and str(country_id).isdigit():
        qs = qs.filter(country_id=int(country_id))
    else:
        qs = qs.none()

    data = [{"id": r.id, "name": r.name} for r in qs.order_by("name")]
    return JsonResponse({"results": data})

""" ============== Cities for Region View =============== """
def cities_for_region(request):
    """
    Return cities for a given region.
    GET param: region_id
    """
    region_id = request.GET.get("region_id")
    """ ============== Get Cities =============== """
    qs = City.objects.all()
    """ ============== Filter Cities by Region ID =============== """
    if region_id and str(region_id).isdigit():
        qs = qs.filter(region_id=int(region_id))
    else:
        qs = qs.none()

    data = [{"id": c.id, "name": c.name} for c in qs.order_by("name")]
    return JsonResponse({"results": data})
