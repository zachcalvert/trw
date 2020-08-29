from django.db import models


class WorkOrder(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    stock_date = models.DateField()
    goal = models.IntegerField(default=0)
    qad = models.IntegerField(default=0, verbose_name="QA'd")
    stocked = models.IntegerField(default=0)
    priority = models.PositiveIntegerField(default=0, blank=False, null=False)
    color = models.CharField(max_length=7, default='#28a745')
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.name

    @property
    def percent_qad(self):
        """This method is used in the dashboard, it returns the percent of items that have been QA'd and not stocked,
        so that the different progress bars can be rendered sequentially.
        """
        diff = self.qad - self.stocked
        return (diff/self.goal) * 100

    @property
    def percent_stocked(self):
        return (self.stocked/self.goal) * 100

    @property
    def short_start_date(self):
        return '{}/{}'.format(self.start_date.month, self.start_date.day)

    @property
    def short_stock_date(self):
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
