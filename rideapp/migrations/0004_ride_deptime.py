# Generated by Django 2.2.5 on 2019-11-16 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideapp', '0003_auto_20191116_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='depTime',
            field=models.DateTimeField(null=True, verbose_name='Departure date and time'),
        ),
    ]
