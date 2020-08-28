from django.db import models

from brands.models import Brand


class ProductionTarget(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField()
    commitment = models.IntegerField(default=0)
    current = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.name

    @property
    def percent_complete(self):
        return (self.current/self.commitment) * 100


class ProductionTargetCheckPoint(models.Model):
    overall_target = models.ForeignKey(ProductionTarget, on_delete=models.CASCADE, related_name='checkpoints')
    date = models.DateField()
    goal = models.IntegerField(default=0)

    @property
    def percent_of_total(self):
        return (self.goal/self.overall_target.commitment) * 100

    @property
    def short_date(self):
        return '{}/{}'.format(self.date.month, self.date.day)
