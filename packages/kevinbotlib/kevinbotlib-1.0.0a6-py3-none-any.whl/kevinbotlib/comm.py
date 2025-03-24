import asyncio
import threading
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar

import orjson
import websockets
from pydantic import BaseModel

import kevinbotlib.exceptions
from kevinbotlib.logger import Logger as _Logger


class BaseSendable(BaseModel, ABC):
    """
    The base for all of KevinbotLib's sendables.

    _**What is a sendable?**_

    A sendable is a basic unit of data that can be transported through the `KevinbotCommClient` and server
    """

    timeout: float | None = None
    data_id: str = "kevinbotlib.dtype.null"
    """Internally used to differentiate sendable types"""
    flags: list[str] = []
    struct: dict[str, Any] = {}
    """Data structure _suggestion_ for use in dashboard applications"""

    def get_dict(self) -> dict:
        """Return the sendable in dictionary form

        Returns:
            dict: The sendable data
        """
        return {
            "timeout": self.timeout,
            "value": None,
            "did": self.data_id,
            "struct": self.struct,
        }


class SendableGenerator(ABC):
    """
    Abstract class for a function capable of being sent over `KevinbotCommClient`
    """

    @abstractmethod
    def generate_sendable(self) -> BaseSendable:
        """Abstract method to generate a sendable

        Returns:
            BaseSendable: The returned sendable
        """


class IntegerSendable(BaseSendable):
    value: int
    """Value to send"""
    data_id: str = "kevinbotlib.dtype.int"
    """Internally used to differentiate sendable types"""
    struct: dict[str, Any] = {"dashboard": [{"element": "value", "format": "raw"}]}
    """Data structure _suggestion_ for use in dashboard applications"""

    def get_dict(self) -> dict:
        """Return the sendable in dictionary form

        Returns:
            dict: The sendable data
        """
        data = super().get_dict()
        data["value"] = self.value
        return data


class BooleanSendable(BaseSendable):
    value: bool
    """Value to send"""
    data_id: str = "kevinbotlib.dtype.bool"
    """Internally used to differentiate sendable types"""
    struct: dict[str, Any] = {"dashboard": [{"element": "value", "format": "raw"}]}
    """Data structure _suggestion_ for use in dashboard applications"""

    def get_dict(self) -> dict:
        """Return the sendable in dictionary form

        Returns:
            dict: The sendable data
        """
        data = super().get_dict()
        data["value"] = self.value
        return data


class StringSendable(BaseSendable):
    value: str
    """Value to send"""
    data_id: str = "kevinbotlib.dtype.str"
    """Internally used to differentiate sendable types"""
    struct: dict[str, Any] = {"dashboard": [{"element": "value", "format": "raw"}]}
    """Data structure _suggestion_ for use in dashboard applications"""

    def get_dict(self) -> dict:
        """Return the sendable in dictionary form

        Returns:
            dict: The sendable data
        """
        data = super().get_dict()
        data["value"] = self.value
        return data


class FloatSendable(BaseSendable):
    value: float
    """Value to send"""
    data_id: str = "kevinbotlib.dtype.float"
    """Internally used to differentiate sendable types"""
    struct: dict[str, Any] = {"dashboard": [{"element": "value", "format": "raw"}]}
    """Data structure _suggestion_ for use in dashboard applications"""

    def get_dict(self) -> dict:
        """Return the sendable in dictionary form

        Returns:
            dict: The sendable data
        """
        data = super().get_dict()
        data["value"] = self.value
        return data


class AnyListSendable(BaseSendable):
    value: list
    """Value to send"""
    data_id: str = "kevinbotlib.dtype.list.any"
    """Internally used to differentiate sendable types"""
    struct: dict[str, Any] = {"dashboard": [{"element": "value", "format": "raw"}]}
    """Data structure _suggestion_ for use in dashboard applications"""

    def get_dict(self) -> dict:
        """Return the sendable in dictionary form

        Returns:
            dict: The sendable data
        """
        data = super().get_dict()
        data["value"] = self.value
        return data


