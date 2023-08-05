from django.core.cache import cache

def get_cached(key):
    return cache.get(key=key)

#for Floor and ElevatorFunctionality when created
def create_cached(key,data):
    # cached data will reside until create function is called again
    cached_data =  get_cached(key=key)

    if cached_data:
        # print("Cached Data: ")
        # print(cached_data)

        cache.delete(key=key)

    cache.set(key=key, value=data)

def list_cached(key):
    cached_data =  get_cached(key=key)

    # print(cached_data == {})

    if cached_data:
        # print("Cached Data: ")
        # print(cached_data)
        return cached_data
    
    return {}
