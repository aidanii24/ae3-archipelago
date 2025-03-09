from typing import Optional, Sequence
from logging import Logger
from enum import Enum
import struct

from .data.Addresses import VersionAddresses, get_version_addresses
from .data.Strings import APHelper, Meta, Game, APConsole
from .interface.pine import Pine


### [< --- HELPERS --- >]
class ConnectionStatus(Enum):
    WRONG_GAME = -1
    DISCONNECTED = 0
    CONNECTED = 1
    IN_GAME = 2

# Workaround for now; pine.write_float() seems to be broken
def hex_int32_to_float(value : int) -> float:
    ## Reinterpret read value as float
    current_as_hex: str = f'{value:x}'
    current_as_float: float = struct.unpack('!f', bytes.fromhex(current_as_hex))[0]

    return current_as_float

def float_to_hex_int32(value : float) -> int:
    return int(hex(struct.unpack("<I", struct.pack("<f", value))[0]), 16)

### [< --- INTERFACE --- >]
class AEPS2Interface:
    pine : Pine = Pine()
    status : ConnectionStatus = ConnectionStatus.DISCONNECTED

    loaded_game : Optional[str] = None
    addresses : VersionAddresses = None
    cached_pointer_targets : dict[int, int] = {}

    sync_task = None
    logger : Logger

    def __init__(self, logger : Logger):
        self.logger = logger

    # { PINE Network }
    def connect_game(self):
        # Check for connection with PCSX2
        if not self.pine.is_connected():
            self.pine.connect()

            if not self.pine.is_connected():
                self.status = ConnectionStatus.DISCONNECTED
                return

            self.logger.info(APConsole.Info.init.value)

            # Erase cache when reconnecting, to ensure its correct
            self.cached_pointer_targets.clear()

        # Check for Game running in PCSX2
        try:
            if self.status is ConnectionStatus.CONNECTED:
                self.logger.info(APConsole.Info.p_init_g.value)

            game_id : str = self.pine.get_game_id()

            self.loaded_game = None

            if game_id in Meta.supported_versions:
                self.loaded_game = game_id
                self.addresses = get_version_addresses(self.loaded_game)
                self.status =  ConnectionStatus.IN_GAME
            elif not self.status is ConnectionStatus.WRONG_GAME:
                self.logger.warning(APConsole.Err.game_wrong.value)
                self.status = ConnectionStatus.WRONG_GAME
        except RuntimeError:
            return
        except ConnectionError:
            return

        if self.status is ConnectionStatus.DISCONNECTED:
            self.status = ConnectionStatus.CONNECTED

    def disconnect_game(self):
        self.pine.disconnect()
        self.loaded_game = None
        self.logger.info(APConsole.Err.sock_disc.value)

    def get_connection_state(self) -> bool:
        try:
            connected : bool = self.pine.is_connected()

            return not (not connected or self.loaded_game is None)
        except RuntimeError:
            return False

    # { Generic }
    def check_pointers_updated(self):
        return bool(self.cached_pointer_targets)

    def follow_pointer_chain(self, start_addr : int) -> int:
        # Get first pointer
        addr : int = self.pine.read_int32(start_addr)

        # Loop through remaining pointers and adding the offsets
        ptrs : Sequence = self.addresses.Pointers[start_addr]
        amt : int = len(ptrs) - 1
        for offset in self.addresses.Pointers[start_addr]:
            addr += offset

            # Do not read value for the last offset
            if ptrs.index(offset) >= amt:
                return addr

            addr = self.pine.read_int32(addr)

            # Getting an Address of 0 means the pointer has not been set yet
            if addr == 0x0:
                return 0x0

        return 0x0

    # { Game Check }
    def get_progress(self) -> str:
        addr : int = self.addresses.GameStates[Game.progress.value]
        addr = self.follow_pointer_chain(addr)

        if addr == 0:
            return "none"

        value: bytes = self.pine.read_bytes(addr, 8)
        value_decoded: str = bytes.decode(value)
        return value_decoded

    def get_unlocked_stages(self) -> int:
        return self.pine.read_int32(self.addresses.GameStates[Game.levels_unlocked.value])

    def get_stage(self) -> str:
        stage_as_bytes : bytes = self.pine.read_bytes(self.addresses.GameStates[Game.current_stage.value], 4)
        return stage_as_bytes.decode("utf-8")

    def check_in_stage(self) -> bool:
        value : int = self.pine.read_int8(self.addresses.GameStates[Game.current_stage.value])
        return value > 0

    def check_warp_gate_state(self) -> bool:
        value : int = self.pine.read_int8(self.addresses.GameStates[Game.on_warp_gate.value])
        return value != 0

    def check_level_confirmed_state(self) -> bool:
        value: int = self.pine.read_int8(self.addresses.GameStates[Game.level_confirmed.value])
        return value != 0

    def get_player_state(self) -> int:
        value : int = self.pine.read_int32(self.addresses.GameStates[Game.state.value])
        return value

    def check_control(self) -> bool:
        value : int = self.get_player_state()
        return value != 0x00 and value != 0x02

    def is_monkey_captured(self, name : str) -> bool:
        address : int = self.addresses.Locations[name]
        return self.pine.read_int8(address) == 0x01

    # { Game Manipulation }
    def set_progress(self, progress : str = APHelper.round2.value):
        addr : int = self.addresses.GameStates[Game.progress.value]
        addr = self.follow_pointer_chain(addr)

        if addr == 0x0:
            return

        as_bytes : bytes = progress.encode() + b'\x00'
        self.pine.write_bytes(addr, as_bytes)

    def set_unlocked_levels(self, index : int):
        self.pine.write_int32(self.addresses.GameStates[Game.levels_unlocked.value], index)

    def clear_equipment(self):
        for button in self.addresses.BUTTONS_BY_INTERNAL:
            self.pine.write_int32(button, 0x0)

    def unlock_equipment(self, address_name : str, auto_equip : bool = False):
        address : int = self.addresses.Items[address_name]
        self.pine.write_int32(self.addresses.Items[address_name], 0x2)

        if auto_equip:
            self.auto_equip(self.addresses.get_gadget_id(address))

    def lock_equipment(self, address_name : str):
        self.pine.write_int32(self.addresses.Items[address_name], 0x1)

    def auto_equip(self, gadget_id: int):
        if gadget_id <= 0:
            return

        target : int = -1
        for button in self.addresses.BUTTONS_BY_INTUIT:
            value = self.pine.read_int32(button)

            # Do not auto-equip when gadget is already assigned
            if value == gadget_id:
                return

            if value != 0x0:
                continue

            if target < 0:
                target = button
                continue

        if target >= 0:
            self.pine.write_int32(target, gadget_id)

    def give_collectable(self, address_name : str, amount : int | float = 0x1):
        address : int = self.addresses.GameStates[address_name]
        current : int = self.pine.read_int32(address)

        if isinstance(amount, int):
            self.pine.write_int32(address, current + amount)
        elif isinstance(amount, float):
            # Workaround for now; pine.write_float() seems to be broken
            ## Reinterpret read value as float
            current_as_float : float = hex_int32_to_float(current)

            ## Convert new value to an int that will be represented as the same hexadecimal value as the float
            new_as_int : int = float_to_hex_int32(current_as_float + amount)

            self.pine.write_int32(address, new_as_int)

    def give_morph_energy(self, amount : float = 3.0):
        # Check recharge state first
        address : int = self.addresses.GameStates[Game.morph_gauge_recharge.value]
        value : int = self.pine.read_int32(address)

        if value != 0x0:
            # Ranges from 0 to 100 for every Morph Stock, with a maximum of 1100 for all 10 Stocks filled.
            value_as_float : float = hex_int32_to_float(value) + (amount / 30.0 * 100.0)
            value : int = float_to_hex_int32(value_as_float)

            self.pine.write_int32(address, value)
            return

        # If recharge state is 0, we check the active gauge, following its pointer chain
        address = self.follow_pointer_chain(self.addresses.GameStates[Game.morph_gauge_active.value])

        if address == 0x0:
            return

        value : int = self.pine.read_int32(address)
        # Ranges from 0 to 30 in vanilla game.
        value_as_float: float = hex_int32_to_float(value) + amount
        value = float_to_hex_int32(value_as_float)
        self.pine.write_int32(address, value)