class DictSendable(BaseSendable):
    value: dict
    """Value to send"""
    data_id: str = "kevinbotlib.dtype.dict"
    """Internally used to differentiate sendable types"""
    struct: dict[str, Any] = {"dashboard": [{"element": "value", "format": "raw"}]}
    """Data structure _suggestion_ for use in dashboard applications"""

    def get_dict(self) -> dict:
        """Return the sendable in dictionary form

        Returns:
            dict: The sendable data
        """
        data = super().get_dict()
        data["value"] = self.value
        return data


class BinarySendable(BaseSendable):
    value: bytes
    """Value to send"""
    data_id: str = "kevinbotlib.dtype.bin"
    """Internally used to differentiate sendable types"""
    struct: dict[str, Any] = {"dashboard": [{"element": "value", "format": "limit:1024"}]}
    """Data structure _suggestion_ for use in dashboard applications"""

    def get_dict(self) -> dict:
        """Return the sendable in dictionary form

        Returns:
            dict: The sendable data
        """
        data = super().get_dict()
        data["value"] = self.value.decode("utf-8")
        return data


T = TypeVar("T", bound=BaseSendable)


class CommPath:
    def __init__(self, path: "str | CommPath") -> None:
        if isinstance(path, CommPath):
            path = path.path
        self._path = path

    def __truediv__(self, new: str):
        return CommPath(self._path.rstrip("/") + "/" + new.lstrip("/"))

    def __str__(self) -> str:
        return self._path

    @property
    def path(self) -> str:
        return self._path


