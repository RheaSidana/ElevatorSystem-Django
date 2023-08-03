from ...models.models import ElevatorRequestStatus, ElevatorFromRequests
from ...functionality import assignFromRequest
from ..functionality import get_Elevator
from ..functionality import cal_Date, cal_ReqList


def create_fromRequest(data):
    status = ElevatorRequestStatus.objects.get(name="open")

    try:
        list = assignFromRequest(status, data)
    except Exception as e:
        raise Exception(str(e))
    return list

def list_fromRequests(data):
    elevator = data["elevator"]
    elevator = get_Elevator(elevator=elevator)
    of_date, next_date = cal_Date(convertFrom=data["date"])

    req_list = cal_ReqList(
        model=ElevatorFromRequests, 
        elevator=elevator, 
        of_date=of_date, 
        next_date=next_date
    )

    return req_list
