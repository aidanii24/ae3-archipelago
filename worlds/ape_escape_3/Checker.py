from typing import TYPE_CHECKING, Set, List

from NetUtils import NetworkItem

from .data.Items import EquipmentItem, CollectableItem, UpgradeableItem
from .data.Addresses import GameStates, Items
from .data.Locations import MONKEYS
from .data.Strings import Game, Itm
from .data import Items

if TYPE_CHECKING:
    from .AE3_Client import AE3Context

### [< --- CHECKS --- >]

async def check_states(ctx : 'AE3Context'):
    # Get current stage
    ctx.current_stage = ctx.ipc.get_stage()

# Ensure game is always set to "round2"
async def correct_progress(ctx : 'AE3Context'):
    ctx.ipc.set_progress()

async def setup_level_select(ctx : 'AE3Context'):
    # In case levels unlocked value glitches out from forcing progression to round2
    if ctx.ipc.pine.read_int32(GameStates[Game.levels_unlocked.value]) > 0x1B:
        ctx.ipc.pine.write_int32(GameStates[Game.levels_unlocked.value], ctx.unlocked_levels)

    # If Super Monkey isn't properly unlocked yet, temporarily do so during level select to prevent Aki from
    # introducing and giving it to the player.
    if not ctx.has_morph_monkey and ctx.ipc.check_warp_gate_state():
        ctx.ipc.unlock_equipment(Items[Itm.morph_monkey.value])

        if ctx.ipc.check_level_confirmed_state():
            ctx.ipc.lock_equipment(Items[Itm.morph_monkey.value])

async def check_items(ctx : 'AE3Context'):
    cache_batch_items : Set[NetworkItem] = set()

    # Get Difference to get only new items
    received : List[NetworkItem] = list(set(ctx.items_received).difference(ctx.cached_received_items))

    # Auto-equip if option is enabled or for handling the starting gadgets
    auto_equip: bool = ctx.auto_equip or not ctx.cached_received_items

    for server_item in received:
        item = Items.from_id(server_item.item)

        # Handle Item depending on category
        ## Unlock Morphs and Gadgets
        if isinstance(item, EquipmentItem):
            ctx.ipc.unlock_equipment(item.address, auto_equip)

        ## Handle Collectables
        elif isinstance(item, CollectableItem) or isinstance(item, UpgradeableItem):
            i = item

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