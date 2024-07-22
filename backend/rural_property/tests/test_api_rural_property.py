import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from ...farmer.models import Farmer
from ...location.models import State, City

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='admin@email.com',
        password='demodemo',
        first_name='Admin',
        last_name='Admin',
    )


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def authenticated_client(api_client, django_user_model):
    user = django_user_model.objects.create_user(email='user@mail.com', password='pass')
    response = api_client.post('/api/login/', {'username': 'user@mail.com', 'password': 'pass'})
    assert response.status_code == status.HTTP_200_OK
    token = response.data['token']
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    return api_client


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


@pytest.mark.django_db
def test_create_rural_property(authenticated_client, farmer, city):
    data = {
        'owner': farmer.pk,
        'city': city.pk,
        'property_name': 'Test Property',
        'area_ha': '100.000',
    }
    response = authenticated_client.post('/api/rural-properties/', data)

    print('cidade....', city.pk)
    print(response.data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['property_name'] == 'Test Property'
    assert response.data['area_ha'] == '100.000'


@pytest.mark.django_db
def test_total_properties(api_client):
    response = api_client.get('/api/rural-properties/total_properties/')
    assert response.status_code == status.HTTP_200_OK
    assert 'total_properties' in response.json()


@pytest.mark.django_db
def test_total_area_ha(api_client):
    response = api_client.get('/api/rural-properties/total_area_ha/')
    assert response.status_code == status.HTTP_200_OK
    assert 'total_area_ha' in response.json()


@pytest.mark.django_db
def test_total_properties_by_state(api_client):
    response = api_client.get('/api/rural-properties/total_properties_by_state/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.django_db
def test_total_areas_by_culture(api_client):
    response = api_client.get('/api/plantations/total_area_by_culture/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.django_db
def test_total_vegetation_area(api_client):
    response = api_client.get('/api/plantations/total_land_use_area/')
    assert response.status_code == status.HTTP_200_OK
    assert 'total_culture_area' in response.json()
