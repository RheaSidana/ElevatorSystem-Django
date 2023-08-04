from rest_framework import serializers

class FullFilElevatorNextRequestsSerializer(serializers.Serializer):
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
