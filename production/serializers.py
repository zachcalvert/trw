from rest_framework import serializers
from .models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):
    ideal_published = serializers.SerializerMethodField()

    class Meta:
        model = WorkOrder 
        fields = ('name', 'factory', 'start_date', 'stock_date', 'qad', 'published', 'stocked', 'goal', 'priority', 'ideal_published')

    def get_ideal_published(self, obj):
        return obj.get_ideal_published()