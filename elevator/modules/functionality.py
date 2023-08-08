from ..models.models import (
    ElevatorFunctionality,
    Operational_Status,
    DoorFunctions,
    Elevator,
    ElevatorRequestStatus,
    Moving,
    Floor,
    Movements,
    ElevatorForRequests,
    ElevatorFromRequests
)
from datetime import datetime
from django.utils import timezone
from django.db.models import Q


def get_ElevatorFunctionality(elevator):
    return ElevatorFunctionality.objects.get(
        elevator=elevator,
    )


def get_AllElevatorFunctions():
    return ElevatorFunctionality.objects.all().order_by("id")


def get_Floor(name):
    return Floor.objects.get(
        name=name
    )


def get_Floor_Count():
    return Floor.objects.all().count()


def get_Operational_Status(status):
    return Operational_Status.objects.get(
        value=status
    )


def get_ElevatorForRequests(status, elevator):
    return ElevatorForRequests.objects.filter(
        status=status,
        elevator=elevator
    ).order_by("reqTime")

def get_ElevatorFromRequest(status, elevator):
    return ElevatorFromRequests.objects.filter(
        status=status,
        elevator=elevator,
    ).order_by("reqTime")

def get_ElevatorForRequests_floor(status, elevator, floor):
    return ElevatorForRequests.objects.filter(
        status=status,
        elevator=elevator,
        floor_id=floor,
    )


def get_ElevatorForRequests_floor_elevatorIsNull(floor):
    return ElevatorForRequests.objects.filter(
        floor_id=floor,
        elevator__isnull=True
    )


def get_ElevatorForRequests_elevatorIsNull():
    return ElevatorForRequests.objects.filter(
        elevator__isnull=True
    )


def get_DoorFunctions(action):
    return DoorFunctions.objects.get(
        name=action
    )


def get_Elevator(elevator):
    return Elevator.objects.get(
        name=elevator
    )


def get_ElevatorRequestStatus_Closed():
    return ElevatorRequestStatus.objects.get(
        name="closed"
    )


def getElevatorRequestStatusOpen():
    return ElevatorRequestStatus.objects.get(
        name="open"
    )


def get_Movements(action):
    return Movements.objects.get(
        action=action,
    )


def get_Moving(direction):
    return Moving.objects.get(
        direction=direction
    )


def get_Elevator_Count():
    return Elevator.objects.count()


def cal_Date(convertFrom):
    of_date = datetime.strptime(convertFrom, "%Y-%m-%d").date()
    of_date = datetime.combine(of_date, datetime.min.time())
    of_date = timezone.make_aware(of_date, timezone.utc)
    next_date = of_date + timezone.timedelta(days=1)
    return of_date, next_date


def cal_ReqList(model, elevator, of_date, next_date):
    return model.objects.filter(
        Q(elevator=elevator) &
        Q(reqTime__gt=of_date) &
        Q(reqTime__lt=next_date)
    )
