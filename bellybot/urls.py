from django.urls import path

from . import views

urlpatterns = [
    path('', views.new_message, name='new_message'),
]