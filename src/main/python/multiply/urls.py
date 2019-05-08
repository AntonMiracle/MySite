from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('learn/', views.learn, name='learn'),
    path('test/', views.test, name='test'),
]
