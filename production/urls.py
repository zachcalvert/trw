from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.target_dashboard, name='target-dashboard'),
]
