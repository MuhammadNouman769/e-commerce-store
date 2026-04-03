""" ============== Imports =============== """
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import models as django_models

# Models
from apps.products.models import Product, ProductVariant
from .models import Cart, CartItem

# Geo Models
from cities_light.models import City, Country, Region


""" ============== Main Cart View =============== """
@login_required
def cart(request):
    # Safety check
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to view your cart")
        return redirect(f"{reverse('users:login')}?next={request.path}")
    
    # Get or create user's cart
    cart_obj, created = Cart.objects.get_or_create(
        user=request.user,
        status=Cart.CartStatus.ACTIVE
    )
    
    # Query param actions
    add_id = request.GET.get("add")
    remove_id = request.GET.get("remove")
    clear = request.GET.get("clear")

    # Handle clear cart
    if clear:
        cart_obj.items.all().delete()
        messages.success(request, "Cart cleared successfully!")
        return redirect("cart")

    # Handle add to cart from URL
    if add_id:
        try:
            product = get_object_or_404(Product, id=add_id, status=Product.ProductStatus.ACTIVE)
            variant = product.variants.first()
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart_obj,
                product=product,
                variant=variant,
                defaults={
                    'product_name': product.title,
                    'price': variant.price if variant else 0,
                    'quantity': 1
                }
            )
            
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            
            messages.success(request, f"{product.title} added to cart!")
        except Product.DoesNotExist:
            messages.error(request, "Product not found!")
        
        return redirect("cart")

    # Handle remove item
    if remove_id:
        try:
            cart_item = CartItem.objects.get(cart=cart_obj, product_id=remove_id)
            product_name = cart_item.product_name
            cart_item.delete()
            messages.success(request, f"{product_name} removed from cart!")
        except CartItem.DoesNotExist:
            messages.error(request, "Item not found in cart!")
        
        return redirect("cart")

    # Handle quantity update
    if request.method == "POST":
        updated = False
        
        for key, value in request.POST.items():
            if key.startswith("qty_"):
                product_id = key.replace("qty_", "", 1)
                try:
                    quantity = int(value)
                    if quantity > 0:
                        cart_item = CartItem.objects.get(cart=cart_obj, product_id=product_id)
                        cart_item.quantity = quantity
                        cart_item.save()
                        updated = True
                except (ValueError, CartItem.DoesNotExist):
                    continue
        
        if updated:
            messages.success(request, "Cart updated successfully!")
        
        return redirect("cart")

    # Get cart items - filter out invalid products
    cart_items = cart_obj.items.select_related(
        'product', 'variant'
    ).prefetch_related(
        'product__images'
    ).order_by('-created_at')
    
    # Remove invalid items
    valid_items = []
    for item in cart_items:
        if item.product and item.product.status == Product.ProductStatus.ACTIVE:
            valid_items.append(item)
        else:
            item.delete()
            messages.warning(request, f"{item.product_name} was removed from your cart (product no longer available)")
    
    # Calculate subtotal
    subtotal = sum(item.total_price for item in valid_items)
    
    # Calculate shipping (free over Rs 5000, else Rs 200)
    shipping = 0 if subtotal >= 5000 else 200
    
    # Get countries for shipping form
    countries = Country.objects.all().order_by("name")
    default_country = countries.filter(code2="PK").first() or countries.first()
    
    context = {
        "cart_items": valid_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": subtotal + shipping,
        "cart_count": cart_obj.total_items,
        "countries": countries,
        "default_country_id": getattr(default_country, "id", None),
        "cart_obj": cart_obj,
    }
    
    return render(request, "shop/cart.html", context)


# ... rest of your AJAX views (they are correct as is)

""" ============== Geo Helper Views =============== """
def regions_for_country(request):
    """Get regions/states for a country"""
    country_id = request.GET.get("country_id")
    
    if country_id and country_id.isdigit():
        regions = Region.objects.filter(country_id=int(country_id)).order_by("name")
    else:
        regions = Region.objects.none()
    
    data = [{"id": r.id, "name": r.name} for r in regions]
    return JsonResponse({"results": data})


