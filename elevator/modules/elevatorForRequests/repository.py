from ...models.models import ElevatorForRequests
from ..functionality import get_Floor

def is_forRequests_exists():
    return ElevatorForRequests.objects.exists()


def count_forRequests():
    return int(
        ElevatorForRequests
        .objects.all().order_by("reqTime")
        .last().reqID.split("_")[1]
    )

def for_request_count():
    if is_forRequests_exists():
        count = count_forRequests() + 1
    else:
        count = 1
    return count

def create_for_request(floor_id, elevator, status, people_count):
    count = for_request_count()
    floor = get_Floor(name=floor_id)
    req_id = "FR_" + str(count)

    return ElevatorForRequests.objects.create(
        reqID=req_id,
        floor_id=floor,
        status=status,
        elevator=elevator,
        count_of_people=people_count
    )

def increment_curr_req_count(elevator_functionality):
    elevator_functionality.curr_req_count += 1
    elevator_functionality.save()

def update_count_of_people(for_request, people_count):
    for_request.count_of_people = people_count
    for_request.save()

def for_requests_of_floor_when_elevator_is_null(floor):
    return ElevatorForRequests.objects.filter(
        floor_id__name=floor,
        elevator__isnull=True
    )

def get_for_requests_of_floor(status, elevator, floor):
    return ElevatorForRequests.objects.filter(
        status=status,
        elevator=elevator,
        floor_id__name=floor,
    )
