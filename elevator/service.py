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
            print("elevator : ")
            print(ele)
            ele_func = defaut_ElevatorFunctionality(ele)
            print("Elevator Functionality: ")
            print(ele_func)


def create_forRequest(data):
    status = ElevatorRequestStatus.objects.get(name="open")
    # print(status)
    list_of_elevators = findAllElevators()
    # print(list_of_elevators)
    if is_allAtTheSameFloor(list_of_elevators):
        assignForRequestWhenAllAtSameFloor(
            list_of_elevators, data, status
        )
    else:
        """
            if is_anyMovingTowardsTheFloor():
                assignForRequestIfMoving
                    1. check in fromRequest
                modify data and return 
        """
        print("elevator")
        print(list_of_elevators)
        assignForRequestToTheNearestElevatorPossible(
            list_of_elevators, data, status
        )


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