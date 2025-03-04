from typing import Optional
from logging import Logger
from enum import Enum

from .data.Addresses import BUTTON_INDEX, GADGET_INDEX, GameStates
from .data.Strings import Meta, Game, APConsole
from .interface.pine import Pine

### [< --- HELPERS --- >]
class ConnectionStatus(Enum):
    DISCONNECTED = 0
    IN_MENU = 1
    IN_GAME = 2

### [< --- INTERFACE --- >]
class AEPS2Interface:
    pine : Pine = Pine()
    status : ConnectionStatus = 0

    loaded_game : Optional[str] = None

    sync_task = None
    logger : Logger

    will_auto_equip : bool = True

    def __init__(self, logger : Logger):
        self.logger = logger

    # { PINE Network }
    def connect_game(self):
        if not self.pine.is_connected():
            self.pine.connect()

            if not self.pine.is_connected():
                return

            self.logger.info(APConsole.Info.init.value)

        try:
            self.logger.info(APConsole.Info.p_init_g)
            game_id : str = self.pine.get_game_id()

            self.loaded_game = None
            if game_id in Meta.sup_ver.value:
                self.loaded_game = game_id
            else:
                self.logger.warning(APConsole.Err.game_wrong.value)
        except RuntimeError:
            pass
        except ConnectionError:
            pass

    def disconnect_game(self):
        self.pine.disconnect()
        self.loaded_game = None
        self.logger.info(APConsole.Err.sock_disc)

    def get_connection_state(self) -> bool:
        try:
            connected : bool = self.pine.is_connected()

            return not (not connected or self.loaded_game is None)
        except RuntimeError:
            return False

    # { Game Check }
    def get_player_state(self) -> int:
        value : int = self.pine.read_int32(GameStates[Game.state.value].value)
        return value

    def can_control(self) -> bool:
        value : int = self.get_player_state()
        return value == 0x00 or value == 0x02

    # { Game Manipulation }
    def unlock_equipment(self, address: int = 0):
        self.pine.write_int32(address, 2)

        if self.will_auto_equip:
            self.auto_equip(GADGET_INDEX.index(address))

    def auto_equip(self, gadget_id: int):
        for button in BUTTON_INDEX:
            value = self.pine.read_int32(button)
            if value != 0x0:
                continue

            self.pine.write_int32(button, gadget_id)