def cities_for_region(request):
    """Get cities for a region/state"""
    region_id = request.GET.get("region_id")
    
    if region_id and region_id.isdigit():
        cities = City.objects.filter(region_id=int(region_id)).order_by("name")
    else:
        cities = City.objects.none()
    
    data = [{"id": c.id, "name": c.name} for c in cities]
    return JsonResponse({"results": data})


""" ============== Add to Cart AJAX =============== """
@login_required
@csrf_exempt
@require_POST
def add_to_cart_ajax(request):
    """AJAX endpoint to add product to cart"""
    try:
        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST
        
        product_id = data.get("product_id")
        variant_id = data.get("variant_id")
        quantity = int(data.get("quantity", 1))
        
        if not product_id:
            return JsonResponse({
                "success": False, 
                "error": "Product ID is required"
            }, status=400)
        
        # Get product
        product = get_object_or_404(
            Product, 
            id=product_id, 
            status=Product.ProductStatus.ACTIVE
        )
        
        # Get or create active cart
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            status=Cart.CartStatus.ACTIVE
        )
        
        # Get variant
        variant = None
        if variant_id:
            variant = get_object_or_404(
                ProductVariant, 
                id=variant_id, 
                product=product
            )
        
        # Calculate price
        if variant:
            price = variant.price
        else:
            first_variant = product.variants.first()
            price = first_variant.price if first_variant else 0
        
        # Check stock
        if variant and variant.track_inventory:
            if quantity > variant.stock_quantity:
                return JsonResponse({
                    "success": False,
                    "error": f"Only {variant.stock_quantity} items available in stock"
                }, status=400)
        
        # Create or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={
                'product_name': product.title,
                'price': price,
                'quantity': quantity
            }
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        # Get updated cart count
        total_items = cart.items.aggregate(
            total=django_models.Sum('quantity')
        )['total'] or 0
        
        return JsonResponse({
            "success": True,
            "message": f"{product.title} added to cart!",
            "cart_count": int(total_items),
            "cart_item_count": cart_item.quantity,
            "cart_total": float(cart.subtotal)
        })
        
    except Product.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Product not found"
        }, status=404)
        
    except ProductVariant.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Variant not found"
        }, status=404)
        
    except ValueError as e:
        return JsonResponse({
            "success": False,
            "error": f"Invalid quantity: {str(e)}"
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }, status=500)


