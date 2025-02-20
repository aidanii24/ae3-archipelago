from dataclasses import dataclass, field
from enum import Enum, IntEnum
from logging import Logger
from time import sleep
from typing import Optional, List, Dict
import array
import dataclasses
import struct

from data.Items import Item
from data.Addresses import Address
from interface.pine import Pine

class ae_ps2_interface:
    ipc : Pine = Pine()
    status : connection_status = 0
    
    logger : Logger

    addresses : Address = None

    def unlock_equipment(ae3_item):
        ipc.write_int32(0x02)

class connection_status(Enum):
    DISCONNECTED = 0
    IN_MENU = 1
    IN_GAME = 2