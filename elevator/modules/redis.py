from django.core.cache import cache

def get_cached(key):
    return cache.get(key=key)

#for Floor and ElevatorFunctionality when created
def create_cached_infiniteTimeout(key,data):
    # cached data will reside until create function is called again
    cached_data =  get_cached(key=key)

    if cached_data:
        cache.delete(key=key)

    cache.set(key=key, value=data, timeout=None)

def list_cached(key):
    cached_data =  get_cached(key=key)

    if cached_data:
        return cached_data
    
    return {}
