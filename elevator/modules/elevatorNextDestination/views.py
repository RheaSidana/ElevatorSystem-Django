from rest_framework import viewsets, status
from rest_framework.response import Response
from ...serializers import ElevatorNextDestinationSerializer
from .service import list_nextDestination

class ElevatorNextDestinationViewSet(viewsets.ModelViewSet):

    def list(self, request):
        data = request.data

        if data == {}:
            return Response({
                "status": 400,
                "message": "Invalid value for elevator's_requests_list. " +
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
            "Elevator": serializer.data
        }, status=status.HTTP_200_OK)
