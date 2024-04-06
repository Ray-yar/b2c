from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add-to-bag/<int:product_id>/', views.add_to_bag, name='add_to_bag'),
    path('remove-from-bag/<int:bag_item_id>/', views.remove_from_bag, name='remove_from_bag'),
    path('update-bag-item-quantity/<int:bag_item_id>/', views.update_bag_item_quantity, name='update_bag_item_quantity'),
]