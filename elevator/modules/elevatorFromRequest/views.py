from rest_framework import viewsets, status
from rest_framework.response import Response
from ...models.models import ElevatorFromRequests
from ...serializers import ElevatorFromRequestsSerializer
from .service import create_fromRequest, list_fromRequests

class RequestFromElevatorViewSet(viewsets.ModelViewSet):
    queryset = ElevatorFromRequests.objects.all()
    serializer_class = ElevatorFromRequestsSerializer

    """
    requestbody = {
        "from_floors": "FL_2",
        "elevators": "EL_1",
        "to_floors": [
            "FL_1", "FL_5"
        ],
        "PeoplePerFloor": [
            2,1
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


class AllRequestsFromElevatorViewSet(viewsets.ReadOnlyModelViewSet):
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

