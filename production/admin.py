from django.contrib import admin

from .models import WorkOrder, WorkOrderCheckPoint


class WorkOrderCheckpointInline(admin.StackedInline):
    model = WorkOrderCheckPoint
    extra = 1


class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'active', 'current', 'goal', 'brand', 'stock_date']

    inlines = [WorkOrderCheckpointInline]


admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(WorkOrderCheckPoint)
