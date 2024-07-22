from rest_framework import serializers

from . import models


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = [
            'id',
            'state',
            'abbreviation',
            'geocode',
        ]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = [
            'id',
            'city',
            'state',
            'geocode',
        ]
