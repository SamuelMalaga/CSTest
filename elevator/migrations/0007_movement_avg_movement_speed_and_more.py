# Generated by Django 5.0.1 on 2024-02-01 15:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevator', '0006_remove_movement_movement_finished_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='avg_movement_speed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movement',
            name='call_origin_floor',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movement',
            name='call_target_floor',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movement',
            name='movement_final_floor',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movement',
            name='movement_finished_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 1, 12, 42, 42, 256425)),
        ),
        migrations.AddField(
            model_name='movement',
            name='movement_origin_floor',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movement',
            name='movement_started_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 1, 12, 42, 42, 256425)),
        ),
        migrations.AddField(
            model_name='movement',
            name='total_movement_time',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AddField(
            model_name='movement',
            name='total_traveled_floors',
            field=models.IntegerField(default=0),
        ),
    ]
