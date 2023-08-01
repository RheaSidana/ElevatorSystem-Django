from django.urls import path
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movements', DataSeedingViewsMovement,basename="movements")
router.register(r'doors', DataSeedingViewsDoor,basename="doors")
router.register(r'moving', DataSeedingViewsMoving,basename="moving")
router.register(r'operational_status', DataSeedingViewsOperational_Status,basename="operational_status")
# router.register(r'elevator_request_type', DataSeedingViewsElevatorRequestType,basename="elevator_request_type")
router.register(r'elevator_request_status', DataSeedingViewsElevatorRequestStatus,basename="elevator_request_status")

urlpatterns = [
    # path('', MovementsListCreateView.as_view()),
]+router.urls
