from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .forms import WorkOrderForm
from .models import Factory, WorkOrder, WorkOrderCheckPoint


class WorkOrderCheckpointInline(admin.StackedInline):
    model = WorkOrderCheckPoint
    extra = 0


class WorkOrderAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = WorkOrderForm
    list_display = ['__str__', 'active', 'qad', 'published', 'stocked', 'goal', 'stock_date', 'factory', 'priority']
    list_filter = ('factory',)
    inlines = [WorkOrderCheckpointInline]


class WorkOrderInline(admin.TabularInline):
    model = WorkOrder
    show_change_link = True
    readonly_fields = ['__str__', 'active', 'qad', 'published', 'stocked', 'goal', 'stock_date']
    exclude = ['name', 'start_date', 'priority']
    extra = 0


class FactoryAdmin(admin.ModelAdmin):
    model = Factory
    inlines = [WorkOrderInline]


admin.site.register(Factory, FactoryAdmin)
admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(WorkOrderCheckPoint)
