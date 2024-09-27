# inventory/tests/test_views.py

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from inventory.models import InventoryItem
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

@pytest.mark.django_db
def test_inventory_item_list(auth_client):
    # Use the 'item-list-create' name defined in the inventory/urls.py
    url = reverse('item-list-create')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_inventory_item_creation(auth_client):
    # Use the 'item-list-create' name defined in the inventory/urls.py
    url = reverse('item-list-create')
    data = {"name": "New Item", "description": "Description", "quantity": 5, "price": 49.99}
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert InventoryItem.objects.count() == 1
    assert InventoryItem.objects.get().name == "New Item"

@pytest.mark.django_db
def test_inventory_item_detail(auth_client):
    # Create an inventory item to be fetched later
    item = InventoryItem.objects.create(name="Existing Item", description="Description", quantity=5, price=49.99)
    # Use the 'item-detail' name defined in the inventory/urls.py with the item ID
    url = reverse('item-detail', args=[item.id])
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "Existing Item"

@pytest.mark.django_db
def test_inventory_item_update(auth_client):
    # Create an inventory item to be updated later
    item = InventoryItem.objects.create(name="Existing Item", description="Description", quantity=5, price=49.99)
    # Use the 'item-detail' name defined in the inventory/urls.py with the item ID
    url = reverse('item-detail', args=[item.id])
    data = {"name": "Updated Item", "description": "Updated Description", "quantity": 10, "price": 99.99}
    response = auth_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    item.refresh_from_db()
    assert item.name == "Updated Item"

@pytest.mark.django_db
def test_inventory_item_delete(auth_client):
    # Create an inventory item to be deleted later
    item = InventoryItem.objects.create(name="Delete Item", description="Description", quantity=5, price=49.99)
    # Use the 'item-detail' name defined in the inventory/urls.py with the item ID
    url = reverse('item-detail', args=[item.id])
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert InventoryItem.objects.count() == 0
