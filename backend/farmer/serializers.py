from rest_framework import serializers

from . import models


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Farmer
        fields = [
            'id',
            'name',
            'cpf',
            'cnpj'
        ]
