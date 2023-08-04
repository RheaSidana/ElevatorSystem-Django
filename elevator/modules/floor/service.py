from ...models.models import Floor

def del_floor():
    Floor.objects.all().delete()

def create_floor(no):
    del_floor()
    floor = "FL_"
    for i in range(1, no+1):
        val = floor + str(i)
        if not Floor.objects.filter(name=val).exists():
            Floor.objects.create(name=val)