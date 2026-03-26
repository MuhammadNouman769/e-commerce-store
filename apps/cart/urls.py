from django.urls import path

from . import views


urlpatterns = [
    path("cart/", views.cart, name="cart"),
    path("geo/regions/", views.regions_for_country, name="geo_regions"),
    path("geo/cities/", views.cities_for_region, name="geo_cities"),
    path('add-to-cart-ajax/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    
]

