from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence
import typing
import multiprocessing
import traceback
import asyncio
import sys

from CommonClient import ClientStatus, logger, handle_url_arg
from settings import get_settings
import Utils

from .data.Strings import Meta, APConsole
from .data.Logic import ProgressionMode, ProgressionModeOptions
from .data.Locations import MONKEYS_MASTER, MONKEYS_MASTER_ORDERED, CAMERAS_MASTER_ORDERED, CELLPHONES_MASTER_ORDERED, \
    SHOP_PROGRESSION_75COMPLETION, SHOP_EVENT_ACCESS_DIRECTORY, SHOP_COLLECTION_MASTER, SHOP_UNIQUE_MASTER
from .data.Stages import STAGES_BREAK_ROOMS, LEVELS_BY_ORDER
from .data.Rules import GoalTarget, GoalTargetOptions, PostGameCondition
from .AE3_Interface import ConnectionStatus, AEPS2Interface
from . import AE3Settings
from .Checker import *
from .data import Items, Locations

# Try importing gui_enabled in Utils first before trying to import them from CommonClient
# Core AP will be officially moving it to Utils in the future, so this is in accommodation for that
gui_loaded_from_utils: bool = False
try:
    from Utils import gui_enabled
    gui_loaded_from_utils = True
except ImportError:
    pass

# Try to load Universal Tracker if present
tracker_loaded: bool = False
try:
    from worlds.tracker.TrackerClient import (ClientCommandProcessor, TrackerGameContext as SuperContext,
                                              get_base_parser, server_loop)
    tracker_loaded = True

    if not gui_loaded_from_utils: from worlds.tracker.TrackerClient import gui_enabled
except ImportError:
    from CommonClient import (ClientCommandProcessor, CommonContext as SuperContext, get_base_parser, server_loop)
    if not gui_loaded_from_utils: from CommonClient import gui_enabled


