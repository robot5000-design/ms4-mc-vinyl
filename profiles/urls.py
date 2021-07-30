from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>/', views.order_history,
         name='order_history'),
    path('add_user_message/<order_number>/', views.add_user_message,
         name='add_user_message'),
]
