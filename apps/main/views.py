from urllib import request

from django.shortcuts import render


def home(request):
    return render(request, 'home/index.html')    
     
def category(request):
    return render(request, 'shop/product_list.html')

def product_detail(request):
    return render(request, 'shop/single-product.html')

def blog(request):
    return render(request, 'blog/blog.html')
def contact(request):
    return render(request, 'contact.html')
def single_blog(request):
    return render(request, 'blog/single-blog.html')
def cart(request):
    return render(request, 'shop/cart.html')
def checkout(request):
    return render(request, 'shop/checkout.html')
def confirm(request):
    return render(request, 'shop/confirmation.html')
# def wishlist(request):
#     return render(request, 'wish-list/add-to-wishlist.html')
def login(request):
    return render(request, 'logins/login.html')
def tracking(request):
    return render(request, 'logins/tracking.html')
def element(request):
    return render(request, 'logins/elements.html')
