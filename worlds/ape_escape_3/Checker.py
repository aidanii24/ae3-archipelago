from typing import TYPE_CHECKING, Set, List
import itertools

from NetUtils import NetworkItem

from .data.Items import ACCESSORIES, ArchipelagoItem, EquipmentItem, CollectableItem, UpgradeableItem, Capacities, AP, \
    EQUIPMENT
from .data.Stages import PROGRESS_ID_BY_ORDER
from .data.Strings import Game, Loc, Itm, APHelper, Stage
from .data.Addresses import NTSCU
from .data.Locations import ACTORS_INDEX, CELLPHONES_STAGE_INDEX, CAMERAS_STAGE_INDEX, MONKEYS_BREAK_ROOMS, \
    MONKEYS_PASSWORDS, MONKEYS_BOSSES, MONKEYS_DIRECTORY, Cellphone_Name_to_ID, LOCATIONS_INDEX, \
    SHOP_CATEGORIES_COLLECTION_DIRECTORY, SHOP_COLLECTION_DIRECTORY, SHOP_PERSISTENT_MASTER, SHOP_PROGRESSION_MORPH, \
    SHOP_BONUS_RC_CARS
from .data import Items

if TYPE_CHECKING:
    from .AE3_Client import AE3Context


### [< --- CHECKS --- >]
async def check_background_states(ctx : 'AE3Context'):
    # Get current stage
    new_channel = ctx.ipc.get_channel()
    ctx.current_stage = ctx.ipc.get_stage()

    # Set to last selected slot (not the id of the level randomized) for convenience and consistency
    if not ctx.current_stage and 0 <= ctx.last_selected_channel_index <= ctx.unlocked_channels:
        ctx.ipc.set_next_channel_choice(ctx.last_selected_channel_index)
        ctx.last_selected_channel_index = -1

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
        # Recheck locations by a number of location groups while loading
        elif ctx.current_stage:
            await sweep_recheck_locations(ctx)

    elif new_channel != ctx.current_channel:
        if new_channel in MONKEYS_DIRECTORY:
            ctx.monkeys_checklist = MONKEYS_DIRECTORY[new_channel]
        elif "b" in new_channel:
            ctx.monkeys_checklist = MONKEYS_BOSSES
    else:
        return

    ctx.current_channel = new_channel
    ctx.in_travel_station = ctx.current_channel == APHelper.travel_station.value

async def sweep_recheck_locations(ctx : 'AE3Context'):
    batch: list[str] = [*ctx.location_groups[ctx.group_check_index * 20:ctx.group_check_index * 20 + 20]]

    await sweep_locations(ctx, [x for y in batch for x in y])

    if ctx.group_check_index * 20 >= len(ctx.location_groups):
        ctx.group_check_index = 0
    else:
        ctx.group_check_index += 1

async def build_checked_cache(ctx : 'AE3Context'):
    # Build Checked Locations cache if needed
    if ctx.cache_missing:
        await sweep_locations(ctx, [x for y in [*ctx.cache_missing[:20]] for x in y])
        del ctx.cache_missing[:20]

        return

    ctx.post_game_condition.check(ctx)
    await ctx.goal_target.check(ctx)

# Ensure game is always set to "round2"
async def correct_progress(ctx : 'AE3Context'):
    ctx.ipc.set_progress()

