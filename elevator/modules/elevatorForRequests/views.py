from rest_framework import viewsets, status
from rest_framework.response import Response
from ...models.models import ElevatorForRequests
from ...serializer.modelSerializers.serializers import ElevatorForRequestsSerializer
from .service import create_forRequest, list_forRequests


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
                "message": "Invalid value for elevator_request. " +
                "Must be floors and people per floor.",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            list_req = create_forRequest(data=data)
        except Exception as ex:
            return Response({
                "status": 500,
                "message": "Internal Server Error, while accessing the DB.",
                "error": str(ex),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ElevatorForRequestsSerializer(
            list_req, many=True)
        return Response({
            "status": 201,
            "Requests": serializer.data
        }, status=status.HTTP_201_CREATED)


class AllRequestsForElevatorViewSet(viewsets.ReadOnlyModelViewSet):
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
