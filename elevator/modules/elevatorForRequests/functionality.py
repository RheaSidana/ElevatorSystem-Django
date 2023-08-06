from ..functionality import get_ElevatorRequestStatus_Open
from ..functionality import get_ElevatorRequestStatus_Closed
from ...models.models import ElevatorForRequests
from ..functionality import get_Floor
from ..elevatorFromRequest.functionality import get_AllOpenFromRequest
from ..functionality import (
    get_Floor_Count, get_ElevatorForRequests,
    get_ElevatorForRequests_floor,
    get_ElevatorForRequests_floor_elevatorIsNull
)
from ..functionality import get_Operational_Status


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
    return int(
        ElevatorForRequests
        .objects.all().order_by("reqID")
        .last().reqID.split("_")[1]
    )


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

            openReq_ofFloor = ForRequestAlreadyExists(
                floor=data["floors"][i],
                elevator=elevFunc.elevator,
                status=status
            )

            if openReq_ofFloor.count() != 0:
                list_Req.append(openReq_ofFloor)
                req_added += 1
                continue

            peopleCount, bufferCount, forReq = forRequest(
                elevator=elevFunc,
                floor_no=data["floors"][i],
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
        return peopleCount, None
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
    return peopleCount, forReq


def assignForRequestIfElevatorAlreadyHasRequests(list_of_elevators, data, status):
    list_req = []
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

                peopleCount, forReq = foundInFromRequest(
                    floor_id=req.to_floor,
                    status=status,
                    elevatorFunc=elevatorFunc,
                    peopleCount=peopleCount,
                    fromReq=req,
                )

                if forReq is not None:
                    list_req.append(forReq)

                if peopleCount != 0:
                    data["PeoplePerFloor"][position] = peopleCount
                else:
                    data["floors"].pop(position)
                    data["PeoplePerFloor"].pop(position)

    return data, list_req


def cal_peopleCount(reqs):
    count = 0
    if reqs:
        for r in reqs:
            count += r.count_of_people
    return count


def findMinDiff(elevator, floor_no, bufferCount, min, openReq=0):
    if (elevator.curr_req_count >= elevator.elevator.requestsCapacity):
        return min
    else:
        elev = elevator.elevator
        if (bufferCount == elev.capacity):
            return min
        else:
            if not openReq or (openReq and len(openReq) < elev.requestsCapacity):
                floorNo_req = int(floor_no.split("_")[1])
                floorNo_elev = int(elevator.floor_no.name.split("_")[1])

                if min > abs(floorNo_req - floorNo_elev):
                    min = floorNo_req - floorNo_elev

    return min


def forRequestToElevator(elevatorFunc, floor_no, people_count, status, bufferCount):
    if elevatorFunc is None:
        print("in None")
        elev = None
        forReq = cal_forRequest_create(
            floor_id=floor_no,
            elevator=elev,
            status=status,
            peopleCount=people_count
        )
        return 0, forReq
    if (elevatorFunc.curr_req_count >= elevatorFunc.elevator.requestsCapacity):
        bufferCount = 0
        return people_count, None
    else:
        if (bufferCount == elevatorFunc.elevator.capacity):
            bufferCount = 0
            return people_count, None
        elev = elevatorFunc.elevator
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
        elevatorFunc.curr_req_count += 1
        elevatorFunc.save()
        forReq.save()

    return people_count, forReq


def ForRequestAlreadyExists(floor, elevator, status):
    floor = get_Floor(
        name=floor
    )
    openReq_Floor = get_ElevatorForRequests_floor(
        status=status,
        elevator=elevator,
        floor=floor
    )

    return openReq_Floor


def assignForRequestToTheNearestElevatorPossible(list_of_elevators_func, data, status):
    list_req = []
    buffCount = 0
    i = 0
    length = len(data["floors"])
    isReqFullFill = True
    req_added = 0
    while i <= (length-1):
        if req_added == length:
            break
        if i != req_added:
            continue
        minDiff = get_Floor_Count()
        minElev = None
        found = False

        # if reqest exist with null elevator 
        # it should not add 1 more req
        floor = get_Floor(name=data["floors"][i])
        req = get_ElevatorForRequests_floor_elevatorIsNull(
            floor=floor,
        )
        if req.count() != 0:
            req_added += 1
            continue

        for elevatorFunc in list_of_elevators_func:
            if req_added == length:
                break

            elev = elevatorFunc.elevator
            if isReqFullFill == True:
                # if request already exists = continue
                openReq_Floor = ForRequestAlreadyExists(
                    floor=data["floors"][i],
                    elevator=elev,
                    status=status
                )
                if openReq_Floor.count() != 0:
                    # list_req.append(openReq_Floor)
                    list_req += openReq_Floor
                    req_added += 1
                    i += 1
                    found = True
                    break

            # if elevFunc.oprStat is not working = continue
            oprStatus = get_Operational_Status(
                status="Working"
            )

            if elevatorFunc.operational_status != oprStatus:
                continue

            # if elevator has any open req = count expected people
            # if elevator can take the request/capacity
            # if nearest then
            openReq = get_ElevatorForRequests(
                status=status,
                elevator=elev
            )

            bufferCount = cal_peopleCount(openReq)
            print("bufferCount = ", str(bufferCount))
            if bufferCount == elev.capacity:
                continue

            if minElev is None:
                minElev = elevatorFunc

            diff = findMinDiff(
                elevator=elevatorFunc,
                floor_no=data["floors"][i],
                bufferCount=bufferCount,
                min=minDiff,
                openReq=openReq
            )

            if diff < minDiff:
                minDiff = diff
                minElev = elevatorFunc
                buffCount = bufferCount

        if not found:
            print("not found")
            print("buffCount: ", str(buffCount))
            print("minElev : ", str(minElev))
            # if buffCount == minElev.elevator.capacity or minElev.curr_req_count == minElev.elevator.requestsCapacity:
                # print("in buffCount")
                # minElev = None

            peopleCount, req = forRequestToElevator(
                elevatorFunc=minElev,
                floor_no=data["floors"][i],
                people_count=data["PeoplePerFloor"][i],
                status=status,
                bufferCount=buffCount,
            )

            if req is not None:
                list_req.append(req)

            if peopleCount != 0:
                data["PeoplePerFloor"][i] = peopleCount
                isReqFullFill = False
            else:
                i += 1
                req_added += 1

        if req_added == length:
            break

    return list_req


def get_AllForRequests(elevator, status):
    return ElevatorForRequests.objects.filter(
        elevator=elevator,
        status=status,
    )
