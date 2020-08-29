from datetime import datetime, timedelta

from django.db.models import Max, Min
from django.shortcuts import render

from production.models import WorkOrder


def dashboard(request):
    active_orders = WorkOrder.objects.filter(active=True)

    today = datetime.today()
    first_day = active_orders.aggregate(Min('start_date'))
    last_day = active_orders.aggregate(Max('stock_date'))

    orders = []
    missed_checkpoints = []
    for order in active_orders:
        start_position = (order.start_date - first_day['start_date__min']).days
        end_position = (order.stock_date - first_day['start_date__min']).days
        width = end_position - start_position

        order_data = {
            "id": order.id,
            "current": order.current,
            "goal": order.goal,
            "name": order.name,
            "start_date": order.short_start_date,
            "start_position": start_position*20,
            "stock_date": order.short_stock_date,
            "end_position": end_position*20,
            "checkpoints": [
                {
                    "date": checkpoint.date,
                    "goal": checkpoint.goal,
                    "id": checkpoint.id,
                    "percent_of_total": checkpoint.percent_of_total,
                    "position": (checkpoint.date - order.start_date).days*20,
                    "short_date": checkpoint.short_date
                } for checkpoint in order.checkpoints.all()
            ],
            "percent_complete": order.percent_complete,
            "width": width*20
        }
        orders.append(order_data)

        missed_checkpoints.extend(
            list(order.checkpoints.filter(date__lt=today, goal__gt=order.current).values_list('id', flat=True))
        )

    print('orders: {}'.format(orders))
    context = {'today': datetime.today(), 'orders': orders, 'missed_checkpoints': missed_checkpoints}
    return render(request, 'production/dashboard.html', context)
