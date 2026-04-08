from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from apps.order_fulfillment.models import Order
from apps.products.models import Shop
from .choices import UserRoleChoices
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
            return redirect("products:product_list")
        return redirect("login")

    return render(request, "users/register.html", {"initial_role": initial_role})


""" ================ Login View ===================== """
def user_login(request):
    next_url = request.POST.get("next") or request.GET.get("next")

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        role_expected = request.POST.get('role')  # 👈 no normalize here

        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        #  Role check ONLY if provided
        if role_expected:
            role_expected = _normalize_role(role_expected)

            if user.role != role_expected:
                messages.error(
                    request,
                    f"Your account is '{user.get_role_display()}'. Please login with correct role.",
                )
                return redirect("login")

        auth_login(request, user)

        #  SELLER → dashboard
        if user.role == UserRoleChoices.SELLER:
            return redirect("products:product_list")

        #  CUSTOMER → next ya home
        if next_url and next_url != "None":
            return redirect(next_url)

        return redirect("home")

    return render(request, "users/login.html", {
        "next": next_url
    })

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
            return redirect("products:product_list")
        return redirect("products:product_list")

    return render(request, "users/seller/login.html")




def logout_view(request):
    logout(request)
    return redirect("home")

def choose_role(request):
    next_url = request.GET.get("next") or "/"
    action = request.GET.get("action")  # 👈 GET se lo

    if request.method == "POST":
        role = _normalize_role(request.POST.get("role"))
        action = request.POST.get("action")

        if action == "login":
            return redirect(f"{reverse('login')}?role={role}&next={next_url}")

        elif action == "register":
            return redirect(f"{reverse('register')}?role={role}&next={next_url}")

    return render(request, "users/chose_role.html", {
        "next": next_url,
        "action": action  # 👈 template me bhejo
    })


