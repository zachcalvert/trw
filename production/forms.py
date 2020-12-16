from django import forms

from production.models import WorkOrder


class UpdateWorkOrderForm(forms.Form):
    qad_items = forms.CharField(label='Items QA\'d')
    published_items = forms.CharField(label='Items published')
    stocked_items = forms.CharField(label='Items stocked')

    def update_work_order(self, work_order, qad, published, stocked):
        work_order.qad += int(qad)
        work_order.published += int(published)
        work_order.stocked += int(stocked)
        work_order.save()


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
