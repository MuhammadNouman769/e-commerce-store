from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login

""" ============= SignIn View ==============="""
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        if password2 != password:
            messages.error(request,"dont match password")
            return redirect('register')

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

""" ================ Login View ===================== """


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "users/login.html")