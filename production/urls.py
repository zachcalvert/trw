from django.urls import path

from . import views

urlpatterns = [
    path('referrer_test/', views.referrer_test, name='referrer_test'),
    path('<factory>', views.dashboard, name='dashboard'),
    path('admin/production/workorder/<int:pk>/update', views.UpdateWorkOrderView.as_view(), name='update_work_order'),
    path('', views.dashboard, name='dashboard'),
]
