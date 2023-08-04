from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ...models.models import Floor
from ...serializers import FloorSerializer
from .service import create_floor
from ..redis import *

floarKey = "Floor"

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
        create_cached(key=Floor, data=serializer.data)
        return Response({
            "status": 201,
            "Floors": serializer.data
        }, status=status.HTTP_201_CREATED)

