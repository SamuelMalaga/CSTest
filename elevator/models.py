from django.db import models
from datetime import datetime, time,timedelta

class Person(models.Model):
    name = models.CharField(max_length = 100)
    age = models.IntegerField()
    def __str__(self):
        return self.name



class Elevator(models.Model):

    elevator_max_speed = models.FloatField(default=4)
    number_of_floors = models.IntegerField(default=10)
    current_floor = models.IntegerField()


class ElevatorCall(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    target_floor = models.IntegerField()
    origin_floor = models.IntegerField()
    elevator = models.ForeignKey(Elevator,on_delete=models.CASCADE)


class Movement(models.Model):

    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete = models.CASCADE)
    elevator_call = models.ForeignKey(ElevatorCall, on_delete = models.CASCADE)
    movement_started_at = models.DateTimeField(default=datetime.now())
    movement_finished_at = models.DateTimeField(default=datetime.now())
    movement_origin_floor = models.IntegerField(default=0)
    movement_final_floor = models.IntegerField(default=0)
    call_origin_floor = models.IntegerField(default=0)
    call_target_floor = models.IntegerField(default=0)
    total_traveled_floors = models.IntegerField(default=0)
    total_movement_time_ms = models.DurationField(default=timedelta())
    avg_movement_speed_floor_by_seconds = models.FloatField(default=0)
