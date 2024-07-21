from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from ..core.models import BaseModel


class RuralProperty(BaseModel):
    owner = models.ForeignKey('farmer.Farmer', verbose_name='proprietário', on_delete=models.PROTECT)
    city = models.ForeignKey('location.City', verbose_name='cidade', on_delete=models.PROTECT)
    property_name = models.CharField('Nome da Propriedade', max_length=255)
    vegetation_area_ha = models.DecimalField('Área de Vegetação Nativa (ha)', max_digits=10, decimal_places=3)
    total_area_ha = models.DecimalField('Área da Propridedade', max_digits=10, decimal_places=3)

    def __str__(self):
        return self.property_name

    @property
    def sum_of_areas(self):
        veg_area = self.vegetation_area_ha
        platantion_area = Plantation.objects.filter(rural_property=self).aggregate(sum=Sum('area_ha'))['sum'] or 0
        return veg_area + platantion_area

    def clean(self):
        if self.sum_of_areas > self.total_area_ha:
            raise ValidationError(
                "A soma das áreas das plantações e da vegetação não pode ser maior que a área total da propriedade."
            )

    def save(self, *args, **kwargs):
        # Save the instance first
        super().save(*args, **kwargs)
        # Now validate
        self.clean()
        # Save again to apply any changes made during validation
        super().save(*args, **kwargs)

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
    )
    name = models.CharField('Nome da Cultura', max_length=50, choices=CULTURE_CHOICES)
    area_ha = models.DecimalField('Área (ha)', max_digits=10, decimal_places=3)
    rural_property = models.ForeignKey('RuralProperty', verbose_name='Propriedade Rural', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def clean(self):
        sum_of_plantation_area = sum(
            plantation.area_ha for plantation in Plantation.objects.filter(rural_property=self.rural_property)
        )
        total_area_used = sum_of_plantation_area + self.rural_property.vegetation_area_ha + self.area_ha
        if total_area_used > self.rural_property.total_area_ha:
            raise ValidationError(
                "A soma das áreas das plantações e da vegetação não pode ser maior que a área total da propriedade."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Área agricultável'
        verbose_name_plural = 'Áreas agricultáveis'
