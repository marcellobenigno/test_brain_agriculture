from rest_framework import viewsets

from . import models
from . import serializers


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.State.objects.filter(active=True)
    serializer_class = serializers.StateSerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.City.objects.filter(active=True)
    serializer_class = serializers.CitySerializer
