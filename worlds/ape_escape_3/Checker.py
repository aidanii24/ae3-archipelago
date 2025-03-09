from typing import TYPE_CHECKING, Set, List

from NetUtils import NetworkItem

from .data.Items import EquipmentItem, CollectableItem, UpgradeableItem
from .data.Addresses import NTSCU
from .data.Locations import MONKEYS
from .data.Strings import Game, Itm
from .data import Items

if TYPE_CHECKING:
    from .AE3_Client import AE3Context

### [< --- CHECKS --- >]

async def check_states(ctx : 'AE3Context'):
    # Get current stage; remove null bytes if present
    ctx.current_stage = ctx.ipc.get_stage().removesuffix("\x00")

# Ensure game is always set to "round2"
async def correct_progress(ctx : 'AE3Context'):
    ctx.ipc.set_progress()

async def setup_level_select(ctx : 'AE3Context'):
    # Force Unlocked Levels to be in sync with the player's chosen option,
    # maxing out at 0x1B as supported by the game
    if ctx.ipc.get_unlocked_stages() > min(ctx.unlocked_stages, 0x1B):
        ctx.ipc.set_unlocked_levels(ctx.unlocked_stages)

    # If Super Monkey isn't properly unlocked yet, temporarily do so during level select to prevent Aki from
    # introducing and giving it to the player.
    if not ctx.has_morph_monkey:
        ctx.ipc.unlock_equipment(Itm.morph_monkey.value)

        if ctx.ipc.check_level_confirmed_state():
            ctx.ipc.lock_equipment(Itm.morph_monkey.value)

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
            ctx.ipc.unlock_equipment(item.name, auto_equip)

            if not ctx.has_morph_monkey and item.address == NTSCU.Items[Itm.morph_monkey.value]:
                ctx.has_morph_monkey = True

        ## Handle Collectables
        elif isinstance(item, CollectableItem) or isinstance(item, UpgradeableItem):
            i = item

            ### <!> NTSC-U Addresses are used when identifying Items regardless of region
            if item.address == NTSCU.GameStates[Game.nothing.value]:
                continue

            ### Handle Morph Energy
            elif item.resource == Game.morph_gauge_active.value:
                ctx.ipc.give_morph_energy(i.amount)

            ### Handle Generic Items
            else:
                ctx.ipc.give_collectable(item.resource, i.amount)

        # Add to temporary container; to be cached as a single batched after
        cache_batch_items.add(server_item)

    # Add to Cache
    ctx.cached_received_items.update(cache_batch_items)

async def check_locations(ctx : 'AE3Context'):
    cleared : Set[int] = set()

    for monkey in MONKEYS:
        if ctx.ipc.is_monkey_captured(monkey.name):
            cleared.add(monkey.address)

    # Get newly checked locations
    cleared = cleared.difference(ctx.checked_locations)

    # Send newly checked locations to server
    if cleared:
        await ctx.send_msgs([{"cmd" : "LocationChecks", "locations" : cleared}])
        ctx.cached_locations_checked.update(cleared)