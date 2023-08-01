from rest_framework import serializers
from .models import *


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = "__all__"


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = "__all__"


class ElevatorFunctionalitySerializer(serializers.ModelSerializer):
    floor_name = serializers.SerializerMethodField()
    movement_action = serializers.SerializerMethodField()
    moving_direction = serializers.SerializerMethodField()
    operational = serializers.SerializerMethodField()
    door_status = serializers.SerializerMethodField()

    class Meta:
        model = ElevatorFunctionality
        fields = [
            "elevator", "floor_name",
            "movement_action", "moving_direction",
            "operational", "door_status",
            "curr_req_count",
            "curr_person_count"]
        depth = 1

    def get_floor_name(self, obj):
        return obj.floor_no.name if obj.floor_no else None

    def get_movement_action(self, obj):
        return obj.movement.action if obj.movement else None

    def get_moving_direction(self, obj):
        return obj.direction.direction if obj.direction else None

    def get_operational(self, obj):
        return obj.operational_status.value if obj.operational_status else None

    def get_door_status(self, obj):
        return obj.door_functionality.name if obj.door_functionality else None


class ElevatorForRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorForRequests
        fields = "__all__"
        depth = 1


class ElevatorFromRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorFromRequests
        fields = "__all__"
        depth = 1


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
