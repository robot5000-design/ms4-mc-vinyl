from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>/', views.checkout_success,
         name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
    path('all_orders/', views.view_all_orders, name='view_all_orders'),
    path('order_detail/<order_number>/', views.view_order_detail,
         name='view_order_detail'),
]
