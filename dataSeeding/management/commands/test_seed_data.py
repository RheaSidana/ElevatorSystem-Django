from django.test import TestCase
from unittest.mock import patch
from .seed_data import *


class CommandTest(TestCase):

    @patch("dataSeeding.management.commands.seed_data.deleteAllDataFromAllModels")
    @patch("dataSeeding.management.commands.seed_data.addMovements")
    @patch("dataSeeding.management.commands.seed_data.addDoorFunctions")
    @patch("dataSeeding.management.commands.seed_data.addMoving")
    @patch("dataSeeding.management.commands.seed_data.addOperational_Status")
    def test_seed_data(self, mock_addOperational_Status, mock_addMoving, mock_addDoorFunctions, mock_addMovements, mock_deleteAllDataFromAllModels):
        command = Command()
        
        command.seed_data()

        mock_deleteAllDataFromAllModels.assert_called_once()
        mock_addMovements.assert_called_once()
        mock_addDoorFunctions.assert_called_once()
        mock_addMoving.assert_called_once()
        mock_addOperational_Status.assert_called_once()
