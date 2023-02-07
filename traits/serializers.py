from rest_framework import serializers


class TraitsSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    trait_name = serializers.CharField(max_length=20, source="name")
    created_at = serializers.DateTimeField(read_only=True)
