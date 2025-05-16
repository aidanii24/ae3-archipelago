from typing import TYPE_CHECKING, Set, List

from NetUtils import NetworkItem

from .data.Items import ACCESSORIES, ArchipelagoItem, EquipmentItem, CollectableItem, UpgradeableItem, Capacities, AP, \
    EQUIPMENT
from .data.Strings import Game, Loc, Itm, APHelper
from .data.Addresses import NTSCU
from .data.Locations import ACTORS_INDEX, CELLPHONES_STAGE_INDEX, CAMERAS_STAGE_INDEX, MONKEYS_BREAK_ROOMS, \
    MONKEYS_PASSWORDS, \
    MONKEYS_BOSSES, MONKEYS_DIRECTORY, Cellphone_Name_to_ID
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
        dummy: str = ctx.dummy_morph if ctx.dummy_morph_needed else ""

        if current_morph_duration != ctx.morph_duration or current_morph_duration != 0.0:
            ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration, dummy)

        # Character could be wrong if morph duration still is not equal after the first set
        current_morph_duration = ctx.ipc.get_morph_duration(ctx.character)
        if current_morph_duration != ctx.morph_duration or current_morph_duration != 0.0:
            ctx.character = ctx.ipc.get_character()
            ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration, dummy)

    # Get which Monkey Group to actively check at the moment based on the stage
    if not new_channel or new_channel is None and not ctx.current_channel:
        # Special Check for Monkey Pink as her boss stage does not provide a Stage ID
        if ctx.ipc.is_in_pink_boss():
            ctx.monkeys_checklist = MONKEYS_BOSSES
            ctx.current_channel = APHelper.boss4.value
        # Recheck locations by each stage while loading
        elif ctx.current_stage:
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
    if ctx.monkeys_checklist_count >= len(ctx.monkeys_index):
        ctx.monkeys_checklist_count = 0

    ctx.monkeys_checklist = ctx.monkeys_index[ctx.monkeys_checklist_count]
    ctx.monkeys_checklist_count += 1

# Ensure game is always set to "round2"
async def correct_progress(ctx : 'AE3Context'):
    ctx.ipc.set_progress()

