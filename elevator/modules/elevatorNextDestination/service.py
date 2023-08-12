from ..functionality import (
    get_Elevator,
    get_elevator_request_status_is_open,
    get_ElevatorForRequests,
    get_ElevatorFunctionality,
    total_floors,
    get_from_requests
)
from ...models.models import ElevatorForRequests, ElevatorFromRequests


def get_requests_floor(model, requestStatus, elevator):
    if model == ElevatorForRequests:
        return get_ElevatorForRequests(
            status=requestStatus,
            elevator=elevator
        ).values_list(
            "floor_id__name", flat=True
        )
    elif model == ElevatorFromRequests:
        return get_from_requests(
            status=requestStatus,
            elevator=elevator
        ).values_list(
            "to_floor__name", flat=True
        )

def get_elevator_requests(ElevatorRequestStatus, elevator):
    requests = []

    forRequestsFloors = get_requests_floor(
        model=ElevatorForRequests,
        requestStatus=ElevatorRequestStatus,
        elevator=elevator
    )
    if forRequestsFloors:
        requests += forRequestsFloors

    fromRequestsFloors = get_requests_floor(
        model=ElevatorFromRequests,
        requestStatus=ElevatorRequestStatus,
        elevator=elevator
    )
    if fromRequestsFloors:
        requests += fromRequestsFloors

    return sorted(requests)


def create_UpAndDownDirectionList(requestsFloor, currentFloor):
    upDirectionList = []
    downDirectionList = []

    for floor in requestsFloor:
        if floor > currentFloor:
            upDirectionList.append(floor)
        elif floor <= currentFloor:
            downDirectionList.append(floor)

    downDirectionList.sort(reverse=True)

    return downDirectionList, upDirectionList


def differenceBetween(toFloor, currentFloor):
    toFloor = int(toFloor.split("_")[1])
    currentFloor = int(currentFloor.split("_")[1])
    return abs(toFloor - currentFloor)


def is_differenceBetweenLessThanMinDifference(toFloor, currentFloor, minDifference):
    return differenceBetween(
        toFloor=toFloor, currentFloor=currentFloor
    ) < minDifference


def get_next_destination_of(elevator, elevatorsRequests):
    elevFunc = get_ElevatorFunctionality(elevator=elevator)

    currentFloor = elevFunc.floor_no.name
    UpDirectionList = []
    downDirectionList = []

    minDifference = total_floors()
    nextDestination = ""
    nextDirection = "Stationary"

    if elevatorsRequests is not None:
        downDirectionList, UpDirectionList = create_UpAndDownDirectionList(
            requestsFloor=elevatorsRequests,
            currentFloor=currentFloor
        )

        if downDirectionList != [] and is_differenceBetweenLessThanMinDifference(
            toFloor=downDirectionList[0],
            currentFloor=currentFloor,
            minDifference=minDifference
        ):
            minDifference = differenceBetween(
                toFloor=downDirectionList[0],
                currentFloor=currentFloor
            )
            nextDestination = downDirectionList.pop(0)
            nextDirection = "Down"

        elif UpDirectionList != []:
            if nextDestination != "" and is_differenceBetweenLessThanMinDifference(
                toFloor=UpDirectionList[0],
                currentFloor=currentFloor,
                minDifference=minDifference
            ):
                downDirectionList.insert(0, nextDestination)

            nextDestination = UpDirectionList.pop(0)
            nextDirection = "Up"

    if currentFloor == nextDestination:
        nextDirection = "Stationary"


    obj = {
        "elevator_name": elevator.name,
        "current_floor": currentFloor,
        "next_floor": nextDestination,
        "next_direction": nextDirection,
        "floorsInUpDirection": UpDirectionList,
        "floorsInDownDirection": downDirectionList,
    }

    return obj


def list_nextDestination(data):
    elevator = data["elevator"]
    elevator = get_Elevator(elevator=elevator)
    open = get_elevator_request_status_is_open()

    requests = get_elevator_requests(
        ElevatorRequestStatus=open,
        elevator=elevator
    )

    try:
        obj = get_next_destination_of(
            elevator=elevator,
            elevatorsRequests=requests
        )
    except Exception as ex:
        raise Exception(ex)
    return obj
