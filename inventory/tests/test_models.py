import pytest
from inventory.models import InventoryItem

@pytest.mark.django_db
def test_inventory_item_creation():
    item = InventoryItem.objects.create(name="Test Item", description="A test item", quantity=10, price=99.99)
    assert item.name == "Test Item"
    assert item.description == "A test item"
    assert item.quantity == 10
    assert item.price == 99.99

@pytest.mark.django_db
def test_inventory_item_string_representation():
    item = InventoryItem(name="Test Item")
    assert str(item) == item.name
