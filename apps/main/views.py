from django.contrib import messages
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'home/index.html')    
     
def category(request):
    return render(request, 'shop/product_list.html')

def product_detail(request):
    return render(request, 'shop/single-product.html')

def blog(request):
    return render(request, 'blog/blog.html')
def contact(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        subject = (request.POST.get("subject") or "").strip()
        message = (request.POST.get("message") or "").strip()
        if not (name and email and message):
            messages.error(request, "Please fill all required fields.")
        else:
            # Placeholder success flow until email/service integration is added.
            messages.success(request, "Your message has been received. We will contact you soon.")
        return redirect("contact_us")
    return render(request, 'contact.html')
def single_blog(request):
    return render(request, 'blog/single-blog.html')
# def wishlist(request):
#     return render(request, 'wish-list/add-to-wishlist.html')
def login(request):
    return render(request, 'logins/login.html')
def tracking(request):
    if request.method == "POST":
        order_id = (request.POST.get("order_id") or "").strip()
        billing_email = (request.POST.get("billing_email") or "").strip()
        if not order_id or not billing_email:
            messages.error(request, "Order ID and Billing Email are required.")
        else:
            messages.info(request, "Tracking lookup is under setup. Please contact support for now.")
        return redirect("tracking")
    return render(request, 'logins/tracking.html')
def element(request):
    return render(request, 'logins/elements.html')


def checkout(request):
    return render(request, "shop/checkout_ui.html")


def confirm(request):
    return render(request, "shop/confirmation.html")
