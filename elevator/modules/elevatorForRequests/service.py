from ...models.models import ElevatorForRequests
from ..functionality import (
    calculate_date,
    requests_list,
    get_Elevator,
    get_elevator_request_status_is_open,
    get_all_elevator_functionality
)
from .functionality import (
    return_for_request_if_elevator_already_has_from_requests,
    create_for_request_to_the_nearest_elevator_possible,
)


def create_for_request(data):
    status = get_elevator_request_status_is_open()
    elevator_functionality_list = get_all_elevator_functionality()

    data, elevator_for_requests_list = return_for_request_if_elevator_already_has_from_requests(
        elevator_functionality_list=elevator_functionality_list, 
        data=data, 
        status=status
    )

    if data:
        elevator_for_requests_list = create_for_request_to_the_nearest_elevator_possible(
            elevator_functionality_list=elevator_functionality_list, 
            data=data, 
            status=status
        )

    return elevator_for_requests_list


def list_forRequests(data):
    elevator_name = data["elevator"]
    elevator = get_Elevator(elevator=elevator_name)

    of_date = data["date"]
    of_date, next_date = calculate_date(convertFrom=of_date)

    return requests_list(
        model=ElevatorForRequests,
        elevator=elevator,
        of_date=of_date,
        next_date=next_date
    )
