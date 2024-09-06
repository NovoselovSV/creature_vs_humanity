from redis import Redis

from settings import redis_url

redis_instance = Redis.from_url(redis_url)
