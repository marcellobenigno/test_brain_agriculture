from django.db import models

from ..core.models import BaseModel


class State(BaseModel):
    state = models.CharField('Estado', max_length=100)
    abbreviation = models.CharField('Sigla', max_length=2, unique=True)
    geocode = models.IntegerField('Geocódigo')

    def __str__(self):
        return self.state

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['state']


class City(BaseModel):
    state = models.ForeignKey('State', verbose_name='Estado', on_delete=models.CASCADE)
    city = models.CharField('Cidade', max_length=100)
    geocode = models.IntegerField('Geocódigo')

    def __str__(self):
        return f'{self.city} - {self.state.abbreviation}'

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'
        ordering = ['state', 'city']
