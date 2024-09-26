from django.core.cache import cache

def get_or_set_cache(key, queryset, timeout=60):
    """
    Retrieve data from cache if available, otherwise set it.

    Args:
        key (str): The cache key.
        queryset (QuerySet): The queryset or object to cache.
        timeout (int): Time in seconds for which the cache should persist.

    Returns:
        data: Cached data or freshly queried data.
    """
    data = cache.get(key)
    if not data:
        data = queryset
        cache.set(key, data, timeout)
    return data
