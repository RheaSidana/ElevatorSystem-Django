from rest_framework import serializers
from ...models.models import ElevatorFunctionality

class ElevatorFunctionalityMovingSerializer(serializers.ModelSerializer):
    elevator_name = serializers.SerializerMethodField()
    moving_direction = serializers.SerializerMethodField()

    class Meta:
        model = ElevatorFunctionality
        fields = ["elevator_name", "moving_direction"]

    def get_elevator_name(self, obj):
        return obj.elevator.name if obj.elevator else None

    def get_moving_direction(self, obj):
        return obj.direction.direction if obj.direction else None

