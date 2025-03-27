from typing import TYPE_CHECKING, Set, List

from NetUtils import ClientStatus, NetworkItem

from .data.Items import ArchipelagoItem, EquipmentItem, CollectableItem, UpgradeableItem
from .data.Strings import Game, Itm, APHelper
from .data.Addresses import NTSCU, AP
from .data.Locations import Loc, MONKEYS_BOSSES, MONKEYS_DIRECTORY
from .data import Items

if TYPE_CHECKING:
    from .AE3_Client import AE3Context


### [< --- CHECKS --- >]
async def check_states(ctx : 'AE3Context'):
    # Get current stage
    new_stage = ctx.ipc.get_channel()

    # Enforce Morph Duration
    if ctx.character >= 0:
        if ctx.ipc.get_morph_duration(ctx.character) != ctx.morph_duration:
            ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration)

        # Character could be wrong if morph duration still is not equal after the first set
        if ctx.ipc.get_morph_duration(ctx.character) != ctx.morph_duration:
            ctx.character = ctx.ipc.get_character()
            ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration)


    # Get which Monkey Group to actively check at the moment based on the stage
    if not new_stage or new_stage is None and not ctx.current_channel:
        # Special Check for Monkey Pink as her boss stage does not provide a Stage ID
        if ctx.ipc.is_in_pink_boss():
            ctx.monkeys_checklist = MONKEYS_BOSSES
            ctx.current_channel = APHelper.boss4.value
        # Recheck locations by each stage while loading
        else:
            await recheck_location_groups(ctx)
            await check_locations(ctx)

        return
    elif new_stage != ctx.current_channel:
        if new_stage in MONKEYS_DIRECTORY:
            ctx.monkeys_checklist = MONKEYS_DIRECTORY[new_stage]
        elif "b" in new_stage:
            ctx.monkeys_checklist = MONKEYS_BOSSES
    else:
        return

    ctx.current_channel = new_stage

async def recheck_location_groups(ctx : 'AE3Context'):
    if ctx.monkeys_checklist_count >= len(MONKEYS_DIRECTORY.values()):
        ctx.monkeys_checklist_count = 0

    ctx.monkeys_checklist = [*MONKEYS_DIRECTORY.values()][ctx.monkeys_checklist_count]
    ctx.monkeys_checklist_count += 1

# Ensure game is always set to "round2"
async def correct_progress(ctx : 'AE3Context'):
    ctx.ipc.set_progress()

async def setup_level_select(ctx : 'AE3Context'):
    # Force Unlocked Stages to be in sync with the player's chosen option,
    # maxing out at 0x1B as supported by the game
    if ctx.ipc.get_unlocked_channels() > max(0, min(ctx.unlocked_channels, 0x1B)):
        ctx.ipc.set_unlocked_stages(ctx.unlocked_channels)

    progress : str = ctx.ipc.get_progress()
    selected_stage: int = ctx.ipc.get_selected_channel()

    # In case player scrolls beyond intended levels before unlocked stages are enforced,
    # force selected level to be the latest unlocked stage
    if selected_stage > ctx.unlocked_channels:
        ctx.ipc.set_selected_stage(ctx.unlocked_channels)

    # Change Progress temporarily for certain levels to be playable. Change back to round2 otherwise.
    if ctx.ipc.is_on_warp_gate():
        # Dr. Tomoki Battle!
        if selected_stage == 0x18 and not ctx.tomoki_defeated:
            ctx.ipc.set_progress(APHelper.pr_boss6.value)
        # Specter Battle!
        elif selected_stage == 0x1A and not ctx.specter1_defeated:
            ctx.ipc.set_progress(APHelper.pr_specter1.value)
        elif progress != APHelper.pr_round2.value:
            ctx.ipc.set_progress()
    elif progress != APHelper.pr_round2.value:
        ctx.ipc.set_progress()

    # If Super Monkey isn't properly unlocked yet, temporarily do so during level select to prevent Aki from
    # introducing and giving it to the player.
    if not ctx.has_morph_monkey:
        ctx.ipc.unlock_equipment(Itm.morph_monkey.value)

    # Temporarily unlock all Chassis when not in Travel Station to make sure their models load correctly when obtained
    # RC Car Chassis can't be changed in levels, so it is safe to keep them on until the next Travel Station visit
    if not ctx.rcc_unlocked:
        if not ctx.ipc.is_a_level_confirmed():
            for _ in range(3):
                ctx.ipc.lock_chassis_direct(_)
        else:
            for _ in range(3):
                ctx.ipc.unlock_chassis_direct(_)

