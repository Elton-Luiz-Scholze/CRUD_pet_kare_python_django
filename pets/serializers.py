from rest_framework import serializers
from .models import SexPet
from groups.serializers import GroupsSerializer
from traits.serializers import TraitsSerializer


class PetsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SexPet.choices, default=SexPet.DEFAULT)
    group = GroupsSerializer()
    traits = TraitsSerializer(many=True)
