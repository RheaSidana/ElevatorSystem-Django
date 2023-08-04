from rest_framework import serializers
from ...models.models import ElevatorFunctionality

class ElevatorFunctionalityDoorSerializer(serializers.ModelSerializer):
    elevator_name = serializers.SerializerMethodField()
    door_status = serializers.SerializerMethodField()

    class Meta:
        model = ElevatorFunctionality
        fields = ["elevator_name", "door_status"]

    def get_elevator_name(self, obj):
        return obj.elevator.name if obj.elevator else None

    def get_door_status(self, obj):
        return obj.door_functionality.name if obj.door_functionality else None

