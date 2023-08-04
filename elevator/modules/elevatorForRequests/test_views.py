from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import RequestForElevatorViewSet, AllRequestsForElevatorViewSet
from unittest.mock import patch, PropertyMock


class RequestForElevatorViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_whenRequestBodyIsEmpty(self):
        data = {}
        request = self.factory.post('/ElevatorForRequest/', data)
        view = RequestForElevatorViewSet.as_view({'post': 'create'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("elevator.modules.elevatorForRequests.views.create_forRequest")
    def test_create_whenDBError(self, mock_create_forRequest):
        data = {
            "floors": ["FL_2", "FL_4"],
            "PeoplePerFloor": [3, 4],
        }
        request = self.factory.post('/ElevatorForRequest/', data)
        view = RequestForElevatorViewSet.as_view({'post': 'create'})
        mock_create_forRequest.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("elevator.modules.elevatorForRequests.views.create_forRequest")
    @patch("elevator.modules.elevatorForRequests.views.ElevatorForRequestsSerializer")
    def test_create(self, mock_ElevatorForRequestsSerializer, mock_create_forRequest):
        data = {
            "floors": ["FL_2", "FL_4"],
            "PeoplePerFloor": [3, 4],
        }
        request = self.factory.post('/ElevatorForRequest/', data)
        view = RequestForElevatorViewSet.as_view({'post': 'create'})
        expectedResponse = {
            "status": 201,
            "Requests": [
                {
                    "reqID": "REQ_1",
                    "reqTime": "2023-08-01T12:00:00Z",
                    "floor_id": "FL_1",
                    "status": "open",
                    "elevator": "EL_1",
                    "count_of_people": 3
                },
                {
                    "reqID": "REQ_2",
                    "reqTime": "2023-08-01T12:05:00Z",
                    "floor_id": "FL_4",
                    "status": "closed",
                    "elevator": "EL_2",
                    "count_of_people": 4
                },
            ]
        }
        mock_create_forRequest.return_value = expectedResponse["Requests"]
        type(mock_ElevatorForRequestsSerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Requests"]
        )

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expectedResponse)


class AllRequestsForElevatorViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list_whenRequestBodyIsEmpty(self):
        data = {}
        request = self.factory.post('/AllElevatorForRequest/', data)
        view = AllRequestsForElevatorViewSet.as_view({'post': 'list'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("elevator.modules.elevatorForRequests.views.list_forRequests")
    def test_list_whenDataNotFound(self, mock_list_forRequests):
        data = {
            "elevator": "EL_3",
            "date": "2023-08-1"
        }
        request = self.factory.post('/AllElevatorForRequest/', data)
        view = AllRequestsForElevatorViewSet.as_view({'post': 'list'})
        mock_list_forRequests.return_value = None

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("elevator.modules.elevatorForRequests.views.list_forRequests")
    def test_list_whenDBError(self, mock_list_forRequests):
        data = {
            "elevator": "EL_3",
            "date": "2023-08-1"
        }
        request = self.factory.post('/AllElevatorForRequest/', data)
        view = AllRequestsForElevatorViewSet.as_view({'post': 'list'})
        mock_list_forRequests.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("elevator.modules.elevatorForRequests.views.list_forRequests")
    @patch("elevator.modules.elevatorForRequests.views.ElevatorForRequestsSerializer")
    def test_list(self, mock_ElevatorForRequestsSerializer, mock_list_forRequests):
        data = {
            "elevator": "EL_3",
            "date": "2023-08-1"
        }
        request = self.factory.post('/AllElevatorForRequest/', data)
        view = AllRequestsForElevatorViewSet.as_view({'post': 'list'})
        expectedResponse = {
            "status": 200,
            "Requests": [
                {
            "reqID": "REQ_3",
            "reqTime": "2023-08-01T12:10:00Z",
            "floor_id": "FL_2",
            "status": "PENDING",
            "elevator": "EL_3",
            "count_of_people": 2
        },
        {
            "reqID": "REQ_4",
            "reqTime": "2023-08-01T12:15:00Z",
            "floor_id": "FL_4",
            "status": "FULFILLED",
            "elevator": "EL_3",
            "count_of_people": 3
        }
            ]
        }
        mock_list_forRequests.return_value = expectedResponse["Requests"]
        type(mock_ElevatorForRequestsSerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Requests"]
        )

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedResponse)