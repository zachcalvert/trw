from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .forms import WorkOrderForm
from .models import WorkOrder, WorkOrderCheckPoint


class WorkOrderCheckpointInline(admin.StackedInline):
    model = WorkOrderCheckPoint
    extra = 1


class WorkOrderAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = WorkOrderForm
    list_display = ['__str__', 'active', 'current', 'goal', 'brand', 'stock_date', 'priority']

    inlines = [WorkOrderCheckpointInline]


admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(WorkOrderCheckPoint)
