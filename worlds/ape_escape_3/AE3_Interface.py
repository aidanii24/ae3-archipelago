from typing import Optional, Sequence
from logging import Logger
from enum import Enum
from math import ceil

from .data.Addresses import VersionAddresses, get_version_addresses
from .data.Items import HUD_OFFSETS
from .data.Locations import CELLPHONES_ID_DUPLICATES, CELLPHONES_STAGE_DUPLICATES, BOSSES_ALTERNATIVE
from .data.Stages import LEVELS_ID_BY_ORDER
from .data.Strings import Itm, Loc, Meta, Game, APHelper, APConsole
from .interface.pine import Pine


### [< --- HELPERS --- >]
class ConnectionStatus(Enum):
    WRONG_GAME = -1
    DISCONNECTED = 0
    CONNECTED = 1
    IN_GAME = 2

    def __bool__(self):
        return self.value > 0


### [< --- INTERFACE --- >]
class AEPS2Interface:
    pine : Pine = Pine()
    status : ConnectionStatus = ConnectionStatus.DISCONNECTED

    loaded_game : Optional[str] = None
    addresses : VersionAddresses = None

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

    def follow_pointer_chain(self, start_address : int, pointer_chain : str) -> int:
        # Get first pointer
        addr : int = self.pine.read_int32(start_address)

        # If pointer is 0, return immediately
        if addr <= 0x0:
            return 0x0

        # Loop through remaining pointers and adding the offsets
        ptrs : Sequence = self.addresses.Pointers[pointer_chain]
        amt : int = len(ptrs) - 1
        for i, offset in enumerate(self.addresses.Pointers[pointer_chain]):
            addr += offset

            # Do not read value for the last offset
            if i >= amt:
                return addr

            addr = self.pine.read_int32(addr)

            # Getting an Address of 0 means the pointer has not been set yet
            if addr == 0x0:
                return 0x0

        return 0x0

    # { Game Check }
    def get_progress(self) -> str:
        addr : int = self.addresses.GameStates[Game.progress.value]
        addr = self.follow_pointer_chain(addr, Game.progress.value)

        if addr == 0:
            return "None"

        value: bytes = self.pine.read_bytes(addr, 8)
        value_decoded: str = bytes.decode(value).replace("\x00", "")
        return value_decoded

    def get_unlocked_channels(self) -> int:
        return self.pine.read_int32(self.addresses.GameStates[Game.channels_unlocked.value])

    def get_selected_channel(self) -> int:
        return self.pine.read_int32(self.addresses.GameStates[Game.channel_selected.value])

    def get_next_channel_choice(self) -> str:
        addr: int = self.follow_pointer_chain(self.addresses.GameStates[Game.progress.value],
                                              Game.channel_next_choice.value)

        if addr == 0x0:
            return ""

        length: int = 4

        # Check length of string in multiples of 4
        for _ in range(2):
            if self.pine.read_bytes(addr + (4 * (_ + 1)), 1) == b'\x00':
                break

            length = max(length + 4, 12)

        id_as_bytes : bytes = self.pine.read_bytes(self.addresses.GameStates[Game.current_channel.value], length)

        # Convert to String
        return id_as_bytes.decode("utf-8").replace("\x00", "")

    def get_channel(self) -> str:
        channel_as_bytes : bytes = self.pine.read_bytes(self.addresses.GameStates[Game.current_channel.value], 4)
        # Decode to String and remove null bytes if present
        return channel_as_bytes.decode("utf-8").replace("\x00", "")

    def get_stage(self) -> str:
        address : int = self.addresses.GameStates[Game.current_room.value]
        length : int = 4

        # Check length of string in multiples of 4
        for _ in range(2):
            if self.pine.read_bytes(address + (4 * (_ + 1)), 1) == b'\x00':
                break

            length = max(length + 4, 12)

        # Decode to string and remove null bytes
        room_as_bytes : bytes = self.pine.read_bytes(self.addresses.GameStates[Game.current_room.value], length)
        return room_as_bytes.decode("utf-8").replace("\x00", "")

    def get_activated_game_mode(self) -> int:
        address = self.addresses.GameStates[Game.game_mode.value]

        return self.pine.read_int32(address)

    def get_current_game_mode(self) -> int:
        address = self.follow_pointer_chain(self.addresses.GameStates[Game.status_tracker.value], Game.game_mode.value)
        if not address:
            return -1

        return self.pine.read_int32(address)

    def check_in_stage(self) -> bool:
        value : int = self.pine.read_int8(self.addresses.GameStates[Game.current_channel.value])
        return value > 0

    def is_on_warp_gate(self) -> bool:
        value : int = self.pine.read_int8(self.addresses.GameStates[Game.on_warp_gate.value])
        return value != 0

    def is_a_level_confirmed(self) -> bool:
        value: int = self.pine.read_int8(self.addresses.GameStates[Game.channel_confirmed.value])
        return value != 0

    def get_character(self) -> int:
        return self.pine.read_int32(self.addresses.GameStates[Game.character.value])

    def get_cookies(self) -> float:
        return self.pine.read_float(self.addresses.GameStates[Game.cookies.value])

    def is_equipment_unlocked(self, address_name : str) -> bool:
        # Redirect address to RC Car if the unlocked equipment is an RC Car Chassis
        if "Chassis" in address_name:
            is_variant_unlocked = self.is_chassis_unlocked(address_name)
            address_name = Itm.gadget_rcc.value
        else:
            is_variant_unlocked = True

        return self.pine.read_int32(self.addresses.Items[address_name]) == 0x2 and is_variant_unlocked

    def is_chassis_unlocked(self, chassis_name : str) -> bool:
        if chassis_name not in Itm.get_chassis_by_id():
            return True

        return self.pine.read_int8(self.addresses.Items[chassis_name]) == 0x1

    def get_current_morph(self):
        return self.pine.read_int8(self.addresses.GameStates[Game.current_morph.value])

    def get_morph_duration(self, character : int = 0) -> float:
        return self.pine.read_int32(self.addresses.get_morph_duration_addresses(character)[0])

    def get_player_state(self) -> int:
        return self.pine.read_int32(self.addresses.GameStates[Game.state.value])

    def get_current_gadget(self) -> int:
        address : int = self.follow_pointer_chain(self.addresses.GameStates[Game.equip_current.value],
                                                  Game.equip_current.value)

        if address == 0x0:
            return -1

        return self.pine.read_int8(address)

    def is_on_water(self) -> bool:
        return self.get_current_gadget() == 0xB

    def is_in_control(self) -> bool:
        state : int = self.get_player_state()

        return state != 0x00 and state != 0x02

    def is_selecting_morph(self) -> bool:
        return self.get_player_state() == 0x03

    def get_button_pressed(self) -> int:
        return self.pine.read_int8(self.addresses.GameStates[Game.pressed.value])

    def check_screen_fading(self) -> int:
        return self.pine.read_int8(self.addresses.GameStates[Game.screen_fade.value])

    def get_screen_fade_count(self) -> int:
        return self.pine.read_int8(self.addresses.GameStates[Game.screen_fade_count.value])

    def get_gui_status(self) -> int:
        return self.pine.read_int8(self.addresses.GameStates[Game.gui_status.value])

    def is_location_checked(self, name : str) -> bool:
        address : int = self.addresses.Locations[name]
        alt_address : int = address
        alt_checked : bool = False

        # Check Permanent State Storage Addresses as well for locations that use it
        has_alt : bool = name in BOSSES_ALTERNATIVE.keys()
        if has_alt:
            alt_address = self.addresses.Locations[BOSSES_ALTERNATIVE[name]]
            alt_checked = self.pine.read_int8(alt_address) == 0x01

        if not alt_checked:
            checked : bool = self.pine.read_int8(address) == 0x01

            # Mark the Permanent Address as well if the original address is checked
            if has_alt and checked:
                self.pine.write_int8(alt_address, 0x01)
        else:
            checked : bool = True

        return checked

    def is_camera_interacted(self) -> bool:
        address : int = self.follow_pointer_chain(self.addresses.GameStates[Game.interact_data.value],
                                                  Game.interact_data.value)
        address += self.addresses.GameStates[Game.pipo_camera.value]

        # Return False when the address is invalid
        if address <= 0x0:
            return False

        as_bytes : bytes = self.pine.read_bytes(address, 5)
        # Try to decode to string, and immediately return if it cannot be decoded
        try:
            as_string: str = as_bytes.decode().replace("\x00", "")
        except UnicodeDecodeError:
            return False

        return as_string == Game.conte.value

    def get_cellphone_interacted(self, stage : str = "") -> str:
        base_address : int = self.follow_pointer_chain(self.addresses.GameStates[Game.interact_data.value],
                                                  Game.interact_data.value)
        address : int = base_address + self.addresses.GameStates[Game.cellphone.value]

        # Return an empty string if either addresses return 0
        if not address <= 0x0:
            as_bytes: bytes = self.pine.read_bytes(address, 3)

            # Try to decode to string, and immediately return if it cannot be decoded
            try:
                as_string : str = as_bytes.decode().replace("\x00", "")
            except UnicodeDecodeError:
                as_string = ""

            if as_string.isdigit():
                if as_string in CELLPHONES_ID_DUPLICATES and stage in CELLPHONES_STAGE_DUPLICATES:
                    as_string = as_string.replace("0", "1", 1)
                return as_string

        # Use alternative Cellphone address when the first one fails
        address = base_address + self.addresses.GameStates[Game.cellphone2.value]

        if address <= 0x0:
            return ""

        as_bytes: bytes = self.pine.read_bytes(address, 3)

        try:
            as_string : str = as_bytes.decode().replace("\x00", "")
        except UnicodeDecodeError:
            as_string = ""

        if as_string.isdigit():
            if as_string in CELLPHONES_ID_DUPLICATES and stage in CELLPHONES_STAGE_DUPLICATES:
                as_string = as_string.replace("0", "1", 1)
            return as_string
        else:
            return ""

    def is_saving(self) -> bool:
        address : int = self.follow_pointer_chain(self.addresses.GameStates[Game.interact_data.value],
                                                  Game.save.value)
        value : bytes = self.pine.read_bytes(address, 4)

        try:
            decoded : str = bytes.decode(value).replace("\x00", "")
        except UnicodeDecodeError:
            return False

        boolean : bool = decoded == Game.save.value
        return boolean

    def is_in_pink_boss(self) -> bool:
        return self.pine.read_int8(self.addresses.GameStates[Game.in_pink_stage.value]) == 0x02

    def is_tomoki_defeated(self) -> bool:
        # Check Permanent Address first
        permanent_checked : bool = self.is_location_checked(Loc.boss_alt_tomoki.value)

        if permanent_checked:
            return True

        address : int = self.follow_pointer_chain(self.addresses.Locations[Loc.boss_tomoki.value],
                                                  Loc.boss_tomoki.value)

        # Return false if pointer is still not initialized
        if address <= 0x0:
            return False

        value : float = self.pine.read_float(address)

        # Change the State value in Dr. Tomoki's Permanent State Address
        if value <= 0.0:
            self.mark_location(Loc.boss_alt_tomoki.value)

        return value <= 0.0

    def get_last_item_index(self) -> int:
        return self.pine.read_int32(self.addresses.GameStates[Game.last_item_index.value])

    def get_persistent_cookie_value(self) -> float:
        return self.pine.read_int32(self.addresses.GameStates[Game.last_cookies.value])

    def get_persistent_morph_energy_value(self) -> float:
        return self.pine.read_int32(self.addresses.GameStates[Game.last_morph_energy.value])

    def get_persistent_morph_stock_value(self) -> float:
        return self.pine.read_int32(self.addresses.GameStates[Game.last_morph_stock.value])

    # { Game Manipulation }
    def set_progress(self, progress : str = APHelper.pr_round2.value):
        addr : int = self.addresses.GameStates[Game.progress.value]
        addr = self.follow_pointer_chain(addr, Game.progress.value)

        if addr == 0x0:
            return

        as_bytes : bytes = progress.encode() + b'\x00'
        self.pine.write_bytes(addr, as_bytes)

    def set_unlocked_stages(self, index : int):
        self.pine.write_int32(self.addresses.GameStates[Game.channels_unlocked.value], index)

    def set_selected_channel(self, index : int):
        self.pine.write_int32(self.addresses.GameStates[Game.channel_selected.value], index)

    def set_next_channel_choice(self, index : int):
        if index > len(LEVELS_ID_BY_ORDER):
            index = 0

        addr: int = self.follow_pointer_chain(self.addresses.GameStates[Game.progress.value],
                                              Game.channel_next_choice.value)

        if addr == 0x0:
            return

        # Clear out current value
        clearing_address: int = addr
        for _ in range(6):
            self.pine.write_int32(clearing_address, 0x0)
            self.pine.write_int32(clearing_address, 0x0)
            clearing_address += 4

        # Convert ID to bytes
        id_as_bytes : bytes = LEVELS_ID_BY_ORDER[index].encode() + b'\x00'

        # Write new value
        self.pine.write_bytes(addr, id_as_bytes)

    def set_change_area_destination(self, area : str):
        as_bytes : bytes = area.encode() + b'\x00'
        self.pine.write_bytes(self.addresses.GameStates[Game.area_dest.value], as_bytes)

    def clear_spawn(self):
        spawn_address : int = self.addresses.GameStates[Game.spawn.value]
        dest_address : int = self.addresses.GameStates[Game.area_dest.value]
        for _ in range(6):
            self.pine.write_int32(spawn_address, 0x0)
            self.pine.write_int32(dest_address, 0x0)
            spawn_address += 4
            dest_address += 4


    def set_game_mode(self, mode : int = 0x100, restart : bool = True):
        address = self.addresses.GameStates[Game.game_mode.value]

        self.pine.write_int32(address, mode)

        if restart:
            self.send_command(Game.restart_stage.value)

    def set_cookies(self, amount : float):
        self.pine.write_float(self.addresses.GameStates[Game.cookies.value], amount)

    def clear_equipment(self):
        for button in self.addresses.BUTTONS_BY_INTERNAL:
            self.pine.write_int32(button, 0x0)

    def unlock_equipment(self, address_name : str, auto_equip : bool = False):
        is_equipped : int = False

        # Redirect address to RC Car if the unlocked equipment is an RC Car Chassis
        if "Chassis" in address_name:
            is_equipped = self.unlock_chassis(address_name)
            address : int = self.addresses.Items[Itm.gadget_rcc.value]
            address_name = Itm.gadget_rcc.value
        else:
            address : int = self.addresses.Items[address_name]

        self.pine.write_int32(self.addresses.Items[address_name], 0x2)

        if auto_equip and not is_equipped and address_name in Itm.get_gadgets_ordered():
            self.auto_equip(self.addresses.get_gadget_id(address))

    def unlock_chassis(self, address_name : str) -> bool:
        self.pine.write_int8(self.addresses.Items[address_name], 0x1)

        is_rcc_unlocked : bool = self.pine.read_int32(self.addresses.Items[Itm.gadget_rcc.value]) == 0x2

        return is_rcc_unlocked

    def unlock_chassis_direct(self, chassis_idx):
        chassis : str = Itm.get_chassis_by_id(no_default=True)[chassis_idx]
        self.pine.write_int8(self.addresses.Items[chassis], 0x1)

    def lock_chassis_direct(self, chassis_idx):
        chassis : str = Itm.get_chassis_by_id(no_default=True)[chassis_idx]

        if chassis:
            self.pine.write_int8(self.addresses.Items[chassis], 0x0)

    def set_chassis_direct(self, chassis_idx : int):
        self.pine.write_int32(self.addresses.GameStates[Game.equip_chassis_active.value], chassis_idx)

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

    def set_morph_duration(self, character : int, duration : float, dummy : str = ""):
        if character < 0:
            return

        durations : Sequence[int] = self.addresses.get_morph_duration_addresses(character)
        if not durations:
            return

        dummy_index : int = Itm.get_morphs_ordered().index(dummy) if dummy else - 1

        for idx, morph in enumerate(durations):
            duration_to_set : float = duration
            # Set duration to 0 if not specified in morphs and exclusive is false
            if dummy and idx == dummy_index:
                duration_to_set = 0.0

            self.pine.write_float(morph, duration_to_set)

    def give_collectable(self, address_name : str, amount : int | float = 0x1, maximum : int | float = 0x0):
        address : int = self.addresses.GameStates[address_name]
        current : int | float = self.pine.read_int32(address) if type(amount) == int else self.pine.read_float(address)
        value : int = 0

        if isinstance(amount, int):
            value = min(current + amount, maximum)
            self.pine.write_int32(address, value)
        elif isinstance(amount, float):
            value = int(min(current + amount, maximum))
            self.pine.write_float(address, min(current + amount, maximum))

        self.update_hud(address_name, value)

    def update_hud(self, address_name : str, value : int):
        if address_name not in HUD_OFFSETS:
            return

        address = self.follow_pointer_chain(self.addresses.GameStates[Game.hud_pointer.value], Game.hud_pointer.value)
        if address <= 0x0:
            return

        # Apply Offset
        address += HUD_OFFSETS[address_name]

        # Get byte length of data and use the correct write function accordingly
        size : int = ceil(value.bit_length() / 8)

        if size <= 1:
            self.pine.write_int8(address, value)
        elif 1 < size <= 2:
            self.pine.write_int16(address, value)
        elif size > 2:
            self.pine.write_int32(address, value)

    def give_morph_energy(self, amount : float = 3.0):
        # Check recharge state first
        address : int = self.addresses.GameStates[Game.morph_gauge_recharge.value]
        current : float = self.pine.read_float(address)

        if current != 0x0:
            # Ranges from 0 to 100 for every Morph Stock, with a maximum of 1100 for all 10 Stocks filled.
            self.pine.write_float(address, current + (amount / 30.0 * 100.0))
            return

        # If recharge state is 0, we check the active gauge, following its pointer chain
        address = self.follow_pointer_chain(self.addresses.GameStates[Game.morph_gauge_active.value],
                                            Game.morph_gauge_active.value)

        if address == 0x0:
            return

        current = self.pine.read_float(address)
        # Ranges from 0 to 30 in vanilla game.
        self.pine.write_float(address, current + amount)

    def set_morph_gauge_charge(self, amount : float = 0.0):
        # Check recharge state first
        address: int = self.addresses.GameStates[Game.morph_gauge_recharge.value]

        # Ranges from 0 to 100 for every Morph Stock, with a maximum of 1100 for all 10 Stocks filled.
        self.pine.write_float(address, amount)

    def set_morph_gauge_timer(self, amount : float = 0.0):
        address = self.follow_pointer_chain(self.addresses.GameStates[Game.morph_gauge_active.value],
                                            Game.morph_gauge_active.value)

        if address == 0x0:
            return

        self.pine.write_float(address, amount)

    def mark_location(self, name : str):
        address : int = self.addresses.Locations[name]
        self.pine.write_int8(address, 0x01)

    def unmark_location(self, name : str):
        address : int = self.addresses.Locations[name]
        self.pine.write_int8(address, 0x00)

    def send_command(self, command : str):
        as_bytes : bytes = command.encode() + b'\x00'
        self.pine.write_bytes(self.addresses.GameStates[Game.command.value], as_bytes)

    def kill_player(self, cookies_lost : float = 0.0):
        if cookies_lost != 0.0:
            cookies : float = self.get_cookies()
            self.set_cookies(max(0.0, cookies - cookies_lost))

        ## self.send_command(Game.kill_player.value) has a transition delay that takes too long
        ## changeArea is more instantaneous, but introduces a buggy respawn when all cookies are depleted
        self.change_area(self.get_stage())

    def change_area(self, destination : str):
        self.set_change_area_destination(destination)
        self.send_command(Game.change_area.value)

    def set_last_item_index(self, value : int):
        self.pine.write_int32(self.addresses.GameStates[Game.last_item_index.value], value)

    def set_persistent_cookie_value(self, value : float):
        self.pine.write_float(self.addresses.GameStates[Game.last_cookies.value], value)

    def set_persistent_morph_energy_value(self, value : float):
        self.pine.write_float(self.addresses.GameStates[Game.last_morph_energy.value], value)

    def set_persistent_morph_stock_value(self, value : float):
        self.pine.write_float(self.addresses.GameStates[Game.last_morph_stock.value], value)

    def save_state(self, slot : int):
        self.pine.save_state(slot)

    def load_state(self, slot : int):
        self.pine.load_state(slot)