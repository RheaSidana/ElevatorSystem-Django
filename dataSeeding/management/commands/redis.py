from django.core.cache import cache


def create_cache(key, data):
    cached_data = cache.get(key=key)

    if cached_data:
        if cached_data != data:
            cache.delete(key=key)

    cache.set(key=key, value=data, timeout=None)
