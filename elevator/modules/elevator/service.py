from ..functionality import get_Elevator
from ..functionality import get_ElevatorRequestStatus_Open
from ..functionality import get_AllElevatorFunctions, get_Elevator_Count
from .functionality import create_ElevatorFunctionality, is_elevatorExists
from .functionality import create_Elevator, create_ElevatorName
from .functionality import findListOfReq, fulfillNextRequest
from .functionality import segregateAccordingToDirection
from ...models.models import Elevator

def create_elevators(data):
    no = data["total_elevators"]
    peopleCapacity = data["capacity"]

    if get_Elevator_Count() > 0:
        Elevator.objects.all().delete()

    for i in range(1, no+1):
        val = create_ElevatorName(no=i)
        if not is_elevatorExists(name=val):
            elevator = create_Elevator(name=val, capacity=peopleCapacity)
            ele_func = create_ElevatorFunctionality(elevator=elevator)


def list_nextDestination(data):
    elevator = data["elevator"]
    elevator = get_Elevator(elevator=elevator)
    status = get_ElevatorRequestStatus_Open()

    list_req = findListOfReq(status=status, elevator=elevator)

    try:
        obj = segregateAccordingToDirection(elevator, sorted(list_req))
    except Exception as ex:
        raise Exception(ex)
    return obj


def list_fullfilElevatorNextRequest():
    list_obj = []
    elevFuncs = get_AllElevatorFunctions()
    data = dict()

    for elevatorFunc in elevFuncs:
        data["elevator"] = elevatorFunc.elevator.name

        obj = list_nextDestination(data=data)

        ob = fulfillNextRequest(
            elevatorFunctionality=elevatorFunc,
            nextDest=obj["next_floor"],
            nextDir=obj["next_direction"],
        )

        list_obj.append(ob)

    return list_obj