class AE3CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: SuperContext):
        super().__init__(ctx)

    def _cmd_resync(self):
        """Sync status of important items such as gadgets, morphs and keys with the server."""
        if not isinstance(self.ctx, AE3Context):
            return

        if self.ctx.is_game_connected and self.ctx.server:
            self.ctx.pending_resync = True

    def _cmd_status(self):
        """Display current status of the game and session, along with a summary of the current progress."""
        if isinstance(self.ctx, AE3Context):
            logger.info(f" [-^-] Client Status")

            if tracker_loaded:
                logger.info(f" [-v-] Universal Tracker Integrated")

            logger.info(f" [-o-] Game")

            if self.ctx.server:
                game_status : int = self.ctx.ipc.status.value
                pgc_complete: bool = False
                if game_status < 0:
                    logger.info(f"{"         Connected but playing a different game"}")
                    return
                elif game_status == 0:
                    logger.info(f"{"         Not Connected to PCSX2"}")
                    return
                else:
                    logger.info(f"{"         Playing Ape Escape 3"}")

                logger.info(f"\n         Goal Target is " 
                            f"{self.ctx.goal_target}")

                if game_status > 0:
                    logger.info(f"         > Progress: "
                                f"{str(self.ctx.goal_target.get_progress(self.ctx))} / "
                                f"{self.ctx.goal_target.amount}")

                # Display required Channel Keys to unlock the End Game for Open Progression
                if self.ctx.progression.name == "Open":
                    logger.info(f"\n        Open Progression requires Channel Keys")
                    open_requirements_met : bool = self.ctx.keys >= len(self.ctx.progression.progression[1:-2])
                    logger.info(f"        > Progress: "
                                f"{self.ctx.keys} / "
                                f"{len(self.ctx.progression.progression[1:-2])}"
                                f"{'    [ COMPLETED! ]' if open_requirements_met else ''}")

                if self.ctx.post_game_condition.amounts:
                    post_game_conditions : str = ""
                    for i, category in enumerate(self.ctx.post_game_condition.amounts.keys()):
                        post_game_conditions += f" {category}"

                        if i == len(self.ctx.post_game_condition.amounts.keys()) - 2:
                            post_game_conditions += " and"
                        elif i != len(self.ctx.post_game_condition.amounts.keys()) - 1:
                            post_game_conditions += ","

                    logger.info(f"\n         Post-Game requires{post_game_conditions}")

                    if game_status > 0:
                        logger.info(f"         > Progress: ")

                        pgc_progress : dict[str, list[int]] = self.ctx.post_game_condition.get_progress(self.ctx)

                        if all(v[0] >= v[1] for v in [*pgc_progress.values()]):
                            pgc_complete = True
                            logger.info(f"         Post-Game Condition(s) are Complete! ")

                        if pgc_progress:
                            for key, value in pgc_progress.items():
                                prog : str = f"{value[0]} / {value[1]}"
                                if value[0] >= value[1]:
                                    prog += f"    [ COMPLETE! ]"

                                logger.info(f"                > {key}: {prog}")

                if game_status > 0:
                    required_keys : int = (len(self.ctx.progression.progression) - 3)
                    if APHelper.keys.value in self.ctx.post_game_condition.amounts:
                        required_keys += self.ctx.post_game_condition.amounts[APHelper.keys.value]
                    all_keys : int = required_keys + self.ctx.extra_keys

                    logger.info(f"\n         Progression: {self.ctx.progression}")
                    logger.info(f"         Channel Keys: {self.ctx.keys} / {required_keys} "
                                f"{f"+ {self.ctx.extra_keys} ({all_keys})" if self.ctx.extra_keys else ""}")

                    if self.ctx.shoppingsanity > 2:
                        if self.ctx.shoppingsanity == 3:
                            initial: int = self.ctx.shop_progression - 1
                            progress: int = self.ctx.keys * self.ctx.shop_progression + initial
                            if progress >= 27 and not pgc_complete:
                                progress = (math.floor((28 - self.ctx.shop_progression) / self.ctx.shop_progression)
                                            * self.ctx.shop_progression - 1)

                            percent: float = min(progress, 27) / 27 * 100
                            logger.info(f"         Shop Availability: {percent:.2f}%")
                        elif self.ctx.shoppingsanity == 4:
                            progress: int = self.ctx.shop_progress
                            stocks: int = int((progress + 1) / self.ctx.shop_progression) - 1
                            target: int = math.ceil(28 / self.ctx.shop_progression) - 1
                            all_stocks: int = self.ctx.restock_progression + self.ctx.extra_shop_stocks
                            logger.info(f"         Shop Stocks: {stocks} / {target} "
                                        f"{f" ({self.ctx.restock_progression})" 
                                        if self.ctx.restock_progression - 1 == stocks 
                                        else ""}"
                                        f"{f"+ {self.ctx.extra_shop_stocks}({all_stocks})" 
                                        if self.ctx.extra_shop_stocks
                                        else ""}")

                    logger.info(f"         Available Channels: {self.ctx.unlocked_channels + 1} / "
                                f"{sum(self.ctx.progression.progression[:-1]) + 1}")

            else:
                logger.info(f"         Disconnected from Server")

            logger.info(f"\n [-=-] Settings")
            logger.info(f"         Auto-Equip is " 
                        f"{"ENABLED" if self.ctx.auto_equip else "DISABLED"}")

            if self.ctx.early_free_play:
                logger.info(f"         Freeplay Toggle is " 
                            f"{"ENABLED" if self.ctx.alt_freeplay else "DISABLED"}")
            else:
                logger.info(f"         Early Freeplay is DISABLED and Freeplay Toggle cannot be toggled.")

            logger.info(f"         DeathLink is " 
                        f"{"ENABLED" if self.ctx.death_link else "DISABLED"}")

    def _cmd_channels(self):
        """List the true order of the channels"""
        if not isinstance(self.ctx, AE3Context):
            return

        if not self.ctx.server or not self.ctx.progression:
            logger.info(f" [!!!] Please connect to an Archipelago Server first!")
            return

        logger.info(f" [-#-] Available Channels: {self.ctx.unlocked_channels + 1} / "
                    f"{sum(self.ctx.progression.progression[:-1]) + 1}")

        group_set: list[list[int]] = []
        count: int = 0
        for i, channel_set in enumerate(self.ctx.progression.progression):
            offset: int = 0
            if i == 0:
                offset = 1

            target: int = count + channel_set + offset
            group_set.append([_ for _ in self.ctx.progression.order[count: target]])
            count = target

        count: int = 0
        for i, sets in enumerate(group_set):
            if not sets:
                continue

            if i and i < len(group_set) - 2:
                logger.info(f"         - < {i} > -----")
            elif i and i == len(group_set) - 1:
                break
            elif i:
                tag: str = ""

                if APHelper.keys.value in self.ctx.post_game_condition.amounts:
                    tag += f"{self.ctx.post_game_condition.amounts[APHelper.keys.value] + i - 1}"
                not_key_condition : list[str] = [k for k in self.ctx.post_game_condition.amounts.keys()
                                                 if k != APHelper.keys.value]
                if not_key_condition:
                    tag += "!"

                logger.info(f"         - < {tag} > -----")

            if count > self.ctx.unlocked_channels:
                break

            for channels in sets:
                logger.info(f"         [{count + 1}] {LEVELS_BY_ORDER[channels]}")
                count += 1

    def _cmd_remaining(self):
        """List remaining locations to check to Goal."""
        if not isinstance(self.ctx, AE3Context):
            return

        if not self.ctx.server or not self.ctx.goal_target:
            logger.info(f" [!!!] Please connect to an Archipelago Server first!")
            return
        elif self.ctx.game_goaled:
            logger.info(f" [-!-] You have already Goaled! You have no more remaining checks!")
            return

        logger.info(f" [-^-] Goal Target Progress: "
                    f"{str(self.ctx.goal_target.get_progress(self.ctx))} / "
                    f"{self.ctx.goal_target.amount}")

        logger.info(f" Remaining Potential Goal Target Locations:")
        remaining : list[str] = self.ctx.goal_target.get_remaining(self.ctx)

        for location in remaining:
            logger.info(f"         > " f"{location}")

    def _cmd_remaining_post_game(self):
        """List remaining locations to check to unlock Post-Game."""
        if not isinstance(self.ctx, AE3Context):
            return

        if not self.ctx.server or not self.ctx.post_game_condition:
            logger.info(f" [!!!] Please connect to an Archipelago Server first!")
            return
        elif self.ctx.game_goaled:
            logger.info(f" [-!-] You have already Goaled! You have no more remaining checks!")
            return

        progress: dict[str, list[int]] = self.ctx.post_game_condition.get_progress(self.ctx)
        remaining: dict[str, list[str]] = self.ctx.post_game_condition.get_remaining(self.ctx)

        if not remaining:
            logger.info(f" [-!-] You have already unlocked Post-Game!")
            return

        logger.info(f" [->-] Post Game Condition Progress: ")

        if all(v[0] >= v[1] for v in [*progress.values()]):
            logger.info(f"         Post-Game Condition(s) are Complete! ")

        if progress:
            for key, value in progress.items():
                prog: str = f"{value[0]} / {value[1]}"
                if value[0] >= value[1]:
                    prog += f"    [ COMPLETE! ]"

                logger.info(f"                > {key}: {prog}")

        logger.info(f"\n Remaining Potential Post Game Condition Locations:")

        for category, remains in remaining.items():
            logger.info(f"         " f"[-/-] {category}")
            for location in remains:
                logger.info(f"                  > " f"{location}")

    def _cmd_auto_equip(self):
        """Toggle if Gadgets should automatically be assigned to a free face button when received."""
        if isinstance(self.ctx, AE3Context):
            self.ctx.auto_equip = not self.ctx.auto_equip

            logger.info(f" [-!-] Auto Equip is now " f"{"ENABLED" if self.ctx.auto_equip else "DISABLED"}")


    def _cmd_freeplay(self):
        """Toggle if Free Play mode should be accessible early by holding L1 or L2 after selecting a channel.
        """
        if isinstance(self.ctx, AE3Context):
            if not self.ctx.early_free_play:
                logger.info(f" [!!!] Early Free Play was set to DISABLED. You cannot toggle Freeplay Toggle.")
                return

            self.ctx.alt_freeplay = not self.ctx.alt_freeplay

            logger.info(f" [-!-] Freeplay Toggle is now " f"{"ENABLED" if self.ctx.alt_freeplay else "DISABLED"}")

    def _cmd_deathlink(self):
        """Toggle if death links should be enabled. This affects both receiving and sending deaths."""
        if isinstance(self.ctx, AE3Context):
            if not self.ctx.should_deathlink_tag_update:
                self.ctx.death_link = not self.ctx.death_link
                self.ctx.should_deathlink_tag_update = True

                logger.info(f" [-!-] DeathLink is now " f"{"ENABLED" if self.ctx.death_link else "DISABLED"}")
            else:
                logger.info(f"[...] A DeathLink toggle has already been requested. Please try again in a few seconds.")

    def _cmd_save_state(self):
        """Save State to the slot specified in the options."""
        if not isinstance(self.ctx, AE3Context):
            return

        if (not (11 <= self.ctx.state_slot <= 255)) and self.ctx.state_slot != 0:
            logger.info(" [-!-] The server has not given the state lot for this session. "
                        "Have you connected to the server at least once?")
            return

        self.ctx.ipc.save_state(self.ctx.state_slot)

    def _cmd_load_state(self):
        """Load State from the slot specified in the options."""
        if not isinstance(self.ctx, AE3Context):
            return

        if (not (11 <= self.ctx.state_slot <= 255)) and self.ctx.state_slot != 0:
            logger.info(" [-!-] The server has not given the state lot for this session. "
                        "Have you connected to the server at least once?")
            return

        self.ctx.ipc.load_state(self.ctx.state_slot)

    # Debug commands
    def _cmd_unlock(self, unlocks : str = "28"):
        """<!> DEBUG | Unlock amount of levels given"""
        if not unlocks.isdigit():
            logger.info(" [-!-] Please enter a number.")
            return

        if isinstance(self.ctx, AE3Context):
            amount: int = int(unlocks)
            self.ctx.unlocked_channels = max(min(amount, 28), 0)

    def _cmd_receive_death(self, count : str = "1"):
        """<!> DEBUG | Simulate receiving a death link"""
        if not count.isdigit():
            logger.info("Please enter a number.")
            return

        if isinstance(self.ctx, AE3Context):
            if not self.ctx.death_link:
                logger.info(" [!!!] DeathLink is currently DISABLED. Deathlink cannot be received.")
                return

            self.ctx.pending_deathlinks = int(count)

