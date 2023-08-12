from ..functionality import (
    get_ElevatorFunctionality,
    get_operational_status,
    get_DoorFunctions
)
from .functionality import (
    assignEveryRequestToNextDestination,
    updateFunctionality,
    updateFunctionality_WhenNotWorking
)


def list_elevFuncMoving(data):
    return get_ElevatorFunctionality(elevator=data["elevator"])


def create_elevFuncOperational(data):
    oprStatus = get_operational_status(status=data["status"])

    elevFunc = get_ElevatorFunctionality(elevator=data["elevator"])

    if (oprStatus.value != "Working"):
        if (
            oprStatus.value == "Maintainence" and
            elevFunc.operational_status == oprStatus
        ) or (
            oprStatus.value == "Non Operational" and
            elevFunc.operational_status == oprStatus
        ):
            return elevFunc

        elif (
            elevFunc.operational_status.value != "Working"
        ):
            elevFunc = updateFunctionality(
                elevatorFunctionality=elevFunc,
                operational_status=oprStatus,
                floor=elevFunc.floor_no
            )
            return elevFunc

        floor = assignEveryRequestToNextDestination(
            elevatorFunctionality=elevFunc)

        elevFunc = updateFunctionality(
            elevatorFunctionality=elevFunc,
            operational_status=oprStatus,
            floor=floor
        )
    else:
        elevFunc = updateFunctionality_WhenNotWorking(
            elevatorFunctionality=elevFunc,
            operational_status=oprStatus,
        )

    return elevFunc


def create_elevFuncDoor(data):
    doorFunc = get_DoorFunctions(action=data["action"])

    elevFunc = get_ElevatorFunctionality(elevator=data["elevator"])

    elevFunc.door_functionality = doorFunc
    elevFunc.save()
    return elevFunc