async def setup_level_select(ctx : 'AE3Context'):
    is_a_level_confirmed: bool = ctx.ipc.is_a_level_confirmed()

    # Force Unlocked Stages to be in sync with the player's chosen option,
    # maxing out at 0x1B as supported by the game
    if ctx.unlocked_channels is None:
        ctx.unlocked_channels = ctx.progression.get_progress(ctx.keys)

    if ctx.ipc.get_unlocked_channels() != max(0, min(ctx.unlocked_channels, 0x1B)):
        ctx.ipc.set_unlocked_stages(ctx.unlocked_channels)

    # Un-mark bosses as defeated to allow their levels to remain accessible
    for monkey in MONKEYS_BOSSES:
        if ctx.ipc.is_monkey_captured(monkey):
            ctx.ipc.release_monkey(monkey)

    progress : str = ctx.ipc.get_progress()
    selected_channel: int = ctx.ipc.get_selected_channel()

    # In case player scrolls beyond intended levels before unlocked stages are enforced,
    # force selected level to be the latest unlocked stage,
    # except if when a level is to be swapped due to channel shuffle
    if selected_channel > ctx.unlocked_channels and not is_a_level_confirmed:
        ctx.ipc.set_selected_channel(ctx.unlocked_channels)

        if ctx.last_selected_channel_index > ctx.unlocked_channels:
            ctx.last_selected_channel_index = ctx.unlocked_channels

    # Change Progress temporarily for certain levels to be playable. Change back to round2 otherwise.
    if ctx.ipc.is_on_warp_gate():
        # Set to last slot (not the id of the level randomized) for convenience and consistency
        if 0 <= ctx.last_selected_channel_index <= ctx.unlocked_channels and not is_a_level_confirmed:
            ctx.ipc.set_selected_channel(ctx.last_selected_channel_index)
            ctx.last_selected_channel_index = -1
            selected_channel = ctx.ipc.get_selected_channel()

        # Dr. Tomoki Battle!
        if selected_channel == 0x18:
            ctx.ipc.set_progress(APHelper.pr_boss6.value)
        # Specter Battle!
        elif selected_channel == 0x1A:
            ctx.ipc.set_progress(APHelper.pr_specter1.value)
        elif progress != APHelper.pr_round2.value:
            ctx.ipc.set_progress()

        # Reset Game Mode Swap state and Set Game Mode value to an unexpected value
        # as sign that the game has not yet set it
        if ctx.swap_freeplay and not ctx.ipc.is_a_level_confirmed() and ctx.is_mode_swapped:
            ctx.is_mode_swapped = False
            ctx.ipc.set_game_mode(0xFFFF, False)
    elif progress != APHelper.pr_round2.value:
        ctx.ipc.set_progress()
    else:
        if ctx.is_channel_swapped:
            ctx.is_channel_swapped = False

    # If Super Monkey isn't properly unlocked yet, temporarily do so during level select to prevent Aki from
    # introducing and giving it to the player. Lock them while on the Pause Menu as well to prevent equipping them
    # from the Quick Morph Menu
    gui_status : int = ctx.ipc.get_gui_status()

    if ctx.dummy_morph_monkey_needed:
        if gui_status < 3:
            ctx.ipc.unlock_equipment(Itm.morph_monkey.value)
        else:
            ctx.ipc.lock_equipment(Itm.morph_monkey.value)

    if ctx.dummy_morph_needed:
        if gui_status < 3:
            ctx.ipc.unlock_equipment(ctx.dummy_morph)
        else:
            ctx.ipc.lock_equipment(ctx.dummy_morph)

    # Temporarily unlock all Chassis when not in Travel Station to make sure their models load correctly when obtained
    # RC Car Chassis can't be changed in levels, so it is safe to keep them on until the next Travel Station visit
    if not ctx.rcc_unlocked:
        if not ctx.ipc.is_a_level_confirmed():
            for _ in range(3):
                ctx.ipc.lock_chassis_direct(_)
        else:
            for _ in range(3):
                ctx.ipc.unlock_chassis_direct(_)

    # Reset the spawnpoint properly as the game leaves it blank when coming from TV Station
    if is_a_level_confirmed:
        ctx.ipc.clear_spawn()

        # If Channel Shuffle is enabled, force switch the game to load the randomized channel
        if ctx.shuffle_channel and not ctx.is_channel_swapped:
            if ctx.last_selected_channel_index < 0:
                ctx.last_selected_channel_index = selected_channel

            ctx.ipc.set_selected_channel(min(ctx.progression.order[selected_channel], 0x1B))
            ctx.is_channel_swapped = True

        # Toggle Freeplay when allowed and needed
        toggle_freeplay(ctx)

        # Lock Super Monkey Morph as Aki won't give it at this point if it's still supposed to be locked,
        # unless required to keep Break Rooms open
        if ctx.dummy_morph_monkey_needed and ctx.dummy_morph != Itm.morph_monkey.value:
            ctx.ipc.lock_equipment(Itm.morph_monkey.value)


