from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers


class FarmerViewSet(viewsets.ModelViewSet):
    queryset = models.Farmer.objects.filter(active=True)
    serializer_class = serializers.FarmerSerializer
    permission_classes = [IsAuthenticated]
