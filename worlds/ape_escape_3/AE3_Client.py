from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus

class ae3_command_processor(ClientCommandProcessor):
    def __init__(self, ctx : CommonContext):
        super().__init__(ctx)
    
    def _cmd_connect(self, address : str = "") -> bool:
        super()._cmd_connect(self, address)