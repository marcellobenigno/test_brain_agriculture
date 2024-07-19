from django.core.exceptions import ValidationError
from django.db import models
from localflavor.br.models import BRCPFField, BRCNPJField

from ..core.models import BaseModel


class Farmer(BaseModel):
    name = models.CharField('nome', max_length=255)
    cpf = BRCPFField('CPF', max_length=11, blank=True, null=True)
    cnpj = BRCNPJField('CNPJ', max_length=14, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.cpf and not self.cnpj:
            raise ValidationError("Deve ser informado CPF ou CNPJ.")
        if self.cpf and self.cnpj:
            raise ValidationError("Não pode informar ambos CPF e CNPJ.")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Proprietário Rural'
        verbose_name_plural = 'Proprietários Rurais'
