from typing import TYPE_CHECKING, Set

from .data import Items
from .data.Addresses import Address
from .data.Items import item_group

if TYPE_CHECKING:
    from .AE3_Client import AE3Context

async def check_items(ctx : 'AE3Context'):
    # Get Items from server
    for server_item in ctx.items_received:
        item = Items.from_id(server_item.item)

        # Check for new Gadgets/Morphs
        if item in item_group["Equipment"]:
            ctx.ipc.unlock_equipment(server_item.item)

async def check_locations(ctx : 'AE3Context'):
    cleared : Set[int] = set()

    for key, value in Address.locations:
        if ctx.ipc.ipc.read_int8(value) == 0x01:
            cleared.add(value)

    # Get newly checked locations
    cleared = cleared.difference(ctx.checked_locations)

    # Send newly checked locations to server
    await ctx.send_msgs([{"cmd" : "LocationChecks", "locations" : cleared}])