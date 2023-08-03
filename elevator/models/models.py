from django.db import models
from dataSeeding.models import *

# Create your models here.
from .floor import Floor
from .elevator import Elevator
from .elevatorFunctionality import ElevatorFunctionality
from .elevatorForRequests import ElevatorForRequests
from .elevatorFromRequests import ElevatorFromRequests
