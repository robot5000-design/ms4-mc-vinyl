from django.urls import path
from . import views

urlpatterns = [
    path('', views.messaging, name='messaging'),
    path('view_message_thread/<ref_number>/', views.view_message_thread,
         name='view_message_thread'),
]
