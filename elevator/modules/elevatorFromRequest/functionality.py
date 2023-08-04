from ..functionality import get_ElevatorRequestStatus_Open, get_ElevatorRequestStatus_Closed
from ...models.models import ElevatorFromRequests
from ..functionality import get_Elevator, get_ElevatorFunctionality, get_Floor

def closeFromRequest(elevator, to_floor):
    openReq = get_ElevatorRequestStatus_Open()
    closeReq = get_ElevatorRequestStatus_Closed()
    ElevatorFromRequests.objects.filter(
        elevator=elevator,
        to_floor=to_floor,
        status=openReq
    ).update(
        status=closeReq
    )
    return

def get_AllOpenFromRequest(status, elevator):
    return ElevatorFromRequests.objects.filter(
        status=status,
        elevator=elevator,
    )

def get_AllOpenFromRequestFloor(status, elevator, to_floor):
    return ElevatorFromRequests.objects.filter(
        status=status,
        elevator=elevator,
        to_floor=to_floor
    )

def is_fromRequests_exists():
    return ElevatorFromRequests.objects.exists()


def count_fromRequests():
    return ElevatorFromRequests.objects.count()


def cal_fromRequest_count():
    if is_fromRequests_exists():
        count = count_fromRequests() + 1
    else:
        count = 1
    return count



def fromRequest(from_floor, elevator, to_floor, status, count_of_people):
    count = cal_fromRequest_count()
    req_id = "EFR_"+str(count)

    return ElevatorFromRequests.objects.create(
        reqID=req_id,
        from_floor=from_floor,
        to_floor=to_floor,
        status=status,
        elevator=elevator, 
        count_of_people = count_of_people
    )


def assignFromRequest(status, data):
    list_req = []
    elevator = get_Elevator(name=data["elevator"])
    elevFunc = get_ElevatorFunctionality(elevator=elevator)

    if elevFunc.floor_no.name != data["from_floor"]:
        raise Exception(
            "Invalid floor from the request is sent." +
            " The elevator is not on that floor.")

    for fl in data["to_floors"]:
        floor = get_Floor(name=fl)
        list_fromReq = get_AllOpenFromRequestFloor(
            status=status,
            elevator=elevator,
            to_floor=floor
        )

        if not list_fromReq:
            from_floor = get_Floor(name=data["from_floor"],)
            position = data["to_floors"].index(fl)
            req = fromRequest(
                from_floor=from_floor,
                elevator=elevator,
                to_floor=floor,
                status=status,
                count_of_people = data["PeoplePerFloor"][position]
            )
            
            list_req.append(req)
        else:
            list_req += list_fromReq
    return list_req
