from django.core.cache import cache

from config.settings import CACHE_ENABLED
from service.models import Client


def get_cached_clients_list():
    """Получает данные из кэша, если кэш пуст, получает данные из БД"""
    if not CACHE_ENABLED:
        return Client.objects.all()
    key = 'clients_list'
    clients = cache.get(key)
    if clients is not None:
        return clients
    clients = Client.objects.all()
    cache.set(key, clients)
    return clients
