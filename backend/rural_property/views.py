from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers


class RuralPropertyViewSet(viewsets.ModelViewSet):
    queryset = models.RuralProperty.objects.filter(active=True)
    serializer_class = serializers.RuralPropertySerializer
    permission_classes = [IsAuthenticated]


class PlantationViewSet(viewsets.ModelViewSet):
    queryset = models.Plantation.objects.filter(active=True)
    serializer_class = serializers.PlantationSerializer
    permission_classes = [IsAuthenticated]
