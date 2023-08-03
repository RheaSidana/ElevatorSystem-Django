from django.db import models
from dataSeeding.models import *
from .floor import Floor
from .elevator import Elevator


class ElevatorFunctionality(models.Model):
    movement = models.ForeignKey(Movements, on_delete=models.CASCADE, related_name="elevator_movement")
    floor_no = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="elevatorOn")
    direction = models.ForeignKey(Moving, on_delete=models.CASCADE, related_name="elevator_direction")
    operational_status = models.ForeignKey(Operational_Status, on_delete=models.CASCADE, related_name="elevator_operational")
    door_functionality = models.ForeignKey(DoorFunctions, on_delete=models.CASCADE, related_name="elevator_door")
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name="elevator")
    curr_req_count = models.IntegerField()
    curr_person_count = models.IntegerField()
    