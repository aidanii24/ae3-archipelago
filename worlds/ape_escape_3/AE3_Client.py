import asyncio

from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled
import Utils

from .AE3_Interface import AEPS2Interface, ConnectionStatus

class ae3_command_processor(ClientCommandProcessor):
    def __init__(self, ctx : CommonContext):
        super().__init__(ctx)

class AE3Context(CommonContext):
    # Feature/Refactor Release : Patch/Minor Release : Minor Patch Release
    client_version : str = "v0.1a"
    
    game : str = "Ape Escape 3"
    platform : str = "PS2"

    ipc : AEPS2Interface = AEPS2Interface()
    is_connected : ConnectionStatus = 0

    def __init__(self):
        super().__init__()
        Utils.init_logging("Ape Escape 3 Archipelago Client" + self.client_version)

    async def get_username(self):
        if not self.auth:
            self.auth = self.username

            if not self.auth:
                logger.info("Please enter your Player/Slot name:")
                self.auth = await self.console_input()

def update_connection_status(ctx : AE3Context, status : ConnectionStatus):
    if ctx.is_connected == status:
        return
    
    if status:
        logger.info("Connected to Ape Escape 3!")
    else:
        logger.info("Cannot connect to PCSX2. Retrying to connect...")
    
    ctx.is_connected = status

async def interafce_sync_task(ctx : AE3Context):
    logger.info("Initializing Ape Escape 3 IPC Interface. Starting connection to PCSX2...")
    ctx.ipc.connect_game()

def start():
    async def main():
        ctx = AE3Context()

        logger.info("Connecting to the Archipelago Server...")

        ctx.server_task = asyncio.create_task(server_loop(ctx), name = "Server Loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.interface_sync_task = asyncio.create_task(interafce_sync_task(ctx), name = "PCSX2 Sync")

        if ctx.interface_sync_task:
            await asyncio.sleep(3)
            await ctx.interface_sync_task
    
    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()

if __name__ == '__main__':
    start()