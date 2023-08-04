from ...models.models import ElevatorForRequests
from rest_framework import serializers

class ElevatorForRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorForRequests
        fields = "__all__"
        depth = 1