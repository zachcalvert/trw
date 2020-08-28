from datetime import datetime

from django.shortcuts import render

from production.models import WorkOrder


def target_dashboard(request):
    today = datetime.today()
    active_orders = WorkOrder.objects.filter(active=True)

    missed_checkpoints = []
    for order in active_orders:
        missed_checkpoints.extend(
            list(order.checkpoints.filter(date__lt=today, goal__gt=order.current).values_list('id', flat=True))
        )

    context = {'today': datetime.today(), 'orders': active_orders, 'missed_checkpoints': missed_checkpoints}
    return render(request, 'production/dashboard.html', context)
