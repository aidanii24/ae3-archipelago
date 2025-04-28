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
from .data.Logic import ProgressionMode
from .data.Locations import CELLPHONES_MASTER, MONKEYS_MASTER, generate_name_to_id
from .data.Rules import GoalTarget, GoalTargetOptions
from .AE3_Interface import ConnectionStatus, AEPS2Interface
from . import AE3Settings
from .Checker import *


class AE3CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_status(self):
        if isinstance(self.ctx, AE3Context):
            logger.info(f" [-^-] Client Status")
            logger.info(f" [-o-] Game:\n         "
                        f"{
                        "Playing Ape Escape 3" if self.ctx.is_connected 
                        else "Not Connected to PCSX2"
                        }")
            logger.info(f"\n [-=-] Settings")
            logger.info(f"         Freeplay Swap is " f"{"ENABLED" if self.ctx.swap_freeplay else "DISABLED"}")
            logger.info(f"         DeathLink is " f"{"ENABLED" if self.ctx.death_link else "DISABLED"}")

    def _cmd_freeplay(self):
        """
        Toggle if Free Play mode and Time Attack mode should be swapped, allowing Free Play to become available
        earlier.
        """
        if isinstance(self.ctx, AE3Context):
            if isinstance(self.ctx, AE3Context):
                if not self.ctx.early_free_play:
                    logger.info(f" [!!!] Early Free Play was set to DISABLED. You cannot toggle Freeplay Swap.")
                    return

                self.ctx.swap_freeplay = not self.ctx.swap_freeplay

                logger.info(f" [-!-] Freeplay Swap is now " f"{"ENABLED" if self.ctx.swap_freeplay else "DISABLED"}")

    def _cmd_deathlink(self):
        """Toggle if death links should be received."""
        if isinstance(self.ctx, AE3Context):
            self.ctx.death_link = not self.ctx.death_link

            logger.info(f" [-!-] DeathLink is now " f"{"ENABLED" if self.ctx.death_link else "DISABLED"}")
    # Debug commands
    def _cmd_unlock(self, unlocks : str = "28"):
        """<!> DEBUG | Unlock amount of levels given"""
        if not unlocks.isdigit():
            logger.info("Please enter a number.")
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
            amount : int = int(count)
            self.ctx.pending_deathlinks += amount

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
    slot_data : dict[str, Utils.Any]
    next_item_slot : int = 0
    pending_deathlinks : int = 0
    cached_locations_checked : Set[int]
    offline_locations_checked : Set[int] = set()
    cached_received_items : Set[NetworkItem]

    # APWorld Properties
    locations_name_to_id : dict[str, int] = generate_name_to_id()

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
    ## Command State can be in either of 3 stages:
    ##  0 - No Exclusive Command Sent
    ##  1 - Command has been sent, awaiting confirmation of execution
    ##  2 - Command Executed, awaiting confirmation to reset
    swap_freeplay : bool = False
    is_mode_swapped : bool = True
    command_state : int = 0
    sending_death : bool = False
    rcc_unlocked : bool = False
    swim_unlocked : bool = False
    morphs_unlocked : list[bool] = [False for _ in range(7)]
    tomoki_defeated : bool = False
    specter1_defeated : bool = False
    game_goaled : bool = False

    # Player Set Settings
    settings : AE3Settings

    auto_equip : bool = False

    # Player Set Options
    progression: ProgressionMode = ProgressionMode.BOSS
    goal_target : GoalTarget = GoalTarget()
    dummy_morph : int = -1
    camerasanity : int = None
    cellphonesanity : bool = None

    morph_duration: float = 0.0

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

        # Attempt Session Save Directory Cleaning
        self.clean_sessions()

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
            self.slot_data = args[APHelper.arg_sl_dt.value]

            ## Load Local Session Save Data
            if self.check_session_save():
                self.load_session()

            ## Progression Mode
            if not self.unlocked_channels and APHelper.progression_mode.value in self.slot_data:
                self.progression = ProgressionMode.get_progression_mode(self.slot_data[APHelper.progression_mode.value])
                self.unlocked_channels = self.progression.get_current_progress(0)

            ## Goal Target
            if not self.goal_target.locations and APHelper.goal_target.value in self.slot_data:
                self.goal_target = GoalTargetOptions[self.slot_data[APHelper.goal_target.value]]()

            ## Monkeysanity - Break Rooms
            if APHelper.monkeysanitybr.value in self.slot_data:
                if self.slot_data[APHelper.monkeysanitybr.value] < 2:
                    self.dummy_morph = 0

            ## Camerasanity
            if self.camerasanity is None and APHelper.camerasanity.value in self.slot_data:
                self.camerasanity = self.slot_data[APHelper.camerasanity.value]

            ## Cellphonesanity
            if self.cellphonesanity is None and APHelper.cellphonesanity.value in self.slot_data:
                self.cellphonesanity = self.slot_data[APHelper.cellphonesanity.value]

            ## Morph Duration
            if self.morph_duration == 0 and APHelper.base_morph_duration.value in self.slot_data:
                self.morph_duration = float(self.slot_data[APHelper.base_morph_duration.value])

            ## Early Free Play
            if APHelper.early_free_play.value in self.slot_data:
                self.early_free_play = self.slot_data[APHelper.early_free_play.value]
                self.swap_freeplay = self.early_free_play

            ## DeathLink
            if APHelper.death_link.value in self.slot_data:
                self.death_link = bool(self.slot_data[APHelper.death_link.value])
                Utils.async_start(self.update_death_link(self.death_link))

        # Initialize Session on receive of RoomInfo Packet
        elif cmd == APHelper.cmd_rminfo.value:
            seed: str = args[APHelper.arg_seed.value]
            if self.seed_name != seed:
                self.seed_name = seed

            self.save_data_filename = Meta.game_acr + "_" + self.seed_name + ".json"

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        super().on_deathlink(data)

        self.pending_deathlinks += 1

    def check_session_save(self) -> bool:
        """Check for valid save file"""
        if not self.save_data_filename:
            return False
        elif not self.save_data_path:
            return False

        return (os.path.isfile(self.save_data_path + self.save_data_filename) and
                os.access(self.save_data_path + self.save_data_filename, os.R_OK))

    def load_session(self):
        """Load existing session"""
        if not self.check_session_save():
            return

        with io.open(self.save_data_path + self.save_data_filename, 'r') as save:
            data : dict = json.load(save)

            # Retrieve Next Item Slot/Amount of Items Received
            self.next_item_slot = data.get(APHelper.item_count.value, 0)

            # Retrieve Offline Checked Locations
            self.offline_locations_checked = set(data.get(APHelper.offline_checked_locations.value, set()))

            # Retrieve Key
            if APHelper.channel_key.value in data:
                self.keys = data[APHelper.channel_key.value]
                self.unlocked_channels = self.progression.get_current_progress(self.keys)

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

            APHelper.item_count.value                   : self.next_item_slot,
            APHelper.offline_checked_locations.value    : [*self.offline_locations_checked],

            APHelper.channel_key.value                  : self.keys,
            Game.character.value                        : self.character,
            Itm.gadget_rcc.value                        : self.rcc_unlocked,
            Itm.gadget_swim.value                       : self.swim_unlocked,
            Game.morph_duration.value                   : self.morph_duration
        }
        with io.open(self.save_data_path + self.save_data_filename, 'w') as save:
            save.write(json.dumps(data))

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
            excess : list[str] = [*dict(sorted(files.items(), key=lambda file : file[1])).keys()]

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
        await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


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

        # Setup Stage when needed and double check locations
        if ctx.current_channel == APHelper.travel_station.value:
            # Initialize properties after tutorial
            if ctx.character < 0:
                ctx.character = ctx.ipc.get_character()

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