# Generated by Django 2.2.15 on 2020-08-28 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stock_date', models.DateField()),
                ('goal', models.IntegerField(default=0)),
                ('current', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brands.Brand')),
            ],
            options={
                'ordering': ['stock_date'],
            },
        ),
        migrations.CreateModel(
            name='WorkOrderCheckPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('goal', models.IntegerField(default=0)),
                ('overall_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkpoints', to='production.WorkOrder')),
            ],
        ),
    ]
