from ..functionality import get_ElevatorRequestStatus_Open
from ..functionality import get_ElevatorRequestStatus_Closed
from ...models.models import ElevatorForRequests
from ..functionality import get_Floor
from ..elevatorFromRequest.functionality import get_AllOpenFromRequest
from ..functionality import (
    get_Elevator_Count, get_ElevatorForRequests,
    get_ElevatorForRequests_floor
)


def closeForRequest(elevator, floor):
    openReq = get_ElevatorRequestStatus_Open()
    closeReq = get_ElevatorRequestStatus_Closed()
    reqs = ElevatorForRequests.objects.filter(
        elevator=elevator,
        floor_id=floor,
        status=openReq
    )
    # .update(
    #     status=closeReq
    # )

    peopleCount = 0
    for r in reqs:
        peopleCount += r.count_of_people

    reqs.update(
        status=closeReq
    )
    return peopleCount


def create_forRequest(reqID, floor_id, status, elevator, count_of_people):
    return ElevatorForRequests.objects.create(
        reqID=reqID,
        floor_id=floor_id,
        status=status,
        elevator=elevator,
        count_of_people=count_of_people
    )


def is_allAtTheSameFloor(list_of_elevator):
    floor = list_of_elevator[0].floor_no
    for elev in list_of_elevator:
        if floor != elev.floor_no:
            return False
    return True


def is_forRequests_exists():
    return ElevatorForRequests.objects.exists()


def count_forRequests():
    return ElevatorForRequests.objects.count()


def cal_forRequest_count():
    if is_forRequests_exists():
        count = count_forRequests() + 1
    else:
        count = 1
    return count


def forRequest(elevator, floor_no, people_count, status, bufferCount):
    if (elevator.curr_req_count >= elevator.elevator.requestsCapacity):
        bufferCount = 0
        return people_count, bufferCount, None
    else:
        if (bufferCount == elevator.elevator.capacity):
            bufferCount = 0
            return people_count, bufferCount, None

        elev = elevator.elevator

        forReq = cal_forRequest_create(
            floor_id=floor_no,
            elevator=elev,
            status=status,
            peopleCount=people_count
        )

        if (bufferCount + people_count <= elev.capacity):
            bufferCount += people_count
            people_count = 0

        else:
            add = (elev.capacity-bufferCount)
            people_count -= add
            forReq.count_of_people = add
            bufferCount = 0

        elevator.curr_req_count += 1
        elevator.save()
        forReq.save()

    return people_count, bufferCount, forReq


def assignForRequestWhenAllAtSameFloor(list_of_elevators_func, data, status):
    req_added = 0

    list_Req = []

    for elevFunc in list_of_elevators_func:
        openReq = get_ElevatorForRequests(
            status=status,
            elevator=elevFunc.elevator
        )


        bufferCount = cal_peopleCount(openReq)


        for i in range(0, (len(data["floors"]))):
            if i != req_added:
                continue

            floor = data["floors"][i]
            floor_no = get_Floor(name=floor)
            openReq_ofFloor = get_ElevatorForRequests_floor(
                status=status,
                elevator=elevFunc.elevator,
                floor=floor_no
            )

            if openReq_ofFloor.count() != 0:
                req_added += 1
                continue

            peopleCount, bufferCount, forReq = forRequest(
                elevator=elevFunc,
                floor_no=floor,
                people_count=data["PeoplePerFloor"][i],
                status=status,
                bufferCount=bufferCount
            )

            if forReq is not None:
                list_Req.append(forReq)

            if peopleCount == 0:
                req_added += 1
            else:
                data["PeoplePerFloor"][i] = peopleCount
                break

        if req_added == (len(data["floors"])):
            break

    return list_Req


def cal_forRequest_create(floor_id, elevator, status, peopleCount):
    count = cal_forRequest_count()
    floor = get_Floor(name=floor_id)
    req_id = "FR_" + str(count)
    return create_forRequest(
        reqID=req_id,
        floor_id=floor,
        status=status,
        elevator=elevator,
        count_of_people=peopleCount
    )