class AE3Context(SuperContext):
    # Archipelago Meta
    client_version: str = APConsole.Info.client_ver.value
    world_version : str = APConsole.Info.world_ver.value

    # Game Details
    game: str = Meta.game
    platform: str = Meta.platform

    # Client Properties
    command_processor : ClientCommandProcessor = AE3CommandProcessor
    tags: set[str] = {"AP"}
    items_handling : int = 0b111

    # Interface Properties
    ipc : AEPS2Interface = AEPS2Interface
    is_game_connected : bool = ConnectionStatus.DISCONNECTED
    has_just_connected : bool = False
    interface_sync_task : asyncio.tasks = None
    last_message : Optional[str] = None

    # Server Properties and Cache
    next_item_slot : int = -1
    pending_auto_save : bool = False
    is_last_save_normal : bool = None
    pending_last_save_status : bool = False
    has_saved_on_transition : bool = True
    has_attempted_auto_load : bool = False
    pending_deathlinks : int = 0
    pending_resync : bool = False
    cached_locations_checked : Set[int]
    offline_locations_checked : Set[int] = set()
    monkeys_index : list[Sequence[str]] = []

    should_deathlink_tag_update : bool = False

    # APWorld Properties
    locations_name_to_id : dict[str, int] = Locations.generate_name_to_id()
    active_locations: set[str] = set(locations_name_to_id.keys()).difference(MONKEYS_PASSWORDS)
    items_name_to_id : dict[str, int] = Items.generate_name_to_id()
    location_groups : list[list[str]] = [[*locations] for locations in LOCATIONS_INDEX.values()]
    group_check_index : int = 0

    cache_missing : list[list[str]] = location_groups.copy()
    is_cache_built : bool = False
    monkeys_checklist : Sequence[str] = MONKEYS_MASTER
    monkeys_checklist_count : int = 0
    pre_hinted: dict = {}

    # Session Properties
    keys : int = 0
    unlocked_channels : int = 0
    current_channel: str = None
    current_stage : str = None
    current_game_mode : int = 0x0
    current_coins: int = 0
    current_jackets : int = 0
    in_travel_station : bool = False
    is_using_data_desk: bool = False
    in_shopping_area : bool = False
    is_shop_ready: bool = False
    has_bought_ticket: bool = False
    last_selected_channel_index : int = -1
    suppress_progress_correction : bool = False
    character : int = -1
    player_control : bool = False

    alt_freeplay : bool = False
    is_mode_swapped : bool = False
    is_channel_swapped : bool = False

    ## Command State can be in either of 3 stages:
    ##  0 - No Exclusive Command Sent
    ##  1 - Command has been sent, awaiting confirmation of execution
    ##  2 - Command Executed, awaiting confirmation to reset
    command_state : int = 0
    sending_death : bool = False
    receiving_death : bool = True
    are_item_status_synced : bool = False

    rcc_unlocked : bool = False
    swim_unlocked : bool = False
    dummy_morph_needed : bool = True
    dummy_morph_monkey_needed : bool = True

    game_goaled : bool = False

    # Local Session Save Properties
    last_item_processed_index : int = -1

    # Player Set Settings
    settings : AE3Settings

    save_state_on_room_transition : bool = False
    save_state_on_item_received : bool = False
    save_state_on_location_check : bool = False
    load_state_on_connect : bool = False

    auto_equip : bool = False

    # Player Set Options
    progression : ProgressionMode = ProgressionModeOptions[0]
    goal_target : GoalTarget = GoalTarget()
    post_game_access_rule_option : int = 0
    post_game_condition : PostGameCondition = None
    shuffle_channel : bool = False
    dummy_morph : str = Itm.morph_monkey.value
    check_break_rooms : bool = False
    camerasanity : int = None
    cellphonesanity : bool = None
    shoppingsanity : int = None
    restock_progression : int = 28
    shop_progress : int = 27
    shop_progression : int = 0
    extra_keys : int = 0
    extra_shop_stocks : int = 0

    morph_duration : float = 0.0
    shuffle_chassis: bool = False
    shuffle_morph_stock: bool = False

    early_free_play : bool = False
    monkey_mart : bool = True
    ticket_consolation: bool = True
    consolation_whitelist: list[str] = [
        APHelper.nothing.value,
        APHelper.hint_filler.value,
        APHelper.hint_progressive.value,
        APHelper.check_filler.value,
        APHelper.check_progressive.value,
        APHelper.check_pgc.value,
        APHelper.check_gt.value,
    ]

    state_slot : int = -1
    death_link : bool = False

    def __init__(self, address, password):
        super().__init__(address, password)

        # Initialize Variables
        Utils.init_logging(APConsole.Info.client_name.value + self.client_version)

        self.ipc = AEPS2Interface(logger)

        self.cached_locations_checked = set()
        for lists in [*MONKEYS_DIRECTORY.values()]:
            if lists not in self.monkeys_index:
                self.monkeys_index.append(lists)

        # Load Settings
        self.settings = get_settings().get("ape_escape_3_options", False)
        assert self.settings, " [!!!] Cannot find Ape Escape 3 Settings!"

        self.save_state_on_room_transition = self.settings.save_state_on_room_transition
        self.save_state_on_item_received = self.settings.save_state_on_item_received
        self.save_state_on_location_check = self.settings.save_state_on_location_check
        self.load_state_on_connect = self.settings.load_state_on_connect

        self.auto_equip = self.settings.auto_equip

    # Archipelago Server Authentication
    async def server_auth(self, password_requested : bool = False):
        # Ask for Password if Requested so
        if password_requested and not self.password:
            await super(AE3Context, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        
        # First Connection Check
        if cmd == APHelper.cmd_conn.value:
            data = args[APHelper.arg_sl_dt.value]

            ## Reset Variables
            self.check_break_rooms = False

            ## Check Generation Version if the client is compatible
            if APHelper.version.value in data:
                world_ver: str = data[APHelper.version.value]
                assert_version_compatibility(world_ver, APConsole.Info.world_ver.value)
            else:
                assert_version_compatibility("", APConsole.Info.world_ver.value)

            ### Save/Load State Slot
            if APHelper.auto_save_slot.value in data:
                self.state_slot = data[APHelper.auto_save_slot.value]

            ## Progression Mode
            if not self.unlocked_channels and APHelper.progression_mode.value in data:
                self.progression = ProgressionModeOptions[data[APHelper.progression_mode.value]]()

                ## Progression
                if APHelper.progression.value in data and self.progression:
                    self.progression.set_progression(data[APHelper.progression.value])

                ## Channel Order
                if APHelper.channel_order.value in data and self.progression:
                    self.progression.set_order(data[APHelper.channel_order.value])

                self.unlocked_channels = self.progression.get_progress(0)

            ## Check Break Room Monkeys and Password Monkeys options to use with Goal Target
            self.check_break_rooms : bool = self.check_break_rooms or self.post_game_access_rule_option == 0

            excluded_stages : list[str] = []
            excluded_locations : list[str] = [*MONKEYS_PASSWORDS]

            # Exclude Shop Items based on Shoppingsanity Type and Blacklisted Channels
            if data[APHelper.blacklist_channel.value] and data[APHelper.shoppingsanity.value] > 0:
                ## Always exclude Ultim-ape Fighter Minigame if anything is blacklisted
                excluded_locations.extend(SHOP_PROGRESSION_75COMPLETION)

                ## Exclude Event/Condition-sensitive Items based on excluded levels
                for region, item in SHOP_EVENT_ACCESS_DIRECTORY.items():
                    if region in data[APHelper.blacklist_channel.value]:
                        excluded_locations.extend(item)

            ## Monkeysanity - Break Rooms
            if APHelper.monkeysanitybr.value in data:
                self.check_break_rooms = self.check_break_rooms or bool(data[APHelper.monkeysanitybr.value])

                if data[APHelper.monkeysanitybr.value] < 2:
                    self.dummy_morph = Itm.morph_knight.value

            if not self.check_break_rooms:
                excluded_stages = [*STAGES_BREAK_ROOMS]

            ### Exclude Blacklisted Channels from Goal Target and Post Game Condition
            if self.progression.progression[-1]:
                for channel in self.progression.order[-self.progression.progression[-1]:]:
                    excluded_locations.extend(MONKEYS_MASTER_ORDERED[channel])
                    excluded_locations.append(CAMERAS_MASTER_ORDERED[channel])

                    excluded_phones_id: list[str] = CELLPHONES_MASTER_ORDERED[channel]
                    excluded_locations.extend(Cellphone_Name_to_ID[cell_id] for cell_id in excluded_phones_id)

            goal_amount : int = 0
            if APHelper.goal_target_ovr.value in data:
                goal_amount : int = data[APHelper.goal_target_ovr.value]

            ## Goal Target
            if not self.goal_target.locations and APHelper.goal_target.value in data:
                goal_target = data[APHelper.goal_target.value]
                self.goal_target = GoalTargetOptions[goal_target](goal_amount,
                                                                  excluded_stages,
                                                                  excluded_locations)

            ## Get Post Game Conditions
            amounts : dict[str, int] = {}

            if APHelper.pgc_monkeys.value in data and data[APHelper.pgc_monkeys.value]:
                amount : int = 441 if data[APHelper.pgc_monkeys.value] < 0 else data[APHelper.pgc_monkeys.value]
                amounts[APHelper.monkey.value] = amount

            if APHelper.pgc_bosses.value in data and data[APHelper.pgc_bosses.value]:
                amounts[APHelper.bosses.value] = data[APHelper.pgc_bosses.value]

            if APHelper.pgc_cameras.value in data and data[APHelper.pgc_cameras.value]:
                amounts[APHelper.camera.value] = data[APHelper.pgc_cameras.value]

            if APHelper.pgc_cellphones.value in data and data[APHelper.pgc_cellphones.value]:
                amounts[APHelper.cellphone.value] = data[APHelper.pgc_cellphones.value]

            if APHelper.pgc_shop.value in data and data[APHelper.pgc_shop.value]:
                amounts[APHelper.shop.value] = data[APHelper.pgc_shop.value]

            if APHelper.pgc_keys.value in data and data[APHelper.pgc_keys.value]:
                amounts[APHelper.keys.value] = data[APHelper.pgc_keys.value]

            # Exclude Channels in Post Game from being required for Post Game to be unlocked
            post_game_start_index = sum(self.progression.progression[:-2]) + 1
            for channel in (self.progression.order[post_game_start_index:
                post_game_start_index + self.progression.progression[-2]]):
                    excluded_locations.extend(MONKEYS_MASTER_ORDERED[channel])
                    excluded_locations.append(CAMERAS_MASTER_ORDERED[channel])

                    excluded_phones_id: list[str] = CELLPHONES_MASTER_ORDERED[channel]
                    excluded_locations.extend(Cellphone_Name_to_ID[cell_id] for cell_id in excluded_phones_id)

            # Exclude Ultim-ape Fighter from being a PGC requirement, as it requires as many monkeys as possible
            excluded_locations.extend(SHOP_PROGRESSION_75COMPLETION)

            ## Post Game Access Rule Initialization
            self.post_game_condition = PostGameCondition(amounts, excluded_stages, excluded_locations)

            ## Shuffle Channel
            if APHelper.shuffle_channel.value in data:
                self.shuffle_channel = data[APHelper.shuffle_channel.value]

            ## Camerasanity
            if self.camerasanity is None and APHelper.camerasanity.value in data:
                self.camerasanity = (data[APHelper.camerasanity.value])

            ## Cellphonesanity
            if self.cellphonesanity is None and APHelper.cellphonesanity.value in data:
                self.cellphonesanity = data[APHelper.cellphonesanity.value]

            ## Shoppingsanity
            if self.shoppingsanity is None and APHelper.shoppingsanity.value in data:
                self.shoppingsanity = data[APHelper.shoppingsanity.value]

                if self.shoppingsanity >= 3 and APHelper.shop_progression.value in data:
                    self.shop_progression = data[APHelper.shop_progression.value]
                    self.shop_progress = self.shop_progression - 1

                ## Restock Progression
                if self. shoppingsanity == 4 and APHelper.restock_progression.value in data:
                    self.restock_progression = data[APHelper.restock_progression.value]


            ## Morph Duration
            if self.morph_duration == 0 and APHelper.base_morph_duration.value in data:
                self.morph_duration = float(data[APHelper.base_morph_duration.value])

            ## Shuffle Chassis
            if APHelper.shuffle_chassis.value in data:
                self.shuffle_chassis = data[APHelper.shuffle_chassis.value]

            ## Shuffle Morph Stock
            if APHelper.shuffle_morph_stocks.value in data:
                self.shuffle_morph_stock = data[APHelper.shuffle_morph_stocks.value]

            ## Extra Keys
            if APHelper.extra_keys.value in data:
                self.extra_keys = data[APHelper.extra_keys.value]

            ## Extra Shop Stocks
            if APHelper.extra_shop_stocks.value in data:
                self.extra_shop_stocks = data[APHelper.extra_shop_stocks.value]

            ## Early Free Play
            if APHelper.early_free_play.value in data:
                self.early_free_play = data[APHelper.early_free_play.value]
                self.alt_freeplay = self.early_free_play

            ## Lucky Ticket Consolation Effect
            if APHelper.ticket_consolation.value in data:
                self.ticket_consolation = data[APHelper.ticket_consolation.value]

                if APHelper.consolation_whitelist.value in data:
                    self.consolation_whitelist = data[APHelper.consolation_whitelist.value]

            ## Enable Monkey Mart
            if APHelper.enable_monkey_mart.value in data:
                self.monkey_mart = data[APHelper.enable_monkey_mart.value]

            ## DeathLink
            if APHelper.death_link.value in data:
                self.death_link = bool(data[APHelper.death_link.value])
                Utils.async_start(self.update_death_link(self.death_link))

            ## Pre-scouted
            if APHelper.hints.value in data:
                self.pre_hinted = {int(key) : value for key, value in data[APHelper.hints.value].items()}

            # Initiate Checked Locations Cache Rebuilding if necessary:
            if not self.locations_checked and not self.cache_missing:
                self.is_cache_built = False
                self.cache_missing = self.location_groups.copy()

            # Initialize/Update Last Save Type Status on server if needed
            if self.load_state_on_connect:
                self.pending_last_save_status = True

            # Create List of Active Locations
            if not self.check_break_rooms:
                self.active_locations.difference_update(MONKEYS_BREAK_ROOMS)

            if self.shoppingsanity > 0:
                if self.shoppingsanity == 2:
                    self.active_locations.difference_update(set(SHOP_UNIQUE_MASTER).difference(SHOP_PERSISTENT_MASTER))
                else:
                    self.active_locations.difference_update(
                        set(SHOP_COLLECTION_MASTER).difference(SHOP_PERSISTENT_MASTER))

        elif cmd == APHelper.cmd_rcv.value:
            index = args["index"]

            # Update Next Item Slot
            if index:
                self.next_item_slot = index

            # Abort if there are no locations, as starting items might get duplicated
            if not self.checked_locations:
                self.are_item_status_synced = True

            # Resync Important Item Statuses
            if self.are_item_status_synced or not self.items_received:
                return

            # Set Character if not yet
            if self.character < 0 and self.current_stage:
                self.character = self.ipc.get_character()

            received_as_id : list[int] = [ i.item for i in self.items_received]

            # Rebuild Progress
            ## Get Keys
            if self.unlocked_channels <= 0:
                self.keys = received_as_id.count(self.items_name_to_id[APHelper.channel_key.value])
                self.unlocked_channels = self.progression.get_progress(self.keys, self.post_game_condition.check(self))
                self.ipc.set_unlocked_stages(self.unlocked_channels)

                if self.shoppingsanity == 3:
                    self.shop_progress = (self.keys + 1) * self.shop_progression - 1

                    if self.shop_progress >= 27:
                        self.shop_progress = (math.floor((28 - self.shop_progression) / self.shop_progression)
                                              * self.shop_progression - 1)

            ## Get Shop Stock
            if self.shoppingsanity == 4 and 0 >= self.shop_progress >= 27:
                self.shop_progress =( (received_as_id.count(self.items_name_to_id[APHelper.shop_stock.value]) + 1) *
                                      self.shop_progression - 1 )

            # Check if dummy morph is needed
            self.dummy_morph_monkey_needed = self.items_name_to_id[Itm.morph_monkey.value] not in received_as_id

            if self.dummy_morph == Itm.morph_monkey.value:
                self.dummy_morph_needed = self.dummy_morph_monkey_needed
            else:
                morph_ids : list[int] = [ self.items_name_to_id[morph] for morph in Itm.get_morphs_ordered() ]
                self.dummy_morph_needed = not any(item in morph_ids for item in received_as_id)

            # Retrace Morph Duration
            if self.morph_duration != 0:
                self.morph_duration += received_as_id.count(self.items_name_to_id[Itm.acc_morph_ext.value]) * 2
                dummy : str = self.dummy_morph if self.dummy_morph_needed else ""
                self.ipc.set_morph_duration(self.character, self.morph_duration, dummy)

            # Check RC Car Unlock
            for rcc in Itm.get_chassis_by_id():
                if self.items_name_to_id[rcc] in received_as_id:
                    self.rcc_unlocked = True
                    break

            # Check Water Net Unlock
            self.swim_unlocked = self.items_name_to_id[Itm.gadget_swim.value] in received_as_id

            self.are_item_status_synced = True

        elif cmd == APHelper.cmd_rtrv.value:
            # Get Latest Last Save Type Status
            last_save_string: str = f"{APHelper.last_save_type.value}_{self.team}_{self.slot}"
            if last_save_string in self.stored_data:
                if self.stored_data[last_save_string] is None:
                    self.is_last_save_normal = True
                else:
                    self.is_last_save_normal = bool(self.stored_data[last_save_string])

        # Initialize Session on receive of RoomInfo Packet
        elif cmd == APHelper.cmd_rminfo.value:
            seed: str = args[APHelper.arg_seed.value]

            # Assume mismatched seeds is an attempt at a new world, and clear local cache of locations
            if self.seed_name != seed:
                self.checked_locations.clear()
                self.locations_checked.clear()

                self.seed_name = seed

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        if not self.death_link:
            return

        super().on_deathlink(data)

        self.pending_deathlinks += 1

    # Client Command GUI
    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = APConsole.Info.game_name.value
        ui.logging_pairs = [("Client", "Archipelago")]

        return ui

    async def check_pgc(self) -> bool:
        if self.post_game_condition.passed:
            return True
        if self.post_game_condition.check(self):
            self.ipc.set_pgc_cache()
            return True

        return False

    async def goal(self):
        if self.game_goaled:
            return

        await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        self.game_goaled = True


def update_connection_status(ctx : AE3Context, status : bool):
    if bool(ctx.is_game_connected) == status:
        return

    if status:
        ctx.has_just_connected = True
        logger.info(APConsole.Info.init_game.value)
    else:
        logger.info(APConsole.Err.sock_fail.value + APConsole.Err.sock_re.value)

    ctx.is_game_connected = status

# Main Client Loop
async def main_sync_task(ctx : AE3Context):
    # Greetings
    logger.info(APConsole.Info.decor.value)
    logger.info("    " + APConsole.Info.greet.value)
    logger.info("    World v" + APConsole.Info.world_ver.value + "    Client v" + APConsole.Info.client_ver.value)
    logger.info(APConsole.Info.decor.value)
    logger.info("\n")
    logger.info(APConsole.Info.p_init.value)

    ctx.ipc.connect_game()

    while not ctx.exit_event.is_set():
        try:
            # Check connection to PCSX2 first
            is_game_connected : bool = ctx.ipc.get_connection_state()
            update_connection_status(ctx, is_game_connected)

            # Check Progress if connection is good
            if is_game_connected:
                await check_game(ctx)

            # Attempt reconnection to PCSX2 otherwise
            else:
                await reconnect_game(ctx)

            if ctx.server and ctx.should_deathlink_tag_update:
                await ctx.update_death_link(ctx.death_link)
                ctx.should_deathlink_tag_update = False

        except ConnectionError:
            ctx.ipc.disconnect_game()
        except Exception as e:
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())

            await asyncio.sleep(3)
            continue

