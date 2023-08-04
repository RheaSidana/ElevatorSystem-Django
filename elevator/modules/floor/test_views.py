from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from rest_framework.response import Response
from unittest.mock import patch, PropertyMock
from .views import FloorViewSet

class FloorViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_whenNoOfFloorsIsEmpty(self):
        data = {}
        request = self.factory.post('/Floors/', data)
        view = FloorViewSet.as_view({'post': 'create'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

