import asyncio

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus
import Utils

from .AE3_Interface import connection_status

class ae3_command_processor(ClientCommandProcessor):
    def __init__(self, ctx : CommonContext):
        super().__init__(ctx)
    
    def _cmd_connect(self, address : str = "") -> bool:
        super()._cmd_connect(self, address)

class ae3_context(CommonContext):
    # Feature/Refactor Release : Patch/Minor Release : Minor Patch Release
    client_version : str = "v0.1a"
    
    game : str = "Ape Escape 3"
    platform : str = "PS2"

    is_connected : connection_status = 0

    def __init__(self):
        super().__init__(self)
        Utils.init_logging("Ape Escape 3 Archipelago Client" + self.client_version)

    async def get_username(self):
        if not self.auth:
            self.auth = self.username

            if not self.auth:
                logger.info("Please enter your Player/Slot name:")
                self.auth = await self.console_input()

async def connect_client(ctx : ae3_context):
    ctx.ae_ps2_interface.connect_game()

def update_connection_status(ctx : ae3_context, status : bool):
    if ctx.is_connected == status:
        return
    
    if status:
        logger.info("Connected to Ape Escape 3!")
    else:
        logger.info("Cannot connect to PCSX2. Retrying to connect...")
    
    ctx.is_connected = status

async def interafce_sync_task(ctx : ae3_context):
    logger.info("Initializing Ape Escape 3 IPC Interface. Starting connection to PCSX2...")
    ctx.AE3_Interface.connect_game()

    ctx.connect_game()

def start():
    async def main():
        ctx = ae3_context()

        logger.info("Connecting to the Archipelago Server...")

        ctx.server_task = asyncio.create_task(server_loop(ctx), name = "Server Loop")

        if gui_enabled:
            ctx.run_gui
        ctx.run_cli

        ctx.interafce_sync_task = asyncio.create_task(interafce_sync_task(ctx), name = "PCSX2 Sync")

        if ctx.interafce_sync_task:
            await asyncio.sleep(3)
            await ctx.interafce_sync_task
    
    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()

if __name__ == '__main__':
    start()