async def setup_area(ctx : 'AE3Context'):
    # In case the Player uses a Morph they are not yet allowed, immediately unmorph them
    current_morph_id : int = ctx.ipc.get_current_morph()
    if current_morph_id:
        is_reset : bool = False

        # Lock in case of false unlocks when unlocking/relocking morphs
        if ctx.dummy_morph_needed:
            if ctx.dummy_morph == Itm.morph_monkey.value:
                if current_morph_id >= 7:
                    ctx.ipc.set_morph_gauge_timer()
                    is_reset = True
            elif ctx.dummy_morph == Itm.morph_knight.value and current_morph_id == 1:
                ctx.ipc.set_morph_gauge_timer()

        # Lock in case of Quick Morph Glitch (Intentionally by the player, or due to the nature of this client)
        if not is_reset and not ctx.ipc.is_equipment_unlocked(Itm.get_morphs_ordered()[current_morph_id - 1]):
            ctx.ipc.set_morph_gauge_timer()

    # Check Screen Fading State in-game
    if ctx.ipc.check_screen_fading() != 0x01 and ctx.ipc.get_player_state() != 0x03:
        # Check Start of Screen Fade
        if ctx.ipc.get_screen_fade_count() > 0x1:
            dispatch_dummy_morph(ctx)

        # Check rest of Screen Fade after Start
        else:
            # Temporarily give a morph during transitions to keep Morph Gauge visible
            # and to spawn Break Room loading zones
            dispatch_dummy_morph(ctx, True)

            ctx.current_stage = ctx.ipc.get_stage()
            ctx.command_state = 2

    # Not/No Longer Screen Fading
    else:
        dispatch_dummy_morph(ctx)

        if ctx.dummy_morph_monkey_needed:
            ctx.ipc.lock_equipment(Itm.morph_monkey.value)

        if ctx.command_state == 2:
            ctx.command_state = 0

async def check_states(ctx : 'AE3Context'):
    if not ctx.command_state:
        cookies: float = ctx.ipc.get_cookies()

        # Check for DeathLinks
        if ctx.death_link:
            if ctx.pending_deathlinks and cookies > 0.0:
                ctx.ipc.kill_player(100.0)
                ctx.pending_deathlinks = max(ctx.pending_deathlinks - 1, 0)
                ctx.receiving_death = True
                ctx.command_state = 1
            # Disable the receiving deathlinks flag when deathlinks run out
            elif not ctx.pending_deathlinks and cookies > 0.0:
                ctx.receiving_death = False
            # Send DeathLinks if there are no more deathlinks occuring
            elif not ctx.receiving_death:
                if not ctx.sending_death and cookies <= 0.0:
                    await ctx.send_death()
                    ctx.sending_death = True
                elif ctx.sending_death and cookies > 0.0:
                    ctx.sending_death = False
        else:
            if ctx.receiving_death: ctx.receiving_death = False
            if ctx.sending_death: ctx.sending_death = False

        # Check Swimming State
        if not ctx.swim_unlocked and ctx.ipc.is_on_water():
            ctx.ipc.kill_player(20.0)
            ctx.command_state = 1

