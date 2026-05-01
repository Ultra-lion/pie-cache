
import sys

MAX_CACHE_SIZE = 1


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            instance = super()._call__(*args, **kwds)
            cls._instances[cls] = instance
        return cls._instances[cls]

class PieCacheManager(metaclass=SingletonMeta):

    def __init__(self):
        self.main_cache=dict()
    
    def set_cache_item(self, key: str, value: str):
        dict_bytes_size = sys.getsizeof(self.main_cache)
        size_mb = dict_bytes_size/(1024*1024)
        if size_mb > MAX_CACHE_SIZE:
            return "Max Cache Size Exceeded"
        else:
            self.main_cache[str]=value
            return 'ok'
    
    def get_cache_item(self, key:str):
        item = self.main_cache.get(key,None)
        if not item:
            return "Not Found"
        else:
            return item
