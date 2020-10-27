from django.urls import path

from . import views

urlpatterns = [
    path('', views.new_message, name='new_message'),
    path('test/', views.new_test_message, name='new_test_message'),
]