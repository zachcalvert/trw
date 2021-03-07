from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView

from rest_framework.response import Response
from rest_framework.views import APIView

from production.forms import UpdateWorkOrderForm
from production.models import Factory, WorkOrder
from production.serializers import WorkOrderSerializer


class UpdateWorkOrderView(FormView):
    form_class = UpdateWorkOrderForm
    template_name = 'admin/production/update_work_order.html'
    success_url = '/admin/production/workorder/'

    def dispatch(self, *args, **kwargs):
        self.workorder = get_object_or_404(WorkOrder, pk=kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        qad = form.cleaned_data['qad_items'] or 0
        published = form.cleaned_data['published_items'] or 0
        stocked = form.cleaned_data['stocked_items'] or 0

        form.update_work_order(self.workorder, qad, published, stocked)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = f'Update {self.workorder.name} counts'
        context['site_header'] = 'TRW Admin'
        context['has_permission'] = True
        context['workorder'] = self.workorder

        return context


class WorkOrderList(APIView):
    """
    List all active work orders
    """
    def get(self, request, format=None):
        work_orders = WorkOrder.objects.filter(active=True)
        serializer = WorkOrderSerializer(work_orders, many=True)
        return Response(serializer.data)
