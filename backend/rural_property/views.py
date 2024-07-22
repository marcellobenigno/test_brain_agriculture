from django.db.models import Sum, Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models
from . import serializers


class RuralPropertyViewSet(viewsets.ModelViewSet):
    queryset = models.RuralProperty.objects.all()
    serializer_class = serializers.RuralPropertySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def total_properties(self, request):
        total_properties = models.RuralProperty.objects.count()
        return Response({'total_properties': total_properties})

    @action(detail=False, methods=['get'])
    def total_area_ha(self, request):
        total_area_ha = models.RuralProperty.objects.aggregate(total_area=Sum('area_ha'))['total_area'] or 0
        return Response({'total_area_ha': total_area_ha})

    @action(detail=False, methods=['get'])
    def total_properties_by_state(self, request):
        properties_by_state = models.RuralProperty.objects \
            .select_related('city__state') \
            .values('city__state__state') \
            .annotate(total_properties=Count('id'), total_area_ha=Sum('area_ha'))
        results = [
            {
                'state': item['city__state__state'],
                'total_properties': item['total_properties'],
                'total_area_ha': item['total_area_ha']
            }
            for item in properties_by_state
        ]

        return Response(results)


class PlantationViewSet(viewsets.ModelViewSet):
    queryset = models.Plantation.objects.all()
    serializer_class = serializers.PlantationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def total_area_by_culture(self, request):
        total_area_by_culture = models.Plantation.objects \
            .exclude(name='Área de Vegetação') \
            .values('name') \
            .annotate(total_area_ha=Sum('area_ha'))

        results = [
            {
                'culture': item['name'],
                'total_area_ha': item['total_area_ha']
            }
            for item in total_area_by_culture
        ]

        return Response(results)

    @action(detail=False, methods=['get'])
    def total_land_use_area_summary(self, request):
        total_culture_area = models.Plantation.objects \
             .exclude(name='Área de Vegetação') \
             .aggregate(total_culture_area=Sum('area_ha'))['total_culture_area'] or 0

        # Soma total da área de Vegetação
        total_vegetation_area = models.Plantation.objects \
            .filter(name='Área de Vegetação') \
            .aggregate(total_vegetation_area=Sum('area_ha'))['total_vegetation_area'] or 0

        return Response({
            'total_culture_area': total_culture_area,
            'total_vegetation_area': total_vegetation_area
        })
