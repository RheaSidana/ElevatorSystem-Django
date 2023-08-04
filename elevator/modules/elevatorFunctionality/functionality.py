

def is_allAtTheSameFloor(list_of_elevator):
    floor = list_of_elevator[0].floor_no
    for elev in list_of_elevator:
        if floor != elev.floor_no:
            return False
    return True