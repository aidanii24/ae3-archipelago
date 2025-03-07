from typing import Optional
from logging import Logger
from enum import Enum
import struct

from .data.Addresses import BUTTON_INDEX, BUTTON_INTUIT_INDEX, GameStates, Pointers, get_gadget_id
from .data.Strings import Meta, Game, APConsole
from .interface.pine import Pine


### [< --- HELPERS --- >]
class ConnectionStatus(Enum):
    WRONG_GAME = -1
    DISCONNECTED = 0
    CONNECTED = 1
    IN_GAME = 2

### [< --- INTERFACE --- >]
class AEPS2Interface:
    pine : Pine = Pine()
    status : ConnectionStatus = 0

    loaded_game : Optional[str] = None

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

        # Check for Game running in PCSX2
        try:
            if self.status is ConnectionStatus.CONNECTED:
                self.logger.info(APConsole.Info.p_init_g.value)

            game_id : str = self.pine.get_game_id()

            self.loaded_game = None

            if game_id in Meta.supported_versions:
                self.loaded_game = game_id
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

    # { Game Check }
    def get_player_state(self) -> int:
        value : int = self.pine.read_int32(GameStates[Game.state.value])
        return value

    def can_control(self) -> bool:
        value : int = self.get_player_state()
        return value == 0x00 or value == 0x02

    # { Game Manipulation }
    def set_progress(self, address : int, progress : str):
        as_bytes : bytes = progress.encode() + b'\x00'
        self.pine.write_bytes(address, as_bytes)

    def clear_equipment(self):
        for button in BUTTON_INDEX:
            self.pine.write_int32(button, 0x0)

    def unlock_equipment(self, address: int = 0, auto_equip : bool = False):
        self.pine.write_int32(address, 0x2)

        if auto_equip:
            self.auto_equip(get_gadget_id(address))

    def auto_equip(self, gadget_id: int):
        if gadget_id <= 0:
            return

        target : int = -1
        for button in BUTTON_INTUIT_INDEX:
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

    def give_collectable(self, address : int, amount : int | float = 0x1):
        current : int = self.pine.read_int32(address)

        if isinstance(amount, int):
            self.pine.write_int32(address, current + amount)
        elif isinstance(amount, float):
            # Workaround for now; pine.write_float() seems to be broken
            ## Reinterpret read value as float
            current_as_hex : str = f'{current:x}'
            current_as_float : float = struct.unpack('!f', bytes.fromhex(current_as_hex))[0]

            ## Get New Value
            new : float = current_as_float + amount

            ## Convert new value to an int that will be interpreted as the same hexadecimal value as the float
            new_as_int : int = int(hex(struct.unpack("<I", struct.pack("<f", new))[0]), 16)

            self.pine.write_int32(address, new_as_int)

    def give_morph_energy(self, amount : float = 3.0):
        # Check recharge state first
        address : int = GameStates[Game.morph_gauge_recharge.value]
        value : int = self.pine.read_int32(address)

        if value != 0x0:
            self.pine.write_float(address, float(value + amount))
            return

        # If recharge state is 0, we check the active gauge, following its pointer chain
        address = GameStates[Game.morph_gauge_active.value]
        for pointer in Pointers[address]:
            address += self.pine.read_int32(address) + pointer

        value = self.pine.read_int32(address)
        self.pine.write_float(address, value + amount)