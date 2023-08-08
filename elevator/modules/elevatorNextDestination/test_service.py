from django.test import TestCase
from unittest.mock import patch
from .service import *
# from ....elevator.modules.elevatorNextDestination.service


class ElevatorNextDestinationTestCase(TestCase):
    @patch("elevator.modules.elevatorNextDestination.service.get_ElevatorForRequests")
    def test_get_requests_floor_ElevatorForRequests(self, mock_get_ElevatorForRequests):
        mock_get_ElevatorForRequests.return_value.values_list.return_value = [
            "FL_1", "FL_2", "FL_3"]

        request_status = "Open"
        elevator = "EL_1"

        result = get_requests_floor(
            ElevatorForRequests, request_status, elevator)

        self.assertEqual(result, ["FL_1", "FL_2", "FL_3"])
        mock_get_ElevatorForRequests.assert_called_once_with(
            status=request_status, elevator=elevator
        )

    @patch("elevator.modules.elevatorNextDestination.service.get_ElevatorFromRequest")
    def test_get_requests_floor_ElevatorFromRequests(self, mock_get_ElevatorFromRequest):
        mock_get_ElevatorFromRequest.return_value.values_list.return_value = [
            "FL_4", "FL_5"]

        request_status = "Closed"
        elevator = "EL_2"

        result = get_requests_floor(
            ElevatorFromRequests, request_status, elevator)

        self.assertEqual(result, ["FL_4", "FL_5"])
        mock_get_ElevatorFromRequest.assert_called_once_with(
            status=request_status, elevator=elevator)

    @patch("elevator.modules.elevatorNextDestination.service.get_requests_floor")
    def test_getElevatorRequests(self, mock_get_requests_floor):
        elevator = "EL_1"
        ElevatorRequestStatus = "Open"
        mock_get_requests_floor.side_effect = [
            ['FL_2', 'FL_3'],
            ['FL_4', 'FL_5']
        ]

        requests = get_elevator_requests(ElevatorRequestStatus, elevator)

        expected_requests = ['FL_2', 'FL_3', 'FL_4', 'FL_5']

        self.assertEqual(requests, expected_requests)


    def test_create_UpAndDownDirectionList(self):
        requestsFloor = ['3', '2', '1']
        currentFloor = '2'
        
        downDirectionList, upDirectionList = create_UpAndDownDirectionList(requestsFloor, currentFloor)

        expected_down_direction_list = ['2', '1']
        expected_up_direction_list = ['3']

        self.assertEqual(downDirectionList, expected_down_direction_list)
        self.assertEqual(upDirectionList, expected_up_direction_list)

    def test_difference_between(self):
        to_floor = "FL_5"
        current_floor = "FL_2"
        
        result = differenceBetween(to_floor, current_floor)
        
        expected_result = 3
        self.assertEqual(result, expected_result)

    @patch("elevator.modules.elevatorNextDestination.service.differenceBetween")
    def test_is_difference_between_less_than_min_difference(self, mock_difference_between):
        mock_difference_between.return_value = 2
        
        to_floor = "FL_5"
        current_floor = "FL_2"
        min_difference = 5
        
        result = is_differenceBetweenLessThanMinDifference(
            toFloor=to_floor, currentFloor=current_floor, minDifference=min_difference
        )
        
        self.assertTrue(result)

    @patch("elevator.modules.elevatorNextDestination.service.get_ElevatorFunctionality")
    @patch("elevator.modules.elevatorNextDestination.service.create_UpAndDownDirectionList")
    @patch("elevator.modules.elevatorNextDestination.service.is_differenceBetweenLessThanMinDifference")
    @patch("elevator.modules.elevatorNextDestination.service.differenceBetween")
    def test_get_next_destination_of(self, mock_difference_between, mock_is_difference, mock_create_list, mock_get_elevator_func):
        elevator_mock = mock_get_elevator_func.return_value
        elevator_mock.name = "EL_1"
        elevator_mock.floor_no.name = "FL_2"
        
        elevators_requests_mock = ['FL_3', 'FL_5']
        mock_create_list.return_value = (['FL_3', 'FL_4'], ['FL_5'])

        mock_is_difference.return_value = True
        mock_difference_between.return_value = 1

        result = getNextDestinationOf(elevator=elevator_mock, elevatorsRequests=elevators_requests_mock)

        expected_result = {
            "elevator_name": "EL_1",
            "current_floor": "FL_2",
            "next_floor": "FL_3",
            "next_direction": "Down",
            "floorsInUpDirection": ['FL_5'],
            "floorsInDownDirection": ['FL_4'],
        }

        self.assertEqual(result, expected_result)

    @patch("elevator.modules.elevatorNextDestination.service.get_Elevator")
    @patch("elevator.modules.elevatorNextDestination.service.getElevatorRequestStatusOpen")
    @patch("elevator.modules.elevatorNextDestination.service.get_elevator_requests")
    @patch("elevator.modules.elevatorNextDestination.service.getNextDestinationOf")
    def test_list_next_destination(self, mock_get_next_dest, mock_get_requests, mock_get_status, mock_get_elevator):
        elevator_mock = mock_get_elevator.return_value
        requests_mock = ['FL_3', 'FL_5']
        obj_mock = {
            "elevator_name": "EL_1",
            "current_floor": "FL_2",
            "next_floor": "FL_3",
            "next_direction": "Down",
            "floorsInUpDirection": ['FL_5'],
            "floorsInDownDirection": ['FL_4'],
        }

        mock_get_elevator.return_value = elevator_mock
        mock_get_status.return_value = "Open"
        mock_get_requests.return_value = requests_mock
        mock_get_next_dest.return_value = obj_mock

        data = {"elevator": "EL_1"}

        result = list_nextDestination(data)

        expected_result = obj_mock

        self.assertEqual(result, expected_result)

    @patch("elevator.modules.elevatorNextDestination.service.get_Elevator")
    @patch("elevator.modules.elevatorNextDestination.service.getElevatorRequestStatusOpen")
    @patch("elevator.modules.elevatorNextDestination.service.get_elevator_requests")
    @patch("elevator.modules.elevatorNextDestination.service.getNextDestinationOf")
    def test_list_next_destination_exception(self, mock_get_next_dest, mock_get_requests, mock_get_status, mock_get_elevator):
        elevator_mock = mock_get_elevator.return_value
        requests_mock = ['FL_3', 'FL_5']

        mock_get_elevator.return_value = elevator_mock
        mock_get_status.return_value = "Open"
        mock_get_requests.return_value = requests_mock
        mock_get_next_dest.side_effect = Exception("Test exception")

        data = {"elevator": "EL_1"}

        with self.assertRaises(Exception) as context:
            list_nextDestination(data)

        self.assertEqual(str(context.exception), "Test exception")
