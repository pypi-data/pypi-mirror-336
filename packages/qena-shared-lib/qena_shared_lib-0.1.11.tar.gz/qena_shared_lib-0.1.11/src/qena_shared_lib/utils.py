from asyncio import AbstractEventLoop, get_running_loop
from functools import lru_cache

from pydantic import TypeAdapter

__all__ = ["AsyncEventLoopMixin", "TypeAdapterCache"]


class AsyncEventLoopMixin:
    @property
    @lru_cache
    def loop(self) -> AbstractEventLoop:
        return get_running_loop()


class TypeAdapterCache:
    _cache: dict[type, TypeAdapter] = {}

    @classmethod
    def cache_annotation(cls, annotation: type) -> None:
        if annotation not in cls._cache:
            cls._cache[annotation] = TypeAdapter(annotation)

    @classmethod
    def get_type_adapter(cls, annotation: type) -> TypeAdapter:
        cls.cache_annotation(annotation)

        return cls._cache[annotation]
