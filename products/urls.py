from django.urls import path
from .views import ProductsView

urlpatterns = [
    path('', ProductsView.as_view(), name='base_url'),
    path('products/', ProductsView.as_view(), name='products_url'),
    path('about-us/', ProductsView.as_view(), name='about_us_url'),
    path('contact-us/', ProductsView.as_view(), name='contact_us_url'),
    path('whishlist/', ProductsView.as_view(), name='wishlist_url'),
    path('checkout/', ProductsView.as_view(), name='checkout_url'),
]