from django.forms import ModelForm

from production.models import WorkOrder


class WorkOrderForm(ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'
