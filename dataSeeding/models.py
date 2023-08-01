from django.db import models

# Create your models here.
class Movements(models.Model):

    action = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.action


class DoorFunctions(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Moving(models.Model):
    direction = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.direction
    
class Operational_Status(models.Model):
    value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.value

# class ElevatorRequestType(models.Model):
#     name = models.CharField(max_length=30, unique=True)

#     def __str__(self):
#         return self.name
    
class ElevatorRequestStatus(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
