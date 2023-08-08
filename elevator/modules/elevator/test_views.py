from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import ElevatorFunctionalityViewSet
from unittest.mock import patch, PropertyMock

class ElevatorFunctionalityViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_whenRequestBodyIsEmpty(self):
        data = {}
        request = self.factory.post('/Elevators/', data)
        view = ElevatorFunctionalityViewSet.as_view({'post': 'create'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("elevator.modules.elevator.views.create_elevators")
    def test_create_whenDBError(self, mock_create_elevators):
        data = {
            "total_elevators": 2,
            "capacity": 5
        }
        request = self.factory.post('/Elevators/', data)
        view = ElevatorFunctionalityViewSet.as_view({'post': 'create'})
        mock_create_elevators.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("elevator.modules.elevator.views.create_elevators")
    @patch("elevator.modules.elevator.views.ElevatorFunctionalitySerializer")
    def test_create(self, mock_ElevatorFunctionalitySerializer, mock_create_elevators):
        data = {
            "total_elevators": 2,
            "capacity": 5
        }
        request = self.factory.post('/Elevators/', data)
        view = ElevatorFunctionalityViewSet.as_view({'post': 'create'})
        expectedResponse = {
            "status": 201,
            "Elevators": [
                {
                    "elevator": {
                        "name": "EL_1",
                        "capacity": 5,
                        "requestsCapacity": 8
                    },
                    "floor_name": "FL_1",
                    "movement_action": "Stop",
                    "moving_direction": "Stationary",
                    "operational": "Working",
                    "door_status": "Close",
                    "curr_req_count": 0,
                    "curr_person_count": 0
                },
                {
                    "elevator": {
                        "name": "EL_1",
                        "capacity": 5,
                        "requestsCapacity": 8
                    },
                    "floor_name": "FL_1",
                    "movement_action": "Stop",
                    "moving_direction": "Stationary",
                    "operational": "Working",
                    "door_status": "Close",
                    "curr_req_count": 0,
                    "curr_person_count": 0
                }
            ]
        }
        mock_create_elevators.return_value = expectedResponse["Elevators"]
        type(mock_ElevatorFunctionalitySerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Elevators"]
        )

        response = view(request)

        self.maxDiff = None
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        self.assertEqual(response.data, expectedResponse)