async def check_game(ctx : AE3Context):
    if ctx.server:
        if ctx.pending_last_save_status:
            await get_last_save_status(ctx)
            ctx.pending_last_save_status = False

    # Check if Game State is safe for Further Checking
    if not ctx.player_control:
        # Auto Load State if desired
        if ctx.state_slot >= 0 and not ctx.has_attempted_auto_load:
            if ctx.is_last_save_normal is not None and not ctx.is_last_save_normal:
                ctx.ipc.load_state(ctx.state_slot)

            if ctx.is_last_save_normal is not None:
                ctx.has_attempted_auto_load = True

        if ctx.ipc.is_in_control():
            ctx.player_control = True

            await asyncio.sleep(1)

        # Run maintenance game checks when not in player control
        if not ctx.suppress_progress_correction:
            await correct_progress(ctx)
        await check_background_states(ctx)

        await asyncio.sleep(0.5)
        return
    elif not ctx.ipc.is_in_control():
        ctx.player_control = False
        return

    # Do not attempt autoload when player is already in-game
    if not ctx.has_attempted_auto_load:
        ctx.has_attempted_auto_load = True

    # Check for Archipelago Connection Errors
    if ctx.server:
        ctx.last_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        # Initialize important variables if not yet initialized
        if ctx.last_item_processed_index < 0:
            ctx.last_item_processed_index = ctx.ipc.get_last_item_index()

        # If there are offline locations to send, do so
        if ctx.offline_locations_checked:
            await update_offline_checked(ctx)

        # Get Character
        if ctx.character < 0:
            ctx.character = ctx.ipc.get_character()

        # Get Cached PGC Status on connect
        if ctx.has_just_connected:
            ctx.post_game_condition.passed = ctx.ipc.check_pgc_cache()

        # Setup Stage when needed and double check locations
        if ctx.in_travel_station:
            if ctx.current_channel != APHelper.travel_station.value:
                ctx.in_travel_station = False
                ctx.is_using_data_desk = False

                if ctx.current_channel == APHelper.shopping_area.value:
                    ctx.in_shopping_area = True
                    await set_persistent_values(ctx)
        elif ctx.in_shopping_area:
            if ctx.current_channel != APHelper.shopping_area.value:
                ctx.in_shopping_area = False

                if ctx.current_channel == APHelper.travel_station.value:
                    await reapply_persistent_values(ctx)
                    ctx.in_travel_station = True
        else:
            if ctx.current_channel == APHelper.travel_station.value:
                ctx.in_travel_station = True
            elif ctx.current_channel == APHelper.shopping_area.value:
                ctx.in_shopping_area = True
                ctx.is_using_data_desk = False
                await rebuild_persistent_values(ctx)
            else:
                ctx.is_using_data_desk = False

        if ctx.in_travel_station:
            await setup_level_select(ctx)
        elif ctx.in_shopping_area:
            await setup_shopping_area(ctx)

        # Build Checked Location Cache
        if not ctx.is_cache_built and not ctx.is_using_data_desk:
            if ctx.cache_missing:
                await build_checked_cache(ctx)
            else:
                if ctx.shoppingsanity == 2:
                    await handle_collection_shop_item_recheck(ctx)

                ctx.is_cache_built = True

        await setup_area(ctx)
        await check_states(ctx)

        # Check Progression
        await receive_items(ctx)

        if not ctx.is_using_data_desk:
            if not ctx.in_travel_station:
                await check_locations(ctx)
            elif ctx.is_cache_built:
                await sweep_recheck_locations(ctx)

        # Revoke has just connected (of Game) status once the first checks are done
        if ctx.has_just_connected or ctx.pending_resync:
            await resync_important_items(ctx)
            ctx.has_just_connected = False

            if ctx.pending_resync:
                logger.info(" [-!-] Resyncing Complete!")
                ctx.pending_resync = False

        # Save State if desired and reset pending state
        if ctx.pending_auto_save and ctx.state_slot >= 0:
            ctx.ipc.save_state(ctx.state_slot)
            ctx.pending_auto_save = False

            if ctx.load_state_on_connect and (ctx.is_last_save_normal or ctx.is_last_save_normal is None):
                ctx.is_last_save_normal = False
                await set_last_save_status(ctx)

        # Sleep functions keep the client from being unresponsive
        await asyncio.sleep(0.5)

    else:
        message : str = APConsole.Info.p_init_sre.value
        if ctx.last_message is not message:
            logger.info(APConsole.Info.p_init_sre.value)
            ctx.last_message = message

        await asyncio.sleep(1)

