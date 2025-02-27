from typing import Optional
from argparse import ArgumentParser, Namespace
import asyncio
import traceback

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
import Utils

from .AE3_Interface import AEPS2Interface
from .Checker import check_locations, check_items


class AE3CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_status(self):
        if isinstance(self.ctx, AE3Context):
            logger.info(f"PCSX2 Status: {'Connected' if self.ctx.is_connected else 'Disconnected'}")

class AE3Context(CommonContext):
    # Feature/Refactor Release : Patch/Minor Release : Minor Patch Release
    client_version: str = "v0.1a"

    game: str = "Ape Escape 3"
    platform: str = "PS2"

    ipc : AEPS2Interface = AEPS2Interface
    is_connected : bool = False
    interface_sync_task : asyncio.tasks = None
    last_error_message : Optional[str] = None

    player_control : bool = True
    current_stage = None

    auto_equip : bool = False

    def __init__(self, address, password):
        super().__init__(address, password)
        Utils.init_logging("Ape Escape 3 Archipelago Client" + self.client_version)

    # Archipelago Server Authentication
    async def server_auth(self, password_requested : bool = False):
        # Ask for Password if Requested so
        if password_requested and not self.password:
            await super(AE3Context, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    # Client Command GUI
    def run_gui(self):
        from kvui import GameManager

        class AE3Manager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Ape Escape 3 Archipelago"

        self.ui = AE3Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name = "ui")

def update_connection_status(ctx : AE3Context, status : bool):
    if ctx.is_connected == status:
        return

    if status:
        logger.info("Connected to Ape Escape 3!")
    else:
        logger.info("Cannot connect to PCSX2. Retrying to connect...")

    ctx.is_connected = status

# Main Client Loop
async def interface_sync_task(ctx : AE3Context):
    logger.info("Initializing PINE Interface, Attempting to connect to PCSX2")
    ctx.ipc.connect_game()

    while not ctx.exit_event.is_set():
        try:
            is_connected = ctx.ipc.get_connection_state()
            update_connection_status(ctx, is_connected)
            if is_connected:
                await check_game(ctx)
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
        if not ctx.ipc.get_player_state():
            ctx.player_state = ctx.ipc.get_player_state()
            await asyncio.sleep(1)
        return
    elif ctx.ipc.get_player_state():
        ctx.player_control = True
        return

    # Check for Connection Errors
    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        # Check Progression
        await check_items(ctx)
        await check_locations(ctx)
    else:
        message : str = "Waiting for player to connect to server..."
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server...")
            ctx.last_error_message = message

        await asyncio.sleep(1)

async def reconnect_game(ctx : AE3Context):
    ctx.ipc.connect_game()
    await asyncio.sleep(3)

def launch():
    async def main():
        # Parse Command Line
        parser : ArgumentParser = get_base_parser()
        parser.add_argument("AE3AP_file", default="", type=str, nargs="?",
                            help="Path to an Archipelago Patch File")
        args : Namespace = parser.parse_args()

        # Create Game Context
        ctx = AE3Context(args.connect, args.password)

        # Archipelago Server Connections
        logger.info("Connecting to the Archipelago Server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        # Create Main Loop
        ctx.interface_sync_task = asyncio.create_task(interface_sync_task(ctx), name="PCSX2 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        # Call Main Client Loop
        if ctx.interface_sync_task:
            await asyncio.sleep(3)
            await ctx.interface_sync_task

    # Run Client
    import colorama

    colorama.init()
    asyncio.run(main())
    colorama.deinit()


if __name__ == '__main__':
    launch()