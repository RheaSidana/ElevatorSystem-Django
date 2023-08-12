from django.test import TestCase
from unittest.mock import patch
from .service import create_for_request, list_forRequests, ElevatorForRequests
# from ....elevator.modules.elevatorForRequests.service

class ElevatorForRequestServiceTestCase(TestCase):
    @patch("elevator.modules.elevatorForRequests.service.get_elevator_request_status_is_open")
    @patch("elevator.modules.elevatorForRequests.service.get_all_elevator_functionality")
    @patch("elevator.modules.elevatorForRequests.service.return_for_request_if_elevator_already_has_from_requests")
    @patch("elevator.modules.elevatorForRequests.service.create_for_request_to_the_nearest_elevator_possible")
    def test_create_for_request(
        self, 
        mock_create_nearest_elevator, 
        mock_return_for_requests,
        mock_get_all_elevator_func, 
        mock_get_request_status
    ):

        data = {"floors": ["EL_1"]} 
        elevator_for_requests_when_elevator_already_has_from_requests = []
        elevator_for_requests_nearest_elevator = ["Assigned: El_1"]
        
        mock_get_request_status.return_value = "Open"
        mock_get_all_elevator_func.return_value = ["elevator_func1", "elevator_func2"]
        mock_return_for_requests.return_value = (
            data, elevator_for_requests_when_elevator_already_has_from_requests
        )
        mock_create_nearest_elevator.return_value = elevator_for_requests_nearest_elevator

        result = create_for_request(data)

        self.assertEqual(result, elevator_for_requests_nearest_elevator)  
        
    @patch("elevator.modules.elevatorForRequests.service.get_elevator_request_status_is_open")
    @patch("elevator.modules.elevatorForRequests.service.get_all_elevator_functionality")
    @patch("elevator.modules.elevatorForRequests.service.return_for_request_if_elevator_already_has_from_requests")
    def test_create_for_request_found_in_from_requests(
        self, 
        mock_return_for_requests,
        mock_get_all_elevator_func, 
        mock_get_request_status
    ):

        data = {"floors": ["EL_1"]} 
        elevator_for_requests_when_elevator_already_has_from_requests = ["Assigned: El_1"]
        
        mock_get_request_status.return_value = "Open"
        mock_get_all_elevator_func.return_value = ["elevator_func1", "elevator_func2"]
        mock_return_for_requests.return_value = (
            {}, elevator_for_requests_when_elevator_already_has_from_requests
        )

        result = create_for_request(data)

        self.assertEqual(result, elevator_for_requests_when_elevator_already_has_from_requests)  

    @patch("elevator.modules.elevatorForRequests.service.get_Elevator")
    @patch("elevator.modules.elevatorForRequests.service.calculate_date")
    @patch("elevator.modules.elevatorForRequests.service.requests_list")
    def test_list_forRequests(
        self, 
        mock_requests_list, 
        mock_calculate_date, 
        mock_get_Elevator
    ):
        #arrange
        data = {
            "elevator": "EL_1",
            "date": "2023-07-30"
        }
        of_date = "2023-07-30"
        next_date= "2023-07-31"
        requests_list = ["FL_2: EL_3"]
        elevator = "EL_1"
        
        mock_get_Elevator.return_value = elevator
        mock_calculate_date.return_value = (
            of_date, next_date
        )
        mock_requests_list.return_value = requests_list
        
        #act
        result = list_forRequests(data)

        #assert
        mock_get_Elevator.assert_called_once_with(elevator=elevator)
        mock_calculate_date.assert_called_once_with(convertFrom=of_date)
        mock_requests_list.assert_called_once_with(
            model=ElevatorForRequests,
            elevator=elevator,
            of_date=of_date,
            next_date=next_date
        )

        self.assertEqual(result, requests_list)

    