async def reconnect_game(ctx : AE3Context):
    ctx.ipc.connect_game()
    await asyncio.sleep(3)

def parse_version(version: str) -> list[str]:
    """
    Converts String of version into a list of attributes (Major.minor.patch-pre+build)

    We use a modified version of Semver for our purposes:
        > Major - Denotes a significant feature update and will not have backwards compatibility
            with any other major version.
        > Minor - Denotes a small feature update and will not have backwards compatibility with previous minor versions.
        > Patch - Denotes bug fixes with compatability with other versions of the same minor and major version.
        > Pre - Denotes a pre-release that is not compatible with any other pre-release version
            of the same Major and Minor version.
        > Build - Denotes a minor pre-release patch that is compatible with the same Major, Minor and Pre version.
    """

    if not str:
        return []

    ext: list[str] = [*version.split("+")]
    ext = [*ext[0].split("-"), *ext[1:]]
    ext = [*ext[0].split("."), *ext[1:]]

    if len(ext) == 4:
        ext.append("0")

    return ext

def compare_versions(subject: list[str], base: list[str]) -> int:
    if len(subject) < 3 or len(base) < 3 or len(subject) != len(base):
        return -2

    # Major Check
    if subject[0] != base[0]:
        return -1

    # Minor Check
    if subject[1] != base[1]:
        return -1

    # Pre Check
    if len(subject) >= len(base) > 3 and subject[3] != base[3]:
        return -1

    return 0