def foundInFromRequest(floor_id, status, elevatorFunc, peopleCount, fromReq):
    elev = elevatorFunc.elevator
    if (elevatorFunc.curr_req_count == elev.requestsCapacity):
        return peopleCount
    # curr_person_count = models.IntegerField()
    else:
        forReq = cal_forRequest_create(
            floor_id=floor_id,
            status=status,
            elevator=elev,
            peopleCount=peopleCount
        )
        bufferCount = elevatorFunc.curr_person_count - fromReq.count_of_people
        if (bufferCount + peopleCount <= elev.requestsCapacity):
            peopleCount = 0
        else:
            add = (elev.requestsCapacity - bufferCount)
            peopleCount -= add
            forReq.count_of_people = add

        elevatorFunc.curr_req_count += 1
        elevatorFunc.save()
        forReq.save()
    return peopleCount


def assignForRequestIfElevatorAlreadyHasRequests(list_of_elevators, data, status):

    for elevatorFunc in list_of_elevators:
        elevator = elevatorFunc.elevator
        list_fromReqs = get_AllOpenFromRequest(
            status=status,
            elevator=elevator,
        )

        for req in list_fromReqs:

            if req.to_floor in data["floors"]:
                position = data["floors"].index(req)
                peopleCount = data["PeoplePerFloor"][position]

                peopleCount = foundInFromRequest(
                    floor_id=req.to_floor,
                    status=status,
                    elevatorFunc=elevatorFunc,
                    peopleCount=peopleCount,
                    fromReq=req,
                )

                if peopleCount != 0:
                    data["PeoplePerFloor"][position] = peopleCount
                else:
                    data["floors"].pop(position)
                    data["PeoplePerFloor"].pop(position)

    return data


def cal_peopleCount(reqs):
    count = 0
    if reqs:
        for r in reqs:
            count += r.count_of_people
    return count


def findMinDiff(elevator, floor_no, bufferCount, min, openReq=0):

    if (elevator.curr_req_count >= elevator.elevator.requestsCapacity):
        return None
    else:
        elev = elevator.elevator
        if (bufferCount == elev.capacity):
            return None
        else:
            if not openReq or (openReq and len(openReq) < elev.requestsCapacity):
                floorNo_req = int(floor_no.split("_")[1])
                floorNo_elev = int(elevator.floor_no.name.split("_")[1])

                if min > abs(floorNo_req - floorNo_elev):
                    min = floorNo_req - floorNo_elev

    return min


def forRequestToElevator(elevator, floor_no, people_count, status, bufferCount):

    if (elevator.curr_req_count >= elevator.elevator.requestsCapacity):
        bufferCount = 0
        return people_count, bufferCount
    else:
        if (bufferCount == elevator.elevator.capacity):
            bufferCount = 0
            return people_count
        elev = elevator.elevator
        forReq = cal_forRequest_create(
            floor_id=floor_no,
            elevator=elev,
            status=status,
            peopleCount=people_count
        )

        if (bufferCount + people_count <= elev.capacity):
            bufferCount += people_count
            people_count = 0

        else:
            add = (elev.capacity-bufferCount)
            bufferCount = 0
            people_count -= add
            forReq.count_of_people = add
        elevator.curr_req_count += 1
        elevator.save()
        forReq.save()

    return people_count


def assignForRequestToTheNearestElevatorPossible(list_of_elevators, data, status):
    buffCount = 0
    i = 0
    expr = i < len(data["floors"])-1
    while expr:
        minDiff = get_Elevator_Count()
        minElev = None

        for elevator in list_of_elevators:
            elev = elevator.elevator
            openReq = get_ElevatorForRequests(
                status=status,
                elevator=elev
            )

            bufferCount = cal_peopleCount(openReq)

            diff = findMinDiff(
                elevator=elevator,
                floor_no=data["floors"][i],
                bufferCount=bufferCount,
                min=minDiff,
                openReq=openReq
            )

            if not diff is None and diff < minDiff:
                minDiff = diff
                minElev = elevator
                buffCount = bufferCount

        peopleCount = forRequestToElevator(
            elevator=minElev,
            floor_no=data["floors"][i],
            people_count=data["PeoplePerFloor"][i],
            status=status,
            bufferCount=buffCount,
        )

        if peopleCount != 0:
            data["PeoplePerFloor"][i] = peopleCount
        else:
            i += 1


def get_AllForRequests(elevator, status):
    return ElevatorForRequests.objects.filter(
        elevator=elevator,
        status=status,
    )
