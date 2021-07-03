from django.urls import path
from . import views

urlpatterns = [
    path('', views.messaging, name='messaging'),
    path('message_thread/<ref_number>/', views.view_message_thread,
         name='view_message_thread'),
    path('admin_reply/<ref_number>/', views.add_admin_reply,
         name='add_admin_reply'),
    path('delete_thread/<ref_number>/', views.delete_thread,
         name='delete_thread'),
    path('change_thread_status/<ref_number>/', views.change_thread_status,
         name='change_thread_status'),
]
