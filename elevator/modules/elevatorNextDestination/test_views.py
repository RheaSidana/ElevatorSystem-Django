from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import ElevatorNextDestinationViewSet
from unittest.mock import patch, PropertyMock
from rest_framework import status

class ElevatorNextDestinationViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list_whenRequestBodyIsEmpty(self):
        data = {}
        request = self.factory.post('/ElevatorNextDestination/', data)
        view = ElevatorNextDestinationViewSet.as_view({'post': 'list'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("elevator.modules.elevator.views.list_nextDestination")
    def test_list_whenDataNotFound(self, mock_list_nextDestination):
        data = {
            "elevator": "EL_3",
        }
        request = self.factory.post('/ElevatorNextDestination/', data)
        view = ElevatorNextDestinationViewSet.as_view({'post': 'list'})
        mock_list_nextDestination.return_value = None

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    @patch("elevator.modules.elevator.views.list_nextDestination")
    def test_list_whenDBError(self, mock_list_nextDestination):
        data = {
            "elevator": "EL_3",
        }
        request = self.factory.post('/ElevatorNextDestination/', data)
        view = ElevatorNextDestinationViewSet.as_view({'post': 'list'})
        mock_list_nextDestination.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("elevator.modules.elevator.views.list_nextDestination")
    @patch("elevator.modules.elevator.views.ElevatorNextDestinationSerializer")
    def test_list(self, mock_ElevatorNextDestinationSerializer, mock_list_nextDestination):
        data = {
            "elevator": "EL_3",
        }
        request = self.factory.post('/ElevatorNextDestination/', data)
        view = ElevatorNextDestinationViewSet.as_view({'post': 'list'})
        expectedResponse = {
            "status": 200,
            "Elevator": {
                "elevator_name": "EL_3",
                "current_floor": "FL_1",
                "next_floor": "",
                "next_direction": "Stationary",
                "moving_direction1": "Up",
                "floor_names1": [],
                "moving_direction2": "Down",
                "floor_names2": []
            }
        }
        mock_list_nextDestination.return_value = expectedResponse["Elevator"]
        type(mock_ElevatorNextDestinationSerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Elevator"]
        )

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedResponse)