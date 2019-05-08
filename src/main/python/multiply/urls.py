from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('learn/', views.learn, name='learn'),
    path('experience/', views.experience, name='experience'),
    path('complete/', views.complete, name='complete'),
]
