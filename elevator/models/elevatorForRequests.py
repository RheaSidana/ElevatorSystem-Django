from django.db import models
from .floor import Floor
from .elevator import Elevator
from dataSeeding.models import ElevatorRequestStatus

class ElevatorForRequests(models.Model):
    reqID = models.CharField(max_length=7, primary_key=True)
    reqTime = models.DateTimeField(auto_now_add=True)
    floor_id = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="requestOn")
    status = models.ForeignKey(ElevatorRequestStatus, on_delete=models.CASCADE, related_name="request_status")
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name="request_for")
    count_of_people = models.IntegerField(default=0)

    def __str__(self):
        return self.reqID