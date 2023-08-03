from rest_framework import viewsets, status
from rest_framework.response import Response
from ...models.models import ElevatorFunctionality
from ...serializers import ElevatorFunctionalitySerializer
from ...serializers import ElevatorNextDestinationSerializer
from ...serializers import FullFilElevatorNextRequestsSerializer
from .service import create_elevators, list_nextDestination
from .service import list_fullfilElevatorNextRequest

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

class ElevatorNextDestinationViewSet(viewsets.ModelViewSet):

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

class FullFilElevatorNextRequestsViewSet(viewsets.ModelViewSet):
    
    def list(self, request):

        try:
            nextReq = list_fullfilElevatorNextRequest()

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

        serializer = FullFilElevatorNextRequestsSerializer(
            nextReq, many=True
        )
        return Response({
            "status": 200,
            "Requests": serializer.data
        }, status=status.HTTP_200_OK)
