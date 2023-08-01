from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Floor)
admin.site.register(Elevator)
admin.site.register(ElevatorFunctionality)
admin.site.register(ElevatorForRequests)
admin.site.register(ElevatorFromRequests)