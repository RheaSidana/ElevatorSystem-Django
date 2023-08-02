from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *
from .service import *

# Create your views here.


class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def create(self, request):
        no_of_floors = request.data.get("total_floors")

        if no_of_floors == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for no_of_floors. Must be an integer.",
            }, status=status.HTTP_400_BAD_REQUEST)

        create_floor(no=no_of_floors)
        serializer = FloorSerializer(self.queryset, many=True)

        return Response({
            "status": 200,
            "Floors": serializer.data
        })


class ElevatorFunctionalityViewSet(viewsets.ModelViewSet):
    queryset = ElevatorFunctionality.objects.all().order_by("id")
    serializer_class = ElevatorFunctionalitySerializer

    def create(self, request):
        no_of_elevators = request.data.get("total_elevators")
        data = request.data

        if no_of_elevators == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for no_of_elevators. Must be an integer.",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            create_elevators(data)
            serializer = ElevatorFunctionalitySerializer(
                self.queryset, many=True)
        except Exception as ex:
            return Response({
                "status": 500,
                "message": "Internal Server Error, while accessing the DB.",
                "error": ex,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": 201,
            "Elevators": serializer.data
        }, status=status.HTTP_201_CREATED)


class RequestForElevatorViewSet(viewsets.ModelViewSet):
    queryset = ElevatorForRequests.objects.all()
    serializer_class = ElevatorForRequestsSerializer

    """
    requestbody = {
        "floors": ["FL_2", "FL_4"],
        "PeoplePerFloor": [3, 4],
    }
    """

    def create(self, request):
        data = request.data

        if data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator_request. "+
                "Must be floors and people per floor.",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            create_forRequest(data=data)
            serializer = ElevatorForRequestsSerializer(
                self.queryset, many=True)
        except Exception as ex:
            return Response({
                "status": 500,
                "message": "Internal Server Error, while accessing the DB.",
                "error": ex,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": 201,
            "Requests": serializer.data
        }, status=status.HTTP_201_CREATED)


class AllRequestsForElevatorViewSet(viewsets.ModelViewSet):
    queryset = ElevatorForRequests.objects.all()
    serializer_class = ElevatorForRequestsSerializer

    def list(self, request):
        data = request.data

        if data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator's_requests_list. " +
                            "Must be elevator and date.",
                            }, status=status.HTTP_400_BAD_REQUEST)

        try:

            """
            requestBody = {
                "elevator" : "EL_3",
                "date": "2023-08-1"
            }
            """
            reqList = list_forRequests(data)
            if not reqList:
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

        serializer = ElevatorForRequestsSerializer(
            reqList, many=True
        )
        return Response({
            "status": 200,
            "Requests": serializer.data
        }, status=status.HTTP_200_OK)


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


class RequestFromElevatorViewSet(viewsets.ModelViewSet):
    queryset = ElevatorFromRequests.objects.all()
    serializer_class = ElevatorFromRequestsSerializer

    """
    requestbody = {
        "from_floors": ["FL_2", "FL_4"],
        "elevators": ["EL_", "EL_"],
        "to_floors": [
            ["FL_1", "FL_5"],
            ["FL_1"]
        ]
    }
    """

    def create(self, request):
        data = request.data

        if data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator_request. "+
                "Must be elevator, from floor and list of to floors.",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            list_fromReq = create_fromRequest(data=data)
            serializer = ElevatorFromRequestsSerializer(
                list_fromReq, many=True)
        except Exception as ex:

            return Response({
                "status": 500,
                "message": "Internal Server Error, while accessing the DB.",
                "error": str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": 200,
            "Requests": serializer.data
        }, status=status.HTTP_200_OK)


class AllRequestsFromElevatorViewSet(viewsets.ModelViewSet):
    queryset = ElevatorFromRequests.objects.all()
    serializer_class = ElevatorFromRequestsSerializer

    def list(self, request):
        data = request.data

        if data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator's_requests_list. "+
                "Must be elevator and date.",
                            }, status=status.HTTP_400_BAD_REQUEST)

        try:

            """
            requestBody = {
                "elevator" : "EL_3",
                "date": "2023-08-1"
            }
            """
            reqList = list_fromRequests(data)
            if not reqList:
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

        serializer = ElevatorFromRequestsSerializer(
            reqList, many=True
        )
        return Response({
            "status": 200,
            "Requests": serializer.data
        }, status=status.HTTP_200_OK)


class ElevatorNextDestinationViewSet(viewsets.ModelViewSet):
    # queryset = ElevatorFromRequests.objects.all()
    # serializer_class = ElevatorFromRequestsSerializer

    def list(self, request):
        data = request.data

        if data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator's_requests_list. "+
                "Must be elevator.",
                            }, status=status.HTTP_400_BAD_REQUEST)

        try:

            """
            requestBody = {
                "elevator" : "EL_3",
            }
            """
            reqList = list_nextDestination(data)
            if not reqList:
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

        serializer = ElevatorNextDestinationSerializer(
            reqList, many=False
        )
        return Response({
            "status": 200,
            "Requests": serializer.data
        }, status=status.HTTP_200_OK)
