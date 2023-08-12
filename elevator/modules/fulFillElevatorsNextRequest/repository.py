from ..functionality import(
    get_elevator_request_status_is_open,
    get_ElevatorRequestStatus_Closed
)
from ...models.models import ElevatorForRequests

def closeForRequest(elevator, floor):
    openReq = get_elevator_request_status_is_open()
    closeReq = get_ElevatorRequestStatus_Closed()
    reqs = ElevatorForRequests.objects.filter(
        elevator=elevator,
        floor_id=floor,
        status=openReq
    )

    peopleCount = sum(reqs.values_list(
        "count_of_people", flat=True
    ))

    reqs.update(
        status=closeReq
    )
    return peopleCount
