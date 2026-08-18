from typing import Any

from NetUtils import ClientStatus

from ..data.Strings import APHelper

try:
    from worlds.tracker.TrackerClient import TrackerGameContext as ClientContext
except ImportError:
    from CommonClient import CommonContext as ClientContext


class DataStorageHandler:
    def __init__(self, protocol: "Protocol", key: str, default: Any, want_reply: bool = False):
        self.protocol = protocol
        self.operations: list[dict[str, Any]] = []
        self.done: bool = False

        self.cmd: dict[str, Any] = {
            "cmd": "Set",
            "key": self.protocol.generate_key_name(key),
            "default": default,
            "operations": self.operations,
        }

        if want_reply:
            self.cmd["want_reply"] = True

    def replace(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "replace",
                "value": value,
            }
        )

    def default(self):
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "default",
                "value": None,
            }
        )

    def add(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "add",
                "value": value,
            }
        )

    def multiply(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "mul",
                "value": value,
            }
        )

    def pow(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "pow",
                "value": value,
            }
        )

    def mod(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "mod",
                "value": value,
            }
        )

    def floor(self) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "floor",
                "value": None,
            }
        )

    def ceil(self) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "ceil",
                "value": None,
            }
        )

    def max(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "max",
                "value": value,
            }
        )

    def min(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "min",
                "value": value,
            }
        )

    def andOp(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "and",
                "value": value,
            }
        )

    def orOp(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "or",
                "value": value,
            }
        )

    def xor(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "xor",
                "value": value,
            }
        )

    def lshift(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "left_shift",
                "value": value,
            }
        )

    def rshift(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "right_shift",
                "value": value,
            }
        )

    def pop(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "pop",
                "value": value,
            }
        )

    def update(self, value: Any) -> None:
        if self.done:
            raise ValueError("This Datastorage has already been finalized and can no longer accept more operations")

        self.operations.append(
            {
                "operation": "update",
                "value": value,
            }
        )

    def end(self):
        if not self.operations:
            return

        self.protocol.msgs.append(self.cmd)
        self.done = True


class Protocol:
    def __init__(self, ctx: ClientContext):
        self.ctx: ClientContext = ctx
        self.msgs: list = []

    def __bool__(self) -> bool:
        return bool(self.ctx.server)

    def generate_key_name(self, basename: str) -> str:
        return "_".join([APHelper.data_id.value, str(self.ctx.team), str(self.ctx.slot), basename])

    def send_locations_checks(self, locations: set[int]) -> None:
        self.msgs.append({"cmd": "LocationChecks", "locations": locations})

    def create_hints(self, locations: list[int]) -> None:
        self.msgs.append(
            {
                "cmd": "CreateHints",
                "locations": locations,
                "player": self.ctx.slot,
            }
        )

    def update_status(self, status: ClientStatus):
        self.msgs.append(
            {
                "cmd": "StatusUpdate",
                "status": status,
            }
        )

    def create_datastorage_setter(self, key: str, default: Any, want_reply: bool = False) -> DataStorageHandler:
        return DataStorageHandler(self, key, default, want_reply)

    def get_datastorage_key(self, *keys) -> None:
        self.msgs.append({"cmd": "Get", "keys": [self.generate_key_name(key) for key in keys]})

    async def send(self):
        if not self.msgs:
            return
        if not self.ctx.server:
            raise ServerUnavailableError

        await self.ctx.send_msgs(self.msgs)

        self.msgs.clear()


class ProtocolError(Exception):
    pass


class ServerUnavailableError(ProtocolError):
    def __init__(self, message: str = "Server unavailable"):
        self.message = message
        super().__init__(self.message)
