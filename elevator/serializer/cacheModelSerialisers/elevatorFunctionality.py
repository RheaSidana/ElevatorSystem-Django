import collections
from ...models.models import ElevatorFunctionality
from rest_framework import serializers

class ElevatorFunctionalitySerializer(serializers.Serializer):
    floor_name = serializers.SerializerMethodField()
    movement_action = serializers.SerializerMethodField()
    moving_direction = serializers.SerializerMethodField()
    operational = serializers.SerializerMethodField()
    door_status = serializers.SerializerMethodField()
    elevator = serializers.SerializerMethodField()

    class Meta:
        fields = [
            "elevator", "floor_name",
            "movement_action", "moving_direction",
            "operational", "door_status",
            "curr_req_count",
            "curr_person_count"]
        
    def get_floor_name(self, obj):
        if "floor_name" in obj:
            return obj["floor_name"]
        else:
            return None
        
    def get_movement_action(self, obj):
        return obj.get("movement_action")

    def get_moving_direction(self, obj):
        return obj.get("moving_direction")

    def get_operational(self, obj):
        return obj.get("operational")

    def get_door_status(self, obj):
        return obj.get("door_status")

    def get_elevator(self, obj):
        return obj.get("elevator")


    