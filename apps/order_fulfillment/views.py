# from django.contrib import messages
# from django.db import transaction
# from django.shortcuts import redirect, render
# from cities_light.models import City, Country, Region
# from django.contrib.auth.decorators import login_required
# from apps.cart.models import Cart, CartItem, ShippingAddress
# from apps.order_fulfillment.models import BillingDetail
# from apps.products.models import Product

# @login_required(login_url="/users/login/")
# def checkout(request):
#     # Checkout uses the same session cart as `apps.cart.views.cart`
#     cart_data = request.session.get("cart", {})

#     product_ids = [int(pid) for pid in cart_data.keys() if str(pid).isdigit()]
#     products = Product.objects.filter(id__in=product_ids).prefetch_related("images", "variants")
#     products_by_id = {p.id: p for p in products}

#     cart_items = []
#     subtotal = 0
#     for pid_str, qty in cart_data.items():
#         try:
#             pid = int(pid_str)
#         except (TypeError, ValueError):
#             continue

#         product = products_by_id.get(pid)
#         if not product:
#             continue

#         variant = product.variants.first()
#         price = variant.price if variant else 0
#         line_total = price * qty
#         subtotal += line_total

#         cart_items.append(
#             {
#                 "product": product,
#                 "qty": qty,
#                 "price": price,
#                 "line_total": line_total,
#             }
#         )

#     countries = Country.objects.all().order_by("name")
#     default_country = countries.filter(code2="PK").first() or countries.first()

#     context = {
#         "cart_items": cart_items,
#         "subtotal": subtotal,
#         "countries": countries,
#         "default_country_id": getattr(default_country, "id", None),
#         "cart_count": sum(int(q) for q in cart_data.values() if isinstance(q, int)),
#     }

#     if request.method == "POST":
#         if not request.user.is_authenticated:
#             messages.error(request, "Please login to checkout.")
#             return redirect("login")

#         # Shipping fields come from the checkout page UI
#         ship_country_id = request.POST.get("ship_country")
#         ship_province_id = request.POST.get("ship_province")
#         ship_city_id = request.POST.get("ship_city")
#         ship_address = (request.POST.get("ship_address") or "").strip()
#         ship_postcode = (request.POST.get("ship_postcode") or "").strip()

#         first_name = (request.POST.get("first_name") or "").strip()
#         last_name = (request.POST.get("last_name") or "").strip()
#         full_name = (first_name + " " + last_name).strip()
#         phone_number = (request.POST.get("phone_number") or "").strip()

#         payment_method = request.POST.get("payment_method") or BillingDetail.PaymentMethods.COD

#         if not ship_country_id or not ship_city_id or not ship_address:
#             messages.error(request, "Please fill shipping address details.")
#             return render(request, "shop/checkout_ui.html", context)

#         with transaction.atomic():
#             # Create a fresh DB cart for this checkout (demo-friendly).
#             Cart.objects.filter(user=request.user).update(is_active=False)
#             cart = Cart.objects.create(user=request.user)

#             # Create shipping address linked to this user.
#             country = Country.objects.get(id=ship_country_id)
#             province = Region.objects.filter(id=ship_province_id).first() if ship_province_id else None
#             city = City.objects.get(id=ship_city_id)

#             shipping_address = ShippingAddress.objects.create(
#                 user=request.user,
#                 full_name=full_name,
#                 phone_number=phone_number,
#                 street_address=ship_address,
#                 country=country,
#                 province=province,
#                 city=city,
#                 postal_code=ship_postcode,
#                 is_default=True,
#             )

#             # Sync cart items from session data.
#             for pid_str, qty in cart_data.items():
#                 try:
#                     pid = int(pid_str)
#                     quantity = int(qty)
#                 except (TypeError, ValueError):
#                     continue
#                 if quantity <= 0:
#                     continue

#                 product = Product.objects.filter(id=pid).first()
#                 if not product:
#                     continue

#                 variant = product.variants.first()
#                 unit_price = variant.price if variant else 0

#                 CartItem.objects.create(
#                     cart=cart,
#                     product=product,
#                     product_name=product.title,
#                     quantity=quantity,
#                     price=unit_price,
#                 )

#             # Create billing record for demo/order confirmation.
#             BillingDetail.objects.create(
#                 user=request.user,
#                 shipping_address=shipping_address,
#                 cart=cart,
#                 payment_method=payment_method,
#                 subtotal=subtotal,
#                 tax=0,
#                 shipping_fee=0,
#                 discount=0,
#                 total_amount=subtotal,
#             )

#             # Clear session cart after successful checkout.
#             request.session["cart"] = {}
#             request.session.modified = True

#         return redirect("confirm")

#     return render(request, "shop/checkout_ui.html", context)


# def confirm(request):
#     if not request.user.is_authenticated:
#         return redirect("login")

#     billing = BillingDetail.objects.select_related(
#         "shipping_address",
#         "cart",
#         "user",
#     ).filter(user=request.user).order_by("-created_at").first()

#     cart_items = []
#     if billing and billing.cart_id:
#         cart_items = list(billing.cart.items.all())

#     return render(
#         request,
#         "shop/confirmation.html",
#         {
#             "billing": billing,
#             "shipping_address": billing.shipping_address if billing else None,
#             "cart_items": cart_items,
#         },
#     )
