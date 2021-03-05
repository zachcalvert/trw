from django.urls import path

from . import views

urlpatterns = [
    path('<factory>', views.dashboard, name='dashboard'),
    path('admin/production/workorder/<int:pk>/update', views.UpdateWorkOrderView.as_view(), name='update_work_order'),
    path('api/work_orders', views.workorders_list),
    path('', views.dashboard, name='dashboard'),
]
