from ...models.models import ElevatorForRequests
from ..functionality import (
    cal_Date,
    cal_ReqList,
    get_Elevator,
    get_ElevatorRequestStatus_Open,
    get_AllElevatorFunctions
)
from .functionality import (
    assignForRequestWhenAllAtSameFloor,
    assignForRequestIfElevatorAlreadyHasRequests,
    assignForRequestToTheNearestElevatorPossible,
    is_allAtTheSameFloor
)


def create_forRequest(data):
    status = get_ElevatorRequestStatus_Open()
    list_of_elevators = get_AllElevatorFunctions()
    if is_allAtTheSameFloor(list_of_elevators):
        # list_forReq ElevatorForRequestsSerializer
        list_forReq = assignForRequestWhenAllAtSameFloor(
            list_of_elevators, data, status
        )
    else:
        data, list_forReq = assignForRequestIfElevatorAlreadyHasRequests(
            list_of_elevators, data, status
        )
        if data != {}:
            list_forReq = assignForRequestToTheNearestElevatorPossible(
                list_of_elevators, data, status
            )
    return list_forReq


def list_forRequests(data):
    elevator = data["elevator"]
    elevator = get_Elevator(elevator=elevator)

    of_date = data["date"]
    of_date, next_date = cal_Date(convertFrom=of_date)

    req_list = cal_ReqList(
        model=ElevatorForRequests,
        elevator=elevator,
        of_date=of_date,
        next_date=next_date
    )

    return req_list
