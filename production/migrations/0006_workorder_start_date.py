# Generated by Django 2.2.15 on 2020-08-28 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0005_remove_workorder_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
