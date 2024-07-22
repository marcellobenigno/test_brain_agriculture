import pytest
from django.core.exceptions import ValidationError

from ..models import Farmer


@pytest.mark.django_db
def test_valid_cpf():
    farmer = Farmer(
        name="John Snow",
        cpf="19538295030",  # Um CPF válido
        cnpj=None
    )
    try:
        farmer.save()
    except ValidationError:
        pytest.fail("Falhou ao validar um CPF válido")


@pytest.mark.django_db
def test_invalid_cpf():
    farmer = Farmer(
        name="John Snow",
        cpf="12345678901",  # Um CPF inválido
        cnpj=None
    )
    with pytest.raises(ValidationError):
        farmer.full_clean()  # Aqui usamos full_clean() para validar o campo


@pytest.mark.django_db
def test_valid_cnpj():
    farmer = Farmer(
        name="John Snow",
        cpf=None,
        cnpj="12345678000195"  # Um CNPJ válido
    )
    try:
        farmer.save()
    except ValidationError:
        pytest.fail("Falhou ao validar um CNPJ válido")


@pytest.mark.django_db
def test_invalid_cnpj():
    farmer = Farmer(
        name="John Snow",
        cpf=None,
        cnpj="12345678000191"  # Um CNPJ inválido
    )
    with pytest.raises(ValidationError):
        farmer.full_clean()  # Aqui usamos full_clean() para validar o campo


@pytest.mark.django_db
def test_no_cpf_or_cnpj():
    farmer = Farmer(
        name="John Snow",
        cpf=None,
        cnpj=None
    )
    with pytest.raises(ValidationError):
        farmer.save()


@pytest.mark.django_db
def test_both_cpf_and_cnpj():
    farmer = Farmer(
        name="John Snow",
        cpf="19538295030",  # Um CPF válido
        cnpj="12345678000195"  # Um CNPJ válido
    )
    with pytest.raises(ValidationError):
        farmer.save()
