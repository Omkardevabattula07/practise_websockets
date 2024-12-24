from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('superuser/', views.superuser_dashboard, name='superuser_dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('chat/<str:room_name>/', views.private_chat, name='private_chat'),
]