from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from apps.order_fulfillment.models import BillingDetail
from apps.products.models import Shop
from apps.users.choices import UserRoleChoices
from .models import User
from django.contrib.auth import logout
from django.shortcuts import redirect

def _normalize_role(value: str) -> str:
    """
    Keep registration/login roles limited to customer/seller.
    Admin accounts must be created from Django admin.
    """
    value = (value or "").strip().lower()
    if value == UserRoleChoices.SELLER:
        return UserRoleChoices.SELLER
    return UserRoleChoices.CUSTOMER


""" ============= SignUp View ==============="""
def register(request):
    # For "Become Seller" link we allow GET param to preselect radio.
    initial_role = _normalize_role(request.GET.get("role"))

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        phone = request.POST.get('phone', '').strip()

        role = _normalize_role(request.POST.get('role'))

        if password2 != password:
            messages.error(request, "Passwords dont match")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("register")

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists!")
            return redirect("register")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            role=role,
            password=make_password(password),
        )

        messages.success(request, "Account created successfully!")
        if role == UserRoleChoices.SELLER:
            return redirect("admin_panel:seller_shop_setup")
        return redirect("login")

    return render(request, "users/register.html", {"initial_role": initial_role})


""" ================ Login View ===================== """
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        role_expected = _normalize_role(request.POST.get('role'))

        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        # Enforce role-based UI. User can still be logged in, but they will be
        # redirected only to the correct area.
        if user.role != role_expected:
            messages.error(
                request,
                f"Your account is '{user.get_role_display()}', please select the correct login type.",
            )
            return redirect("login")

        auth_login(request, user)
        messages.success(request, "Login successfully!")

        if user.role == UserRoleChoices.SELLER:
            return redirect("admin_panel:seller_dashboard")
        return redirect("home")

    initial_role = _normalize_role(request.GET.get("role"))
    return render(request, "users/login.html", {"initial_role": initial_role})


@login_required
def customer_dashboard(request):
    # Redirect sellers to seller panel.
    if request.user.role == UserRoleChoices.SELLER:
        return redirect("admin_panel:seller_dashboard")

    if request.user.role != UserRoleChoices.CUSTOMER:
        return redirect("home")

    orders = (
        BillingDetail.objects.select_related("shipping_address", "cart")
        .filter(user=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "users/customer/dashboard.html",
        {"orders": orders},
    )


@login_required
def customer_order_detail(request, billing_id: int):
    if request.user.role != UserRoleChoices.CUSTOMER:
        return HttpResponseForbidden("Not allowed")

    billing = (
        BillingDetail.objects.select_related("shipping_address", "cart", "user")
        .filter(id=billing_id, user=request.user)
        .first()
    )
    if not billing:
        raise HttpResponseForbidden("Order not found")

    cart_items = billing.cart.items.select_related("product").all()

    return render(
        request,
        "users/customer/order_detail.html",
        {"billing": billing, "cart_items": cart_items},
    )


""" =========================================================
Role-specific UI (Customer vs Seller)
========================================================= """


def customer_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        phone = request.POST.get("phone", "").strip()

        if password2 != password:
            messages.error(request, "Passwords don't match")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("register")

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists!")
            return redirect("register")

        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            role=UserRoleChoices.CUSTOMER,
            password=make_password(password),
        )

        messages.success(request, "Account created successfully!")
        return redirect("login")  # customer login

    return render(request, "users/customer/register.html")


def seller_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        phone = request.POST.get("phone", "").strip()

        if password2 != password:
            messages.error(request, "Passwords don't match")
            return redirect("seller_register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("seller_register")

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists!")
            return redirect("seller_register")

        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            role=UserRoleChoices.SELLER,
            password=make_password(password),
        )

        messages.success(request, "Seller account created successfully!")
        return redirect("seller_login")

    return render(request, "users/seller/register.html")


def customer_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        if user.role != UserRoleChoices.CUSTOMER:
            messages.error(
                request,
                f"Your account is '{user.get_role_display()}'. Please login as the correct type.",
            )
            return redirect("login")

        auth_login(request, user)
        messages.success(request, "Login successfully!")
        # Customer dashboard nahi chahiye; main page/home pe redirect.
        return redirect("home")

    return render(request, "users/customer/login.html")


def seller_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("seller_login")

        if user.role != UserRoleChoices.SELLER:
            messages.error(
                request,
                f"Your account is '{user.get_role_display()}'. Please login as the correct type.",
            )
            return redirect("seller_login")

        auth_login(request, user)
        messages.success(request, "Seller login successfully!")

        if Shop.objects.filter(owner=user).exists():
            return redirect("admin_panel:seller_dashboard")
        return redirect("admin_panel:seller_shop_setup")

    return render(request, "users/seller/login.html")




def logout_view(request):
    logout(request)
    return redirect("home")