async def setup_area(ctx : 'AE3Context'):
    if ctx.ipc.is_screen_fading():
        if ctx.ipc.get_screen_fade_count() > 0x0:
            ctx.ipc.lock_equipment(Itm.morph_monkey.value)
        # Temporarily give a morph during transitions to keep Morph Gauge visible
        else:
            ctx.ipc.unlock_equipment(Itm.morph_monkey.value)
    else:
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
            ### Add Key Count and unlock levels accordingly
            if item.item_id == AP[APHelper.channel_key.value]:
                ctx.keys += 1
                ctx.unlocked_channels = ctx.progression.get_current_progress(ctx.keys)

            ### Update Server about Goal Achieved when Victory is achieved
            if item.item_id == AP[APHelper.victory.value]:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        ## Unlock Morphs and Gadgets
        elif isinstance(item, EquipmentItem):
            ctx.ipc.unlock_equipment(item.name, ctx.character, auto_equip)

            ### Check if RC Car or any Chassis is unlocked
            if ctx.rcc_unlocked and item.name in Itm.get_chassis_by_id(ctx.character):
                ctx.rcc_unlocked = True

                # Relock all other RC cars
                for idx, name in Itm.get_chassis_by_id(no_default=True):
                    if name == item.name:
                        continue

                    ctx.ipc.lock_chassis_direct(idx)

            ### Check if Super Monkey is properly unlocked
            if not ctx.has_morph_monkey and item.address == NTSCU.Items[Itm.morph_monkey.value]:
                ctx.has_morph_monkey = True

        ## Handle Collectables
        elif isinstance(item, CollectableItem) or isinstance(item, UpgradeableItem):
            i = item
            maximum : int | float = 0x0

            if isinstance(item, CollectableItem):
                maximum = item.capacity

            ### <!> NTSC-U Addresses are used when identifying Items regardless of region
            if item.address == NTSCU.GameStates[Game.nothing.value]:
                continue

            ### Handle Morph Energy
            elif item.resource == Game.morph_gauge_active.value:
                ctx.ipc.give_morph_energy(i.amount)

            ### Handle Morph Extension
            elif item.resource == Game.duration_knight_b.value:
                ctx.morph_duration += item.amount
                ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration)

            ### Handle Generic Items
            else:
                ctx.ipc.give_collectable(item.resource, i.amount, maximum)

        # Add to temporary container; to be cached as a single batched after
        cache_batch_items.add(server_item)

    # Add to Cache
    ctx.cached_received_items.update(cache_batch_items)

async def check_locations(ctx : 'AE3Context'):
    cleared : Set[int] = set()

    for monkey in ctx.monkeys_checklist:
        # Special Case for Tomoki
        if ctx.current_channel == APHelper.boss6.value:
            if ctx.ipc.is_tomoki_defeated():
                cleared.add(ctx.monkeys_name_to_id[Loc.boss_tomoki.value])
                continue

        if ctx.ipc.is_monkey_captured(monkey):
            cleared.add(ctx.monkeys_name_to_id[monkey])

            if monkey == Loc.boss_specter.value:
                ctx.specter1_defeated = True

    # Get newly checked locations
    cleared = cleared.difference(ctx.checked_locations)

    # Send newly checked locations to server
    if cleared:
        await ctx.send_msgs([{"cmd" : "LocationChecks", "locations" : cleared}])
        ctx.cached_locations_checked.update(cleared)