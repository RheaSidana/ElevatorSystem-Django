from rest_framework import viewsets
from .models import *
from .serializers import *
from .management.commands.data import *

class DataSeedingViewsMovement(viewsets.ReadOnlyModelViewSet):
    queryset = Movements.objects.all()
    serializer_class = MovementsSerializer
    
class DataSeedingViewsDoor(viewsets.ReadOnlyModelViewSet):
    queryset = DoorFunctions.objects.all()
    serializer_class = DoorFunctionsSerializer

class DataSeedingViewsMoving(viewsets.ReadOnlyModelViewSet):
    queryset = Moving.objects.all()
    serializer_class = MovingSerializer
    
class DataSeedingViewsOperational_Status(viewsets.ReadOnlyModelViewSet):
    queryset = Operational_Status.objects.all()
    serializer_class = Operational_StatusSerializer
    
    
class DataSeedingViewsElevatorRequestStatus(viewsets.ReadOnlyModelViewSet):
    queryset = ElevatorRequestStatus.objects.all()
    serializer_class = ElevatorRequestStatusSerializer