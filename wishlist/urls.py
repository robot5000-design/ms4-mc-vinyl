from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_wishlist, name='view_wishlist'),
    path('add/<item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<item_id>/', views.remove_from_wishlist,
         name='remove_from_wishlist'),
    path('transfer/', views.transfer_all_to_cart, name='transfer_all_to_cart'),
]