async def check_items(ctx : 'AE3Context'):
    # Check if there are items missed from since the client was open; Refuse to take items until this index is confirmed
    if ctx.last_item_processed_index < 0:
        return
    # Sync with Last Processed Item Index if necessary:
    elif ctx.last_item_processed_index:
        ctx.next_item_slot = max(min(ctx.last_item_processed_index, ctx.next_item_slot), 0)

    # Resync Next Item Slot if empty and locations have been checked
    if not ctx.next_item_slot and ctx.items_received and ctx.checked_locations:
        ctx.next_item_slot = len(ctx.items_received)
    # Reset Next Item Slot if not empty and no locations have been checked
    elif ctx.next_item_slot and not ctx.checked_locations and ctx.items_received and ctx.items_received[-1].player < 1:
        ctx.next_item_slot = 0

    # Get Difference to get only new items
    received : List[NetworkItem] = ctx.items_received[ctx.next_item_slot:]
    ctx.next_item_slot += len(received)
    ctx.last_item_processed_index = ctx.next_item_slot

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
                ctx.unlocked_channels = ctx.progression.get_progress(ctx.keys)

        ## Unlock Morphs and Gadgets
        elif isinstance(item, EquipmentItem):
            ctx.ipc.unlock_equipment(item.name, auto_equip)

            ## Check for Water Net
            if not ctx.swim_unlocked and item.name == Itm.gadget_swim.value:
                ctx.swim_unlocked = True

            ### Check if RC Car or any Chassis is unlocked
            if not ctx.rcc_unlocked and item.name in Itm.get_chassis_by_id():
                ctx.rcc_unlocked = True
                ctx.ipc.unlock_equipment(Itm.gadget_rcc.value)

                # Relock all other RC cars
                for idx, name in enumerate(Itm.get_chassis_by_id(no_default=True)):
                    if name == item.name:
                        continue

                    ctx.ipc.lock_chassis_direct(idx)

            ### Track Morphs Unlocked
            if item.name in Itm.get_morphs_ordered():
                # Update need of dummy morph
                if item.name == Itm.morph_monkey.value:
                    if ctx.dummy_morph_monkey_needed:
                        ctx.dummy_morph_monkey_needed = False

                    if ctx.dummy_morph_needed:
                        ctx.dummy_morph_needed = False

                        if ctx.dummy_morph != item.name:
                            ctx.ipc.lock_equipment(ctx.dummy_morph)
                elif ctx.dummy_morph != Itm.morph_monkey.value and ctx.dummy_morph_needed:
                    ctx.dummy_morph_needed = False

                    # Force Lock Fantasy Knight to prevent it from being able to be always available afterward,
                    # even if it wasn't the morph unlocked
                    if item.name != ctx.dummy_morph:
                        ctx.ipc.lock_equipment(ctx.dummy_morph)

                dummy: str = ctx.dummy_morph if ctx.dummy_morph_needed else ""
                ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration, dummy)

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

                dummy: str = ctx.dummy_morph if ctx.dummy_morph_needed else ""
                ctx.ipc.set_morph_duration(ctx.character, ctx.morph_duration, dummy)

            ### Handle Generic Items
            else:
                ctx.ipc.give_collectable(item.resource, i.amount, maximum)

    if received:
        # Recheck Locations when receiving items for cases when locations are checked manually by the server/host
        await ctx.goal_target.check(ctx)

        # Save session for everytime there are new items received
        ctx.save_session()

async def resync_important_items(ctx : 'AE3Context'):
    # Do not resync if no items have been processed at all yet
    if ctx.last_item_processed_index < 1:
        return

    equipment : list[EquipmentItem] = [ *EQUIPMENT, *ACCESSORIES ]
    received_id : list[int] = [ item[0] for item in ctx.items_received ]
    for equip in equipment:
        if equip.item_id in received_id:
            if not ctx.ipc.is_equipment_unlocked(equip.name):
                ctx.ipc.unlock_equipment(equip.name, ctx.auto_equip)

                # Recheck RC Car Unlock
                if not ctx.rcc_unlocked and equip.item_id in Itm.get_chassis_by_id():
                    ctx.rcc_unlocked = True

                # Recheck Water Net Unlock
                if not ctx.swim_unlocked and equip.name == Itm.gadget_swim.value:
                    ctx.swim_unlocked = True

                # Recheck Dummy Morphs Status
                if equip.name == Itm.morph_monkey.value:
                    if ctx.dummy_morph_monkey_needed:
                        ctx.dummy_morph_monkey_needed = False

                    if ctx.dummy_morph_needed:
                        ctx.dummy_morph_needed = False
                elif ctx.dummy_morph_needed and equip.name in Itm.get_morphs_ordered():
                    ctx.dummy_morph_needed = False

    # Lock Fantasy Knight when it should not be available in case it remains open after dummy_morph_needed has changed
    knight_id : int = ctx.items_name_to_id[Itm.morph_knight.value]
    if knight_id not in received_id and not ctx.dummy_morph_needed and ctx.ipc.is_equipment_unlocked(
            Itm.morph_knight.value):
        ctx.ipc.lock_equipment(Itm.morph_knight.value)

