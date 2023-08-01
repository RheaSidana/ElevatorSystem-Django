from rest_framework import serializers
from .models import *

class MovementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movements
        fields = '__all__'

class DoorFunctionsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = DoorFunctions
        fields = '__all__'
        
class MovingSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Moving
        fields = '__all__'
        
class Operational_StatusSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Operational_Status
        fields = '__all__'
        
# class ElevatorRequestTypeSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = ElevatorRequestType
#         fields = '__all__'

class ElevatorRequestStatusSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ElevatorRequestStatus
        fields = '__all__'
