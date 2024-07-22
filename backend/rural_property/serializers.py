from rest_framework import serializers

from . import models


class RuralPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RuralProperty
        fields = [
            'id',
            'owner',
            'city',
            'property_name',
            'area_ha',
        ]


class PlantationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plantation
        fields = [
            'id',
            'name',
            'area_ha',
            'rural_property',
        ]
