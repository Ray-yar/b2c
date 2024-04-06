from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='base_url'),
    path('products/', views.ProductView.as_view(), name='products_url'),
    path('about-us/', views.about_us, name='about_us_url'),
    path('contact-us/', views.contact_us, name='contact_us_url'),
    path('products/<product_id>/', views.product_detail, name='product_details_url'),
    path('reviews/<review_id>/delete/', views.delete_review, name='review_delete'),
    path('whishlist/', views.wishlist, name='wishlist_url'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]