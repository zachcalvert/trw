from django.forms import ModelForm
from django.forms.widgets import TextInput

from production.models import WorkOrder


class WorkOrderForm(ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