async def setup_level_select(ctx : 'AE3Context'):
    is_a_level_confirmed: bool = ctx.ipc.is_a_level_confirmed()
    post_game_state : bool = ctx.post_game_condition.check(ctx)

    # Force Unlocked Stages to be in sync with the player's chosen option,
    # maxing out at 0x1B as supported by the game
    if ctx.unlocked_channels is None:
        ctx.unlocked_channels = ctx.progression.get_progress(ctx.keys, post_game_state)
    elif post_game_state and ctx.unlocked_channels < sum(ctx.progression.progression[:-1]):
        ctx.unlocked_channels = ctx.progression.get_progress(ctx.keys, post_game_state)

    if ctx.ipc.get_unlocked_channels() != max(0, min(ctx.unlocked_channels, 0x1B)):
        ctx.ipc.set_unlocked_stages(ctx.unlocked_channels)

    progress : str = ctx.ipc.get_progress()
    selected_channel: int = ctx.ipc.get_selected_channel()

    # In case player scrolls beyond intended levels before unlocked stages are enforced,
    # force selected level to be the latest unlocked stage,
    # except if when a level is to be swapped due to channel shuffle
    if selected_channel > ctx.unlocked_channels and not is_a_level_confirmed:
        ctx.ipc.set_selected_channel(ctx.unlocked_channels)

        if ctx.last_selected_channel_index > ctx.unlocked_channels:
            ctx.last_selected_channel_index = ctx.unlocked_channels

    ## Reapply Persistent Values when coming from the Shopping Area
    if ctx.ipc.get_persistent_cookie_value():
        await reapply_persistent_values(ctx)

    gui_status: int = ctx.ipc.get_gui_status()

    if ctx.ipc.is_on_warp_gate():
        # Change Progress temporarily for certain levels to be playable. Change back to round2 otherwise.
        if selected_channel == 0x18 or selected_channel == 0x1A:
            target_progress : str = APHelper.pr_boss6.value if selected_channel == 0x18 else APHelper.pr_specter1.value

            if progress != target_progress:
                ctx.ipc.set_progress(target_progress)
        elif progress != APHelper.pr_round2.value:
            ctx.ipc.set_progress()

        # Release Bosses as needed to enter the level normally
        bosses_indexes : list[int] = [0x03, 0x08, 0xC, 0x11, 0x15, -1, -2, 0x1B]
        if selected_channel in bosses_indexes:
            boss : str = MONKEYS_BOSSES[bosses_indexes.index(selected_channel)]
            boss_captured : bool = ctx.ipc.is_location_checked(boss)

            if boss_captured:
                ctx.ipc.unmark_location(boss)

        # Reset Game Mode Swap state and Set Game Mode value to an unexpected value
        # as sign that the game has not yet set it
        if ctx.alt_freeplay and not ctx.ipc.is_a_level_confirmed() and ctx.is_mode_swapped:
            ctx.is_mode_swapped = False
            ctx.ipc.set_game_mode(0xFFFF, False)
    else:
        ctx.post_game_condition.check(ctx)

        if progress != APHelper.pr_round2.value:
            ctx.ipc.set_progress()

            if ctx.suppress_progress_correction:
                ctx.suppress_progress_correction = False

        if ctx.is_channel_swapped:
            ctx.is_channel_swapped = False

        if ctx.save_state_on_room_transition and not ctx.has_saved_on_transition:
            ctx.has_saved_on_transition = True
            ctx.pending_auto_save = True

        if ctx.load_state_on_connect and not ctx.is_last_save_normal and ctx.ipc.is_saving() and gui_status >= 3:
            ctx.is_last_save_normal = True
            await set_last_save_status(ctx)

    # If Super Monkey isn't properly unlocked yet, temporarily do so during level select to prevent Aki from
    # introducing and giving it to the player. Lock them while on the Pause Menu as well to prevent equipping them
    # from the Quick Morph Menu
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

    # Reset the spawnpoint properly as the game leaves it blank when coming from TV Station
    if is_a_level_confirmed:
        ctx.ipc.clear_spawn()

        if ctx.ipc.get_button_pressed() == 0x07:    # L1/L2 Buttons
            set_freeplay_mode(ctx)
        else:
            mode : int = ctx.ipc.get_activated_game_mode()
            if mode == 0x100: ctx.current_game_mode = 0x4
            elif mode == 0x001: ctx.current_game_mode = 0x3
            else: ctx.current_game_mode = 0x0

        # If Channel Shuffle is enabled, force switch the game to load the randomized channel
        if not ctx.is_channel_swapped:
            # Save last selected channel index
            if ctx.last_selected_channel_index < 0:
                ctx.last_selected_channel_index = selected_channel

            ctx.ipc.set_selected_channel(min(ctx.progression.order[selected_channel], 0x1B))
            ctx.is_channel_swapped = True

        # Lock Super Monkey Morph as Aki won't give it at this point if it's still supposed to be locked,
        # unless required to keep Break Rooms open
        if ctx.dummy_morph_monkey_needed and ctx.dummy_morph != Itm.morph_monkey.value:
            ctx.ipc.lock_equipment(Itm.morph_monkey.value)

        if ctx.save_state_on_room_transition and ctx.has_saved_on_transition:
            ctx.has_saved_on_transition = False

