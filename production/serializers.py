from rest_framework import serializers
from .models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkOrder 
        fields = ('name', 'factory', 'start_date', 'stock_date', 'qad', 'published', 'stocked', 'goal', 'priority', 'active')
