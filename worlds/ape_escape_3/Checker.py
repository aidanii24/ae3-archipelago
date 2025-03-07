from typing import TYPE_CHECKING, Set, List

from NetUtils import NetworkItem

from .data.Items import EquipmentItem, CollectableItem, UpgradeableItem
from .data.Addresses import GameStates
from .data.Locations import MONKEYS
from .data.Strings import APHelper, Game
from .data import Items

if TYPE_CHECKING:
    from .AE3_Client import AE3Context

### [< --- CHECKS --- >]
async def check_states(ctx : 'AE3Context'):
    # Make sure progress is always set to "round2"
    if ctx.cached_locations_checked and not ctx.player_control:
        await force_progress(ctx)

    # Check current stage
    stage_as_bytes = ctx.ipc.pine.read_bytes(GameStates[Game.current_stage.value], 4)
    ctx.current_stage = stage_as_bytes.decode("utf-8")

async def setup_level_select(ctx : 'AE3Context'):
    if ctx.ipc.pine.read_int32(GameStates[Game.levels_unlocked.value]) > 0x1B:
        ctx.ipc.pine.write_int32(GameStates[Game.levels_unlocked.value], ctx.progress)

async def force_progress(ctx : 'AE3Context'):
    value : bytes = ctx.ipc.pine.read_bytes(GameStates[Game.progress.value], 8)
    value_decoded : str = bytes.decode(value)
    ctx.current_stage = value_decoded

    if value_decoded != APHelper.round2.value:
        as_bytes: bytes = APHelper.round2.value.encode() + b'\x00'
        ctx.ipc.pine.write_bytes(GameStates[APHelper.round2.value], as_bytes)

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