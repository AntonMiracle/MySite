from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.main),
    path('main/', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('accounts/login/', views.login),
    path('logout/', views.logout, name='logout'),
]
