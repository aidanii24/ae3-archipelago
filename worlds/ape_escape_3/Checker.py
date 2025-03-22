from typing import TYPE_CHECKING, Set, List

from NetUtils import NetworkItem

from .data.Items import ArchipelagoItem, EquipmentItem, CollectableItem, UpgradeableItem
from .data.Strings import Game, Itm, APHelper
from .data.Addresses import NTSCU, AP
from .data.Locations import MONKEYS_BOSSES, MONKEYS_DIRECTORY
from .data import Items

if TYPE_CHECKING:
    from .AE3_Client import AE3Context


### [< --- CHECKS --- >]
async def check_states(ctx : 'AE3Context'):
    # Get current stage; remove null bytes if present
    new_stage = ctx.ipc.get_stage().removesuffix("\x00")

    # Get which Monkey Group to actively check at the moment based on the stage
    if new_stage != APHelper.travel_station.value and new_stage == ctx.current_stage:
        return
    if new_stage == "" or new_stage is None :
        pass
    elif new_stage in MONKEYS_DIRECTORY:
        ctx.monkeys_checklist = MONKEYS_DIRECTORY[new_stage]
    elif "b" in new_stage:
        ctx.monkeys_checklist = MONKEYS_BOSSES
    # Iteratively check when in TV Station or Shopping District
    else:
        if ctx.monkeys_checklist_count >= len(MONKEYS_DIRECTORY.values()):
            ctx.monkeys_checklist_count = 0

        ctx.monkeys_checklist = [*MONKEYS_DIRECTORY.values()][ctx.monkeys_checklist_count]
        ctx.monkeys_checklist_count += 1

    ctx.current_stage = new_stage

# Ensure game is always set to "round2"
async def correct_progress(ctx : 'AE3Context'):
    ctx.ipc.set_progress()

async def setup_level_select(ctx : 'AE3Context'):
    # Force Unlocked Stages to be in sync with the player's chosen option,
    # maxing out at 0x1B as supported by the game
    if ctx.ipc.get_unlocked_stages() > max(0, min(ctx.unlocked_stages, 0x1B)):
        ctx.ipc.set_unlocked_stages(ctx.unlocked_stages)

    progress : str = ctx.ipc.get_progress()
    selected_stage: int = ctx.ipc.get_selected_stage()

    # In case player scrolls beyond intended levels before unlocked stages are enforced,
    # force selected level to be the latest unlocked stage
    if selected_stage > ctx.unlocked_stages:
        ctx.ipc.set_selected_stage(ctx.unlocked_stages)

    # Allow players to select Dr. Tomoki Battle by temporarily setting the game progress to boss6
    # Set back to round2 otherwise, or when exiting level select
    if not ctx.tomoki_defeated:
        if ctx.ipc.check_warp_gate_state():
            if selected_stage == 0x18:
                ctx.ipc.set_progress(APHelper.pr_boss6.value)
            elif progress != APHelper.pr_round2.value:
                ctx.ipc.set_progress()
        elif progress != APHelper.pr_round2.value:
            ctx.ipc.set_progress()

    # If Super Monkey isn't properly unlocked yet, temporarily do so during level select to prevent Aki from
    # introducing and giving it to the player.
    if not ctx.has_morph_monkey:
        ctx.ipc.unlock_equipment(Itm.morph_monkey.value)

        if ctx.ipc.check_stage_confirmed_state():
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
        ## Handle Archipelago Items
        if isinstance(item, ArchipelagoItem):
            # Add Key Count and unlock levels accordingly
            if item.item_id == AP[APHelper.channel_key.value]:
                ctx.keys += 1
                ctx.unlocked_stages = ctx.progression.get_current_progress(ctx.keys)

        ## Unlock Morphs and Gadgets
        elif isinstance(item, EquipmentItem):
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

    for monkey in ctx.monkeys_checklist:
        # Special Case for Tomoki
        if ctx.current_stage == APHelper.boss6.value:
            if ctx.ipc.is_tomoki_defeated():
                cleared.add(ctx.monkeys_name_to_id[monkey])
                continue

        if ctx.ipc.is_monkey_captured(monkey):
            cleared.add(ctx.monkeys_name_to_id[monkey])

    # Get newly checked locations
    cleared = cleared.difference(ctx.checked_locations)

    # Send newly checked locations to server
    if cleared:
        await ctx.send_msgs([{"cmd" : "LocationChecks", "locations" : cleared}])
        ctx.cached_locations_checked.update(cleared)