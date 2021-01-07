from rest_framework import serializers

from .models import VaccineType, VolunteersModel

class VaccineTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VaccineType
        fields = ('group', 'name', 'type',)


class VolunteersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VolunteersModel
        fields = ('group', 'dose', 'positive',)