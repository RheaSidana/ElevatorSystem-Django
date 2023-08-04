from django.core.management.base import BaseCommand
from dataSeeding.models import *  
from .data import *
from .redis import *

movementsKey = "Movements"
doorFunctionsKey = "DoorFunctions"
movingKey = "Moving"
operationalStatusKey = "Operational_Status"
elevatorRequestStatusKey = "ElevatorRequestStatus"

class Command(BaseCommand):
    help = 'Seeds the database models with initial data'

    def handle(self, *args, **kwargs):
        self.seed_data()

    def seed_data(self):
        deleteAllDataFromAllModels()
        print("\n\n......... SEEDING DATA ..........")
        print("\n ********* \n")
        addMovements()
        create_cache(key=movementsKey, data=getAll(model=Movements))
        print("\n ********* \n")
        addDoorFunctions()
        create_cache(key=doorFunctionsKey, data=getAll(model=DoorFunctions))
        print("\n ********* \n")
        addMoving()
        create_cache(key=movingKey, data=getAll(model=Moving))
        print("\n ********* \n")
        addOperational_Status()
        create_cache(key=operationalStatusKey, data=getAll(model=Operational_Status))
        print("\n ********* \n")
        addElevatorRequestStatus()
        create_cache(key=elevatorRequestStatusKey, data=getAll(model=ElevatorRequestStatus))
