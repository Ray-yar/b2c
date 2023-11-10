from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='base_url'),
    path('products/', views.all_products, name='products_url'),
    path('about-us/', views.about_us, name='about_us_url'),
    path('contact-us/', views.contact_us, name='contact_us_url'),
    path('whishlist/', views.all_products, name='wishlist_url'),
    path('products/<product_id>/', views.product_detail, name='product_details_url'),
]