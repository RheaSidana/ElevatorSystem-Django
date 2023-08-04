from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from rest_framework.response import Response
from unittest.mock import patch, PropertyMock
from .views import (
    RequestFromElevatorViewSet,
    AllRequestsFromElevatorViewSet
)


class RequestFromElevatorViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_whenRequestBodyIsEmpty(self):
        data = {}
        request = self.factory.post('/ElevatorFromRequest/', data)
        view = RequestFromElevatorViewSet.as_view({'post': 'create'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("elevator.modules.elevatorFromRequest.views.create_fromRequest")
    def test_create_whenDBError(self, mock_create_fromRequest):
        data = {
            "from_floors": "FL_2",
            "elevators": "EL_1",
            "to_floors": ["FL_1", "FL_5"],
            "PeoplePerFloor": [2, 1]
        }
        request = self.factory.post('/ElevatorFromRequest/', data)
        view = RequestFromElevatorViewSet.as_view({'post': 'create'})
        mock_create_fromRequest.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("elevator.modules.elevatorFromRequest.views.create_fromRequest")
    @patch("elevator.modules.elevatorFromRequest.views.ElevatorFromRequestsSerializer")
    def test_create(self, mock_ElevatorFromRequestsSerializer, mock_create_fromRequest):
        data = {
            "from_floors": "FL_2",
            "elevators": "EL_1",
            "to_floors": ["FL_1", "FL_5"],
            "PeoplePerFloor": [2, 1]
        }
        request = self.factory.post('/ElevatorFromRequest/', data)
        view = RequestFromElevatorViewSet.as_view({'post': 'create'})
        expectedResponse = {
            "status": 200,
            "Requests": [
                {
                    "reqID": "REQ_1",
                    "from_floor": "FL_2",
                    "elevator": "EL_1",
                    "to_floor": "FL_1",
                    "count_of_people": 2
                },
                {
                    "reqID": "REQ_2",
                    "from_floor": "FL_2",
                    "elevator": "EL_1",
                    "to_floor": "FL_5",
                    "count_of_people": 1
                }
            ]
        }
        mock_create_fromRequest.return_value = expectedResponse["Requests"]
        type(mock_ElevatorFromRequestsSerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Requests"]
        )

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedResponse)


class AllRequestsFromElevatorViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list_whenRequestBodyIsEmpty(self):
        data = {}
        request = self.factory.post('/AllRequestsFromElevator/', data)
        view = AllRequestsFromElevatorViewSet.as_view({'post': 'list'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("elevator.modules.elevatorFromRequest.views.list_fromRequests")
    def test_list_whenDataNotFound(self, mock_list_fromRequests):
        data = {
            "elevator": "EL_3",
            "date": "2023-08-1"
        }
        request = self.factory.post('/AllRequestsFromElevator/', data)
        view = AllRequestsFromElevatorViewSet.as_view({'post': 'list'})
        mock_list_fromRequests.return_value = None

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("elevator.modules.elevatorFromRequest.views.list_fromRequests")
    def test_list_whenDBError(self, mock_list_fromRequests):
        data = {
            "elevator": "EL_3",
            "date": "2023-08-1"
        }
        request = self.factory.post('/AllRequestsFromElevator/', data)
        view = AllRequestsFromElevatorViewSet.as_view({'post': 'list'})
        mock_list_fromRequests.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("elevator.modules.elevatorFromRequest.views.list_fromRequests")
    @patch("elevator.modules.elevatorFromRequest.views.ElevatorFromRequestsSerializer")
    def test_list(self, mock_ElevatorFromRequestsSerializer, mock_list_fromRequests):
        data = {
            "elevator": "EL_3",
            "date": "2023-08-1"
        }
        request = self.factory.post('/AllRequestsFromElevator/', data)
        view = AllRequestsFromElevatorViewSet.as_view({'post': 'list'})
        expectedResponse = {
            "status": 200,
            "Requests": [
                {
                    "reqID": "REQ_3",
                    "from_floor": "FL_1",
                    "elevator": "EL_3",
                    "to_floor": "FL_2",
                    "count_of_people": 3
                },
                {
                    "reqID": "REQ_4",
                    "from_floor": "FL_2",
                    "elevator": "EL_3",
                    "to_floor": "FL_4",
                    "count_of_people": 2
                }
            ]
        }
        mock_list_fromRequests.return_value = expectedResponse["Requests"]
        type(mock_ElevatorFromRequestsSerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Requests"]
        )

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedResponse)
