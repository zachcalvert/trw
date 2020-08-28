from django.shortcuts import render

from production.models import WorkOrder


def target_dashboard(request):
    active_orders = WorkOrder.objects.filter(active=True)
    context = {'orders': active_orders}
    return render(request, 'production/dashboard.html', context)
