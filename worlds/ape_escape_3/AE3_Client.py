from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence
from datetime import datetime
import io
import os.path
import typing
import multiprocessing
import traceback
import asyncio
import json

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled, \
                          ClientStatus
import Utils
from settings import get_settings

from .data.Strings import Meta, APConsole
from .data.Logic import ProgressionMode, ProgressionModeOptions
from .data.Locations import CELLPHONES_MASTER, MONKEYS_MASTER, MONKEYS_PASSWORDS, MONKEYS_MASTER_ORDERED, \
    CAMERAS_MASTER_ORDERED, CELLPHONES_MASTER_ORDERED
from .data.Stages import STAGES_BREAK_ROOMS, LEVELS_BY_ORDER
from .data.Rules import GoalTarget, GoalTargetOptions, PostGameAccessRule, PostGameAccessRuleOptions
from .AE3_Interface import ConnectionStatus, AEPS2Interface
from . import AE3Settings
from .Checker import *
from .data import Items, Locations


class AE3CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_status(self):
        if isinstance(self.ctx, AE3Context):
            logger.info(f" [-^-] Client Status")

            logger.info(f" [-o-] Game")

            if self.ctx.server:
                logger.info(f"{
                            "         Playing Ape Escape 3" if self.ctx.is_connected 
                            else "         No Game Detected"
                            }")
                logger.info(f"         Goal Target is " 
                            f"{self.ctx.goal_target}")
                logger.info(f"         > Progress: "
                            f"{str(self.ctx.goal_target.get_progress(self.ctx))} / "
                            f"{self.ctx.goal_target.amount}")

                if ((len(self.ctx.goal_target.locations) == 1 and Loc.boss_specter_final.value in
                        self.ctx.goal_target.locations) or self.ctx.shuffle_channel):
                    logger.info(f"\n         Post-Game Requirement is "
                                f"{self.ctx.post_game_access_rule}")
                    logger.info(f"         > Progress: "
                                f"{str(self.ctx.post_game_access_rule.get_progress(self.ctx))} / "
                                f"{self.ctx.post_game_access_rule.amount}")

                all_keys : int = len(self.ctx.progression.progression) - 1
                if self.ctx.post_game_access_rule_option < 4:
                    all_keys -= 1

                logger.info(f"\n         Progression:")
                logger.info(f"         Channel Keys: {self.ctx.keys} / {all_keys}")
                logger.info(f"         Available Levels: {self.ctx.unlocked_channels + 1} / 28\n")
                for level in range(self.ctx.unlocked_channels + 1):
                    logger.info(f"         [ {level + 1} ] {LEVELS_BY_ORDER[self.ctx.progression.order[level]]}")

            else:
                logger.info(f"         Disconnected from Server")

            logger.info(f"\n [-=-] Settings")
            logger.info(f"         Auto-Equip is " 
                        f"{"ENABLED" if self.ctx.auto_equip else "DISABLED"}")

            if self.ctx.early_free_play:
                logger.info(f"         Freeplay Swap is " 
                            f"{"ENABLED" if self.ctx.swap_freeplay else "DISABLED"}")
            else:
                logger.info(f"         Early Freeplay is DISABLED and Freeplay Swap cannot be toggled.")

            logger.info(f"         DeathLink is " 
                        f"{"ENABLED" if self.ctx.death_link else "DISABLED"}")

    def _cmd_remaining(self):
        """List remaining locations to check to Goal."""
        if not isinstance(self.ctx, AE3Context):
            return

        if not self.ctx.server or not self.ctx.goal_target:
            logger.info(f" [!!!] Please connect to an Archipelago Server first!")
        elif self.ctx.game_goaled:
            logger.info(f" [-!-] You have already Goaled! You have no more remaining checks!")

        logger.info(f" [-!-] Remaining Target Locations:")
        remaining : list[str] = self.ctx.goal_target.get_remaining(self.ctx)

        for location in remaining:
            logger.info(f"         > " f"{location}")

    def _cmd_auto_equip(self):
        """Toggle if Gadgets should automatically be assigned to a free face button when received."""
        if isinstance(self.ctx, AE3Context):
            self.ctx.auto_equip = not self.ctx.auto_equip

            logger.info(f" [-!-] Freeplay Swap is now " f"{"ENABLED" if self.ctx.swap_freeplay else "DISABLED"}")


    def _cmd_freeplay(self):
        """Toggle if Free Play mode and Time Attack mode should be swapped, allowing Free Play to become available
        earlier.
        """
        if isinstance(self.ctx, AE3Context):
            if not self.ctx.early_free_play:
                logger.info(f" [!!!] Early Free Play was set to DISABLED. You cannot toggle Freeplay Swap.")
                return

            self.ctx.swap_freeplay = not self.ctx.swap_freeplay

            logger.info(f" [-!-] Freeplay Swap is now " f"{"ENABLED" if self.ctx.swap_freeplay else "DISABLED"}")

    async def _cmd_deathlink(self):
        """Toggle if death links should be received."""
        if isinstance(self.ctx, AE3Context):
            self.ctx.death_link = not self.ctx.death_link

            logger.info(f" [-!-] DeathLink is now " f"{"ENABLED" if self.ctx.death_link else "DISABLED"}")

            await self.ctx.update_death_link(self.ctx.death_link)
    # # Debug commands
    # def _cmd_unlock(self, unlocks : str = "28"):
    #     """<!> DEBUG | Unlock amount of levels given"""
    #     if not unlocks.isdigit():
    #         logger.info("Please enter a number.")
    #         return
    #
    #     if isinstance(self.ctx, AE3Context):
    #         amount: int = int(unlocks)
    #         self.ctx.unlocked_channels = max(min(amount, 28), 0)
    #
    # def _cmd_receive_death(self, count : str = "1"):
    #     """<!> DEBUG | Simulate receiving a death link"""
    #     if not count.isdigit():
    #         logger.info("Please enter a number.")
    #         return
    #
    #     if isinstance(self.ctx, AE3Context):
    #         if self.ctx.death_link:
    #             logger.info(" [!!!] DeathLink is currently DISABLED. Deathlink cannot be received.")
    #             return
    #
    #         amount : int = int(count)
    #         self.ctx.pending_deathlinks += amount

