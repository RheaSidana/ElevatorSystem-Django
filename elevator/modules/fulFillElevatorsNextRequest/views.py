from rest_framework import viewsets, status
from rest_framework.response import Response
from .service import list_fulfillElevatorsNextRequest
from ...serializers import FulFillElevatorsNextRequestsSerializer

class FulFillElevatorNextRequestsViewSet(viewsets.ModelViewSet):
    def list(self, request):

        try:
            nextReq = list_fulfillElevatorsNextRequest()

            if not nextReq:
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

        serializer = FulFillElevatorsNextRequestsSerializer(
            nextReq, many=True
        )
        return Response({
            "status": 200,
            "Requests": serializer.data
        }, status=status.HTTP_200_OK)
