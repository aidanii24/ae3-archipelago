from typing import TYPE_CHECKING, Set, List

from NetUtils import ClientStatus, NetworkItem

from .data.Items import ArchipelagoItem, EquipmentItem, CollectableItem, UpgradeableItem
from .data.Strings import Game, Itm, APHelper
from .data.Addresses import Capacities, NTSCU, AP, Cellphone_ID
from .data.Locations import ACTORS_INDEX, CELLPHONES_STAGE_INDEX, Loc, CAMERAS_STAGE_INDEX, MONKEYS_BOSSES, \
    MONKEYS_DIRECTORY
from .data import Items

if TYPE_CHECKING:
    from .AE3_Client import AE3Context


### [< --- CHECKS --- >]
async def check_background_states(ctx : 'AE3Context'):
    # Get current stage
    new_channel = ctx.ipc.get_channel()
    ctx.current_stage = ctx.ipc.get_stage()

    # Enforce Morph Duration
    if ctx.character >= 0:
        current_morph_duration : float = ctx.ipc.get_morph_duration(ctx.character)
        unlocked_morphs : list[int] = [idx for idx, _ in enumerate(ctx.morphs_unlocked) if _]

        if current_morph_duration != ctx.morph_duration or current_morph_duration != 0.0:
            ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration, unlocked_morphs)

        # Character could be wrong if morph duration still is not equal after the first set
        current_morph_duration = ctx.ipc.get_morph_duration(ctx.character)
        if current_morph_duration != ctx.morph_duration or current_morph_duration != 0.0:
            ctx.character = ctx.ipc.get_character()
            ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration, unlocked_morphs)

    # Get which Monkey Group to actively check at the moment based on the stage
    if not new_channel or new_channel is None and not ctx.current_channel:
        # Special Check for Monkey Pink as her boss stage does not provide a Stage ID
        if ctx.ipc.is_in_pink_boss():
            ctx.monkeys_checklist = MONKEYS_BOSSES
            ctx.current_channel = APHelper.boss4.value
        # Recheck locations by each stage while loading
        else:
            await recheck_location_groups(ctx)
            await check_locations(ctx)

        return
    elif new_channel != ctx.current_channel:
        if new_channel in MONKEYS_DIRECTORY:
            ctx.monkeys_checklist = MONKEYS_DIRECTORY[new_channel]
        elif "b" in new_channel:
            ctx.monkeys_checklist = MONKEYS_BOSSES
    else:
        return

    ctx.current_channel = new_channel

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
    if ctx.unlocked_channels is None:
        ctx.unlocked_channels = ctx.progression.get_current_progress(ctx.keys)

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
    if not ctx.morphs_unlocked[-1]:
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
    # Check Screen Fading State in-game
    if ctx.ipc.check_screen_fading() != 0x01 and ctx.ipc.get_player_state() != 0x03:
        # Check Start of Screen Fade
        if ctx.ipc.get_screen_fade_count() > 0x1:
            if not ctx.morphs_unlocked[-1]:
                ctx.ipc.lock_equipment(Itm.morph_monkey.value)

        # Check rest of Screen Fade after Start
        else:
            # Temporarily give a morph during transitions to keep Morph Gauge visible
            # and to spawn Break Room loading zones
            if not ctx.morphs_unlocked[-1]:
                ctx.ipc.unlock_equipment(Itm.morph_monkey.value)

            ctx.current_stage = ctx.ipc.get_stage()
            ctx.command_state = 2

    # Not/No Longer Screen Fading
    else:
        if not ctx.morphs_unlocked[-1]:
            ctx.ipc.lock_equipment(Itm.morph_monkey.value)

        if ctx.command_state == 2:
            ctx.command_state = 0

async def check_states(ctx : 'AE3Context'):
    if not ctx.command_state:
        # Check for DeathLinks
        if ctx.pending_deathlinks:
            ctx.ipc.kill_player(100.0)
            ctx.pending_deathlinks -= 1
            ctx.command_state = 1
        # Send DeathLinks
        else:
            cookies : float = ctx.ipc.get_cookies()

            if not ctx.sending_death and cookies <= 0.0:
                await ctx.send_death()
                ctx.sending_death = True
            elif ctx.sending_death and cookies > 0.0:
                ctx.sending_death = False

        # Check Swimming State
        if not ctx.swim_unlocked and ctx.ipc.is_on_water():
            ctx.ipc.kill_player(20.0)
            ctx.command_state = 1

