from rest_framework import viewsets, status
from rest_framework.response import Response
from ...models.models import ElevatorFunctionality
from ...serializers import ElevatorFunctionalitySerializer
from .service import (
    create_elevators,
)
from ...serializer.cacheModelSerialisers.elevatorFunctionality import (
    ElevatorFunctionalitySerializer as ElevFuncSerializerOfCache
)
from ..redis import create_cached_infiniteTimeout, list_cached

elevatorFunctionalityKey = "ElevatorFunctionality"


class ElevatorFunctionalityViewSet(viewsets.ModelViewSet):
    queryset = ElevatorFunctionality.objects.all().order_by("id")
    serializer_class = ElevatorFunctionalitySerializer

    def create(self, request):
        # no_of_elevators = request.data.get("total_elevators")
        data = request.data

        if data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for no_of_elevators. Must be an integer.",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            create_elevators(data)
            serializer = ElevatorFunctionalitySerializer(
                self.queryset, many=True)
            create_cached_infiniteTimeout(
                key=elevatorFunctionalityKey, data=serializer.data)
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

    def list(self, request):
        data = list_cached(elevatorFunctionalityKey)

        if data:
            serializer = ElevFuncSerializerOfCache(data, many=True)
            return Response({
                "status": 200,
                "Elevators": serializer.data
            }, status=status.HTTP_200_OK)

        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = ElevatorFunctionalitySerializer(queryset, many=True)
            create_cached_infiniteTimeout(
                key=elevatorFunctionalityKey, data=serializer.data)
        except Exception as ex:
            return Response({
                "status": 500,
                "message": "Internal Server Error, while accessing the DB.",
                "error": ex,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": 200,
            "Elevators": serializer.data
        }, status=status.HTTP_200_OK)
