from django.shortcuts import render


def home(request):
    return render(request, 'home/index.html')    
     
def category(request):
    return render(request, 'shop/category.html')

def product_detail(request):
    return render(request, 'shop/single-product.html')

# def about_us(request):
#     return render(request, 'about/about.html')
# def contact(request):
#     return render(request, 'contacts/contact.html')
# def men(request):
#     return render(request, 'products/men.html')

def cart(request):
    return render(request, 'shop/cart.html')
def checkout(request):
    return render(request, 'shop/checkout.html')
# def order_complete(request):
#     return render(request, 'order_complete/order-complete.html')
# def wishlist(request):
#     return render(request, 'wish-list/add-to-wishlist.html')

# def login(request):
#     return render(request, 'users/login.html')
