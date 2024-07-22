import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

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
