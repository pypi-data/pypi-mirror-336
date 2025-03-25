import asyncio
import uuid
from typing import TypeVar, Generic

from .historian import Historian, find_historian, SUSPENDED, wrap_methods_as_historian_events


#
# Note: The following Queue and Event classes
# are intended to be used as type hints
#


class Queue:
    def __init__(self):
        self._queue = asyncio.Queue()

    async def put(self, item):
        return await self._queue.put(item)

    async def get(self):
        return await self._queue.get()

    async def empty(self):
        return self._queue.empty()


class Event:
    # Why this class?
    # When wrapped for historians, all methods become async
    # So this class gives async versions of the methods
    # so IDEs and typehints indicate the actual behavior
    def __init__(self):
        self._event = asyncio.Event()

    async def wait(self):
        await self._event.wait()

    async def set(self):
        self._event.set()

    async def clear(self):
        self._event.clear()

    async def is_set(self):
        return self._event.is_set()


class State:
    def __init__(self, value):
        self._value = value

    async def get(self):
        return self._value

    async def set(self, value):
        self._value = value

    def value(self):
        # TODO - why do we need this?
        return self._value


class IdentityQueue:
    """Put and Get return and identity + the value"""
    def __init__(self, *args, **kwargs):
        self._queue = asyncio.Queue(*args, **kwargs)

    async def put(self, value):
        identity = str(uuid.uuid4())
        return identity, await self._queue.put((identity, value))

    async def get(self):
        return await self._queue.get()


T = TypeVar('T')


class InternalResource(Generic[T]):
    """Internal resources are used inside the workflow context"""

    def __init__(self, name, identity, resource: T):
        self._name = name
        self._identity = identity
        self._resource: T = resource
        self._historian = find_historian()

    async def __aenter__(self) -> T:
        await self._historian.register_resource(self._name, self._identity, self._resource)
        return wrap_methods_as_historian_events(self._resource, self._name, self._identity, self._historian)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        suspending = (exc_type == asyncio.CancelledError and exc_val.args and exc_val.args[0] == SUSPENDED)
        await self._historian.delete_resource(self._name, self._identity, suspending=suspending)


def queue(name, identity):
    return InternalResource(name, identity, Queue())


def event(name, identity):
    return InternalResource(name, identity, Event())


def state(name, identity, value):
    return InternalResource(name, identity, State(value))


def identity_queue(name):
    return InternalResource(name, None, IdentityQueue())

class _ResourceWrapper:
    def __init__(self, name: str, identity: str | None, historian: 'Historian', resource_class):
        self._name = name
        self._identity = identity
        self._historian = historian
        self._resource_class = resource_class

    # TODO: Is it fine that we essentially don't do anything if `field` is an attribute or private?
    def __getattr__(self, field):
        if field.startswith('_'):
            return
        if not callable(getattr(self._resource_class, field)):
            return

        async def wrapper(*args, _name=self._name, _identity=self._identity, **kwargs):
            return await self._historian.record_external_event(_name, _identity, field, *args, **kwargs)

        return wrapper

def wrap_as_queue(name: str, identity: str | None, historian: Historian) -> Queue:
    return _ResourceWrapper(name, identity, historian, Queue)

def wrap_as_event(name: str, identity: str | None, historian: Historian) -> Event:
    return _ResourceWrapper(name, identity, historian, Event)

def wrap_as_state(name: str, identity: str | None, historian: Historian) -> State:
    return _ResourceWrapper(name, identity, historian, State)

def wrap_as_identity_queue(name: str, identity: str | None, historian: Historian) -> IdentityQueue:
    return _ResourceWrapper(name, identity, historian, IdentityQueue)