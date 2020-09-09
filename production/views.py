from datetime import datetime

from django.db.models import Max, Min
from django.http import Http404
from django.shortcuts import render

from production.models import Factory, WorkOrder


def dashboard(request, factory=None):
    if not factory:
        return render(request, 'production/whoopsie.html')
    try:
        factory = Factory.objects.get(name=factory.upper())
    except Factory.DoesNotExist:
        return render(request, 'production/whoopsie.html')

    active_orders = WorkOrder.objects.filter(active=True, factory=factory)

    today = datetime.today()
    first_day = active_orders.aggregate(Min('start_date'))

    orders = []
    missed_checkpoints = []
    for order in active_orders:
        start_position = (order.start_date - first_day['start_date__min']).days
        width = (order.stock_date - first_day['start_date__min']).days - start_position

        order_data = {
            "checkpoints": [
                {
                    "date": checkpoint.date,
                    "goal": checkpoint.goal,
                    "id": checkpoint.id,
                    "percent_of_total": checkpoint.percent_of_total,
                    "position": (checkpoint.date - order.start_date).days,
                    "short_date": checkpoint.short_date,
                } for checkpoint in order.checkpoints.all()
            ],
            "goal": order.goal,
            "id": order.id,
            "name": order.name,
            "percent_qad": order.percent_qad,
            "percent_published": order.percent_published,
            "percent_stocked": order.percent_stocked,
            "published": order.published,
            "qad": order.qad,
            "start_date": order.short_start_date,
            "start_position": start_position,
            "stock_date": order.short_stock_date,
            "stocked": order.stocked,
            "width": width
        }
        orders.append(order_data)

        missed_checkpoints.extend(
            list(order.checkpoints.filter(date__lt=today, goal__gt=order.stocked).values_list('id', flat=True))
        )

    context = {'today': datetime.today(), 'orders': orders, 'missed_checkpoints': missed_checkpoints}
    return render(request, 'production/dashboard.html', context)


def referrer_test(request):
    return render(request, 'production/referrer_test.html')