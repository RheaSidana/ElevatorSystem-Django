from django.test import TestCase
from unittest.mock import patch, call
from .data import *

class DataTestCase(TestCase):

    @patch("dataSeeding.management.commands.data.Movements")
    @patch("dataSeeding.management.commands.data.DoorFunctions")
    @patch("dataSeeding.management.commands.data.Moving")
    @patch("dataSeeding.management.commands.data.Operational_Status")
    def test_delete_all_data(self, mock_Operational_Status, mock_Moving, mock_DoorFunctions, mock_Movements):
        # arrange
        mock_Movements.objects.exists.return_value = True
        mock_Movements.objects.all.delete.return_value = "Deleted"
        mock_DoorFunctions.objects.exists.return_value = True
        mock_DoorFunctions.objects.all.delete.return_value = "Deleted"
        mock_Moving.objects.exists.return_value = True
        mock_Moving.objects.all.delete.return_value = "Deleted"
        mock_Operational_Status.objects.exists.return_value = True
        mock_Operational_Status.objects.all.delete.return_value = "Deleted"

        # act
        deleteAllDataFromAllModels()
        # assert
        self.assertEqual(Movements.objects.count(), 0)
        self.assertEqual(DoorFunctions.objects.count(), 0)
        self.assertEqual(Moving.objects.count(), 0)
        self.assertEqual(Operational_Status.objects.count(), 0)

    @patch("dataSeeding.management.commands.data.Movements")
    @patch("dataSeeding.management.commands.data.DoorFunctions")
    @patch("dataSeeding.management.commands.data.Moving")
    @patch("dataSeeding.management.commands.data.Operational_Status")
    def test_when_no_data_to_delete(self, mock_Operational_Status, mock_Moving, mock_DoorFunctions, mock_Movements):
        # arrange
        mock_Movements.objects.count.return_value = 3
        mock_Movements.objects.exists.return_value = True

        mock_DoorFunctions.objects.exists.return_value = True
        mock_DoorFunctions.objects.count.return_value = 5

        mock_Moving.objects.exists.return_value = False
        mock_Moving.objects.count.return_value = 0

        mock_Operational_Status.objects.exists.return_value = False
        mock_Operational_Status.objects.count.return_value = 0

        mock_Movements.objects.all.delete.return_value = "Deleted"
        # Movements.objects.create(action = "dummy")
        # DoorFunctions.objects.create(name = "dummy")

        print(mock_Movements.objects.count())

        self.assertNotEqual(mock_Movements.objects.count(), 0)
        self.assertNotEqual(mock_DoorFunctions.objects.count(), 0)
        self.assertEqual(mock_Moving.objects.count(), 0)
        self.assertEqual(mock_Operational_Status.objects.count(), 0)

        # act
        deleteAllDataFromAllModels()

        mock_Movements.objects.all.return_value.delete.assert_called_once()
        mock_Movements.objects.count.return_value = 0

        mock_DoorFunctions.objects.all.return_value.delete.assert_called_once()
        mock_DoorFunctions.objects.count.return_value = 0

        mock_Moving.objects.all.return_value.delete.assert_not_called()
        mock_Operational_Status.objects.all.return_value.delete.assert_not_called()

        self.assertEqual(mock_Movements.objects.count(), 0)
        self.assertEqual(mock_DoorFunctions.objects.count(), 0)

    @patch("dataSeeding.management.commands.data.Movements")
    def test_addMovements(self, mock_Movements):
        # arrange
        mock_Movements.objects.filter.return_value.exists.return_value = False

        # act
        addMovements()

        # assert
        calls = [call(action='Start'), call(
            action='Stop'), call(action='Running')]
        mock_Movements.objects.create.assert_has_calls(calls, any_order=True)

    @patch("dataSeeding.management.commands.data.Movements")
    def test_addMovements_when_db_has_data(self, mock_Movements):
        # arrange
        mock_Movements.objects.filter.return_value.exists.return_value = True

        # act
        addMovements()

        # assert
        mock_Movements.objects.create.assert_not_called()

    @patch("dataSeeding.management.commands.data.DoorFunctions")
    def test_addDoorFunction(self, mock_DoorFunctions):
        # arrange
        mock_DoorFunctions.objects.filter.return_value.exists.return_value = False

        # act
        addDoorFunctions()

        # assert
        calls = [call(name='Open'), call(name='Close')]
        mock_DoorFunctions.objects.create.assert_has_calls(
            calls, any_order=True)

    @patch("dataSeeding.management.commands.data.DoorFunctions")
    def test_addDoorFunction_when_db_has_data(self, mock_DoorFunctions):
        # arrange
        mock_DoorFunctions.objects.filter.return_value.exists.return_value = True

        # act
        addDoorFunctions()

        # assert
        mock_DoorFunctions.objects.create.assert_not_called()

    @patch("dataSeeding.management.commands.data.Moving")
    def test_addMoving(self, mock_Moving):
        # arrange
        mock_Moving.objects.filter.return_value.exists.return_value = False

        # act
        addMoving()

        # assert
        calls = [call(direction='Up'), call(direction='Down'),
                 call(direction='Stationary')]
        mock_Moving.objects.create.assert_has_calls(
            calls, any_order=True)

    @patch("dataSeeding.management.commands.data.Moving")
    def test_addMoving_when_db_has_data(self, mock_Moving):
        # arrange
        mock_Moving.objects.filter.return_value.exists.return_value = True

        # act
        addMoving()

        # assert
        mock_Moving.objects.create.assert_not_called()

    @patch("dataSeeding.management.commands.data.Operational_Status")
    def test_addOperational_Status(self, mock_Operational_Status):
        # arrange
        mock_Operational_Status.objects.filter.return_value.exists.return_value = False

        # act
        addOperational_Status()

        # assert
        calls = [call(value='Working'), call(value='Maintainence'),
                 call(value='Non Operational')]
        mock_Operational_Status.objects.create.assert_has_calls(
            calls, any_order=True)

    @patch("dataSeeding.management.commands.data.Operational_Status")
    def test_addOperational_Status_when_db_has_data(self, mock_Operational_Status):
        # arrange
        mock_Operational_Status.objects.filter.return_value.exists.return_value = True

        # act
        addOperational_Status()

        # assert
        mock_Operational_Status.objects.create.assert_not_called()