class AE3Context(CommonContext):
    # Archipelago Meta
    client_version: str = APConsole.Info.client_ver.value
    world_version : str = APConsole.Info.world_ver.value

    # Game Details
    game: str = Meta.game
    platform: str = Meta.platform

    # Client Properties
    command_processor : ClientCommandProcessor = AE3CommandProcessor
    items_handling : int = 0b111
    save_data_path : str = None
    save_data_filename : str = None

    # Interface Properties
    ipc : AEPS2Interface = AEPS2Interface
    is_connected : bool = ConnectionStatus.DISCONNECTED
    interface_sync_task : asyncio.tasks = None
    last_message : Optional[str] = None

    # Server Properties and Cache
    next_item_slot : int = 0
    pending_deathlinks : int = 0
    cached_locations_checked : Set[int]
    offline_locations_checked : Set[int] = set()
    cached_received_items : Set[NetworkItem]

    # APWorld Properties
    locations_name_to_id : dict[str, int] = Locations.generate_name_to_id()
    items_name_to_id : dict[str, int] = Items.generate_name_to_id()

    monkeys_checklist : Sequence[str] = MONKEYS_MASTER
    monkeys_checklist_count : int = 0

    cellphones_checklist : Sequence[str] = CELLPHONES_MASTER

    # Session Properties
    keys : int = 0
    unlocked_channels : int = 0
    current_channel: str = None
    current_stage : str = None
    character : int = -1
    player_control : bool = False

    swap_freeplay : bool = False
    is_mode_swapped : bool = True
    is_channel_swapped : bool = False

    ## Command State can be in either of 3 stages:
    ##  0 - No Exclusive Command Sent
    ##  1 - Command has been sent, awaiting confirmation of execution
    ##  2 - Command Executed, awaiting confirmation to reset
    command_state : int = 0
    sending_death : bool = False
    are_item_status_synced : bool = False
    are_location_status_synced : bool = False

    rcc_unlocked : bool = False
    swim_unlocked : bool = False
    dummy_morph_needed : bool = True
    dummy_morph_monkey_needed : bool = True
    morphs_unlocked : list[bool] = [False for _ in range(7)]

    tomoki_defeated : bool = False
    specter1_defeated : bool = False

    game_goaled : bool = False

    # Player Set Settings
    settings : AE3Settings

    auto_equip : bool = False

    # Player Set Options
    progression : ProgressionMode = ProgressionModeOptions[0]
    goal_target : GoalTarget = GoalTarget()
    post_game_access_rule_option : int = 0
    post_game_access_rule : PostGameAccessRule = PostGameAccessRule()
    shuffle_channel : bool = False
    dummy_morph : str = Itm.morph_monkey.value
    camerasanity : int = None
    cellphonesanity : bool = None

    morph_duration : float = 0.0

    early_free_play : bool = False

    death_link : bool = False

    def __init__(self, address, password):
        super().__init__(address, password)

        # Initialize Variables
        Utils.init_logging(APConsole.Info.client_name.value + self.client_version)

        self.ipc = AEPS2Interface(logger)

        self.cached_locations_checked = set()
        self.cached_received_items = set()

        # Define Save Data Path
        self.save_data_path = Utils.user_path() + "/data/saves"
        if not os.path.isdir(self.save_data_path):
            try:
                os.mkdir(self.save_data_path)
            except OSError:
                self.save_data_path = ""

        if self.save_data_path:
            self.save_data_path += "/"

        # Load Settings
        self.settings = get_settings().get("ape_escape_3_options", False)
        assert self.settings, " [!!!] Cannot find Ape Escape 3 Settings!"

        self.auto_equip = self.settings.auto_equip

    # Archipelago Server Authentication
    async def server_auth(self, password_requested : bool = False):
        # Ask for Password if Requested so
        if password_requested and not self.password:
            await super(AE3Context, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        # First Connection Check
        if cmd == APHelper.cmd_conn.value:
            data = args[APHelper.arg_sl_dt.value]

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

            # Define Goal Target for other options that need it
            goal_target: int = 0

            ## Post-Game Access Rule
            if APHelper.post_game_access_rule.value in data:
                self.post_game_access_rule_option = data[APHelper.post_game_access_rule.value]

            ## Check Break Room Monkeys and Password Monkeys options to use with Goal Target
            add_break_rooms : bool = self.post_game_access_rule_option == 0

            excluded_stages : list[str] = []
            excluded_locations : list[str] = [*MONKEYS_PASSWORDS]
            additional_locations : list[str] = []

            ## Monkeysanity - Break Rooms
            if APHelper.monkeysanitybr.value in data:
                add_break_rooms = add_break_rooms or bool(data[APHelper.monkeysanitybr.value])

                if data[APHelper.monkeysanitybr.value] < 2:
                    self.dummy_morph = Itm.morph_knight.value

            if not add_break_rooms:
                excluded_stages = [*STAGES_BREAK_ROOMS]

            ## Goal Target
            if not self.goal_target.locations and APHelper.goal_target.value in data:
                goal_target = data[APHelper.goal_target.value]
                self.goal_target = GoalTargetOptions[goal_target](excluded_stages, excluded_locations)

            ### Exclude locations from final channel
            excluded_locations.extend(MONKEYS_MASTER_ORDERED[self.progression.order[-1]])
            excluded_locations.extend(CELLPHONES_MASTER_ORDERED[self.progression.order[-1]])
            excluded_locations.append(CAMERAS_MASTER_ORDERED[self.progression.order[-1]])

            # If Specter is a Post Game Access Rule, and he gets shuffled to become the post game channel,
            # change the required location to the next penultimate placed boss
            if (self.post_game_access_rule_option >= 4 and
                self.progression.order[-1] == self.progression.boss_indices[-2]):
                if MONKEYS_BOSSES[-2] in excluded_locations:
                    excluded_locations.remove(MONKEYS_BOSSES[-2])

                    for level in reversed(self.progression.order):
                        if level == self.progression.boss_indices[-2]:
                            continue
                        elif level in self.progression.boss_indices:
                            additional_locations.append(MONKEYS_BOSSES[self.progression.boss_indices.index(level)])
                            break

            ## Post Game Access Rule Initialization
            self.post_game_access_rule = PostGameAccessRuleOptions[self.post_game_access_rule_option](
                    excluded_stages, excluded_locations, additional_locations)

            ## Shuffle Channel
            if APHelper.shuffle_channel.value in data:
                self.shuffle_channel = data[APHelper.shuffle_channel.value]

            ## Camerasanity
            if self.camerasanity is None and APHelper.camerasanity.value in data:
                self.camerasanity = (data[APHelper.camerasanity.value] or goal_target == 5 or
                                     self.post_game_access_rule_option == 2)

            ## Cellphonesanity
            if self.cellphonesanity is None and APHelper.cellphonesanity.value in data:
                self.cellphonesanity = (data[APHelper.cellphonesanity.value] or goal_target == 6 or
                                        self.post_game_access_rule_option == 3)

            ## Morph Duration
            if self.morph_duration == 0 and APHelper.base_morph_duration.value in data:
                self.morph_duration = float(data[APHelper.base_morph_duration.value])

            ## Early Free Play
            if APHelper.early_free_play.value in data:
                self.early_free_play = data[APHelper.early_free_play.value]

            ## DeathLink
            if APHelper.death_link.value in data:
                self.death_link = bool(data[APHelper.death_link.value])
                Utils.async_start(self.update_death_link(self.death_link))

            ## Location Status Sync
            if self.are_location_status_synced or not self.checked_locations:
                return

            received_as_id : list[int] = [ l for l in self.checked_locations]

            self.tomoki_defeated = self.locations_name_to_id[Loc.boss_tomoki.value] in received_as_id
            self.specter1_defeated = self.locations_name_to_id[Loc.boss_specter.value] in received_as_id

            self.are_location_status_synced = True

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

            ## Get Keys
            self.keys = received_as_id.count(self.items_name_to_id[APHelper.channel_key.value])
            self.unlocked_channels = self.progression.get_progress(self.keys)

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

        # Initialize Session on receive of RoomInfo Packet
        elif cmd == APHelper.cmd_rminfo.value:
            seed: str = args[APHelper.arg_seed.value]
            if self.seed_name != seed:
                self.seed_name = seed

            self.save_data_filename = Meta.game_acr + "_" + self.seed_name + ".json"

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        super().on_deathlink(data)

        if not self.death_link:
            return

        self.pending_deathlinks += 1

    # @deprecated("Local Storage of Session Data is unused at the moment.")
    def check_session_save(self) -> bool:
        """Check for valid save file"""
        if not self.save_data_filename:
            return False
        elif not self.save_data_path:
            return False

        # return (os.path.isfile(self.save_data_path + self.save_data_filename) and
        #         os.access(self.save_data_path + self.save_data_filename, os.R_OK))
        return False

    # @deprecated("Local Storage of Session Data is unused at the moment.")
    def load_session(self):
        """Load existing session"""
        if not self.check_session_save():
            return

        with io.open(self.save_data_path + self.save_data_filename, 'r') as save:
            data : dict = json.load(save)

            # Retrieve Next Item Slot/Amount of Items Received
            #self.next_item_slot = data.get(APHelper.item_count.value, 0)

            # Retrieve Offline Checked Locations
            self.offline_locations_checked = set(data.get(APHelper.offline_checked_locations.value, set()))

            # Retrieve Key
            if APHelper.channel_key.value in data:
                self.keys = data[APHelper.channel_key.value]
                self.unlocked_channels = self.progression.get_progress(self.keys)

            # Retrieve Character
            if Game.character.value in data:
                self.character = data[Game.character.value]

                # Retrieve Morph Duration
                if Game.morph_duration.value in data:
                    self.morph_duration = data[Game.morph_duration.value]
                    self.ipc.set_morph_duration(self.character, self.morph_duration)

            # Retrieve Important Items
            self.rcc_unlocked = data.get(Itm.gadget_rcc.value, False)
            self.swim_unlocked = data.get(Itm.gadget_swim.value, False)

        self.ipc.logger.info(" [-!-] A Session Data save has been found and successfully loaded.")

    # @deprecated("Local Storage of Session Data is unused at the moment.")
    def save_session(self):
        """Save current session progress"""
        if self.game_goaled:
            return

        # Prevent Spammed Messages
        if not self.save_data_filename or not self.save_data_path:
            logger.warning(APConsole.Err.save_no_init.value)
            return

        data = {
            APHelper.goaled.value                       : self.game_goaled,
            APHelper.last_save.value                    : datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),

            #APHelper.item_count.value                   : self.next_item_slot,
            APHelper.offline_checked_locations.value    : [*self.offline_locations_checked],

            APHelper.channel_key.value                  : self.keys,
            Game.character.value                        : self.character,
            Itm.gadget_rcc.value                        : self.rcc_unlocked,
            Itm.gadget_swim.value                       : self.swim_unlocked,
            Game.morph_duration.value                   : self.morph_duration
        }
        with io.open(self.save_data_path + self.save_data_filename, 'w') as save:
            save.write(json.dumps(data))

    # @deprecated("Local Storage of Session Data is unused at the moment.")
    def delete_session(self):
        if not self.check_session_save():
            return

        if not self.settings or not self.settings.delete_goaled:
            return

        try:
            if os.path.isfile(self.save_data_path + self.save_data_filename):
                os.remove(self.save_data_path + self.save_data_filename)
        except OSError:
            pass

        if not self.check_session_save():
            self.ipc.logger.info(" [-!-] Current Session Data has successfully been erased.")

    # @deprecated("Local Storage of Session Data is unused at the moment.")
    def clean_sessions(self):
        """
        This will attempt to delete Session Data that has already goaled or has not been saved too for too long
        depending on the set user options.
        """
        if not self.save_data_path or not os.path.isdir(self.save_data_path):
            return

        if not self.settings.delete_goaled and not self.settings.delete_excess and not self.settings.delete_old:
            return

        files: dict[str, int] = {}
        discard: list[str] = []

        for file in self.save_data_path:
            # Only check the AE3 Save JSON files
            if not file.startswith("AE3_") and not file.endswith(".json"):
                continue

            # Ensure this is actually a file
            if not os.path.isfile(self.save_data_path + "/" + file):
                continue

            try:
                with io.open(self.save_data_path + self.save_data_filename, 'r') as save:
                    data = json.load(save)

                    if self.settings.delete_goaled and APHelper.goaled.value in data:
                        if data[APHelper.goaled.value]:
                            discard.append(file)
                            continue

                    if APHelper.last_save.value in data:
                        delta : int = (datetime.now() - datetime.strptime(data[APHelper.last_save.value],
                                                                             "%Y-%m-%dT%H:%M:%S.%fZ")).days
                        # Immediately add to discard pile if last save is more than the specified amount of days
                        if self.settings.delete_old and delta > self.settings.delete_old:
                            discard.append(file)
                        # Otherwise, send to be checked for excess remaining
                        elif self.settings.delete_excess:
                            files.setdefault(file, delta)
            except OSError as error:
                print(error)
                return

        # Sort by days since last saved in ascending order, and remove the oldest ones that exceed the excess amount
        if len(files) > 10:
            excess_amount : int = len(files) - self.settings.delete_excess - 1
            excess : list[str] = [*dict(sorted(files.items(), key=lambda f : file[1])).keys()]

            discard.extend(excess[-excess_amount:])

        if discard:
            try:
                for file in discard:
                    os.remove(self.save_data_path + "/" + file)
            except OSError as error:
                print(error)
                return

    # Client Command GUI
    def run_gui(self):
        from kvui import GameManager

        class AE3Manager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = APConsole.Info.game_name.value

        self.ui = AE3Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name = "ui")

    async def goal(self):
        if self.game_goaled:
            return

        await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        self.game_goaled = True


