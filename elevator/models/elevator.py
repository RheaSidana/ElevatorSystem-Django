from django.db import models

class Elevator(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    capacity  = models.IntegerField()
    requestsCapacity = models.IntegerField()

    def __str__(self):
        return self.name
