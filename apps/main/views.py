from django.shortcuts import render


def home(request):
    return render(request, 'home/index.html')    
     
def category(request):
    return render(request, 'shop/category.html')

def product_detail(request):
    return render(request, 'shop/single-product.html')

def blog(request):
    return render(request, 'blog/blog.html')
# def contact(request):
#     return render(request, 'contacts/contact.html')
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

# def login(request):
#     return render(request, 'users/login.html')
