from ..functionality import get_ElevatorFunctionality
from ..functionality import get_Operational_Status
from ..functionality import get_DoorFunctions

def list_elevFuncMoving(data):
    return get_ElevatorFunctionality(elevator=data["elevator"])

"""
if any req found assign to other elevators
"""
def create_elevFuncOperational(data):
    oprStatus = get_Operational_Status(status=data["status"])

    elevFunc = get_ElevatorFunctionality(elevator=data["elevator"])

    elevFunc.operational_status = oprStatus
    elevFunc.save()

    return elevFunc


def create_elevFuncDoor(data):
    doorFunc = get_DoorFunctions(action=data["action"])

    elevFunc = get_ElevatorFunctionality(elevator=data["elevator"])

    elevFunc.door_functionality = doorFunc
    elevFunc.save()
    return elevFunc