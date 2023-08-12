from .repository import closeForRequest
from elevator.modules.elevatorFromRequest.functionality import closeFromRequest
from ..functionality import (
    get_all_elevator_functionality,
    get_Movements,
    get_DoorFunctions,
    get_Moving, 
    get_Floor,
    get_ElevatorForRequests_elevatorIsNull
)
from ..elevatorForRequests.service import create_for_request
from ..elevatorNextDestination.service import list_nextDestination

def cal_FulFill_Direction(direction, elevatorFunctionality, steps):
    if elevatorFunctionality.direction != direction:
        elevatorFunctionality.direction = direction
    step = "Moving: " + elevatorFunctionality.direction.direction
    steps.append(step)
    return cal_FulFill_CurrentFloor(
        elevatorFunctionality=elevatorFunctionality,
        steps=steps
    )


def cal_FulFill_CurrentFloor(elevatorFunctionality, steps):
    step = "From floor: " + elevatorFunctionality.floor_no.name
    steps.append(step)
    return elevatorFunctionality, steps


def cal_FulFill_DoorFunctions(elevatorFunctionality, door, steps):
    if elevatorFunctionality.door_functionality != door:
        elevatorFunctionality.door_functionality = door
    step = "Door : " + elevatorFunctionality.door_functionality.name
    steps.append(step)
    return elevatorFunctionality, steps


def cal_FulFill_NextFloor(elevatorFunctionality, floor, steps):
    if elevatorFunctionality.floor_no != floor:
        elevatorFunctionality.floor_no = floor
    step = "Reached Floor: " + elevatorFunctionality.floor_no.name
    steps.append(step)
    return elevatorFunctionality, steps


def fulfill_whenOperStatusIsWorking(elevatorFunctionality, steps, nextDir, nextDest):
    movement = get_Movements(action="Running")
    elevatorFunctionality, steps = cal_FulFill_Movements(
        movement=movement,
        elevatorFunctionality=elevatorFunctionality,
        steps=steps
    )

    direction = get_Moving(direction=nextDir)
    elevatorFunctionality, steps = cal_FulFill_Direction(
        direction=direction,
        elevatorFunctionality=elevatorFunctionality,
        steps=steps
    )

    floor = get_Floor(name=nextDest)
    elevatorFunctionality, steps = cal_FulFill_NextFloor(
        elevatorFunctionality=elevatorFunctionality,
        floor=floor,
        steps=steps
    )
    fulFilled = elevatorFunctionality.floor_no.name

    doorOpen = get_DoorFunctions(action="Open")
    elevatorFunctionality, steps = cal_FulFill_DoorFunctions(
        elevatorFunctionality=elevatorFunctionality,
        door=doorOpen,
        steps=steps
    )

    doorClose = get_DoorFunctions(action="Close")
    elevatorFunctionality, steps = cal_FulFill_DoorFunctions(
        elevatorFunctionality=elevatorFunctionality,
        door=doorClose,
        steps=steps
    )

    elev = elevatorFunctionality.elevator

    peopleCount = closeForRequest(elevator=elev,
                                  floor=elevatorFunctionality.floor_no)
    elevatorFunctionality.curr_req_count -= 1

    if elevatorFunctionality.curr_person_count + peopleCount > elev.capacity:
        add = elev.capacity - elevatorFunctionality.curr_person_count
        elevatorFunctionality.curr_person_count += add
    else:
        elevatorFunctionality.curr_person_count += peopleCount

    steps.append("Closed ForRequests")
    peopleCount = closeFromRequest(elevator=elevatorFunctionality.elevator,
                                   to_floor=elevatorFunctionality.floor_no)
    elevatorFunctionality.curr_person_count -= peopleCount
    steps.append("Closed FromRequests")

    steps.append("Ready for next direction !!")
    elevatorFunctionality.save()
    return elevatorFunctionality, steps, fulFilled




def cal_FulFill_Movements(movement, elevatorFunctionality, steps):
    if elevatorFunctionality.movement != movement:
        elevatorFunctionality.movement = movement
    step = "Movement: " + elevatorFunctionality.movement.action
    steps.append(step)
    return elevatorFunctionality, steps

def fulfill_whenNoNextDestination(elevatorFunctionality, steps):
    movement = get_Movements(action="Stop")
    elevatorFunctionality, steps = cal_FulFill_Movements(
        movement=movement,
        elevatorFunctionality=elevatorFunctionality,
        steps=steps
    )

    direction = get_Moving(direction="Stationary")
    elevatorFunctionality, steps = cal_FulFill_Direction(
        direction=direction,
        elevatorFunctionality=elevatorFunctionality,
        steps=steps
    )

    doorClose = get_DoorFunctions(action="Close")
    elevatorFunctionality, steps = cal_FulFill_DoorFunctions(
        elevatorFunctionality=elevatorFunctionality,
        door=doorClose,
        steps=steps
    )
    elevatorFunctionality.save()
    return elevatorFunctionality, steps

def fulfillNextRequest(elevatorFunctionality, nextDest, nextDir):
    fulFilled = None
    steps = []
    if nextDest == "":
        elevatorFunctionality, steps = fulfill_whenNoNextDestination(
            elevatorFunctionality=elevatorFunctionality,
            steps=steps
        )

    elif elevatorFunctionality.operational_status.value == "Working":
        elevatorFunctionality, steps, fulFilled = fulfill_whenOperStatusIsWorking(
            elevatorFunctionality=elevatorFunctionality,
            steps=steps,
            nextDest=nextDest,
            nextDir=nextDir
        )
    # elevatorFunctionality.save()

    return {
        "elevator_name": elevatorFunctionality.elevator.name,
        "current_floor": elevatorFunctionality.floor_no.name,
        "fulfilled_floor": fulFilled,
        "steps": steps,
    }


def fulfill(elevatorFunctionality):
    data = dict()

    data["elevator"] = elevatorFunctionality.elevator.name

    obj = list_nextDestination(data=data)

    ob = fulfillNextRequest(
        elevatorFunctionality=elevatorFunctionality,
        nextDest=obj["next_floor"],
        nextDir=obj["next_direction"],
    )

    return ob

def assignForRequestIfElevatorIsNull():
    elevatorNullReqs = get_ElevatorForRequests_elevatorIsNull()

    if elevatorNullReqs:
        data = {
            "floors": [],
            "PeoplePerFloor": []
        }
        for req in elevatorNullReqs:
            data["floors"].append(req.floor_id.name)
            data["PeoplePerFloor"].append(
                req.count_of_people
            )
            req.delete()
            create_for_request(data=data)


def list_fulfillElevatorsNextRequest():
    list_obj = []
    elevFuncs = get_all_elevator_functionality()

    for elevatorFunc in elevFuncs:
        ob = fulfill(elevatorFunctionality=elevatorFunc)

        list_obj.append(ob)
    assignForRequestIfElevatorIsNull()

    return list_obj
