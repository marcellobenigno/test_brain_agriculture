from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from ..models import RuralProperty, Plantation
from ...farmer.models import Farmer
from ...location.models import City, State


@pytest.fixture
def farmer(db):
    return Farmer.objects.create(
        name="John Snow",
        cpf="19538295030",
        cnpj=None
    )


@pytest.fixture
def state(db):
    return State.objects.create(
        state="Paraíba",
        abbreviation="PB",
        geocode=25
    )


@pytest.fixture
def city(db, state):
    return City.objects.create(
        state=state,
        city="João Pessoa",
        geocode=2507507,
    )


@pytest.fixture
def rural_property(db, farmer, city):
    return RuralProperty.objects.create(
        owner=farmer,
        city=city,
        property_name="Test Property",
        area_ha=Decimal('100.000')
    )


@pytest.mark.django_db
def test_create_rural_property(rural_property):
    assert RuralProperty.objects.count() == 1
    assert rural_property.property_name == "Test Property"
    assert rural_property.area_ha == Decimal('100.000')


@pytest.mark.django_db
def test_create_plantation(rural_property):
    plantation = Plantation.objects.create(
        name='Soja',
        area_ha=Decimal('50.000'),
        rural_property=rural_property
    )
    assert Plantation.objects.count() == 1
    assert plantation.name == 'Soja'
    assert plantation.area_ha == Decimal('50.000')


@pytest.mark.django_db
def test_sum_of_areas(rural_property):
    Plantation.objects.create(
        name='Soja',
        area_ha=Decimal('50.000'),
        rural_property=rural_property
    )
    Plantation.objects.create(
        name='Milho',
        area_ha=Decimal('30.000'),
        rural_property=rural_property
    )
    assert rural_property.sum_of_areas == Decimal('80.000')


@pytest.mark.django_db
def test_plantation_area_validation(rural_property):
    Plantation.objects.create(
        name='Soja',
        area_ha=Decimal('50.000'),
        rural_property=rural_property
    )
    with pytest.raises(ValidationError):
        Plantation.objects.create(
            name='Milho',
            area_ha=Decimal('60.000'),
            rural_property=rural_property
        )


@pytest.mark.django_db
def test_update_plantation_area_validation(rural_property):
    plantation1 = Plantation.objects.create(
        name='Soja',
        area_ha=Decimal('50.000'),
        rural_property=rural_property
    )
    plantation2 = Plantation.objects.create(
        name='Milho',
        area_ha=Decimal('40.000'),
        rural_property=rural_property
    )
    plantation2.area_ha = Decimal('60.000')
    with pytest.raises(ValidationError):
        plantation2.save()
