import io
import os.path
import typing
from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence
import multiprocessing
import traceback
import asyncio
import json

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
import Utils

from .data.Strings import Meta, APConsole
from .data.Logic import GameMode
from .data.Locations import MONKEYS_MASTER, generate_name_to_id
from .AE3_Interface import ConnectionStatus, AEPS2Interface
from .Checker import *


class AE3CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_status(self):
        if isinstance(self.ctx, AE3Context):
            logger.info(f"{APConsole.Info.p_check.value}"
                        f"{APConsole.Info.init.value if self.ctx.is_connected else APConsole.Info.exit.value}")

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
    cached_received_items : Set[NetworkItem]

    # APWorld Properties
    monkeys_name_to_id : dict[str, int] = generate_name_to_id()
    monkeys_checklist : Sequence[str] = MONKEYS_MASTER
    monkeys_checklist_count : int = 0

    # Session Properties
    keys : int = 0
    unlocked_channels : int = 0
    current_channel: str = None
    character : int = -1
    player_control : bool = False
    ## Command State can be in either of 3 stages:
    ##  0 - No Exclusive Command Sent
    ##  1 - Command has been sent, awaiting confirmation of execution
    ##  2 - Command Executed, awaiting confirmation to reset
    command_state : int = 0
    sending_death : bool = False
    rcc_unlocked : bool = False
    swim_unlocked : bool = False
    morphs_unlocked : list[bool] = [False for _ in range(7)]
    tomoki_defeated : bool = False
    specter1_defeated : bool = False

    # Player Set Options
    auto_equip : bool = False
    morph_duration : float = 0.0
    progression : GameMode = GameMode.BOSS
    death_link : bool = False

    def __init__(self, address, password):
        super().__init__(address, password)
        Utils.init_logging(APConsole.Info.client_name.value + self.client_version)

        self.ipc = AEPS2Interface(logger)

        self.cached_locations_checked = set()
        self.cached_received_items = set()

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

            ## Game Mode
            if not self.unlocked_channels and APHelper.game_mode.value in self.slot_data:
                self.progression = GameMode.get_gamemode(self.slot_data[APHelper.game_mode.value])
                self.unlocked_channels = self.progression.get_current_progress(0)

            ## Morph Duration
            if self.morph_duration == 0 and APHelper.base_morph_duration.value in self.slot_data:
                self.morph_duration = float(self.slot_data[APHelper.base_morph_duration.value])

            ## Auto-Equip
            if APHelper.auto_equip.value in self.slot_data:
                self.auto_equip = bool(self.slot_data[APHelper.auto_equip.value])

            ## DeathLink
            if APHelper.arg_deathl.value in self.slot_data:
                self.death_link = bool(self.slot_data[APHelper.arg_deathl.value])
                Utils.async_start(self.update_death_link(self.death_link))

        # Initialize Session on receive of RoomInfo Packet
        elif cmd == APHelper.cmd_rminf.value:
            seed: str = args[APHelper.arg_seed.value]
            if self.seed_name != seed:
                self.seed_name = seed

            self.save_data_path = Meta.game_acr + "_" + self.seed_name + ".json"

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        super().on_deathlink(data)

        self.pending_deathlinks += 1

    def check_session_save(self):
        """Check for valid save file"""
        if not self.save_data_path:
            return False

        return os.path.isfile(self.save_data_path) and os.access(self.save_data_path, os.R_OK)

    def load_session(self):
        """Load existing session"""
        if not self.check_session_save():
            return

        with io.open(self.save_data_path, 'r') as save:
            data : dict = json.load(save)

            # Retrieve Next Item Slot/Amount of Items Received
            if APHelper.item_count.value in data:
                self.next_item_slot = data[APHelper.item_count.value]

            # Retrieve Key
            if APHelper.channel_key.value in data:
                self.keys = data[APHelper.channel_key.value]
                self.unlocked_channels = self.progression.get_current_progress(self.keys)

            # Retrieve Character
            if Game.character.value in data:
                self.character = data[Game.character.value]

                # Retrieve Morph Duration
                if Game.duration_knight_b.value in data:
                    self.morph_duration = data[Game.duration_knight_b.value]
                    self.ipc.set_morph_duration(self.character, self.morph_duration)

            # Retrieve Important Items
            if Itm.gadget_rcc.value in data:
                self.rcc_unlocked = data[Itm.gadget_rcc.value]

            if Itm.gadget_swim.value in data:
                self.swim_unlocked = data[Itm.gadget_swim.value]

    def save_session(self):
        """Save current session progress"""
        # Prevent Spammed Messages
        if not self.last_message == APConsole.Info.saving.value:
            logger.info(APConsole.Info.saving.value)
            self.last_message = APConsole.Info.saving.value

        if not self.save_data_path:
            logger.warning(APConsole.Err.save_no_init.value)
            return

        data = {
            APHelper.item_count.value       : self.next_item_slot,

            APHelper.channel_key.value      : self.keys,
            Game.character.value            : self.character,
            Itm.gadget_rcc.value            : self.rcc_unlocked,
            Itm.gadget_swim.value           : self.swim_unlocked,
            Game.duration_knight_b.value    : self.morph_duration
        }

        with io.open(self.save_data_path, 'w') as save:
            save.write(json.dumps(data))

    # Client Command GUI
    def run_gui(self):
        from kvui import GameManager

        class AE3Manager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = APConsole.Info.game_name.value

        self.ui = AE3Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name = "ui")


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