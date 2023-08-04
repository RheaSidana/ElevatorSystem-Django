from ...models.models import ElevatorFromRequests
from rest_framework import serializers

class ElevatorFromRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorFromRequests
        fields = "__all__"
        depth = 1
