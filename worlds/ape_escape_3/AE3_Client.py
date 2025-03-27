from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence
import multiprocessing
import traceback
import asyncio

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
    client_version: str = APConsole.Info.client_ver.value
    world_version : str = APConsole.Info.world_ver.value

    game: str = Meta.game
    platform: str = Meta.platform

    command_processor = AE3CommandProcessor
    items_handling = 0b111

    ipc : AEPS2Interface = AEPS2Interface
    is_connected : bool = ConnectionStatus.DISCONNECTED
    interface_sync_task : asyncio.tasks = None
    last_error_message : Optional[str] = None

    slot_data : dict[str, Utils.Any]
    cached_locations_checked : Set[int]
    cached_received_items : Set[NetworkItem]

    monkeys_name_to_id : dict[str, int] = generate_name_to_id()
    monkeys_checklist : Sequence[str] = MONKEYS_MASTER
    monkeys_checklist_count : int = 0

    keys : int = 0
    unlocked_channels : int = 0
    current_channel: str = None
    character : int = -1
    player_control : bool = False
    # Each byte corresponds to the unlocked chassis, in the same order as their ID's (excluding default)
    rcc_unlocked : bool = False
    has_morph_monkey : bool = False
    tomoki_defeated : bool = False
    specter1_defeated : bool = False

    auto_equip : bool = False
    morph_duration : float = 10.0
    progression : GameMode = GameMode.BOSS

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
        if cmd != "Connected":
            return

        self.slot_data = args["slot_data"]

        # Get Relevant Runtime options
        ## Game Mode
        if APHelper.game_mode.value in args["slot_data"]:
            self.progression = GameMode.get_gamemode(args["slot_data"][APHelper.game_mode.value])
            self.unlocked_channels = self.progression.get_current_progress(0)

        ## Morph Duration
        if APHelper.base_morph_duration.value in args["slot_data"]:
            self.morph_duration = float(args["slot_data"][APHelper.base_morph_duration.value])

        ## Auto-Equip
        if APHelper.auto_equip.value in args["slot_data"]:
            self.auto_equip = bool(args["slot_data"][APHelper.auto_equip.value])

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
        await check_states(ctx)

        await asyncio.sleep(0.5)
        return
    elif not ctx.ipc.is_in_control():
        ctx.player_control = False
        return

    # Check for Archipelago Connection Errors
    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        # Setup Stage when needed and double check locations
        if ctx.current_channel == APHelper.travel_station.value:
            # Get character after Tutorial
            if ctx.character < 0:
                ctx.character = ctx.ipc.get_character()

            await setup_level_select(ctx)
            await recheck_location_groups(ctx)
        else:
            await setup_area(ctx)

        # Check Progression
        await check_items(ctx)
        await check_locations(ctx)

        # Sleep functions keep the client from being unresponsive
        await asyncio.sleep(0.5)

    else:
        message : str = APConsole.Info.p_init_sre.value
        if ctx.last_error_message is not message:
            logger.info(APConsole.Info.p_init_sre.value)
            ctx.last_error_message = message

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