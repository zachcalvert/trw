# Generated by Django 2.2.15 on 2020-08-29 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0006_workorder_start_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorder',
            old_name='current',
            new_name='qad',
        ),
        migrations.AddField(
            model_name='workorder',
            name='stocked',
            field=models.IntegerField(default=0, verbose_name="QA'd"),
        ),
    ]