class CommunicationServer:
    """WebSocket-based server for handling real-time data synchronization."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8765) -> None:  # noqa: S104 # TODO: do we need to fix this
        self.host: str = host
        self.port: int = port

        self.logger = _Logger()

        self.data_store: dict[str, dict[str, Any]] = {}
        self.clients: set[websockets.ServerConnection] = set()
        self.tasks = set()

        self.serving = False

    async def remove_expired_data(self) -> None:
        """Periodically removes expired data based on timeouts."""
        while True:
            current_time = time.time()
            expired_keys = [
                key
                for key, entry in self.data_store.items()
                if entry["data"]["timeout"] and entry["tsu"] + entry["data"]["timeout"] < current_time
            ]
            for key in expired_keys:
                del self.data_store[key]
                await self.broadcast({"action": "delete", "key": key})
            await asyncio.sleep(1)

    async def broadcast(self, message: dict[str, Any]) -> None:
        """Broadcasts a message to all connected clients."""
        if self.clients:
            msg = orjson.dumps(message)
            await asyncio.gather(*(client.send(msg) for client in self.clients))

    async def handle_client(self, websocket: websockets.ServerConnection) -> None:
        """Handles incoming WebSocket connections."""
        self.clients.add(websocket)
        self.logger.info(f"New client connected: {websocket.id}")
        try:
            await websocket.send(orjson.dumps({"action": "sync", "data": self.data_store}))
            async for message in websocket:
                msg = orjson.loads(message)
                if msg["action"] == "publish":
                    key = msg["key"]
                    tsc = time.time() if key not in self.data_store else self.data_store[key]["tsc"]
                    self.data_store[key] = {
                        "data": msg["data"],
                        "tsu": time.time(),
                        "tsc": tsc,
                    }
                    await self.broadcast({"action": "update", "key": key, "data": self.data_store[key]})
                elif msg["action"] == "delete" and msg["key"] in self.data_store:
                    del self.data_store[msg["key"]]
                    await self.broadcast({"action": "delete", "key": msg["key"]})
        except websockets.ConnectionClosed:
            pass
        finally:
            self.logger.info(f"Client disconnected: {websocket.id}")
            self.clients.remove(websocket)

    async def serve_async(self) -> None:
        """Starts the WebSocket server."""
        self.logger.info("Starting a new KevinbotCommServer")
        server = await websockets.serve(self.handle_client, self.host, self.port, max_size=2**48 - 1, compression=None)
        task = asyncio.create_task(self.remove_expired_data())
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        self.serving = True
        await server.wait_closed()
        self.serving = False

    def serve(self):
        asyncio.run(self.serve_async())

    def wait_until_serving(self, timeout: float = 5.0):
        start_time = time.time()
        while not self.serving:
            if time.time() > start_time + timeout:
                msg = "The server is not serving. You most likely called `wait_until_serving` before starting the server, or the server failed to start"
                raise kevinbotlib.exceptions.ServerTimeoutException(msg)
            time.sleep(0.02)


class CommunicationClient:
    """KevinbotLib WebSocket-based client for real-time data synchronization and communication."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8765,
        on_update: Callable[[str, Any], None] | None = None,
        on_delete: Callable[[str], None] | None = None,
        on_connect: Callable[[], None] | None = None,
        on_disconnect: Callable[[], None] | None = None,
        *,
        auto_reconnect: bool = True,
        register_basic_types: bool = True,
    ) -> None:
        self._host = host
        self._port = port
        self.auto_reconnect = auto_reconnect

        self.logger = _Logger()

        self.data_store: dict[str, Any] = {}
        self.data_types: dict[str, type[BaseSendable]] = {}

        self.running = False
        self.websocket: websockets.ClientConnection | None = None
        self.loop = asyncio.get_event_loop()
        self.thread: threading.Thread | None = None

        self.on_update = on_update
        self.on_delete = on_delete
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect

        # Modified to store a list of (data_type, callback) tuples per key
        self.hooks: dict[str, list[tuple[type[BaseSendable], Callable[[str, BaseSendable | None], Any]]]] = {}

        if register_basic_types:
            self.register_type(BaseSendable)
            self.register_type(IntegerSendable)
            self.register_type(BooleanSendable)
            self.register_type(StringSendable)
            self.register_type(FloatSendable)
            self.register_type(AnyListSendable)
            self.register_type(DictSendable)

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value
        if self.is_connected():
            self.disconnect()
            self.connect()

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value: str):
        self._port = value
        if self.is_connected():
            self.disconnect()
            self.connect()

    def get_latency(self) -> float:
        return self.websocket.latency if self.websocket else float("inf")

    def register_type(self, data_type: type[BaseSendable]):
        self.data_types[data_type.model_fields["data_id"].default] = data_type
        self.logger.trace(
            f"Registered data type of id {data_type.model_fields['data_id'].default} as {data_type.__name__}"
        )

    def connect(self) -> None:
        """Starts the client in a background thread."""
        if self.running:
            self.logger.warning("Client is already running")
            return

        self.running = True
        self.thread = threading.Thread(
            target=self._run_async_loop,
            daemon=True,
            name="KevinbotLib.CommClient.AsyncLoop",
        )
        self.thread.start()

    def wait_until_connected(self, timeout: float = 5.0):
        start_time = time.time()
        while not self.websocket:
            if time.time() > start_time + timeout:
                msg = "The connection timed out"
                raise kevinbotlib.exceptions.HandshakeTimeoutException(msg)
            time.sleep(0.02)

    def is_connected(self):
        return bool(self.websocket)

    def disconnect(self) -> None:
        """Stops the client and closes the connection gracefully."""
        self.running = False
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self._close_connection(), self.loop)

    def _run_async_loop(self) -> None:
        """Runs the async event loop in a separate thread."""
        asyncio.set_event_loop(self.loop)
        if not self.loop.is_running():
            self.loop.run_until_complete(self._connect_and_listen())
        else:
            asyncio.run_coroutine_threadsafe(self._connect_and_listen(), self.loop)

    async def _connect_and_listen(self) -> None:
        """Handles connection and message listening."""
        prev_connection = False
        while self.running:
            try:
                async with websockets.connect(
                    f"ws://{self._host}:{self._port}",
                    max_size=2**48 - 1,
                    ping_interval=1,
                    compression=None,
                ) as ws:
                    self.websocket = ws
                    if not prev_connection:
                        self.logger.info("Connected to the server")
                        if self.on_connect:
                            self.on_connect()
                    prev_connection = True
                    await self._handle_messages()
            except (
                websockets.ConnectionClosed,
                ConnectionError,
                OSError,
                websockets.InvalidMessage,
            ) as e:
                self.logger.error(f"Unexpected error: {e!r}")
                self.websocket = None
                if prev_connection and self.on_disconnect:
                    self.on_disconnect()
                    self.data_store = {}
                prev_connection = False
                if self.auto_reconnect and self.running:
                    self.logger.warning("Can't connect to server, retrying...")
                    await asyncio.sleep(1)
                else:
                    break

    async def _handle_messages(self) -> None:
        """Processes incoming messages."""
        if not self.websocket:
            return
        try:
            async for message in self.websocket:
                data = orjson.loads(message)

                if data["action"] == "sync":
                    for hook in self.hooks:
                        if data["data"].get(hook) != self.data_store.get(hook):
                            # Call all callbacks for this hook
                            for hook_type, callback in self.hooks[hook]:
                                callback(hook, hook_type(**data["data"].get(hook)["data"]))
                    self.data_store = data["data"]
                elif data["action"] == "update":
                    key, value = data["key"], data["data"]
                    self.data_store[key] = value
                    if self.on_update:
                        self.on_update(key, value)
                    if key in self.hooks:
                        # Call all callbacks for this key
                        for hook_type, callback in self.hooks[key]:
                            callback(key, hook_type(**data["data"]["data"]))
                elif data["action"] == "delete":
                    key = data["key"]
                    self.data_store.pop(key, None)
                    if self.on_delete:
                        self.on_delete(key)
                    if key in self.hooks:
                        # Call all callbacks with None for this key
                        for _, callback in self.hooks[key]:
                            callback(key, None)
        except orjson.JSONDecodeError as e:
            self.logger.error(f"Error processing messages: {e}")

    async def _close_connection(self) -> None:
        """Closes the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            self.logger.info("Connection closed")
            if self.on_disconnect:
                self.on_disconnect()
            self.websocket = None

    def add_hook(
        self,
        key: str | CommPath,
        data_type: type[T],
        callback: Callable[[str, T | None], Any],
    ):
        """Adds a hook for when new data is received from the key.

        Args:
            key (str | CommPath): Key for data hook
            data_type (type[T]): Expected data type for the hook
            callback (Callable[[str, T | None], Any]): Callback to invoke when data changes
        """
        if isinstance(key, CommPath):
            key = key.path

        if key not in self.hooks:
            self.hooks[key] = []
        self.hooks[key].append((data_type, callback))  # type: ignore

    def send(self, key: str | CommPath, data: BaseSendable | SendableGenerator) -> None:
        """Publishes data to the server."""
        if not self.running or not self.websocket:
            self.logger.error(f"Cannot publish to {key}: client is not connected")
            return

        if isinstance(key, CommPath):
            key = key.path

        if isinstance(data, SendableGenerator):
            data = data.generate_sendable()

        async def _publish() -> None:
            if not self.websocket:
                return
            message = orjson.dumps({"action": "publish", "key": key, "data": data.get_dict()})
            await self.websocket.send(message)

        asyncio.run_coroutine_threadsafe(_publish(), self.loop)

    def get(self, key: str | CommPath, data_type: type[T], default: Any = None) -> T | None:
        """Retrieves stored data."""
        if isinstance(key, CommPath):
            key = key.path

        if key not in self.data_store:
            return None
        if self.data_store.get(key, default)["data"]["did"] != data_type.model_fields["data_id"].default:
            self.logger.error(
                f"Couldn't get value of {key}, requested value of id {data_type.model_fields['data_id'].default}, got one of {self.data_store.get(key, default)['data']['did']}"
            )
            return None

        return data_type(**self.data_store.get(key, default)["data"])

    def get_raw(self, key: str | CommPath) -> dict | None:
        if isinstance(key, CommPath):
            key = key.path

        if key not in self.data_store:
            return None

        return self.data_store.get(key, None)["data"]

    def get_keys(self):
        return list(self.data_store.keys())

    def delete(self, key: str | CommPath) -> None:
        """Deletes data from the server."""
        if isinstance(key, CommPath):
            key = key.path

        if not self.running or not self.websocket:
            self.logger.error("Cannot delete: client is not connected")
            return

        async def _delete() -> None:
            if not self.websocket:
                return
            message = orjson.dumps({"action": "delete", "key": key})
            await self.websocket.send(message)

        asyncio.run_coroutine_threadsafe(_delete(), self.loop)