async def setup_shopping_area(ctx : 'AE3Context'):
    if ctx.in_shoppping_area:
        if ctx.shoppingsanity >= 3:
            ctx.suppress_progress_correction = True
            ctx.ipc.set_progress(PROGRESS_ID_BY_ORDER[min(ctx.shop_progression, 27)])

        await set_persistent_values(ctx)

async def set_persistent_values(ctx : 'AE3Context'):
    stocks: int = ctx.ipc.get_morph_stock()
    ctx.ipc.set_persistent_morph_stock_value(stocks)


    if ctx.shoppingsanity:
        for i in range(len(Itm.get_real_chassis_by_id())):
            if ctx.ipc.is_location_checked(SHOP_BONUS_RC_CARS[i]):
                ctx.ipc.unlock_chassis_direct(i)
            else:
                ctx.ipc.lock_chassis_direct(i)

        stock_shop_item: int = ctx.ipc.get_shop_morph_stock_checked()

        # Swap out the current Morph Stocks the player has for the amount of Morph Stocks checked as a Shop Item Location
        ctx.ipc.set_morph_stock(stock_shop_item)
    else:
        ctx.ipc.set_morph_stock(10)

    if not ctx.monkey_mart:
        cookies: int = int(ctx.ipc.get_cookies())
        energy: int = int(ctx.ipc.get_morph_gauge_recharge_value())

        ctx.ipc.set_persistent_cookie_value(cookies)
        ctx.ipc.set_persistent_morph_energy_value(energy)

async def reapply_persistent_values(ctx : 'AE3Context'):
    if ctx.shoppingsanity:
        for i in range(len(Itm.get_real_chassis_by_id())):
            if ctx.ipc.is_chassis_unlocked(Itm.get_chassis_by_id()[i]):
                ctx.ipc.unlock_chassis_direct(i)
            else:
                ctx.ipc.lock_chassis_direct(i)

        stock_shop_item: int = int(ctx.ipc.get_morph_stock())
        ctx.ipc.set_shop_morph_stock_checked(stock_shop_item)

    stocks: int = ctx.ipc.get_persistent_morph_stock_value()
    ctx.ipc.set_morph_stock(stocks)

    if not ctx.monkey_mart:
        cookies: float = ctx.ipc.get_persistent_cookie_value()
        energy: float = ctx.ipc.get_persistent_morph_energy_value()

        ctx.ipc.set_cookies(cookies)
        ctx.ipc.set_morph_gauge_recharge(energy)
        ctx.ipc.set_persistent_cookie_value(0)
        ctx.ipc.set_persistent_morph_energy_value(0)

