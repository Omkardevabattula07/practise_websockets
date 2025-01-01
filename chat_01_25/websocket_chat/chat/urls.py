from django.urls import path
from . import views

urlpatterns = [
    # path('', views.login_view, name='login'),
     path('', views.login_view, name='login'),
    # path('users/', views.user_list, name='user_list'),
    # path('logout/', views.user_logout, name='logout'),
    path('superuser/', views.superuser_dashboard, name='superuser_dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('chat/<str:username>/', views.private_chat, name='private_chat'),
]
