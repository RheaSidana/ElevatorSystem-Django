from ...models.models import Floor

def create_floor(no):
    floor = "FL_"
    for i in range(1, no+1):
        val = floor + str(i)
        if not Floor.objects.filter(name=val).exists():
            Floor.objects.create(name=val)