def assert_version_compatibility(subject: str, base: str):
    subject_ver: list[str] = parse_version(subject)
    base_ver: list[str] = parse_version(base)

    error: int = compare_versions(subject_ver, base_ver)

    if not error:
        return

    if error == -2:
        raise AssertionError(f"The world being connected to has been generated with an incompatible version of "
                             f"Ape Escape 3 Archipelago. Connection Aborted.")

    elif error == -1:
        raise AssertionError(f"The world being connected to has been generated with an Ape Escape 3 Archipelago "
                             f"version that this client is not compatible with. Connection Aborted."
                             f"\nWorld version: {subject}\nClient version: {base}")

# Starting point of function
async def main(args: Namespace):
    multiprocessing.freeze_support()

    # Create Game Context
    ctx = AE3Context(args.connect, args.password)

    # Archipelago Server Connections
    logger.info(APConsole.Info.p_init_s.value)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

    if tracker_loaded:
        ctx.run_generator()
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    # Create Main Loop
    ctx.interface_sync_task = asyncio.create_task(main_sync_task(ctx), name="PCSX2 Sync")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await ctx.shutdown()

    # Call Main Client Loop
    if ctx.interface_sync_task:
        await asyncio.sleep(3)
        await ctx.interface_sync_task

def launch(*args: str):
    launch_init(*args)

def launch_init(*args: Sequence[str]) -> None:
    # Run Client
    import colorama

    # Parse Command Line
    parser: ArgumentParser = get_base_parser()
    parser.add_argument("--patch", default="", type=str, nargs="?",
                        help="Path to an Archipelago Patch File")
    parser.add_argument("--name", default="", type=str, nargs="?", help="Slot Name to connect as")
    parser.add_argument("--url", default="", type=str, nargs="?",
                        help="URL of Archipelago Room to connect to")
    launch_args: Namespace = handle_url_arg(parser.parse_args(*args))

    colorama.init()
    asyncio.run(main(launch_args))
    colorama.deinit()

# Ensures file will only run as the main file
if __name__ == '__main__':
    launch(*sys.argv[1:])