from ...models.models import Floor
from rest_framework import serializers

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = "__all__"