""" ============== Remove from Cart AJAX =============== """
@login_required
@csrf_exempt
@require_POST
def remove_from_cart_ajax(request):
    """AJAX endpoint to remove item from cart"""
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        variant_id = data.get("variant_id")
        
        if not product_id:
            return JsonResponse({
                "success": False,
                "error": "Product ID is required"
            }, status=400)
        
        # Get user's active cart
        cart = Cart.objects.filter(
            user=request.user,
            status=Cart.CartStatus.ACTIVE
        ).first()
        
        if not cart:
            return JsonResponse({
                "success": False,
                "error": "Cart not found"
            }, status=404)
        
        # Find and remove item
        query = CartItem.objects.filter(cart=cart, product_id=product_id)
        
        if variant_id:
            query = query.filter(variant_id=variant_id)
        else:
            query = query.filter(variant__isnull=True)
        
        deleted_count, _ = query.delete()
        
        if deleted_count == 0:
            return JsonResponse({
                "success": False,
                "error": "Item not found in cart"
            }, status=404)
        
        # Get updated cart count
        total_items = cart.items.aggregate(
            total=django_models.Sum('quantity')
        )['total'] or 0
        
        return JsonResponse({
            "success": True,
            "message": "Item removed from cart",
            "cart_count": int(total_items),
            "cart_subtotal": float(cart.subtotal)
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


""" ============== Update Cart AJAX =============== """
@login_required
@csrf_exempt
@require_POST
def update_cart_ajax(request):
    """AJAX endpoint to update cart item quantity"""
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        variant_id = data.get("variant_id")
        quantity = int(data.get("quantity", 1))
        
        if not product_id:
            return JsonResponse({
                "success": False,
                "error": "Product ID is required"
            }, status=400)
        
        if quantity < 1:
            return JsonResponse({
                "success": False,
                "error": "Quantity must be at least 1"
            }, status=400)
        
        # Get user's active cart
        cart = Cart.objects.filter(
            user=request.user,
            status=Cart.CartStatus.ACTIVE
        ).first()
        
        if not cart:
            return JsonResponse({
                "success": False,
                "error": "Cart not found"
            }, status=404)
        
        # Find cart item
        query = CartItem.objects.filter(cart=cart, product_id=product_id)
        
        if variant_id:
            query = query.filter(variant_id=variant_id)
        else:
            query = query.filter(variant__isnull=True)
        
        cart_item = query.first()
        
        if not cart_item:
            return JsonResponse({
                "success": False,
                "error": "Item not found in cart"
            }, status=404)
        
        # Update quantity
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            "success": True,
            "message": "Cart updated",
            "line_total": float(cart_item.total_price),
            "cart_subtotal": float(cart.subtotal),
            "cart_count": cart.total_items
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


""" ============== Get Cart Summary AJAX =============== """
@login_required
def get_cart_summary(request):
    """AJAX endpoint to get cart summary"""
    try:
        cart = Cart.objects.filter(
            user=request.user,
            status=Cart.CartStatus.ACTIVE
        ).first()
        
        if not cart:
            return JsonResponse({
                "success": True,
                "cart_count": 0,
                "cart_subtotal": 0,
                "cart_items": []
            })
        
        items = []
        for item in cart.items.all():
            items.append({
                "id": item.id,
                "product_id": item.product.id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "price": float(item.price),
                "total_price": float(item.total_price),
                "image": item.product.images.first().images.url if item.product.images.first() else None
            })
        
        return JsonResponse({
            "success": True,
            "cart_count": cart.total_items,
            "cart_subtotal": float(cart.subtotal),
            "cart_items": items
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)
        
@login_required
@csrf_exempt
@require_POST
def apply_promo(request):
    """Apply promo code to cart"""
    try:
        data = json.loads(request.body)
        promo_code = data.get("code", "").strip().upper()
        
        # Simple promo codes example
        promo_codes = {
            "SAVE10": {"discount": 10, "type": "percentage", "min_amount": 1000},
            "SAVE100": {"discount": 100, "type": "fixed", "min_amount": 5000},
            "WELCOME20": {"discount": 20, "type": "percentage", "min_amount": 2000},
            "FREESHIP": {"discount": 200, "type": "fixed", "min_amount": 3000},
        }
        
        # Get user's cart
        cart = Cart.objects.filter(
            user=request.user,
            status=Cart.CartStatus.ACTIVE
        ).first()
        
        if not cart or cart.is_empty:
            return JsonResponse({
                "success": False,
                "error": "Cart is empty"
            }, status=400)
        
        subtotal = cart.subtotal
        
        if promo_code in promo_codes:
            promo = promo_codes[promo_code]
            
            if subtotal < promo.get("min_amount", 0):
                return JsonResponse({
                    "success": False,
                    "error": f"Minimum order amount of Rs {promo['min_amount']} required for this promo code"
                })
            
            if promo["type"] == "percentage":
                discount = (subtotal * promo["discount"]) / 100
            else:
                discount = promo["discount"]
            
            # Save discount in session or cart
            request.session['promo_code'] = promo_code
            request.session['discount'] = float(discount)
            
            return JsonResponse({
                "success": True,
                "message": f"Promo code {promo_code} applied! You saved Rs {int(discount)}",
                "discount": int(discount)
            })
        else:
            return JsonResponse({
                "success": False,
                "error": "Invalid promo code"
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)        