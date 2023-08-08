from unittest.mock import Mock, patch, call
from django.test import TestCase
from .service import (
    is_elevator_exists,
    create_elevator_name,
    create_elevator,
    create_elevator_functionality,
    create_elevators
)


class ElevatorTests(TestCase):
    @patch("elevator.modules.elevator.service.Elevator")
    def test_isElevatorExists_whenExists(self, mock_Elevator):
        mock_Elevator.objects.filter.return_value.exists.return_value = True

        elevator_exists = is_elevator_exists(name="elevator")

        self.assertTrue(elevator_exists)

    @patch("elevator.modules.elevator.service.Elevator")
    def test_isElevatorExists_whenDoesNotExists(self, mock_Elevator):
        mock_Elevator.objects.filter.return_value.exists.return_value = False

        elevator_exists = is_elevator_exists(name="elevator")

        self.assertFalse(elevator_exists)

    def test_createElevatorName(self):
        no = 3
        expectedElevatorName = "EL_3"

        elevatorName = create_elevator_name(no=no)

        self.assertEqual(elevatorName, expectedElevatorName)

    @patch("elevator.modules.elevator.service.Elevator.objects.create")
    def test_create_Elevator(self, mock_create):
        name = "EL_1"
        capacity = 10

        create_elevator(name, capacity)

        mock_create.assert_called_once_with(
            name=name,
            capacity=capacity,
            requestsCapacity=8,
        )

    @patch("elevator.modules.elevator.service.ElevatorFunctionality.objects.create")
    @patch("elevator.modules.elevator.service.get_Movements")
    @patch("elevator.modules.elevator.service.get_Floor")
    @patch("elevator.modules.elevator.service.get_Moving")
    @patch("elevator.modules.elevator.service.get_Operational_Status")
    @patch("elevator.modules.elevator.service.get_DoorFunctions")
    def test_create_ElevatorFunctionality(
        self,  mock_get_DoorFunctions, mock_get_Operational_Status,
        mock_get_Moving, mock_get_Floor,
        mock_get_Movements, mock_create
    ):
        elevator = Mock()
        mock_get_Movements.return_value = Mock()
        mock_get_Floor.return_value = Mock()
        mock_get_Moving.return_value = Mock()
        mock_get_Operational_Status.return_value = Mock()
        mock_get_DoorFunctions.return_value = Mock()

        create_elevator_functionality(elevator)

        mock_create.assert_called_once_with(
            movement=mock_get_Movements.return_value,
            floor_no=mock_get_Floor.return_value,
            direction=mock_get_Moving.return_value,
            operational_status=mock_get_Operational_Status.return_value,
            door_functionality=mock_get_DoorFunctions.return_value,
            elevator=elevator,
            curr_req_count=0,
            curr_person_count=0,
        )

    @patch("elevator.modules.elevator.service.get_Elevator_Count")
    @patch("elevator.modules.elevator.service.Elevator.objects.all")
    @patch("elevator.modules.elevator.service.is_elevator_exists")
    @patch("elevator.modules.elevator.service.create_elevator_name")
    @patch("elevator.modules.elevator.service.create_elevator")
    @patch("elevator.modules.elevator.service.create_elevator_functionality")
    def test_create_elevators(self,
                              mock_create_ElevatorFunctionality,
                              mock_create_elevator,
                              mock_create_elevator_name,
                              mock_is_elevator_exists,
                              mock_Elevator_objects_all,
                              mock_get_Elevator_Count
                              ):
        data = {
            "total_elevators": 3,
            "capacity": 10
        }
        mock_get_Elevator_Count.return_value = 0
        mock_create_elevator_name.side_effect = ["EL_1", "EL_2", "EL_3"]
        mock_is_elevator_exists.side_effect = [False, False, False]
        mock_elevator_instances = [Mock(), Mock(), Mock()]
        mock_create_elevator.side_effect = mock_elevator_instances
        mock_create_ElevatorFunctionality.side_effect = [
            Mock(), Mock(), Mock()]

        create_elevators(data)

        mock_create_elevator_name.assert_has_calls([
            call(no=1), call(no=2), call(no=3)
        ])
        mock_is_elevator_exists.assert_has_calls([
            call(name="EL_1"), call(name="EL_2"), call(name="EL_3")
        ])
        mock_create_elevator.assert_has_calls([
            call(name="EL_1", capacity=10),
            call(name="EL_2", capacity=10),
            call(name="EL_3", capacity=10)
        ])
        mock_create_ElevatorFunctionality.assert_has_calls([
            call(elevator=mock_elevator_instances[0]),
            call(elevator=mock_elevator_instances[1]),
            call(elevator=mock_elevator_instances[2])
        ])
