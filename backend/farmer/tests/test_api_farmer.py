import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Farmer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, django_user_model):
    # Criação de um usuário e obtenção de token
    user = django_user_model.objects.create_user(email='user@mail.com', password='pass')
    response = api_client.post('/api/login/', {'username': 'user@mail.com', 'password': 'pass'})
    assert response.status_code == status.HTTP_200_OK
    token = response.data['token']
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    return api_client


@pytest.mark.django_db
def test_list_farmers(authenticated_client):
    # Criação de um Farmer
    Farmer.objects.create(name="John Snow", cpf="19538295030")

    # Teste do endpoint de listagem
    response = authenticated_client.get(reverse('farmers-list'))
    assert response.status_code == status.HTTP_200_OK
    results = response.data['results']
    assert len(results) == 1
    assert results[0]['name'] == "John Snow"


@pytest.mark.django_db
def test_create_farmer(authenticated_client):
    # Teste do endpoint de criação
    data = {
        'name': 'Jane Doe',
        'cpf': '98765432100'
    }
    response = authenticated_client.post(reverse('farmers-list'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Jane Doe'
    assert response.data['cpf'] == '98765432100'


@pytest.mark.django_db
def test_create_farmer_invalid_cpf(authenticated_client):
    # Teste do endpoint de criação com CPF inválido
    data = {
        'name': 'Invalid CPF',
        'cpf': '12345678901'
    }
    response = authenticated_client.post(reverse('farmers-list'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_farmer(authenticated_client):
    farmer = Farmer.objects.create(name="John Snow", cpf="19538295030")

    # Teste do endpoint de atualização
    data = {
        'name': 'John Updated',
        'cpf': '19538295030'
    }
    response = authenticated_client.put(reverse('farmers-detail', args=[farmer.id]), data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'John Updated'


@pytest.mark.django_db
def test_delete_farmer(authenticated_client):
    farmer = Farmer.objects.create(name="John Snow", cpf="19538295030")

    # Teste do endpoint de exclusão
    response = authenticated_client.delete(reverse('farmers-detail', args=[farmer.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Farmer.objects.count() == 0
