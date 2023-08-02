from dataSeeding.models import *
from django.db import models

def deleteModelData(model, name):
    if model.objects.exists(): 
        # print("********************")
        # print("Data before")
        # print(Movements.objects.all())
        print("Deleting all data from Table: "+ name)
        model.objects.all().delete()
        # print("Data after: ")
        # print(Movements.objects.all())

def deleteAllDataFromAllModels():
    deleteModelData(Movements, "Movements")
    deleteModelData(DoorFunctions, "DoorFunctions")
    deleteModelData(Moving, "Moving")
    deleteModelData(Operational_Status, "Operational_Status")
    deleteModelData(ElevatorRequestStatus, "ElevatorRequestStatus")

def addMovements():
    print("Adding Movements !")
    objects = [
        {
            "action": "Start",
        },
        {
            "action": "Stop",
        },
        {
            "action": "Running",
        },
    ]

    for obj in objects:
        action  = obj["action"]
        if not Movements.objects.filter(action = action).exists():
            movement = Movements.objects.create(
                action = action
            )
            # print("Action : "+ action)

def addDoorFunctions():
    print("Adding DoorFunctions !")
    objects = [
        {
            "name": "Open",
        },
        {
            "name": "Close",
        }
    ]

    for obj in objects:
        name = obj["name"]
        if not DoorFunctions.objects.filter(name = name).exists():
            fn = DoorFunctions.objects.create(
                name = name
            )
            # print("DoorFunc: ")
            # print(fn)

def addMoving():
    print("Adding Moving !")
    objects = [
        {
            "dir": "Up",
        },
        {
            "dir": "Down",
        },
        {
            "dir": "Stationary",
        }
    ]

    for obj in objects:
        direction = obj["dir"]
        if not Moving.objects.filter(direction = direction).exists():
            mom = Moving.objects.create(direction = direction)
            # print("Moving: ")
            # print(mom)
            
def addOperational_Status():
    print("Adding Operational_Status !")
    objects = [
        {
            "val": "Working",
        },
        {
            "val": "Maintainence",
        },
        {
            "val": "Non Operational",
        }
    ]

    for obj in objects:
        val = obj["val"]
        if not Operational_Status.objects.filter(value = val).exists():
            opr = Operational_Status.objects.create(value = val)
            
def addElevatorRequestStatus():
    print("Adding ElevatorRequestStatus !")
    objects = [
        {
            "val": "open",
        },
        {
            "val": "closed",
        },
    ]

    for obj in objects:
        val = obj["val"]
        if not ElevatorRequestStatus.objects.filter(name = val).exists():
            opr = ElevatorRequestStatus.objects.create(name = val)
            