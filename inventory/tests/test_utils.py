import pytest
from inventory.utils.cache import get_or_set_cache
from django.core.cache import cache

@pytest.mark.django_db
def test_get_or_set_cache():
    cache_key = 'test_key'
    test_data = 'test_data'

    # Ensure cache is initially empty
    assert cache.get(cache_key) is None

    # Set cache
    data = get_or_set_cache(cache_key, test_data, 300)
    assert data == test_data
    assert cache.get(cache_key) == test_data

    # Retrieve from cache
    cached_data = get_or_set_cache(cache_key, 'new_data', 300)
    assert cached_data == test_data  # Should return the original cached data
