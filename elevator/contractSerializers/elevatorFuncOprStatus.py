from rest_framework import serializers
from ..models.models import ElevatorFunctionality

class ElevatorFunctionalityOperationalSerializer(serializers.ModelSerializer):
    elevator_name = serializers.SerializerMethodField()
    operational = serializers.SerializerMethodField()

    class Meta:
        model = ElevatorFunctionality
        fields = ["elevator_name", "operational"]

    def get_elevator_name(self, obj):
        return obj.elevator.name if obj.elevator else None

    def get_operational(self, obj):
        return obj.operational_status.value if obj.operational_status else None

