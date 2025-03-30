from flask_caching import Cache

cache_config = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 5,
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': 6380,
    'CACHE_REDIS_DB': 0
}

cache = Cache(config=cache_config)
