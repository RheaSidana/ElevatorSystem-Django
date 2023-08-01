from django.urls import path
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Floors', FloorViewSet, basename="floors")
router.register(r'Elevators', ElevatorFunctionalityViewSet,
                basename="elevators")
router.register(r'ForRequest', RequestForElevatorViewSet,
                basename="forRequest")
router.register(r'ElevatorForRequest',
                AllRequestForElevatorViewSet, basename="elevatorForRequest")

urlpatterns = [
]+router.urls
