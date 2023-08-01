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

        if no_of_floors is None:
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
    queryset = ElevatorFunctionality.objects.all()
    serializer_class = ElevatorFunctionalitySerializer

    def create(self, request):
        no_of_elevators = request.data.get("total_elevators")
        data = request.data

        if no_of_elevators is None:
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

        if data is None:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator_request. Must be an integer.",
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
            "Elevators": serializer.data
        }, status=status.HTTP_201_CREATED)


class AllRequestForElevatorViewSet(viewsets.ModelViewSet):
    queryset = ElevatorForRequests.objects.all()
    serializer_class = ElevatorForRequestsSerializer

    def list(self, request):
        data = request.data

        if data is None:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator's_requests_list. " +
                            "Must be an integer.",
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
            "status": 201,
            "Elevators": serializer.data
        }, status=status.HTTP_201_CREATED)