async def setup_area(ctx : 'AE3Context'):
    # MORPH LOCK ENFORCEMENT
    ## In case the Player uses a Morph they are not yet allowed, immediately unmorph them
    current_morph_id : int = ctx.ipc.get_current_morph()
    if current_morph_id:
        is_reset : bool = False

        ## Lock in case of false unlocks when unlocking/relocking morphs
        if ctx.dummy_morph_needed:
            if ctx.dummy_morph == Itm.morph_monkey.value:
                if current_morph_id >= 7:
                    ctx.ipc.set_morph_gauge_timer()
                    is_reset = True
            elif ctx.dummy_morph == Itm.morph_knight.value and current_morph_id == 1:
                ctx.ipc.set_morph_gauge_timer()

        ## Lock in case of Quick Morph Glitch (Intentionally by the player, or due to the nature of this client)
        if not is_reset and not ctx.ipc.is_equipment_unlocked(Itm.get_morphs_ordered()[current_morph_id - 1]):
            ctx.ipc.set_morph_gauge_timer()

    # SCREEN FADING
    ## Check Screen Fading State in-game
    if ctx.ipc.check_screen_fading() != 0x01 and ctx.ipc.get_player_state() != 0x03:
        ## Check Start of Screen Fade In
        if ctx.ipc.get_screen_fade_count() > 0x1:
            dispatch_dummy_morph(ctx)

            # Check Current Game Mode
            if ctx.ipc.check_screen_fading() == 0x01:
                current_mode: int = ctx.ipc.get_current_game_mode()
                if current_mode > 0:
                    ctx.current_game_mode = current_mode
                    if ctx.current_game_mode >= 0xFF:
                        ctx.current_game_mode = 0x0

            # Save State if desired
            ## Gate function as this gets activated before and after a transition, which is undesired
            if ctx.save_state_on_room_transition and ctx.has_saved_on_transition:
                ctx.has_saved_on_transition = False

        ## Check rest of Screen Fade after Start
        else:
            # Temporarily give a morph during transitions to keep Morph Gauge visible
            # and to spawn Break Room loading zones
            dispatch_dummy_morph(ctx, True)

            # Set Shopping Area Progress if in Shopping Area
            await setup_shopping_area(ctx)

            ctx.current_stage = ctx.ipc.get_stage()
            ctx.command_state = 2

    ## Not/No Longer Screen Fading
    else:
        dispatch_dummy_morph(ctx)

        if ctx.dummy_morph_monkey_needed:
            ctx.ipc.lock_equipment(Itm.morph_monkey.value)

        if ctx.command_state == 2:
            ctx.command_state = 0

        # Allow Save State on Screen Transition again
        if ctx.save_state_on_room_transition and not ctx.has_saved_on_transition:
            ctx.has_saved_on_transition = True
            ctx.pending_auto_save = True


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
            elif not ctx.pending_deathlinks and ctx.receiving_death and cookies > 0.0:
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


