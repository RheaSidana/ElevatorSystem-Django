from ..elevatorForRequests.service import (
    create_for_request,
)
from ..functionality import (
    get_Floor,
    get_ElevatorRequestStatus_Closed,
    get_elevator_request_status_is_open,
    get_Movements,
    get_DoorFunctions,
    get_Moving,
    get_from_requests,
    get_ElevatorForRequests
)
from ..fulFillElevatorsNextRequest.service import fulfill


def updateFromRequests(elevatorFunctionality, floor_no):
    status = get_elevator_request_status_is_open()

    allFromReq = get_from_requests(
        status=status,
        elevator=elevatorFunctionality.elevator
    )

    close_status = get_ElevatorRequestStatus_Closed()

    allFromReq.update(
        to_floor=floor_no,
        status=close_status
    )

    return


def updateForRequests(elevatorFunctionality):
    status = get_elevator_request_status_is_open()
    allForReq = get_ElevatorForRequests(
        elevator=elevatorFunctionality.elevator,
        status=status,
    )

    data = {
        "floors": [],
        "PeoplePerFloor": []
    }
    if allForReq != {}:
        reqs = allForReq
        reqs.delete()
        for req in allForReq:
            data["floors"].append(req.floor_id.name)
            data["PeoplePerFloor"].append(req.count_of_people)

        if data["floors"] != []:
            create_for_request(data=data)

    return


def assignEveryRequestToNextDestination(elevatorFunctionality):
    elevFulfill = fulfill(
        elevatorFunctionality=elevatorFunctionality
    )

    floor_to = get_Floor(elevFulfill["current_floor"])
    # update open from requests
    # to the next floor
    # and close the fromRequests
    updateFromRequests(
        elevatorFunctionality=elevatorFunctionality,
        floor_no=floor_to
    )

    # get all the forRequests
    # data = {
    #    "floors": ["FL_2", "FL_4"],
    #    "PeoplePerFloor": [3, 4],
    # }
    # delete ForRequest of the elevator
    # create ForRequest with the data
    updateForRequests(
        elevatorFunctionality=elevatorFunctionality
    )

    return floor_to


def updateFunctionality(elevatorFunctionality, operational_status, floor):
    movement_stop = get_Movements(action="Stop")
    direction = get_Moving(direction="Stationary")
    door = get_DoorFunctions(action="Open")

    elevatorFunctionality.operational_status = operational_status
    elevatorFunctionality.movement = movement_stop
    elevatorFunctionality.floor_no = floor
    elevatorFunctionality.direction = direction
    elevatorFunctionality.door_functionality = door
    elevatorFunctionality.curr_req_count = 0
    elevatorFunctionality.curr_person_count = 0

    elevatorFunctionality.save()

    return elevatorFunctionality

def updateFunctionality_WhenNotWorking(elevatorFunctionality, operational_status):
    if elevatorFunctionality.operational_status.value == "Working":
        return elevatorFunctionality
    
    movement_stop = get_Movements(action="Stop")
    direction = get_Moving(direction="Stationary")
    door = get_DoorFunctions(action="Close")

    elevatorFunctionality.operational_status = operational_status
    elevatorFunctionality.movement = movement_stop
    elevatorFunctionality.direction = direction
    elevatorFunctionality.door_functionality = door

    elevatorFunctionality.save()

    return elevatorFunctionality