def update_connection_status(ctx : AE3Context, status : bool):
    if ctx.is_connected == status:
        return

    if status:
        logger.info(APConsole.Info.init_game.value)
    else:
        logger.info(APConsole.Err.sock_fail.value + APConsole.Err.sock_re.value)

    ctx.is_connected = status

# Main Client Loop
async def main_sync_task(ctx : AE3Context):
    # Greetings
    logger.info(APConsole.Info.decor.value)
    logger.info("    " + APConsole.Info.greet.value)
    logger.info("    " + APConsole.Info.world_ver.value + "    " + APConsole.Info.client_ver.value)
    logger.info(APConsole.Info.decor.value)
    logger.info("\n")
    logger.info(APConsole.Info.p_init.value)
    ctx.ipc.connect_game()

    while not ctx.exit_event.is_set():
        try:
            # Check connection to PCSX2 first
            is_connected = ctx.ipc.get_connection_state()
            update_connection_status(ctx, is_connected)

            # Check Progress if connection is good
            if is_connected:
                await check_game(ctx)

            # Attempt reconnection to PCSX2 otherwise
            else:
                await reconnect_game(ctx)
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
    # Check if Game State is safe for Further Checking
    if not ctx.player_control:
        if ctx.ipc.is_in_control():
            ctx.player_control = True

            await asyncio.sleep(1)

        # Run maintenance game checks when not in player control
        await correct_progress(ctx)
        await check_background_states(ctx)

        await asyncio.sleep(0.5)
        return
    elif not ctx.ipc.is_in_control():
        ctx.player_control = False
        return

    # Check for Archipelago Connection Errors
    if ctx.server:
        ctx.last_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        # Get Character
        if ctx.character < 0:
            ctx.character = ctx.ipc.get_character()

        # Setup Stage when needed and double check locations
        if ctx.current_channel == APHelper.travel_station.value:
            await setup_level_select(ctx)
            await recheck_location_groups(ctx)
        else:
            await setup_area(ctx)

        await check_states(ctx)

        # Check Progression
        await check_items(ctx)
        await check_locations(ctx)

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

# Starting point of function
def launch():
    async def main():
        multiprocessing.freeze_support()

        # Parse Command Line
        parser : ArgumentParser = get_base_parser()
        parser.add_argument("AE3AP_file", default="", type=str, nargs="?",
                            help="Path to an Archipelago Patch File")
        args : Namespace = parser.parse_args()

        # Create Game Context
        ctx = AE3Context(args.connect, args.password)

        # Archipelago Server Connections
        logger.info(APConsole.Info.p_init_s.value)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

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

    # Run Client
    import colorama

    colorama.init()
    asyncio.run(main())
    colorama.deinit()

# Ensures file will only run as the main file
if __name__ == '__main__':
    launch()