import redis

dragonfly_uri = "redis://user:password@host:port"
redis_client = redis.from_url(dragonfly_uri, decode_responses=True,socket_timeout=5,socket_connect_timeout=5)
