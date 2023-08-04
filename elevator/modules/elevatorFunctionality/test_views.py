from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from rest_framework.response import Response
from unittest.mock import patch, PropertyMock
from ...views import (
    ElevatorFunctionalityMovingViewSet,
    ElevatorFunctionalityOperationalViewSet,
    ElevatorFunctionalityDoorViewSet,
)

class ElevatorFunctionalityMovingViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list_whenRequestBodyIsEmpty(self):
        data = {}
        request = self.factory.post('/ElevatorMoving/', data)
        view = ElevatorFunctionalityMovingViewSet.as_view({'post': 'list'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("elevator.modules.elevatorFunctionality.views.list_elevFuncMoving")
    def test_list_whenDataNotFound(self, mock_list_elevFuncMoving):
        data = {"elevator": "EL_3"}
        request = self.factory.post('/ElevatorMoving/', data)
        view = ElevatorFunctionalityMovingViewSet.as_view({'post': 'list'})
        mock_list_elevFuncMoving.return_value = None

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("elevator.modules.elevatorFunctionality.views.list_elevFuncMoving")
    @patch("elevator.modules.elevatorFunctionality.views.ElevatorFunctionalityMovingSerializer")
    def test_list(self, mock_ElevatorFunctionalityMovingSerializer, mock_list_elevFuncMoving):
        data = {"elevator": "EL_3"}
        request = self.factory.post('/ElevatorMoving/', data)
        view = ElevatorFunctionalityMovingViewSet.as_view({'post': 'list'})
        expectedResponse = {
            "status": 200,
            "Requests": {
                "elevator_name": "EL_3",
                "moving_direction": "Up",
            },
        }
        mock_list_elevFuncMoving.return_value = expectedResponse["Requests"]
        type(mock_ElevatorFunctionalityMovingSerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Requests"]
        )

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedResponse)

    @patch("elevator.modules.elevatorFunctionality.views.list_elevFuncMoving")
    def test_list_whenDataNotFound(self, mock_list_elevFuncMoving):
        data = {"elevator": "EL_3"}
        request = self.factory.post('/ElevatorMoving/', data)
        view = ElevatorFunctionalityMovingViewSet.as_view({'post': 'list'})
        mock_list_elevFuncMoving.return_value = None

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ElevatorFunctionalityOperationalViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_whenRequestBodyIsEmpty(self):
        data = {}
        request = self.factory.post('/ElevatorOperation/', data)
        view = ElevatorFunctionalityOperationalViewSet.as_view({'post': 'create'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("elevator.modules.elevatorFunctionality.views.create_elevFuncOperational")
    def test_create_whenDataNotFound(self, mock_create_elevFuncOperational):
        data = {"elevator": "EL_3", "status": "Maintenance"}
        request = self.factory.post('/ElevatorOperation/', data)
        view = ElevatorFunctionalityOperationalViewSet.as_view({'post': 'create'})
        mock_create_elevFuncOperational.return_value = None

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("elevator.modules.elevatorFunctionality.views.create_elevFuncOperational")
    @patch("elevator.modules.elevatorFunctionality.views.ElevatorFunctionalityOperationalSerializer")
    def test_create(self, mock_ElevatorFunctionalityOperationalSerializer, mock_create_elevFuncOperational):
        data = {"elevator": "EL_3", "status": "Maintenance"}
        request = self.factory.post('/ElevatorOperation/', data)
        view = ElevatorFunctionalityOperationalViewSet.as_view({'post': 'create'})
        expectedResponse = {
            "status": 200,
            "Requests": {
                "elevator_name": "EL_3",
                "operational": "Maintenance",
            },
        }
        mock_create_elevFuncOperational.return_value = expectedResponse["Requests"]
        type(mock_ElevatorFunctionalityOperationalSerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Requests"]
        )

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expectedResponse)

    @patch("elevator.modules.elevatorFunctionality.views.create_elevFuncOperational")
    def test_create_whenDBError(self, mock_create_elevFuncOperational):
        data = {"elevator": "EL_3", "status": "Maintenance"}
        request = self.factory.post('/ElevatorOperation/', data)
        view = ElevatorFunctionalityOperationalViewSet.as_view({'post': 'create'})
        mock_create_elevFuncOperational.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

class ElevatorFunctionalityDoorViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_whenRequestBodyIsEmpty(self):
        data = {}
        request = self.factory.post('/ElevatorDoor/', data)
        view = ElevatorFunctionalityDoorViewSet.as_view({'post': 'create'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("elevator.modules.elevatorFunctionality.views.create_elevFuncDoor")
    def test_create_whenDataNotFound(self, mock_create_elevFuncDoor):
        data = {"elevator": "EL_3", "action": "Open"}
        request = self.factory.post('/ElevatorDoor/', data)
        view = ElevatorFunctionalityDoorViewSet.as_view({'post': 'create'})
        mock_create_elevFuncDoor.return_value = None

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("elevator.modules.elevatorFunctionality.views.create_elevFuncDoor")
    def test_create_whenDBError(self, mock_create_elevFuncDoor):
        data = {"elevator": "EL_3", "action": "Open"}
        request = self.factory.post('/ElevatorDoor/', data)
        view = ElevatorFunctionalityDoorViewSet.as_view({'post': 'create'})
        mock_create_elevFuncDoor.side_effect = Exception("Database error")

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch("elevator.modules.elevatorFunctionality.views.create_elevFuncDoor")
    @patch("elevator.modules.elevatorFunctionality.views.ElevatorFunctionalityDoorSerializer")
    def test_create(self, mock_ElevatorFunctionalityDoorSerializer, mock_create_elevFuncDoor):
        data = {"elevator": "EL_3", "action": "Open"}
        request = self.factory.post('/ElevatorDoor/', data)
        view = ElevatorFunctionalityDoorViewSet.as_view({'post': 'create'})
        expectedResponse = {
            "status": 201,
            "Elevator": {
                "elevator_name": "EL_3",
                "door_status": "Open"
            }
        }
        mock_create_elevFuncDoor.return_value = expectedResponse["Elevator"]
        type(mock_ElevatorFunctionalityDoorSerializer.return_value).data = PropertyMock(
            return_value=expectedResponse["Elevator"]
        )

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expectedResponse)

