from rest_framework import serializers

class ElevatorNextDestinationSerializer(serializers.Serializer):
    elevator_name = serializers.CharField()
    current_floor = serializers.CharField()
    next_floor = serializers.CharField()
    next_direction = serializers.CharField()
    floorsInUpDirection = serializers.ListField(child=serializers.CharField())
    floorsInDownDirection = serializers.ListField(child=serializers.CharField())

    def get_elevator_name(self, obj):
        return obj.elevator_name if hasattr(obj, "elevator_name") else None
    
    def get_current_floor(self, obj):
        return obj.current_floor if hasattr(obj, "current_floor") else None
    
    def get_next_direction(self, obj):
        return obj.next_direction if hasattr(obj, "next_direction") else None
    
    def get_next_floor(self, obj):
        return obj.next_floor if hasattr(obj, "next_floor") else None

    def get_floorsInUpDirection(self, obj):
        return obj.floorsInUpDirection if hasattr(obj, "floorsInUpDirection") else []
    
    def get_floorsInDownDirection(self, obj):
        return obj.floorsInDownDirection if hasattr(obj, "floorsInDownDirection") else []
