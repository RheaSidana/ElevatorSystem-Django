from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ...models.models import Floor
from ...serializers import FloorSerializer
from .service import create_floor

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

