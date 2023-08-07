from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ...models.models import Floor
from ...serializers import FloorSerializer
from .service import create_floor
from ..redis import *

floorKey = "Floor"

class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def create(self, request):
        no_of_floors = request.data.get("total_floors")

        if request.data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for no_of_floors. Must be an integer.",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            create_floor(no=no_of_floors)
        except Exception as ex:
            return Response({
                "status": 500,
                "message": "Internal Server Error, while accessing the DB.",
                "error": ex,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = FloorSerializer(self.queryset, many=True)
        create_cached_infiniteTimeout(key=Floor, data=serializer.data)
        return Response({
            "status": 201,
            "Floors": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        data = list_cached(floorKey)

        if data:
            serializer = FloorSerializer(
                data, many = True
            )
            return Response({
                "status": 200,
                "Elevators": serializer.data
            }, status=status.HTTP_200_OK)
        
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = FloorSerializer(queryset, many=True)
            create_cached_infiniteTimeout(key=floorKey,data=serializer.data)
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

