# apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # ya jo aapka user model hai
from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # Password match check
        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")  # ya render wapas form ke sath

        # Email already exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("register")

        # Phone already exists check (optional)
        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists!")
            return redirect("register")

        # User create
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=make_password(password),
        )
        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "users/register.html")
