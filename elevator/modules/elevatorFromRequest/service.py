from ...models.models import ElevatorRequestStatus, ElevatorFromRequests
from ..elevatorFromRequest.functionality import assignFromRequest
from ..functionality import get_Elevator
from ..functionality import calculate_date, requests_list


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
    of_date, next_date = calculate_date(convertFrom=data["date"])

    req_list = requests_list(
        model=ElevatorFromRequests,
        elevator=elevator,
        of_date=of_date,
        next_date=next_date
    )

    return req_list
