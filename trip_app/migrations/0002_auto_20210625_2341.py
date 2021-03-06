# Generated by Django 2.2 on 2021-06-26 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='travel_date_from',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='travel_date_to',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
