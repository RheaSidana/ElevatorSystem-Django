from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from .views import FulFillElevatorNextRequestsViewSet
from unittest.mock import patch, PropertyMock
from rest_framework import status

class FullFilElevatorNextRequestsViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list_whenDataNotFound(self):
        request = self.factory.get('/FullFilElevatorNextRequests/')
        view = FulFillElevatorNextRequestsViewSet.as_view({'get': 'list'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    @patch("elevator.modules.fulFillElevatorsNextRequest.views.list_fulfillElevatorsNextRequest")
    def test_list_whenDBError(self, mock_list_fullfilElevatorNextRequest):
        request = self.factory.get('/FullFilElevatorNextRequests/')
        view = FulFillElevatorNextRequestsViewSet.as_view({'get': 'list'})
        mock_list_fullfilElevatorNextRequest.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("elevator.modules.fulFillElevatorsNextRequest.views.list_fulfillElevatorsNextRequest")
    @patch("elevator.modules.fulFillElevatorsNextRequest.views.FulFillElevatorNextRequestsViewSet")
    def test_list(self, mock_FullFilElevatorNextRequestsSerializer, mock_list_fullfilElevatorNextRequest):
        expectedResponse = {
            "status": 200,
            "Requests": [
                {
                    "elevator_name": "EL_1",
                    "current_floor": "FL_1",
                    "fulfilled_floor": None,
                    "steps": [
                        "Movement: Stop",
                        "Moving: Stationary",
                        "From floor: FL_1",
                        "Door : Close"
                    ]
                },
                {
                    "elevator_name": "EL_2",
                    "current_floor": "FL_1",
                    "fulfilled_floor": None,
                    "steps": [
                        "Movement: Stop",
                        "Moving: Stationary",
                        "From floor: FL_1",
                        "Door : Close"
                    ]
                }
            ]
        }
        mock_list_fullfilElevatorNextRequest.return_value = expectedResponse["Requests"]
        type(mock_FullFilElevatorNextRequestsSerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Requests"]
        )

        request = self.factory.get('/FullFilElevatorNextRequests/')
        view = FulFillElevatorNextRequestsViewSet.as_view({'get': 'list'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedResponse)

