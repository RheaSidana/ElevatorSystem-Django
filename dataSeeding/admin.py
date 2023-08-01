from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Movements)
admin.site.register(DoorFunctions)
admin.site.register(Moving)
admin.site.register(Operational_Status)
# admin.site.register(ElevatorRequestType)
admin.site.register(ElevatorRequestStatus)
