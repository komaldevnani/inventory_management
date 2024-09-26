from rest_framework import generics, permissions
from .models import InventoryItem
from .serializers import InventoryItemSerializer
from .utils.cache import get_or_set_cache

CACHE_TIMEOUT = 60 * 15  # 15 minutes

class InventoryItemListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cache_key = 'inventory_item_list'
        queryset = get_or_set_cache(cache_key, super().get_queryset(), CACHE_TIMEOUT)
        return queryset

    def perform_create(self, serializer):
        # Invalidate cache when a new item is created
        cache.delete('inventory_item_list')
        return super().perform_create(serializer)


class InventoryItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        cache_key = f'inventory_item_{obj.pk}'
        data = get_or_set_cache(cache_key, obj, CACHE_TIMEOUT)
        return data

    def perform_update(self, serializer):
        # Invalidate cache for the specific item and list view
        cache.delete(f'inventory_item_{self.get_object().pk}')
        cache.delete('inventory_item_list')
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        # Invalidate cache for the specific item and list view
        cache.delete(f'inventory_item_{instance.pk}')
        cache.delete('inventory_item_list')
        return super().perform_destroy(instance)
