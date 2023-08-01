from django.core.management.base import BaseCommand
from dataSeeding.models import *  
from .data import *


class Command(BaseCommand):
    help = 'Seeds the database models with initial data'

    def handle(self, *args, **kwargs):
        self.seed_data()

    def seed_data(self):
        deleteAllDataFromAllModels()
        print("\n\n......... SEEDING DATA ..........")
        print("\n ********* \n")
        addMovements()
        print("\n ********* \n")
        addDoorFunctions()
        print("\n ********* \n")
        addMoving()
        print("\n ********* \n")
        addOperational_Status()
        print("\n ********* \n")
        # addElevatorRequestType()
        # print("\n ********* \n")
        addElevatorRequestStatus()
