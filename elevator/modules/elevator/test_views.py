from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import ElevatorFunctionalityViewSet, ElevatorNextDestinationViewSet, FullFilElevatorNextRequestsViewSet
from unittest.mock import patch, PropertyMock
# from ....elevator.modules.elevator.views import ElevatorFunctionalityViewSet


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

class FullFilElevatorNextRequestsViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list_whenDataNotFound(self):
        request = self.factory.get('/FullFilElevatorNextRequests/')
        view = FullFilElevatorNextRequestsViewSet.as_view({'get': 'list'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("elevator.modules.elevator.views.list_fullfilElevatorNextRequest")
    def test_list_whenDBError(self, mock_list_fullfilElevatorNextRequest):
        request = self.factory.get('/FullFilElevatorNextRequests/')
        view = FullFilElevatorNextRequestsViewSet.as_view({'get': 'list'})
        mock_list_fullfilElevatorNextRequest.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("elevator.modules.elevator.views.list_fullfilElevatorNextRequest")
    @patch("elevator.modules.elevator.views.FullFilElevatorNextRequestsSerializer")
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
        view = FullFilElevatorNextRequestsViewSet.as_view({'get': 'list'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedResponse)

