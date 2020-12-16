from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin

from .forms import WorkOrderForm
from .models import Factory, WorkOrder, WorkOrderCheckPoint


class WorkOrderCheckpointInline(admin.StackedInline):
    model = WorkOrderCheckPoint
    extra = 0


class WorkOrderAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = WorkOrderForm
    list_display = ['__str__', 'active', 'qad', 'published', 'stocked', 'goal', 'stock_date', 'factory', 'last_updated', 'priority', 'update_link']
    list_filter = ('factory',)
    inlines = [WorkOrderCheckpointInline]

    def update_link(self, obj):
        url = reverse("update_work_order", args=[obj.pk])
        return format_html('<a href="{}">Update counts</a>', url)


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
