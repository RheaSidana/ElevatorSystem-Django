from ..functionality import (
    get_ElevatorFunctionality,
    get_Operational_Status,
    get_DoorFunctions
)
from .functionality import (
    assignNextNearestFloorInTheSameDirection,
    updateFunctionality
)


def list_elevFuncMoving(data):
    return get_ElevatorFunctionality(elevator=data["elevator"])


def create_elevFuncOperational(data):
    oprStatus = get_Operational_Status(status=data["status"])

    elevFunc = get_ElevatorFunctionality(elevator=data["elevator"])

    if (oprStatus.value != "Working"):
        print(oprStatus.value)
        floor = assignNextNearestFloorInTheSameDirection(
            elevatorFunctionality=elevFunc)

    updateFunctionality(
        elevatorFunctionality=elevFunc,
        operational_status=oprStatus,
        floor=floor
    )

    return elevFunc


def create_elevFuncDoor(data):
    doorFunc = get_DoorFunctions(action=data["action"])

    elevFunc = get_ElevatorFunctionality(elevator=data["elevator"])

    elevFunc.door_functionality = doorFunc
    elevFunc.save()
    return elevFunc
