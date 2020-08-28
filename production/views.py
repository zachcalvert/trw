from django.shortcuts import render

from production.models import ProductionTarget


def target_dashboard(request):
    active_targets = ProductionTarget.objects.filter(active=True)
    context = {'targets': active_targets}
    return render(request, 'production/dashboard.html', context)
