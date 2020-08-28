from django.contrib import admin

from .models import ProductionTarget, ProductionTargetCheckPoint


class ProductionTargetCheckpointInline(admin.StackedInline):
    model = ProductionTargetCheckPoint
    extra = 1


class ProductionTargetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'active', 'current', 'commitment', 'brand', 'date']

    inlines = [ProductionTargetCheckpointInline]


admin.site.register(ProductionTarget, ProductionTargetAdmin)
admin.site.register(ProductionTargetCheckPoint)
