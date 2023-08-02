from django.db import models
from dataSeeding.models import *

# Create your models here.
class Floor(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    
class Elevator(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    capacity  = models.IntegerField()
    requestsCapacity = models.IntegerField()

    def __str__(self):
        return self.name

class ElevatorFunctionality(models.Model):
    movement = models.ForeignKey(Movements, on_delete=models.CASCADE, related_name="elevator_movement")
    floor_no = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="elevatorOn")
    direction = models.ForeignKey(Moving, on_delete=models.CASCADE, related_name="elevator_direction")
    operational_status = models.ForeignKey(Operational_Status, on_delete=models.CASCADE, related_name="elevator_operational")
    door_functionality = models.ForeignKey(DoorFunctions, on_delete=models.CASCADE, related_name="elevator_door")
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name="elevator")
    curr_req_count = models.IntegerField()
    curr_person_count = models.IntegerField()
    
class ElevatorForRequests(models.Model):
    reqID = models.CharField(max_length=7, primary_key=True)
    reqTime = models.DateTimeField(auto_now_add=True)
    floor_id = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="requestOn")
    # type = models.ForeignKey(ElevatorRequestType, on_delete=models.CASCADE, related_name="request")
    status = models.ForeignKey(ElevatorRequestStatus, on_delete=models.CASCADE, related_name="request_status")
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name="request_for")
    count_of_people = models.IntegerField(default=0)

    def __str__(self):
        return self.reqID
    
class ElevatorFromRequests(models.Model):
    reqID = models.CharField(max_length=7, primary_key=True)
    reqTime = models.DateTimeField(auto_now_add=True)
    from_floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="request_from_floor")
    to_floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="request_to_floor")
    # type = models.ForeignKey(ElevatorRequestType, on_delete=models.CASCADE, related_name="request")
    status = models.ForeignKey(ElevatorRequestStatus, on_delete=models.CASCADE, related_name="request_from_status")
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name="request_from")
    count_of_people = models.IntegerField(default=0)

    def __str__(self):
        return self.reqID
