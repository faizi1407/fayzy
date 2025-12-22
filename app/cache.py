import redis
import os
import json
from typing import Optional

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client: Optional[redis.Redis] = None


def get_redis() -> redis.Redis:
    """Get Redis client."""
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client


class CacheService:
    """Service for caching feature entitlements."""
    
    def __init__(self):
        self.redis = get_redis()
        self.ttl = 300  # 5 minutes cache TTL
    
    def get_user_features(self, user_id: int) -> Optional[set]:
        """Get cached user features."""
        try:
            cache_key = f"user_features:{user_id}"
            cached = self.redis.get(cache_key)
            if cached:
                return set(json.loads(cached))
        except Exception:
            # If Redis fails, continue without cache
            pass
        return None
    
    def set_user_features(self, user_id: int, features: set):
        """Cache user features."""
        try:
            cache_key = f"user_features:{user_id}"
            self.redis.setex(cache_key, self.ttl, json.dumps(list(features)))
        except Exception:
            # If Redis fails, continue without cache
            pass
    
    def invalidate_user_features(self, user_id: int):
        """Invalidate cached user features."""
        try:
            cache_key = f"user_features:{user_id}"
            self.redis.delete(cache_key)
        except Exception:
            pass