async def receive_items(ctx : 'AE3Context'):
    # Check if there are items missed from since the client was open; Refuse to take items until this index is confirmed
    if ctx.last_item_processed_index < 0:
        ctx.last_item_processed_index = ctx.ipc.get_last_item_index()
    # Sync with Last Processed Item Index if necessary:
    elif ctx.last_item_processed_index:
        if ctx.next_item_slot < 0:
            ctx.next_item_slot = ctx.last_item_processed_index
        else:
            ctx.next_item_slot = max(min(ctx.last_item_processed_index, ctx.next_item_slot), 0)


    # Resync Next Item Slot if empty and locations have been checked
    if not ctx.next_item_slot and ctx.items_received and ctx.checked_locations:
        ctx.next_item_slot = len(ctx.items_received)

    # Auto-equip if option is enabled or for handling the starting inventory
    auto_equip: bool = ctx.auto_equip or not ctx.last_item_processed_index

    # Get Difference to get only new items
    received : List[NetworkItem] = ctx.items_received[ctx.next_item_slot:]
    ctx.next_item_slot += len(received)
    ctx.last_item_processed_index = ctx.next_item_slot
    for server_item in received:
        item = Items.from_id(server_item.item)

        # Handle Item depending on category
        ## Handle Archipelago Items
        if isinstance(item, ArchipelagoItem):
            ### Add Key Count and unlock levels accordingly
            if item.item_id == AP[APHelper.channel_key.value]:
                ctx.keys += 1
                ctx.unlocked_channels = ctx.progression.get_progress(ctx.keys, ctx.post_game_condition.check(ctx))
            elif item.item_id == AP[APHelper.shop_stock.value]:
                ctx.shop_progression += ctx.shop_progress

                await setup_shopping_area(ctx)

            # Save State if desired
            if ctx.save_state_on_item_received and not ctx.pending_auto_save:
                ctx.pending_auto_save = True

        ## Unlock Morphs and Gadgets
        elif isinstance(item, EquipmentItem):
            ctx.ipc.unlock_equipment(item.name, auto_equip)

            ## Check for Water Net
            if not ctx.swim_unlocked and item.name == Itm.gadget_swim.value:
                ctx.swim_unlocked = True

            ### Check if RC Car or any Chassis is unlocked
            if item.name in Itm.get_chassis_by_id():
                ctx.ipc.unlock_equipment(item.name, auto_equip)
                if not ctx.rcc_unlocked:
                    ctx.rcc_unlocked = True

                    # if item.name != Itm.gadget_rcc.value:
                    #     ctx.ipc.set_chassis_direct(Itm.get_chassis_by_id(False).index(item.name))

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

            # Save State if desired
            if ctx.save_state_on_item_received and not ctx.pending_auto_save:
                ctx.pending_auto_save = True

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
                ctx.ipc.give_collectable(item.resource, i.amount, maximum, ctx.in_shoppping_area)

    if received:
        # Save Last Item Index Processed into Game Memory
        ctx.ipc.set_last_item_index(ctx.last_item_processed_index)

        # Recheck Locations when receiving items for cases when locations are checked manually by the server/host
        await ctx.goal_target.check(ctx)
        ctx.post_game_condition.check(ctx)

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

    # Resync Channel Keys
    keys : int = received_id.count(ctx.items_name_to_id[APHelper.channel_key.value])
    unlocked : int = ctx.progression.get_progress(keys, ctx.post_game_condition.check(ctx))
    if ctx.keys != keys or ctx.unlocked_channels != unlocked:
        ctx.keys = keys
        ctx.unlocked_channels = unlocked
        ctx.ipc.set_unlocked_stages(ctx.unlocked_channels)

    # Resync Shop Stock
    if ctx.shoppingsanity >= 3:
        shop_stocks : int = received_id.count(ctx.items_name_to_id[APHelper.shop_stock.value])
        if ctx.shop_progress != shop_stocks * ctx.shop_progression:
            ctx.shop_progress = shop_stocks * ctx.shop_progression

            await setup_shopping_area(ctx)

