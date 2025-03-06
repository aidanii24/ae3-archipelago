from argparse import ArgumentParser, Namespace
from typing import Optional, Set
import multiprocessing
import traceback
import asyncio

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import NetworkItem
import Utils

from .data.Strings import APHelper, Meta, APConsole
from .AE3_Interface import ConnectionStatus, AEPS2Interface
from .Checker import check_locations, check_items


class AE3CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_status(self):
        if isinstance(self.ctx, AE3Context):
            logger.info(f"PCSX2 Status: {'Connected' if self.ctx.is_connected else 'Disconnected'}")

class AE3Context(CommonContext):
    # Feature/Refactor Release : Patch/Minor Release : Minor Patch Release
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

    player_control : bool = True
    current_stage = None

    auto_equip : bool = False

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
    # Check if Game State is safe for Checking
    if ctx.player_control:
        if not ctx.ipc.can_control():
            ctx.player_control = False
            await asyncio.sleep(1)

        await asyncio.sleep(0.5)
        return
    elif ctx.ipc.can_control():
        ctx.player_control = True
        return

    # Check for Archipelago Connection Errors
    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        # Check Progression
        await check_items(ctx)

        if await check_locations(ctx):
            # Await after new location check to reduce connection drops (improves PONG efficacy)
            await asyncio.sleep(1)

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