async def check_items(ctx : 'AE3Context'):
    cache_batch_items : Set[NetworkItem] = set()

    # Get Difference to get only new items
    received : List[NetworkItem] = ctx.items_received[ctx.next_item_slot:]
    ctx.next_item_slot += len(received)

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
            ctx.ipc.unlock_equipment(item.name, auto_equip)

            ### Check if RC Car or any Chassis is unlocked
            if ctx.rcc_unlocked and item.name in Itm.get_chassis_by_id():
                ctx.rcc_unlocked = True

                # Relock all other RC cars
                for idx, name in Itm.get_chassis_by_id(no_default=True):
                    if name == item.name:
                        continue

                    ctx.ipc.lock_chassis_direct(idx)

            ### Track Morphs Unlocked
            if item.name in Itm.get_morphs_ordered():
                index : int = Itm.get_morphs_ordered().index(item.name)
                ctx.morphs_unlocked[index] = True
                ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration, [index], True)

        ## Handle Collectables
        elif isinstance(item, CollectableItem) or isinstance(item, UpgradeableItem):
            i = item
            maximum : int | float = 0x0

            # Get Maximum Values
            if item.resource in Capacities:
                maximum = Capacities[item.resource]

            ### <!> NTSC-U Addresses are used when identifying Items regardless of region
            if item.address == NTSCU.GameStates[Game.nothing.value]:
                continue

            ### Handle Morph Energy
            elif item.resource == Game.morph_gauge_active.value:
                ctx.ipc.give_morph_energy(i.amount)

            ### Handle Morph Extension
            elif item.resource == Game.morph_duration.value:
                ctx.morph_duration += item.amount

                unlocked_morphs = [idx for idx, _ in enumerate(ctx.morphs_unlocked) if _]
                ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration, unlocked_morphs, True)

            ### Handle Generic Items
            else:
                ctx.ipc.give_collectable(item.resource, i.amount, maximum)

        # Add to temporary container; to be cached as a single batched after
        cache_batch_items.add(server_item)

    # Add to Cache
    ctx.cached_received_items.update(cache_batch_items)

    # Save when new items appear
    if received:
        ctx.save_session()

async def check_locations(ctx : 'AE3Context'):
    cleared : Set[int] = set()

    # Monkey Check
    for monkey in ctx.monkeys_checklist:
        ## Special Case for Tomoki
        if ctx.current_channel == APHelper.boss6.value:
            if ctx.ipc.is_tomoki_defeated():
                cleared.add(ctx.locations_name_to_id[Loc.boss_tomoki.value])
                continue

        if ctx.ipc.is_monkey_captured(monkey):
            cleared.add(ctx.locations_name_to_id[monkey])

            if monkey == Loc.boss_specter.value:
                ctx.specter1_defeated = True

    if not ctx.current_channel == APHelper.travel_station.value:
        # Camera Check
        if ctx.camerasanity and ctx.current_stage in CAMERAS_STAGE_INDEX:
            if ctx.ipc.is_camera_interacted():

                are_actors_present : bool = True
                if ctx.camerasanity == 2:
                    for actor in ACTORS_INDEX[CAMERAS_STAGE_INDEX[ctx.current_stage]]:
                        are_actors_present = not ctx.ipc.is_monkey_captured(actor)

                        if not are_actors_present:
                            break

                if are_actors_present:
                    cleared.add(ctx.locations_name_to_id[CAMERAS_STAGE_INDEX[ctx.current_stage]])

        # Cellphone Check
        if ctx.cellphonesanity and ctx.current_stage in CELLPHONES_STAGE_INDEX:
            tele_text_id : str = ctx.ipc.get_cellphone_interacted(ctx.current_stage)
            if tele_text_id in Cellphone_ID:
                location_id : int = ctx.locations_name_to_id[Cellphone_ID[tele_text_id]]
                cleared.add(location_id)

                # Obsolete Interact Data to prevent false checking of phones when transitioning into an adjacent
                # stage with a phone of the same ID
                ctx.ipc.obsolete_interact_data()

    # Get newly checked locations
    cleared = cleared.difference(ctx.checked_locations)

    # Send newly checked locations to server
    if cleared:
        ctx.cached_locations_checked.update(cleared)

        if ctx.server:
            # Send Locations checked offline
            if ctx.offline_locations_checked:
                cleared.update(ctx.offline_locations_checked)
                ctx.offline_locations_checked.clear()

            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": cleared}])
        else:
            # When offline, save checked locations to a different set
            ctx.offline_locations_checked.update(cleared)
