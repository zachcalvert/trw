# Generated by Django 2.2.15 on 2020-08-27 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0002_auto_20200827_2145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productiontarget',
            old_name='amount',
            new_name='commitment',
        ),
        migrations.AddField(
            model_name='productiontarget',
            name='current',
            field=models.IntegerField(default=1000),
            preserve_default=False,
        ),
    ]