async def check_locations(ctx : 'AE3Context'):
    cleared : Set[int] = set()

    is_in_normal_game_mode : bool = ctx.current_game_mode == 0x0

    # Monkey Check
    if is_in_normal_game_mode:
        for monkey in ctx.monkeys_checklist:
            if monkey in MONKEYS_PASSWORDS:
                continue

            if not ctx.check_break_rooms and monkey in MONKEYS_BREAK_ROOMS:
                continue

            ## Special Case for Tomoki
            if ctx.current_channel == APHelper.boss6.value:
                if not ctx.ipc.is_location_checked(Loc.boss_alt_tomoki.value) and ctx.ipc.is_tomoki_defeated():
                    cleared.add(ctx.locations_name_to_id[Loc.boss_tomoki.value])
                    ctx.ipc.mark_location(Loc.boss_alt_tomoki.value)
            elif ctx.ipc.is_location_checked(monkey):
                location_id : int = ctx.locations_name_to_id[monkey]
                cleared.add(location_id)

                if monkey == Loc.boss_specter_final.value and ctx.current_channel == APHelper.specter2.value:
                    ctx.ipc.set_progress(Stage.specter1.value)
                    ctx.suppress_progress_correction = True

    if not ctx.current_channel == APHelper.travel_station.value:
        # Camera Check
        if ctx.camerasanity and ctx.current_stage in CAMERAS_STAGE_INDEX:
            if ctx.ipc.is_location_checked(CAMERAS_STAGE_INDEX[ctx.current_stage]):
                location_id: int = ctx.locations_name_to_id[CAMERAS_STAGE_INDEX[ctx.current_stage]]
                cleared.add(location_id)
            elif ctx.ipc.is_camera_interacted():
                camera_name : str = CAMERAS_STAGE_INDEX[ctx.current_stage]

                if not ctx.ipc.is_location_checked(camera_name):
                    are_actors_ready : bool = True
                    if ctx.camerasanity == 1:
                        for actor in ACTORS_INDEX[camera_name]:
                            are_actors_ready = are_actors_ready and not ctx.ipc.is_location_checked(actor)

                    if are_actors_ready:
                        location_id : int = ctx.locations_name_to_id[camera_name]
                        cleared.add(location_id)
                        ctx.ipc.mark_location(camera_name)

        # Check if there's any new checks from Monkeys/Cameras before checking cellphone
        cleared = cleared.difference(ctx.checked_locations)

        # Cellphone Check
        gui_status : int = ctx.ipc.get_gui_status()
        interacting_with_phone : bool = gui_status > 1 or (gui_status and not cleared)
        if (is_in_normal_game_mode and ctx.cellphonesanity and interacting_with_phone and
                ctx.current_stage in CELLPHONES_STAGE_INDEX):
            tele_text_id : str = ctx.ipc.get_cellphone_interacted(ctx.current_stage)
            if (tele_text_id in CELLPHONES_STAGE_INDEX[ctx.current_stage] and
                    tele_text_id in Cellphone_Name_to_ID and
                    not ctx.ipc.is_location_checked(tele_text_id)):
                location_id : int = ctx.locations_name_to_id[Cellphone_Name_to_ID[tele_text_id]]
                ctx.ipc.mark_location(tele_text_id)
                cleared.add(location_id)

    # Shop Items Check
    if ctx.in_shoppping_area and ctx.shoppingsanity:
        stocks_checked : list[str] = [*SHOP_PROGRESSION_MORPH[:ctx.ipc.get_morph_stock()]]

        ctx.ipc.set_shop_morph_stock_checked(len(stocks_checked))
        cleared.update(ctx.locations_name_to_id[stock] for stock in stocks_checked)

        for category in [*SHOP_CATEGORIES_COLLECTION_DIRECTORY.keys()][1:]:
            category_count: int = 0
            for item in SHOP_CATEGORIES_COLLECTION_DIRECTORY[category]:
                if ctx.ipc.is_location_checked(item):
                    category_count += 1

                    if 0 < ctx.shoppingsanity != 2:
                        cleared.add(ctx.locations_name_to_id[item])

                # Count Collection Type
                if ctx.shoppingsanity == 2 and category_count and category in SHOP_COLLECTION_DIRECTORY:
                    cleared.update(*SHOP_COLLECTION_DIRECTORY[category][:category_count - 1])

    # Get newly checked locations
    cleared = cleared.difference(ctx.checked_locations)

    # Send newly checked locations to server
    if cleared:
        ctx.locations_checked.update(cleared)

        if ctx.save_state_on_location_check:
            ctx.pending_auto_save = True

        if ctx.server:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": cleared}])
            await ctx.goal_target.check(ctx)

            if ctx.post_game_condition.check(ctx):
                new_unlocked : int = ctx.progression.get_progress(ctx.keys, True)
                if ctx.unlocked_channels < new_unlocked:
                    ctx.unlocked_channels = new_unlocked
                    ctx.ipc.set_unlocked_stages(ctx.unlocked_channels)
        else:
            ctx.offline_locations_checked.update(cleared)

async def update_offline_checked(ctx : 'AE3Context'):
    if not ctx.offline_locations_checked:
        return

    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": ctx.offline_locations_checked}])
    ctx.offline_locations_checked.clear()

