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


class ElevatorNextDestinationSerializer(serializers.Serializer):
    elevator_name = serializers.CharField()
    current_floor = serializers.CharField()
    next_floor = serializers.CharField()
    next_direction = serializers.CharField()
    moving_direction1 = serializers.CharField()
    floor_names1 = serializers.ListField(child=serializers.CharField())
    moving_direction2 = serializers.CharField()
    floor_names2 = serializers.ListField(child=serializers.CharField())

    def get_elevator_name(self, obj):
        return obj.elevator_name if hasattr(obj, "elevator_name") else None
    
    def get_current_floor(self, obj):
        return obj.current_floor if hasattr(obj, "current_floor") else None

    def get_moving_direction1(self, obj):
        return obj.moving_direction1 if hasattr(obj, "moving_direction1") else None

    def get_moving_direction2(self, obj):
        return obj.moving_direction2 if hasattr(obj, "moving_direction2") else None
    
    def get_next_direction(self, obj):
        return obj.next_direction if hasattr(obj, "next_direction") else None
    
    def get_next_floor(self, obj):
        return obj.next_floor if hasattr(obj, "next_floor") else None

    def get_floor_names1(self, obj):
        return obj.floor_names1 if hasattr(obj, "floor_names1") else []
    
    def get_floor_names2(self, obj):
        return obj.floor_names2 if hasattr(obj, "floor_names2") else []

class FullFilElevatorRequestsSerializer(serializers.Serializer):
    elevator_name = serializers.CharField()
    current_floor = serializers.CharField()
    fulfilled_floor = serializers.CharField()
    steps = serializers.ListField(child=serializers.CharField())

    def get_elevator_name(self, obj):
        return obj.elevator_name if hasattr(obj, "elevator_name") else None
    
    def get_current_floor(self, obj):
        return obj.current_floor if hasattr(obj, "current_floor") else None
    
    def get_fulfilled_floor(self, obj):
        return obj.fulfilled_floor if hasattr(obj, "fulfilled_floor") else None
    
    def get_steps(self, obj):
        return obj.steps if hasattr(obj, "steps") else []
