from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('learn/', views.learn, name='learn'),
    path('tasks/', views.tasks, name='tasks'),
    path('complete/', views.complete, name='complete'),
]