async def check_locations(ctx : 'AE3Context'):
    cleared : Set[int] = set()
    volatile_cleared : Set[int] = set()

    # Monkey Check
    for monkey in ctx.monkeys_checklist:
        if monkey in MONKEYS_PASSWORDS:
            continue

        if not ctx.check_break_rooms and monkey in MONKEYS_BREAK_ROOMS:
            continue

        ## Special Case for Tomoki
        if ctx.current_channel == APHelper.boss6.value:
            if ctx.ipc.is_tomoki_defeated():
                cleared.add(ctx.locations_name_to_id[Loc.boss_tomoki.value])
                volatile_cleared.add(ctx.locations_name_to_id[Loc.boss_tomoki.value])
                continue

        if ctx.ipc.is_monkey_captured(monkey):
            location_id : int = ctx.locations_name_to_id[monkey]
            cleared.add(location_id)
            ctx.checked_monkeys_cache.add(location_id)

            if monkey in MONKEYS_BOSSES:
                volatile_cleared.add(location_id)

    if not ctx.current_channel == APHelper.travel_station.value:
        # Camera Check
        if ctx.camerasanity and ctx.current_stage in CAMERAS_STAGE_INDEX:
            if ctx.ipc.is_camera_interacted():
                are_actors_ready : bool = True
                if ctx.camerasanity == 1:
                    for actor in ACTORS_INDEX[CAMERAS_STAGE_INDEX[ctx.current_stage]]:
                        are_actors_ready = are_actors_ready and not ctx.ipc.is_monkey_captured(actor)

                if are_actors_ready:
                    location_id : int = ctx.locations_name_to_id[CAMERAS_STAGE_INDEX[ctx.current_stage]]
                    cleared.add(location_id)
                    volatile_cleared.add(location_id)

        # Check if there's any new checks from Monkeys/Cameras before checking cellphone
        cleared = cleared.difference(ctx.checked_locations)

        # Cellphone Check
        gui_status : int = ctx.ipc.get_gui_status()
        interacting_with_phone : bool = gui_status > 1 or (gui_status and not cleared)
        if ctx.cellphonesanity and interacting_with_phone and ctx.current_stage in CELLPHONES_STAGE_INDEX:
            tele_text_id : str = ctx.ipc.get_cellphone_interacted(ctx.current_stage)
            if tele_text_id in CELLPHONES_STAGE_INDEX[ctx.current_stage] and tele_text_id in Cellphone_Name_to_ID:
                location_id : int = ctx.locations_name_to_id[Cellphone_Name_to_ID[tele_text_id]]
                cleared.add(location_id)
                volatile_cleared.add(location_id)

    # Get newly checked locations
    cleared = cleared.difference(ctx.checked_locations)
    volatile_cleared = volatile_cleared.intersection(cleared)

    # Send newly checked locations to server
    if cleared:
        ctx.locations_checked.update(cleared)

        if ctx.server:
            # Send Locations checked offline
            if ctx.offline_locations_checked:
                cleared.update(ctx.offline_locations_checked)
                ctx.offline_locations_checked.clear()

            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": cleared}])
            await ctx.goal_target.check(ctx)
            ctx.post_game_access_rule.check(ctx)

        else:
            # When offline, save checked locations to a different set
            ctx.offline_locations_checked.update(cleared)

    # Save Session when Volatile Locations have been checked
    if volatile_cleared:
        ctx.checked_volatile_locations.update(volatile_cleared)
        ctx.save_session()

def dispatch_dummy_morph(ctx : 'AE3Context', unlock : bool = False):
    if not ctx.dummy_morph or ctx.dummy_morph is None or not ctx.dummy_morph_needed:
        return

    if unlock:
        ctx.ipc.unlock_equipment(ctx.dummy_morph)
    else:
        ctx.ipc.lock_equipment(ctx.dummy_morph)

def toggle_freeplay(ctx : 'AE3Context'):
    if not ctx.swap_freeplay or ctx.is_mode_swapped:
        return

    current_mode : int = ctx.ipc.get_game_mode()

    if current_mode == 0x001:
        ctx.ipc.set_game_mode(0x100, False)
    elif current_mode == 0x100:
        ctx.ipc.set_game_mode(0x001, False)
    else:
        return

    ctx.is_mode_swapped = True