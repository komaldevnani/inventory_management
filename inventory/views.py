# inventory/views.py

import logging
from rest_framework import generics, permissions
from .models import InventoryItem
from .serializers import InventoryItemSerializer
from .utils.cache import get_or_set_cache
from .utils.custom_exceptions import ItemNotFoundException, InvalidDataException
from django.core.cache import cache
from rest_framework.response import Response

# Get the logger for the inventory app
logger = logging.getLogger('inventory')

CACHE_TIMEOUT = 60 * 15  # 15 minutes

class InventoryItemListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.info("Fetching the list of inventory items.")
        try:
            cache_key = 'inventory_item_list'
            queryset = get_or_set_cache(cache_key, super().get_queryset(), CACHE_TIMEOUT)
            logger.debug(f"Inventory items retrieved from cache or database: {queryset}")
            return queryset
        except Exception as e:
            logger.error(f"Error fetching inventory items: {e}")
            raise

    def perform_create(self, serializer):
        try:
            if serializer.is_valid():
                cache.delete('inventory_item_list')
                logger.info(f"Creating new inventory item: {serializer.validated_data}")
                return super().perform_create(serializer)
            else:
                logger.warning(f"Invalid data provided for inventory item creation: {serializer.errors}")
                raise InvalidDataException
        except Exception as e:
            logger.error(f"Error creating inventory item: {e}")
            raise

class InventoryItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            obj = super().get_object()
            cache_key = f'inventory_item_{obj.pk}'
            data = get_or_set_cache(cache_key, obj, CACHE_TIMEOUT)
            logger.info(f"Retrieved inventory item with ID {obj.pk}.")
            return data
        except InventoryItem.DoesNotExist:
            logger.warning(f"Inventory item not found with ID {self.kwargs['pk']}.")
            raise ItemNotFoundException
        except Exception as e:
            logger.error(f"Error retrieving inventory item: {e}")
            raise

    def perform_update(self, serializer):
        try:
            if serializer.is_valid():
                cache.delete(f'inventory_item_{self.get_object().pk}')
                cache.delete('inventory_item_list')
                logger.info(f"Updating inventory item with ID {self.get_object().pk}. Data: {serializer.validated_data}")
                return super().perform_update(serializer)
            else:
                logger.warning(f"Invalid data provided for updating inventory item with ID {self.get_object().pk}: {serializer.errors}")
                raise InvalidDataException
        except Exception as e:
            logger.error(f"Error updating inventory item: {e}")
            raise

    def perform_destroy(self, instance):
        try:
            logger.info(f"Deleting inventory item with ID {instance.pk}.")
            cache.delete(f'inventory_item_{instance.pk}')
            cache.delete('inventory_item_list')
            return super().perform_destroy(instance)
        except InventoryItem.DoesNotExist:
            logger.warning(f"Inventory item not found with ID {instance.pk}.")
            raise ItemNotFoundException
        except Exception as e:
            logger.error(f"Error deleting inventory item: {e}")
            raise
