from typing import TYPE_CHECKING, Set, List

from NetUtils import NetworkItem

from .data.Items import EquipmentItem, CollectableItem
from .data.Addresses import GameStates, get_gadget_id
from .data.Locations import MONKEYS
from .data.Strings import Game
from .data import Items

if TYPE_CHECKING:
    from .AE3_Client import AE3Context

### [< --- CHECKS --- >]
async def check_items(ctx : 'AE3Context'):
    cache_batch_items : Set[NetworkItem] = set()

    # Get Difference to get only new items
    received : List[NetworkItem] = list(set(ctx.items_received).difference(ctx.cached_received_items))

    for server_item in received:
        item = Items.from_id(server_item.item)

        # Handle Item depending on category
        ## Unlock Morphs and Gadgets
        if isinstance(item, EquipmentItem):
            ctx.ipc.unlock_equipment(item.address)

            if not ctx.cached_received_items:
                ctx.ipc.auto_equip(get_gadget_id(item.address))

        ## Handle Collectables
        elif isinstance(item, CollectableItem):
            i : CollectableItem = item

            ### Handle Morph Energy
            if item.address == GameStates[Game.morph_gauge_active.value]:
                ctx.ipc.give_morph_energy(i.amount)

            ### Handle Generic Items
            else:
                ctx.ipc.give_collectable(item.address, i.amount)

        # Add to temporary container; to be cached as a single batched after
        cache_batch_items.add(server_item)

    # Add to Cache
    ctx.cached_received_items.update(cache_batch_items)

async def check_locations(ctx : 'AE3Context') -> bool:
    cleared : Set[int] = set()

    for monkey in MONKEYS:
        if ctx.ipc.pine.read_int8(monkey.address) == 0x01:
            cleared.add(monkey.address)

    # Get newly checked locations
    cleared = cleared.difference(ctx.checked_locations)

    # Send newly checked locations to server
    if cleared:
        await ctx.send_msgs([{"cmd" : "LocationChecks", "locations" : cleared}])
        ctx.cached_locations_checked.update(cleared)
        return True
    return False