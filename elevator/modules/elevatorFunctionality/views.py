from rest_framework import viewsets, status
from rest_framework.response import Response
from ...models.models import ElevatorFunctionality
from ...serializers import ElevatorFunctionalityMovingSerializer, ElevatorFunctionalityOperationalSerializer, ElevatorFunctionalityDoorSerializer
from .service import list_elevFuncMoving, create_elevFuncOperational, create_elevFuncDoor

class ElevatorFunctionalityMovingViewSet(viewsets.ModelViewSet):
    queryset = ElevatorFunctionality.objects.all().order_by("id")
    serializer_class = ElevatorFunctionalityMovingSerializer

    def list(self, request):
        data = request.data

        if data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator's_requests_list. " +
                            "Must be a elevator.",
                            }, status=status.HTTP_400_BAD_REQUEST)

        """
            requestBody = {
                "elevator": "EL_3"
            }
        """
        try:
            eleFunc = list_elevFuncMoving(data)
            if not eleFunc:
                return Response({
                    "status": 404,
                    "message": "Data not Found",
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                "status": 500,
                "message": "Internal Server Error, while accessing the DB.",
                "error": str(ex),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ElevatorFunctionalityMovingSerializer(eleFunc)
        return Response({
            "status": 200,
            "Requests": serializer.data
        }, status=status.HTTP_200_OK)

class ElevatorFunctionalityOperationalViewSet(viewsets.ModelViewSet):
    queryset = ElevatorFunctionality.objects.all().order_by("id")
    serializer_class = ElevatorFunctionalityOperationalSerializer

    def create(self, request):
        data = request.data

        if data is {}:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator's_requests_list. " +
                            "Must be elevator and status.",
                            }, status=status.HTTP_400_BAD_REQUEST)

        """
            requestBody = {
                "elevator": "EL_3",
                "status": "Maintainence"
            }
        """
        try:
            eleFunc = create_elevFuncOperational(data)
            if not eleFunc:
                return Response({
                    "status": 404,
                    "message": "Data not Found",
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                "status": 500,
                "message": "Internal Server Error, while accessing the DB.",
                "error": str(ex),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ElevatorFunctionalityOperationalSerializer(eleFunc)
        return Response({
            "status": 200,
            "Requests": serializer.data
        }, status=status.HTTP_200_OK)

class ElevatorFunctionalityDoorViewSet(viewsets.ModelViewSet):
    queryset = ElevatorFunctionality.objects.all().order_by("id")
    serializer_class = ElevatorFunctionalityDoorSerializer

    def create(self, request):
        data = request.data

        if data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator's_requests_list. " +
                            "Must be elevator and action.",
                            }, status=status.HTTP_400_BAD_REQUEST)

        """
            requestBody = {
                "elevator": "EL_3",
                "action": "Open"
            }
        """
        try:
            eleFunc = create_elevFuncDoor(data)
            if not eleFunc:
                return Response({
                    "status": 404,
                    "message": "Data not Found",
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                "status": 500,
                "message": "Internal Server Error, while accessing the DB.",
                "error": str(ex),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ElevatorFunctionalityDoorSerializer(eleFunc)
        return Response({
            "status": 201,
            "Elevator": serializer.data
        }, status=status.HTTP_201_CREATED)

