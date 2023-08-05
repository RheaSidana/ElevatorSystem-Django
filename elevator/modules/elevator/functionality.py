from ...models.models import ElevatorFunctionality
from ..functionality import get_Floor, get_Movements, get_Elevator_Count
from ..functionality import get_Moving, get_Operational_Status
from ..functionality import get_DoorFunctions, get_ElevatorFunctionality
from ...models.models import Elevator
from ..functionality import get_ElevatorForRequests
from ..elevatorFromRequest.functionality import get_AllOpenFromRequest
from ..elevatorFromRequest.functionality import closeFromRequest
from ..elevatorForRequests.functionality import closeForRequest

requestCapacity = 8


def is_elevatorExists(name):
    return Elevator.objects.filter(name=name).exists()


def create_ElevatorName(no):
    return "EL_" + str(no)


def create_Elevator(name, capacity):
    return Elevator.objects.create(
        name=name, capacity=capacity, requestsCapacity=requestCapacity,
    )


def create_ElevatorFunctionality(elevator):
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


def findListOfReq(status, elevator):
    list_req = []

    list_forReqs = get_ElevatorForRequests(
        status=status,
        elevator=elevator
    )

    if list_forReqs != []:
        for fr in list_forReqs:
            list_req.append(fr.floor_id.name)

    list_fromReqs = get_AllOpenFromRequest(
        status=status,
        elevator=elevator,
    )
    if list_fromReqs != []:
        for fr in list_fromReqs:
            list_req.append(fr.to_floor.name)

    return list_req


def create_LeftListAndRightList(list_requests, currentFloor):
    right_list = []
    left_list = []
    for fl in list_requests:
        if fl > currentFloor:
            right_list.append(fl)
        elif fl < currentFloor:
            left_list.append(fl)

    left_list.sort(reverse=True)

    return left_list, right_list


def cal_diff(first, second):
    return abs(first - second)


def cal_minDiffAndPop(list, curr):
    min_diff = cal_diff(int(list[0].split("_")[1]), int(curr.split("_")[1]))
    pop = list.pop(0)
    return min_diff, pop


def segregateAccordingToDirection(elevator, list_req):
    elevFunc = get_ElevatorFunctionality(elevator=elevator)

    currentFloor = elevFunc.floor_no.name
    right_list = []
    left_list = []

    min_diff = get_Elevator_Count()
    pop = ""
    direct = get_Moving(direction="Stationary")

    if list_req is not None:
        left_list, right_list = create_LeftListAndRightList(
            list_requests=list_req,
            currentFloor=currentFloor
        )

        if left_list != [] and cal_diff(int(left_list[0].split("_")[1]), int(currentFloor.split("_")[1])) < min_diff:
            min_diff, pop = cal_minDiffAndPop(
                list=left_list, curr=currentFloor)
            direct = get_Moving(direction="Down")
        elif right_list != []:
            if pop != "" and abs(int(right_list[0].split("_")[1]) - int(currentFloor.split("_")[1])) < min_diff:
                left_list.insert(0, pop)
            min_diff, pop = cal_minDiffAndPop(
                list=right_list, curr=currentFloor)
            direct = get_Moving(direction="Up")

    obj = {
        "elevator_name": elevator.name,
        "current_floor": currentFloor,
        "next_floor": pop,
        "next_direction": direct.direction,
        "moving_direction1": "Up",
        "floor_names1": right_list,
        "moving_direction2": "Down",
        "floor_names2": left_list,
    }

    return obj


def cal_FulFill_Movements(movement, elevatorFunctionality, steps):
    if elevatorFunctionality.movement != movement:
        elevatorFunctionality.movement = movement
    step = "Movement: " + elevatorFunctionality.movement.action
    steps.append(step)
    return elevatorFunctionality, steps


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
    return elevatorFunctionality, steps, fulFilled


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
    elevatorFunctionality.save()

    return {
        "elevator_name": elevatorFunctionality.elevator.name,
        "current_floor": elevatorFunctionality.floor_no.name,
        "fulfilled_floor": fulFilled,
        "steps": steps,
    }

