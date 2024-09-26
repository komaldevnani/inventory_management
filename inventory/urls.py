from django.urls import path
from .views import InventoryItemListCreateView, InventoryItemRetrieveUpdateDestroyView

urlpatterns = [
    path('items/', InventoryItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', InventoryItemRetrieveUpdateDestroyView.as_view(), name='item-detail'),
]
