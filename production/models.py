from django.db import models

from brands.models import Brand


class WorkOrder(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.CASCADE)
    stock_date = models.DateField()
    goal = models.IntegerField(default=0)
    current = models.IntegerField(default=0)
    priority = models.PositiveIntegerField(default=0, blank=False, null=False)
    color = models.CharField(max_length=7, default='#28a745')
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.name

    @property
    def percent_complete(self):
        return (self.current/self.goal) * 100

    @property
    def short_date(self):
        return '{}/{}'.format(self.stock_date.month, self.stock_date.day)


class WorkOrderCheckPoint(models.Model):
    overall_target = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='checkpoints')
    date = models.DateField()
    goal = models.IntegerField(default=0)

    @property
    def percent_of_total(self):
        return (self.goal/self.overall_target.goal) * 100

    @property
    def short_date(self):
        return '{}/{}'.format(self.date.month, self.date.day)