# Used to check the in-game status of locations as stored in their permanent addresses
async def sweep_locations(ctx : 'AE3Context', batch : list[str]):
    cleared : set[int] = set()

    if any(stock_shop_item in cleared for stock_shop_item in SHOP_PROGRESSION_MORPH):
        cleared.update(*SHOP_PROGRESSION_MORPH[ctx.ipc.get_shop_morph_stock_checked()])

    for location in batch:
        if location in SHOP_PROGRESSION_MORPH:
            continue

        name : str = location if location not in Cellphone_Name_to_ID.keys() else Cellphone_Name_to_ID[location]

        if (ctx.current_game_mode == 0x100 and ctx.current_stage in LOCATIONS_INDEX and
                location in LOCATIONS_INDEX[ctx.current_stage]):
            continue

        if ctx.ipc.is_location_checked(location):
            cleared.add(ctx.locations_name_to_id[name])

    ctx.locations_checked.update(cleared)

    # Update Server for Locations checked that it did not know is checked
    cleared = cleared.difference(ctx.checked_locations)
    if cleared and ctx.server:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": cleared}])
        await check_progression(ctx)

# Handle Re-checking of Shop Items in Collection Type
async def handle_collection_shop_item_recheck(ctx: 'AE3Context'):
    if ctx.shoppingsanity != 2: return

    cleared : set[int] = set()
    for category in SHOP_COLLECTION_DIRECTORY.keys():
        category_item_ids: set[int] = set(ctx.locations_name_to_id[item]
                                          for item in SHOP_CATEGORIES_COLLECTION_DIRECTORY[category]
                                          if item not in SHOP_PERSISTENT_MASTER)

        amount_checked: int = len(category_item_ids.intersection(ctx.locations_checked))

        if amount_checked:
            cleared.update(ctx.locations_name_to_id[item]
                           for item in SHOP_COLLECTION_DIRECTORY[category][:amount_checked - 1])
            ctx.locations_checked.difference_update(category_item_ids)

    ctx.locations_checked.update(cleared)

    if cleared and ctx.server:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": cleared}])
        await check_progression(ctx)

        ctx.post_game_condition.check(ctx)
        await ctx.goal_target.check(ctx)

    if not ctx.is_cache_built:
        ctx.is_cache_built = True

async def check_progression(ctx : 'AE3Context'):
    await ctx.goal_target.check(ctx)

    if ctx.post_game_condition.check(ctx):
        new_unlocked: int = ctx.progression.get_progress(ctx.keys, True)
        if ctx.unlocked_channels < new_unlocked:
            ctx.unlocked_channels = new_unlocked
            ctx.ipc.set_unlocked_stages(ctx.unlocked_channels)

def dispatch_dummy_morph(ctx : 'AE3Context', unlock : bool = False):
    if not ctx.dummy_morph or ctx.dummy_morph is None or not ctx.dummy_morph_needed:
        return

    if unlock:
        ctx.ipc.unlock_equipment(ctx.dummy_morph)
    else:
        ctx.ipc.lock_equipment(ctx.dummy_morph)

def set_freeplay_mode(ctx : 'AE3Context'):
    if not ctx.alt_freeplay or ctx.is_mode_swapped:
        return

    current_mode : int = ctx.ipc.get_activated_game_mode()

    if current_mode != 0x100:   # Freeplay is represented as 0x001
        ctx.ipc.set_game_mode(0x100, False)
        ctx.current_game_mode = 0x4
    else:
        return

    ctx.is_mode_swapped = True

async def set_last_save_status(ctx : 'AE3Context'):
    is_last_save_normal : bool = True if ctx.is_last_save_normal is None else ctx.is_last_save_normal

    await ctx.send_msgs([{
        "cmd": "Set",
        "key": f"{APHelper.last_save_type.value}_{ctx.team}_{ctx.slot}",
        "default": True,
        "operations": [{"operation": "replace", "value": is_last_save_normal}]
    }])

async def get_last_save_status(ctx : 'AE3Context'):
    await ctx.send_msgs([{
        "cmd": "Get",
        "keys": [f"{APHelper.last_save_type.value}_{ctx.team}_{ctx.slot}"]
    }])