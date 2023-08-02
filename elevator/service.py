from .models import *
from dataSeeding.models import *
from datetime import datetime, date
from django.utils import timezone
from .functionality import *
from django.db.models import Q


def create_floor(no):
    floor = "FL_"
    for i in range(1, no+1):
        val = floor + str(i)
        if not Floor.objects.filter(name=val).exists():
            Floor.objects.create(name=val)


def create_elevators(data):
    no = data["total_elevators"]
    cap = data["capacity"]
    reqCap = 8
    elevator = "EL_"
    # remove below line after 1 execute
    # Elevator.objects.all().delete()
    # ElevatorFunctionality.objects.all().delete()
    for i in range(1, no+1):
        val = elevator + str(i)
        if not Elevator.objects.filter(name=val).exists():
            ele = Elevator.objects.create(
                name=val, capacity=cap, requestsCapacity=reqCap,
            )
            ele_func = defaut_ElevatorFunctionality(ele)


def create_forRequest(data):
    status = ElevatorRequestStatus.objects.get(name="open")
    list_of_elevators = findAllElevatorFunctions()
    if is_allAtTheSameFloor(list_of_elevators):
        # list_forReq ElevatorForRequestsSerializer
        list_forReq = assignForRequestWhenAllAtSameFloor(
            list_of_elevators, data, status
        )
    else:
        """
            if is_anyMovingTowardsTheFloor():
                assignForRequestIfMoving
                    1. check in fromRequest
                modify data and return 
        """
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
    of_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    of_date = datetime.combine(of_date, datetime.min.time())
    of_date = timezone.make_aware(of_date, timezone.utc)
    next_date = of_date + timezone.timedelta(days=1)

    elevator = Elevator.objects.get(name=elevator)
    req_list = ElevatorForRequests.objects.filter(
        Q(elevator=elevator) &
        Q(reqTime__gt=of_date) &
        Q(reqTime__lt=next_date)
    )

    return req_list


def list_elevFuncMoving(data):
    return ElevatorFunctionality.objects.get(
        elevator=data["elevator"],
    )


def create_elevFuncOperational(data):
    oprStatus = Operational_Status.objects.get(
        value=data["status"]
    )

    elevFunc = ElevatorFunctionality.objects.get(
        elevator=data["elevator"],
    )

    elevFunc.operational_status = oprStatus
    elevFunc.save()

    return elevFunc


def create_elevFuncDoor(data):
    doorFunc = DoorFunctions.objects.get(
        name=data["action"],
    )

    elevFunc = ElevatorFunctionality.objects.get(
        elevator=data["elevator"],
    )

    elevFunc.door_functionality = doorFunc
    elevFunc.save()
    return elevFunc


def create_fromRequest(data):
    status = ElevatorRequestStatus.objects.get(name="open")

    try:
        list = assignFromRequest(status, data)
    except Exception as e:
        raise Exception(str(e))
    return list


def list_fromRequests(data):
    elevator = data["elevator"]
    of_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    of_date = datetime.combine(of_date, datetime.min.time())
    of_date = timezone.make_aware(of_date, timezone.utc)
    next_date = of_date + timezone.timedelta(days=1)

    elevator = Elevator.objects.get(name=elevator)
    req_list = ElevatorFromRequests.objects.filter(
        Q(elevator=elevator) &
        Q(reqTime__gt=of_date) &
        Q(reqTime__lt=next_date)
    )

    return req_list


def list_nextDestination(data):
    elevator = data["elevator"]
    elevator = Elevator.objects.get(name=elevator)
    status = ElevatorRequestStatus.objects.get(name="open")

    list_req = findListOfReq(status=status, elevator=elevator)

    try:
        obj = segregateAccordingToDirection(elevator, sorted(list_req))
    except Exception as ex:
        raise Exception(ex)
    return obj


def list_fullfilElevatorNextRequest():
    list_obj = []
    elevFuncs = findAllElevatorFunctions()
    # elevFunc = ElevatorFunctionality.objects.all().order_by("id")
    data = dict()

    for elevatorFunc in elevFuncs:
        data["elevator"] = elevatorFunc.elevator.name

        obj = list_nextDestination(data=data)
        
        ob = fullfil(
            elevatorFunc = elevatorFunc,
            nextDest = obj["next_floor"],
            nextDir = obj["next_direction"],
        )

        list_obj.append(ob)

    return list_obj
