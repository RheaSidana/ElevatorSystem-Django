from rest_framework import serializers

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
