from dataclasses import dataclass, field
from enum import Enum, IntEnum
from logging import Logger
from time import sleep
from typing import Optional, List, Dict
import array
import dataclasses
import struct

from .data.Addresses import Address
from .data.Items import Item
from .interface.pine import Pine

class ae_ps2_interface:
    ipc : Pine = Pine()
    status : connection_status = 0
    
    sync_task = None
    logger : Logger

    addresses : Address = None

    will_auto_equip : bool = true

    buttons : List[int] = [Address.player.equip_triangle, Address.player.equip_cross, Address.player.equip_square,
            Address.player.equip_circle]

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
    def unlock_equipment(self, address : int = 0):
        ipc.write_int32(Address.items.sky_flyer, 2)    # Test: unlocks Sky Flyer

        if self.will_auto_equip:
            auto_equip(7)
    
    def auto_equip(self, id : int):
        target : int = 0
        
        for button in buttons:
            if button != 0:
                continue

            ipc.write_int32(button, id)
    
    def steal_equipment(self):
        ipc.write_int32(Address.items.sky_flyer, 1)

        for button in buttons:
            if button != 6:
                continue
            
            ipc.write_int32(button, 0)


class connection_status(Enum):
    DISCONNECTED = 0
    IN_MENU = 1
    IN_GAME = 2