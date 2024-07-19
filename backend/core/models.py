from django.db import models


class BaseModel(models.Model):
    active = models.BooleanField('Ativo', default=True, blank=True)
    created = models.DateTimeField('Criado', auto_now_add=True)
    updated = models.DateTimeField('Modificado', auto_now=True)

    class Meta:
        abstract = True
