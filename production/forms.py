from django import forms

from production.models import WorkOrder


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = '__all__'

    def clean(self):
        qad = self.cleaned_data.get('qad')
        published = self.cleaned_data.get('published')
        stocked = self.cleaned_data.get('stocked')
        goal = self.cleaned_data.get('goal')
        start_date = self.cleaned_data.get('start_date')
        stock_date = self.cleaned_data.get('stock_date')

        if qad > goal:
            raise forms.ValidationError("The number of QA'd items cannot be greater than the overall goal.")

        if published > qad:
            raise forms.ValidationError("The number of published items cannot be greater than the number of QA'd items.")

        if stocked > published:
            raise forms.ValidationError("The number of stocked items cannot be greater than the number of published items.")

        if start_date > stock_date:
            raise forms.ValidationError("Stock date must be after Start date.")

        return self.cleaned_data
