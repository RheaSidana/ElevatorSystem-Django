from django.contrib import admin
from .models import *
from .models.models import Floor, Elevator, ElevatorForRequests, ElevatorFunctionality,ElevatorFromRequests

# Register your models here.
admin.site.register(Floor)
admin.site.register(Elevator)
admin.site.register(ElevatorFunctionality)
admin.site.register(ElevatorForRequests)
admin.site.register(ElevatorFromRequests)