from django.urls import path

from . import views


urlpatterns = [
    path("cart/", views.cart, name="cart"),
    path("geo/regions/", views.regions_for_country, name="geo_regions"),
    path("geo/cities/", views.cities_for_region, name="geo_cities"),
    path('add-to-cart-ajax/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('remove_from_cart_ajax/',views.remove_from_cart_ajax, name='remove_from_cart_ajax'),
    path('update-cart-ajax/', views.update_cart_ajax, name='update_cart_ajax'),
    path('api/cart/apply-promo/', views.apply_promo, name='apply_promo'),
    
]

