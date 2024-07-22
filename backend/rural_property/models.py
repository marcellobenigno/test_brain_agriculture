from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from ..core.models import BaseModel


class RuralProperty(BaseModel):
    owner = models.ForeignKey('farmer.Farmer', verbose_name='proprietário', on_delete=models.PROTECT)
    city = models.ForeignKey('location.City', verbose_name='cidade', on_delete=models.PROTECT)
    property_name = models.CharField('Nome da Propriedade', max_length=255)
    area_ha = models.DecimalField('Área da Propridedade', max_digits=10, decimal_places=3)

    def __str__(self):
        return self.property_name

    @property
    def sum_of_areas(self):
        return Plantation.objects.filter(
            rural_property=self
        ).aggregate(sum=Sum('area_ha'))['sum'] or 0

    class Meta:
        verbose_name = 'Propriedade Rural'
        verbose_name_plural = 'Propriedades Rurais'


class Plantation(BaseModel):
    CULTURE_CHOICES = (
        ('Algodão', 'Algodão'),
        ('Café', 'Café'),
        ('Cana de Açúcar', 'Cana de Açúcar'),
        ('Milho', 'Milho'),
        ('Soja', 'Soja'),
        ('Área de Vegetação', 'Área de Vegetação'),
    )
    name = models.CharField('Nome da Cultura', max_length=50, choices=CULTURE_CHOICES)
    area_ha = models.DecimalField('Área (ha)', max_digits=10, decimal_places=3)
    rural_property = models.ForeignKey('RuralProperty', verbose_name='Propriedade Rural', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def clean(self):
        if self.pk:
            existing_area = Plantation.objects.get(pk=self.pk).area_ha
        else:
            existing_area = 0
        new_sum_of_areas = self.rural_property.sum_of_areas - existing_area + self.area_ha
        if new_sum_of_areas > self.rural_property.area_ha:
            raise ValidationError(
                'A soma das áreas das plantações e vegetação não pode ser maior que a área total da propriedade rural.'
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Área agricultável'
        verbose_name_plural = 'Áreas agricultáveis'
