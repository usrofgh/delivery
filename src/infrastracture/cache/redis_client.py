from redis import Redis

from bootstrap.settings import settings

redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
print(redis_client.ping())
