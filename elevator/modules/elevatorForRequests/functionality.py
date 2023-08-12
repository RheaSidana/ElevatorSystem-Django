from ..functionality import (
    total_floors, get_ElevatorForRequests,
    get_from_requests
)
from .repository import *


def create_for_request_when_floor_in_from_request(
        floor_id, status, elevator_functionality, people_count, fromReq):

    elevator = elevator_functionality.elevator

    if (elevator_functionality.curr_req_count == elevator.requestsCapacity):
        return people_count, None

    else:
        for_request = create_for_request(
            floor_id=floor_id,
            status=status,
            elevator=elevator,
            people_count=people_count
        )
        buffer_count = elevator_functionality.curr_person_count - fromReq.count_of_people

        if (buffer_count + people_count <= elevator.requestsCapacity):
            people_count = 0

        else:
            people_can_board_elevator = (
                elevator.requestsCapacity - buffer_count)
            people_count -= people_can_board_elevator
            update_count_of_people(
                for_request=for_request,
                people_count=people_can_board_elevator
            )

        increment_curr_req_count(elevator_functionality)

    return people_count, for_request


def return_for_request_if_elevator_already_has_from_requests(
        elevator_functionality_list, data, status):
    requests_list = []
    for elevator_functionality in elevator_functionality_list:
        elevator = elevator_functionality.elevator
        from_requests_to_floor_list = get_from_requests(
            status=status,
            elevator=elevator,
        ).values_list(
            "to_floor", flat=True
        )

        for floor_request in from_requests_to_floor_list:
            if floor_request in data["floors"]:
                position = data["floors"].index(floor_request)
                people_count = data["PeoplePerFloor"][position]

                people_count, for_request = create_for_request_when_floor_in_from_request(
                    floor_id=floor_request,
                    status=status,
                    elevator_functionality=elevator_functionality,
                    people_count=people_count,
                    fromReq=floor_request,
                )

                if for_request is not None:
                    requests_list.append(for_request)

                if people_count != 0:
                    data["PeoplePerFloor"][position] = people_count
                else:
                    data["floors"].pop(position)
                    data["PeoplePerFloor"].pop(position)

    return data, requests_list


def min_diff_btw_elevator_and_requested_floor(
        elevator_functionality, floor_no, bufferCount, min_diff, open_requests=0):

    elevator = elevator_functionality.elevator
    if (elevator_functionality.curr_req_count >= elevator.requestsCapacity):
        return min_diff
    else:
        if (bufferCount == elevator.capacity):
            return min_diff
        else:
            if not open_requests or (
                    open_requests and
                    len(open_requests) < elevator.requestsCapacity):
                floorNo_req = int(floor_no.split("_")[1])
                floorNo_elev = int(
                    elevator_functionality.floor_no.name.split("_")[1])

                if min_diff > abs(floorNo_req - floorNo_elev):
                    min_diff = floorNo_req - floorNo_elev

    return min_diff


def create_for_request_when_new_request(
        elevator_functionality, floor_no, people_count, status, buffer_count):
    # when no elevator is available to take request
    if elevator_functionality is None:
        elevator = None
        for_request = create_for_request(
            floor_id=floor_no,
            elevator=elevator,
            status=status,
            people_count=people_count
        )
        return 0, for_request

    # when elevator is available to take request
    elevator = elevator_functionality.elevator
    if (elevator_functionality.curr_req_count >= elevator.requestsCapacity):
        buffer_count = 0
        return people_count, None
    else:
        # when no capacity
        if (buffer_count == elevator.capacity):
            buffer_count = 0
            return people_count, None
        # when has capacity

        for_request = create_for_request(
            floor_id=floor_no,
            elevator=elevator,
            status=status,
            people_count=people_count
        )

        if (buffer_count + people_count <= elevator.capacity):
            buffer_count += people_count
            people_count = 0

        else:
            people_can_board_elevator = (elevator.capacity - buffer_count)
            buffer_count = 0
            people_count -= people_can_board_elevator
            update_count_of_people(
                for_request=for_request,
                people_count=people_can_board_elevator
            )

        increment_curr_req_count(elevator_functionality)

    return people_count, for_request


def create_for_request_to_the_nearest_elevator_possible(
        elevator_functionality_list, data, status):
    requests_list = []
    buffCount = 0
    i = 0
    req_length = len(data["floors"])
    is_req_added_successfully = True
    req_added = 0

    while i <= (req_length-1):
        if req_added == req_length:
            break

        if i != req_added:
            continue

        # if reqest exist with null elevator
        req_with_null_elevator = for_requests_of_floor_when_elevator_is_null(
            floor=data["floors"][i],
        )
        if req_with_null_elevator.count() != 0:
            req_added += 1
            i += 1
            continue

        # if request is new request
        min_diff_btw_elevator_and_floor = total_floors()
        elevator_functionality_of_min_diff = None
        req_found = False

        for elevator_functionality in elevator_functionality_list:
            if req_added == req_length:
                break

            elevator = elevator_functionality.elevator

            if is_req_added_successfully == True:
                # if request already exists = continue
                open_req_floor = get_for_requests_of_floor(
                    floor=data["floors"][i],
                    elevator=elevator,
                    status=status
                )

                if open_req_floor.count() != 0:
                    # list_req.append(openReq_Floor)
                    requests_list += open_req_floor
                    req_added += 1
                    i += 1
                    req_found = True
                    break

            # if elevFunc.oprStat is not working = continue
            if elevator_functionality.operational_status.value != "Working":
                continue

            # if elevator has any open req
            open_requests = get_ElevatorForRequests(
                status=status,
                elevator=elevator
            )

            # cal expected capacity of elevator
            bufferCount = sum(open_requests.values_list(
                "count_of_people", flat=True
            ))
            # if not capacity to add people to the elevator
            if bufferCount == elevator.capacity:
                continue

            if elevator_functionality_of_min_diff is None:
                elevator_functionality_of_min_diff = elevator_functionality

            diff = min_diff_btw_elevator_and_requested_floor(
                elevator_functionality=elevator_functionality,
                floor_no=data["floors"][i],
                bufferCount=bufferCount,
                min_diff=min_diff_btw_elevator_and_floor,
                open_requests=open_requests
            )

            if diff < min_diff_btw_elevator_and_floor:
                min_diff_btw_elevator_and_floor = diff
                elevator_functionality_of_min_diff = elevator_functionality
                buffCount = bufferCount

        if not req_found:
            peopleCount, req_with_null_elevator = create_for_request_when_new_request(
                elevator_functionality=elevator_functionality_of_min_diff,
                floor_no=data["floors"][i],
                people_count=data["PeoplePerFloor"][i],
                status=status,
                buffer_count=buffCount,
            )

            if req_with_null_elevator is not None:
                requests_list.append(req_with_null_elevator)

            if peopleCount != 0:
                data["PeoplePerFloor"][i] = peopleCount
                is_req_added_successfully = False
            else:
                i += 1
                req_added += 1

        if req_added == req_length:
            break

    return requests_list
