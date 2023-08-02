from django.urls import path
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Floors', FloorViewSet, basename="Floors")
router.register(r'Elevators', ElevatorFunctionalityViewSet,
                basename="Elevators")
router.register(r'ElevatorForRequest', RequestForElevatorViewSet,
                basename="ElevatorForRequest")
router.register(r'AllElevatorForRequest',
                AllRequestsForElevatorViewSet, basename="AllElevatorForRequest")
router.register(r'ElevatorMoving',
                ElevatorFunctionalityMovingViewSet, basename="ElevatorMoving")
router.register(r'ElevatorOperation',
                ElevatorFunctionalityOperationalViewSet, basename="ElevatorOperation")
router.register(r'ElevatorDoor',
                ElevatorFunctionalityDoorViewSet, basename="ElevatorDoor")
router.register(r'ElevatorFromRequest',
                RequestFromElevatorViewSet, basename="ElevatorFromRequest")
router.register(r'ElevatorAllFromRequest',
                AllRequestsFromElevatorViewSet, basename="ElevatorAllFromRequest")
router.register(r'ElevatorNextDestination',
                ElevatorNextDestinationViewSet, basename="ElevatorNextDestination")

urlpatterns = [
]+router.urls
