from .models.models import *
from .modules.functionality import *


def findAllOpenForRequest(status, elevator):
    return get_ElevatorForRequests(status=status,elevator=elevator) 


def findAllOpenFromRequestFloor(status, elevator, to_floor):
    return ElevatorFromRequests.objects.filter(
        status=status,
        elevator=elevator,
        to_floor=to_floor
    )


def findAllOpenFromRequest(status, elevator):
    return ElevatorFromRequests.objects.filter(
        status=status,
        elevator=elevator,
    )


def is_allAtTheSameFloor(list_of_elevator):
    floor = list_of_elevator[0].floor_no
    for elev in list_of_elevator:
        if floor != elev.floor_no:
            return False
    return True


def forRequest(elevator, floor_no, people_count, status, bufferCount):
    if ElevatorForRequests.objects.exists():
        count = ElevatorForRequests.objects.count() + 1
    else:
        count = 1

    if (elevator.curr_req_count >= elevator.elevator.requestsCapacity):
        bufferCount = 0
        return people_count, bufferCount
    else:
        elev = elevator.elevator
        if (bufferCount == elevator.elevator.capacity):
            bufferCount = 0
            return people_count, bufferCount
        else:
            floor = Floor.objects.get(name=floor_no)
            req_id = "FR_" + str(count)
            forReq = ElevatorForRequests.objects.create(
                reqID=req_id,
                floor_id=floor,
                status=status,
                elevator=elev,
                count_of_people=people_count
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

    return people_count, bufferCount


def assignForRequestWhenAllAtSameFloor(list_of_elevators, data, status):
    req_added = 0
    for elev in list_of_elevators:
        bufferCount = 0
        for i in range(0, (len(data["floors"]))):
            if i != req_added:
                continue
            peopleCount, bufferCount = forRequest(
                elevator=elev,
                floor_no=data["floors"][i],
                people_count=data["PeoplePerFloor"][i],
                status=status,
                bufferCount=bufferCount
            )
            if peopleCount == 0:
                req_added += 1
            else:
                data["PeoplePerFloor"][i] = peopleCount
                break
        if req_added == (len(data["floors"])):
            break


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


def cal_peopleCount(reqs):
    count = 0
    if reqs:
        for r in reqs:
            count += r.count_of_people
    return count


def forRequestToElevator(elevator, floor_no, people_count, status, bufferCount):
    if ElevatorForRequests.objects.exists():
        count = ElevatorForRequests.objects.count() + 1
    else:
        count = 1

    if (elevator.curr_req_count >= elevator.elevator.requestsCapacity):
        bufferCount = 0
        return people_count, bufferCount
    else:
        elev = elevator.elevator
        if (bufferCount == elevator.elevator.capacity):
            bufferCount = 0
            return people_count
        else:
            floor = Floor.objects.get(name=floor_no)
            req_id = "FR_" + str(count)
            forReq = ElevatorForRequests.objects.create(
                reqID=req_id,
                floor_id=floor,
                status=status,
                elevator=elev,
                count_of_people=people_count
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
    count = ElevatorFunctionality.objects.count()

    buffCount = 0
    i = 0
    expr = i < len(data["floors"])-1
    while expr:
        minDiff = count
        minElev = None

        for elevator in list_of_elevators:
            elev = elevator.elevator
            openReq = findAllOpenForRequest(
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


def fromRequest(from_floor, elevator, to_floor, status, count_of_people):
    count = ElevatorFromRequests.objects.count()+1
    if count is None:
        count = 1

    req_id = "EFR_"+str(count)

    ElevatorFromRequests.objects.create(
        reqID=req_id,
        from_floor=from_floor,
        to_floor=to_floor,
        status=status,
        elevator=elevator, 
        count_of_people = count_of_people
    )


def assignFromRequest(status, data):
    list_req = []
    elevator = Elevator.objects.get(
        name=data["elevator"]
    )


    elevFunc = ElevatorFunctionality.objects.get(
        elevator=elevator
    )

    if elevFunc.floor_no.name != data["from_floor"]:
        raise Exception(
            "Invalid floor from the request is sent." +
            " The elevator is not on that floor.")

    for fl in data["to_floors"]:
        floor = Floor.objects.get(
            name=fl
        )

        list_fromReq = findAllOpenFromRequestFloor(
            status=status,
            elevator=elevator,
            to_floor=floor
        )
        if not list_fromReq:
            from_floor = Floor.objects.get(
                name=data["from_floor"],
            )
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







def foundInFromRequest(floor_id, status, elevatorFunc, peopleCount, fromReq):
    elev = elevatorFunc.elevator
    if (elevatorFunc.curr_req_count == elev.requestsCapacity):
        return peopleCount
    # curr_person_count = models.IntegerField()
    else:
        if ElevatorForRequests.objects.exists():
            count = ElevatorForRequests.objects.count() + 1
        else:
            count = 1
        floor = Floor.objects.get(name=floor_id)
        req_id = "FR_" + str(count)
        forReq = ElevatorForRequests.objects.create(
            reqID=req_id,
            floor_id=floor,
            status=status,
            elevator=elev,
            count_of_people=peopleCount
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
        list_fromReqs = findAllOpenFromRequest(
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








