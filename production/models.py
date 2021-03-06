from datetime import datetime

from django.db import models
from django.utils import timezone


class Factory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField

    class Meta:
        verbose_name_plural = "factories"

    def __str__(self):
        return self.name


class WorkOrder(models.Model):
    name = models.CharField(max_length=100)
    factory = models.ForeignKey(Factory, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField(null=True)
    stock_date = models.DateField()
    qad = models.IntegerField(default=0, verbose_name="QA'd")
    published = models.IntegerField(default=0)
    stocked = models.IntegerField(default=0)
    goal = models.IntegerField(default=0)
    priority = models.PositiveIntegerField(default=0, blank=False, null=False)
    active = models.BooleanField(default=False)
    last_updated = models.DateTimeField(default=timezone.now(), verbose_name="Counts last updated")

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.name

    __original_qad = None
    __original_published = None
    __original_stocked = None

    def __init__(self, *args, **kwargs):
        super(WorkOrder, self).__init__(*args, **kwargs)
        self.__original_qad = self.qad
        self.__original_published = self.published
        self.__original_stocked = self.stocked

    @property
    def percent_qad(self):
        """This method is used in the dashboard, it returns the percent of items that have been QA'd and not stocked,
        so that the different progress bars can be rendered sequentially.
        """
        diff = self.qad - self.published
        return (diff/self.goal) * 100

    @property
    def percent_published(self):
        diff = self.published - self.stocked
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

    def get_ideal_published(self):
        today = datetime.today()

        if self.checkpoints.filter(date=today).exists():
            return self.checkpoints.filter(date=today).first().goal

        last_checkpoint = self.checkpoints.filter(date__lt=today).order_by('-date').first()
        start = last_checkpoint.date if last_checkpoint else self.start_date
        start_amount = last_checkpoint.goal if last_checkpoint else 0

        next_checkpoint = self.checkpoints.filter(date__gt=today).order_by('date').first()
        end = next_checkpoint.date if next_checkpoint else self.stock_date
        end_amount = next_checkpoint.goal if next_checkpoint else self.goal

        days = (end - start).days
        amount_done = end_amount - start_amount
        ideal = start_amount + (amount_done//days)

        return ideal

    def save(self, *args, **kwargs):
        if (self.qad != self.__original_qad or self.published != self.__original_published or self.stocked != self.__original_stocked):
            self.last_updated = timezone.now()

        super(WorkOrder, self).save(*args, **kwargs)


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
