from redis.asyncio import Redis
from typing import List, Optional, Any, cast
from ...ioc.singleton import SingletonMeta


class AsyncRedisClient(metaclass=SingletonMeta):
    def __init__(self, redis_connection: Optional[Redis] = None) -> None:
        if not hasattr(self, "redis") and isinstance(redis_connection, Redis):
            self.redis: Redis = redis_connection

    async def set(self, key: str, value: Any, expiry: Optional[int] = None) -> bool:
        return bool(await self.redis.set(key, value, ex=expiry))

    async def get(self, key: str) -> Optional[bytes]:
        return await self.redis.get(key)

    async def delete(self, key: str) -> int:
        return await self.redis.delete(key)

    async def delete_all_keys(self, keys: List[str]) -> int:
        return await self.redis.delete(*keys)

    async def get_keys(self, pattern: str = "*") -> List[str]:
        return cast(List[str], await self.redis.keys(pattern))

    async def execute_command(self, *commands: str) -> Any:
        return await self.redis.execute_command(*commands)

    async def close_connection(self) -> None:
        await self.redis.close()
