import pytest
from rest_framework import status
from rest_framework.test import APIClient

from .models import State, City


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def setup_data(db):
    # Cria os estados
    state1 = State.objects.create(state='São Paulo', abbreviation='SP', geocode=35)
    state2 = State.objects.create(state='Minas Gerais', abbreviation='MG', geocode=31)

    # Cria as cidades
    city1 = City.objects.create(city='São Paulo', state=state1, geocode=3550308)
    city2 = City.objects.create(city='Belo Horizonte', state=state2, geocode=3106200)

    return state1, state2, city1, city2


@pytest.mark.django_db
def test_list_states(api_client, setup_data):
    response = api_client.get('/api/states/')
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    print("Response JSON:", data)

    assert isinstance(data, dict), f"Expected dict, got {type(data)}"
    assert 'results' in data, "Key 'results' not found in response"

    results = data['results']

    assert any(state['state'] == 'São Paulo' for state in results)
    assert any(state['state'] == 'Minas Gerais' for state in results)


@pytest.mark.django_db
def test_list_cities(api_client, setup_data):
    response = api_client.get('/api/cities/')
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    print("Response JSON:", data)

    assert isinstance(data, dict), f"Expected dict, got {type(data)}"
    assert 'results' in data, "Key 'results' not found in response"

    results = data['results']

    # Verificar o número de cidades na lista de resultados
    assert len(results) == 2
    assert any(city['city'] == 'São Paulo' for city in results)
    assert any(city['city'] == 'Belo Horizonte' for city in results)


@pytest.mark.django_db
def test_retrieve_city(api_client, setup_data):
    _, _, city1, _ = setup_data
    response = api_client.get(f'/api/cities/{city1.id}/')
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    print("Response JSON:", data)

    # Verificar os dados retornados da cidade
    assert data['city'] == city1.city
    assert data['state'] == city1.state.id
