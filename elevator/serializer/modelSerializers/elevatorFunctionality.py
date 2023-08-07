import collections
from ...models.models import ElevatorFunctionality
from rest_framework import serializers

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
        if obj.floor_no:
            return obj.floor_no.name
        # elif obj["floor_name"]:
        #     return obj["floor_name"]
        else:
            return None

    def get_movement_action(self, obj):
        # if obj is collections.OrderedDict:
        #     return obj.movement_action
        if obj.movement:
            return obj.movement.action  
        # if obj["movement_action"]:
        #     return obj["movement_action"]
        else:
            return None

    def get_moving_direction(self, obj):
        # if obj is collections.OrderedDict:
        #     return obj.moving_direction
        if obj.direction:
            return obj.direction.direction 
        # if obj["moving_direction"]:
        #     return obj["moving_direction"]
        else:
            return None

    def get_operational(self, obj):
        # if obj is collections.OrderedDict:
        #     return obj.operational
        if obj.operational_status:
            return obj.operational_status.value
        # if obj["operational"]:
        #     return obj["operational"]
        else: 
            return None

    def get_door_status(self, obj):
        # if obj is collections.OrderedDict:
        #     return obj.door_status
        if obj.door_functionality:
            return obj.door_functionality.name
        # if obj["door_status"]:
        #     return obj["door_status"]
        else:
            return None

