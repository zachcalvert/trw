# Generated by Django 2.2.15 on 2020-09-08 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0012_auto_20200901_0347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='factory',
            options={'verbose_name_plural': 'factories'},
        ),
        migrations.AddField(
            model_name='workorder',
            name='published',
            field=models.IntegerField(default=0),
        ),
    ]
