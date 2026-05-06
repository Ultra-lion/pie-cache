
import sys

MAX_CACHE_SIZE = 256


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwds)
            cls._instances[cls] = instance
        return cls._instances[cls]

class PieCacheManager(metaclass=SingletonMeta):

    def __init__(self):
        self.main_cache=dict()
        self.cache_size_bytes=0
    
    def set_cache_item(self, key: str, value: str):
        
        key_size = sys.getsizeof(key)
        old_val = self.main_cache.get(key)
        old_val_size=None
        if old_val is not None:
            old_val_size = sys.getsizeof(old_val)
            self.cache_size_bytes-=(key_size+old_val_size)

        val_size = sys.getsizeof(value)

        self.cache_size_bytes+=(key_size+val_size)
        size_mb = self.cache_size_bytes/(1024*1024)

        if size_mb > MAX_CACHE_SIZE:
            self.cache_size_bytes-=(key_size+val_size)

            if old_val_size is not None:
                self.cache_size_bytes+=(key_size+old_val_size)

            return "Max Cache Size Exceeded"
        
        self.main_cache[key]=value
        return 'ok'
    
    def get_cache_item(self, key:str):
        item = self.main_cache.get(key,None)
        if not item:
            return "Not Found"
        else:
            return item
    
    def del_item_cache(self, key:str):
        if key in self.main_cache:
            value = self.main_cache[key]
            key_size = sys.getsizeof(key)
            val_size = sys.getsizeof(value)
            self.cache_size_bytes-=(key_size+val_size)
            del self.main_cache[key]
