from rest_framework import serializers
from .models import WorkOrder, WorkOrderCheckPoint


class CheckpointSerializer(serializers.ModelSerializer):
    percent_of_total = serializers.SerializerMethodField()

    class Meta:
        model = WorkOrderCheckPoint
        fields = ['goal', 'short_date', 'percent_of_total']

    def get_percent_of_total(self, obj):
        return obj.get_percent_of_total()


class WorkOrderSerializer(serializers.ModelSerializer):
    ideal_published = serializers.SerializerMethodField()
    checkpoints = serializers.SerializerMethodField()

    class Meta:
        model = WorkOrder 
        fields = ('name', 'factory', 'start_date', 'stock_date', 'qad', 'published', 'stocked', 'goal', 'priority', 'ideal_published', 'checkpoints')

    def get_ideal_published(self, obj):
        return obj.get_ideal_published()

    def get_checkpoints(self, obj):
        return obj.get_checkpoints()
