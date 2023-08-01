from .models import *
import math


def defaut_ElevatorFunctionality(elevator):
    return ElevatorFunctionality.objects.create(
        movement=Movements.objects.get(action="Stop"),
        floor_no=Floor.objects.get(name="FL_1"),
        direction=Moving.objects.get(direction="Stationary"),
        operational_status=Operational_Status.objects.get(value="Working"),
        door_functionality=DoorFunctions.objects.get(name="Close"),
        elevator=elevator,
        curr_req_count=0,
        curr_person_count=0,
    )


def findAllElevators():
    return ElevatorFunctionality.objects.all().order_by("id")

# not in use yet


def findAllOpenForRequest(status, elevator):
    list_elev = ElevatorForRequests.objects.filter(
        # status=status,
        elevator=elevator
    )
    return list_elev

# not in use yet


def findAllOpenFromRequest(status, elevator):
    return ElevatorFromRequests.objects.filter(
        status=status,
        elevator=elevator
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
    print("\nin nearest\n")
    # if ElevatorForRequests.objects.exists():
    #     count = ElevatorForRequests.objects.count() + 1
    # else:
    #     count = 1

    if (elevator.curr_req_count >= elevator.elevator.requestsCapacity):
        return None
    else:
        elev = elevator.elevator
        if (bufferCount == elev.capacity):
            return None
        else:
            print("dfhdjfnhdf")
            print("elev: " + elev.name)
            print("openReq: " + str(len(openReq)))
            if not openReq or (openReq and len(openReq) < elev.requestsCapacity):
                floorNo_req = int(floor_no.split("_")[1])
                floorNo_elev = int(elevator.floor_no.name.split("_")[1])
                print("elevator floor: " + elevator.floor_no.name)
                print(floorNo_elev)
                print("req floor: " + floor_no)
                print(floorNo_req)
                print("diff: " + str(abs(floorNo_req-floorNo_elev)))
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
    
    print("req count" + str(count))

    if (elevator.curr_req_count >= elevator.elevator.requestsCapacity):
        bufferCount = 0
        print("in cap")
        return people_count, bufferCount
    else:
        print("is cap"  )
        elev = elevator.elevator
        if (bufferCount == elevator.elevator.capacity):
            bufferCount = 0
            print("in people")
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
            # print("in <=")
            people_count = 0

        else:
            add = (elev.capacity-bufferCount)
            print("cap-bufferCount")
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
    i=0
    expr = i < len(data["floors"])-1
    while expr:
    # range(0, len(data["floors"])):
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

        print("People Count: "+ str(peopleCount))
        print("i: "+ str(i))
        if peopleCount != 0:
            data["PeoplePerFloor"][i] = peopleCount
        else: 
            i += 1
