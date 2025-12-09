from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
     return render(request, 'home/index.html')
     
     
def women(request):
     return render(request, 'products/women.html')

def about_us(request):
    return render(request, 'about/about.html')
def contact(request):
    return render(request, 'contacts/contact.html')
def men(request):
    return render(request, 'products/men.html')
def products_details(request):
    return render(request, 'products/product-detail.html')
def cart(request):
    return render(request, 'cart/cart.html')
def checkout(request):
    return render(request, 'check_out/checkout.html')
def order_complete(request):
    return render(request, 'order_complete/order-complete.html')
def wishlist(request):
    return render(request, 'wish-list/add-to-wishlist.html')
def login(request):
    return render(request, 'users/login.html')