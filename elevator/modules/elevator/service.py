from ..functionality import get_Elevator_Count
from ...models.models import Elevator
from ...models.models import ElevatorFunctionality
from ..functionality import (
    get_Floor,
    get_Movements,
    get_Moving,
    get_Operational_Status,
    get_DoorFunctions
)

requestCapacity = 8


def is_elevator_exists(name):
        return Elevator.objects.filter(name=name).exists()

def create_elevator_name(no):
    return "EL_" + str(no)


def create_elevator(name, capacity):
    return Elevator.objects.create(
        name=name, capacity=capacity, requestsCapacity=requestCapacity,
    )


def create_elevator_functionality(elevator):
    return ElevatorFunctionality.objects.create(
        movement=get_Movements(action="Stop"),
        floor_no=get_Floor(name="FL_1"),
        direction=get_Moving(direction="Stationary"),
        operational_status=get_Operational_Status(status="Working"),
        door_functionality=get_DoorFunctions(action="Close"),
        elevator=elevator,
        curr_req_count=0,
        curr_person_count=0,
    )

def create_elevators(data):
    no = data["total_elevators"]
    peopleCapacity = data["capacity"]

    if get_Elevator_Count() > 0:
        Elevator.objects.all().delete()

    for i in range(1, no+1):
        val = create_elevator_name(no=i)
        if not is_elevator_exists(name=val):
            elevator = create_elevator(name=val, capacity=peopleCapacity)
            ele_func = create_elevator_functionality(elevator=elevator)
