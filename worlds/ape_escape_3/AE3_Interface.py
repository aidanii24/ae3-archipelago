from enum import Enum
from logging import Logger
from typing import List

from .data.Addresses import Address
from .interface.pine import Pine


class ConnectionStatus(Enum):
    DISCONNECTED = 0
    IN_MENU = 1
    IN_GAME = 2


class AEPS2Interface:
    ipc: Pine = Pine()
    status: ConnectionStatus = 0

    sync_task = None
    logger: Logger

    addresses: Address = None

    will_auto_equip: bool = True

    buttons: List[int] = [Address.player["equip_triangle"], Address.player["equip_cross"],
                          Address.player["equip_square"], Address.player["equip_circle"]]

    # PINE Connection
    def connect_game(self):
        if not self.ipc.is_connected():
            self.ipc.connect()

            if not self.ipc.is_connected:
                return

            self.logger.info("Connected to PCSX2.")

    def disconnect_game(self):
        self.ipc.disconnect()
        self.logger.info("Disconnected from PCSX2")

    # Game Manipulation
    def unlock_equipment(self, addr: int = 0):
        self.ipc.write_int32(Address.items["sky_flyer"], 2)  # Test: unlocks Sky Flyer

        if self.will_auto_equip:
            self.auto_equip(7)

    def auto_equip(self, btn_id: int):
        for button in self.buttons:
            if button != 0:
                continue

            self.ipc.write_int32(button, btn_id)

    def steal_equipment(self):
        self.ipc.write_int32(Address.items.sky_flyer, 1)

        for button in self.buttons:
            if button != 6:
                continue

            self.ipc.write_int32(button, 0)
