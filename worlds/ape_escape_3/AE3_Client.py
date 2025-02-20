from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus

from .AE3_Interface import connection_status

class ae3_command_processor(ClientCommandProcessor):
    def __init__(self, ctx : CommonContext):
        super().__init__(ctx)
    
    def _cmd_connect(self, address : str = "") -> bool:
        super()._cmd_connect(self, address)

class ae3_context(CommonContext):
    game : str = "Ape Escape 3"
    is_connected : connection_status = 0

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

    async def get_username(self):
        if not self.auth:
            self.auth = self.username

            if not self.auth:
                logger.info("Please enter your Player/Slot name:")
                self.auth = await self.console_input()

async def connect_client(ctx : ae3_context):
    logger.info("Initializing Ape Escape 3 IPC Interface. Starting connection to PCSX2...")
    ctx.ae_ps2_interface.connect_game()

def update_connection_status(ctx : ae3_context, status : bool):
    if ctx.is_connected == status:
        return
    
    if status:
        logger.info("Connected to Ape Escape 3!")
    else:
        logger.info("Cannot connect to PCSX2. Retrying to connect...")
    
    ctx.is_connected = status