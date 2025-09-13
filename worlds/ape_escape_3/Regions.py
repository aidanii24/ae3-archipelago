from typing import TYPE_CHECKING

from BaseClasses import Entrance, Location, Region

from .data.Stages import STAGES_BREAK_ROOMS, STAGES_DIRECTORY, STAGES_MASTER, ENTRANCES_MASTER, STAGES_DIRECTORY_LABEL, \
    STAGES_SHOP_PROGRESSION, STAGES_FARMABLE, AE3EntranceMeta, STAGES_FARMABLE_SNEAKY_BORG
from .data.Locations import CAMERAS_INDEX, CELLPHONES_INDEX, MONKEYS_PASSWORDS, MONKEYS_INDEX, EVENTS_INDEX, \
    SHOP_PROGRESSION_MASTER, SHOP_PROGRESSION_MORPH, SHOP_COLLECTION_INDEX, CameraLocation, CellphoneLocation, \
    EventMeta, MonkeyLocation, ShopItemLocation, SHOP_PROGRESSION_DIRECTORY, SHOP_EVENT_ACCESS_DIRECTORY, \
    SHOP_PROGRESSION_75COMPLETION
from .data.Logic import Rulesets
from .data.Strings import Stage

if TYPE_CHECKING:
    from . import AE3World


### [< --- HELPERS --- >]
def establish_entrance(player : int, name : str, parent_region : Region, destination : Region,
                       ruleset : Rulesets = None):
    """Connects the parent region to its destinations and assigns access rules where present."""
    entrance : Entrance = Entrance(player, name, parent_region)

    if ruleset is not None and ruleset:
        entrance.access_rule = ruleset.condense(player)

    parent_region.exits.append(entrance)
    entrance.connect(destination)

def create_regions(world : "AE3World"):
    entrance_rules : dict[str, Rulesets] = {**world.logic_preference.entrance_rules,
                                            **world.shop_rules.entrance_rules,
                                            **world.progression.generate_rules(world),}
    # world.logic_preference.entrance_rules.update(world.progression.generate_rules(world))

    add_cameras : bool = bool(world.options.camerasanity)
    add_cellphones : bool = bool(world.options.cellphonesanity.value)
    add_break_rooms : bool = bool(world.options.monkeysanity_break_rooms.value)

    # Initialize Regions
    stages : dict[str, Region] = {name : Region(name, world.player, world.multiworld) for name in STAGES_MASTER
                                  if name not in world.shop_rules.blacklisted_stages}
    entrances : list[AE3EntranceMeta] = [*ENTRANCES_MASTER,
                                  *world.shop_rules.entrances,
                                  *world.progression.level_select_entrances]
    blacklisted_entrances : list[Entrance] = [*world.logic_preference.blacklisted_entrances,
                                              *world.shop_rules.blacklisted_entrances]

    # Connect Regions
    for entrance in entrances:
        if entrance.name in blacklisted_entrances:
            continue

        ruleset : Rulesets = Rulesets()

        if entrance.parent in stages:
            parent = stages[entrance.parent]
        else:
            continue

        if entrance.destination in stages:
            destination = stages[entrance.destination]
        else:
            continue

        if entrance.name in entrance_rules:
            ruleset = entrance_rules[entrance.name]

        establish_entrance(world.player, entrance.name, parent, destination, ruleset)

    # Register Indirect Connections
    if world.options.shoppingsanity.value > 1:
        farmable_stages : list[str] = [*STAGES_FARMABLE]
        if world.options.farm_logic_sneaky_borgs.value:
            farmable_stages.extend(STAGES_FARMABLE_SNEAKY_BORG)

        # Register Shop Expensive Entrance as requiring an indirect condition
        for entrance in stages[Stage.region_shop_expensive.value].entrances:
            if entrance.name == Stage.entrance_shop_expensive.value:

                for region in [region for name, region in stages.items() if name in farmable_stages]:
                    world.multiworld.register_indirect_condition(region, entrance)

            break

    # Define Regions
    blacklist : list[str] = [stage for channel in world.options.blacklist_channel.value
                             for stage in STAGES_DIRECTORY_LABEL[channel]
                             if channel in STAGES_DIRECTORY_LABEL]

    for stage in stages.values():
        # Skip Blacklisted Stages
        if stage.name in blacklist:
            continue

        # Skip stage if Monkeysanity Break Rooms is enabled and the stage is a break room.
        # It should be safe to skip outright since there are no break rooms with Cameras or Cellphones in them.
        if not add_break_rooms and stage.name in STAGES_BREAK_ROOMS:
            continue

        # Define Locations
        ## Monkeys
        if stage.name in MONKEYS_INDEX:
            for monkeys in MONKEYS_INDEX[stage.name]:
                if not world.options.monkeysanity_passwords and monkeys in MONKEYS_PASSWORDS:
                    continue

                meta : MonkeyLocation = MonkeyLocation(monkeys)
                loc : Location = meta.to_location(world.player, stage)

                # Initialize Ruleset for Location
                ruleset : Rulesets = Rulesets()
                if monkeys in world.logic_preference.monkey_rules.keys():
                    ruleset = world.logic_preference.monkey_rules[monkeys]

                ruleset.critical.update(world.logic_preference.default_critical_rule)

                loc.access_rule = ruleset.condense(world.player)

                stage.locations.append(loc)

        ## Cameras
        if add_cameras and stage.name in CAMERAS_INDEX:
            camera : str = CAMERAS_INDEX[stage.name]
            meta : CameraLocation = CameraLocation(camera)
            loc : Location = meta.to_location(world.player, stage)

            # Add Access Rule for completing the stage to ensure maximum accessibility,
            # if the player chooses to require the monkey actors for the Cameras,
            # and they did not choose to have early Freeplay
            if world.options.camerasanity == 1 and not world.options.early_free_play:
                ruleset : Rulesets = Rulesets()
                parent_channel : str = ""
                for channel, regions in STAGES_DIRECTORY.items():
                    if not stage.name in regions:
                        continue

                    parent_channel = channel
                    break

                if parent_channel:
                    ruleset = world.logic_preference.get_channel_clear_rules(parent_channel)

                loc.access_rule = ruleset.condense(world.player)

            stage.locations.append(loc)

        ## Cellphones
        if add_cellphones:
            if stage.name in CELLPHONES_INDEX:
                for cellphone in CELLPHONES_INDEX[stage.name]:
                    meta : CellphoneLocation = CellphoneLocation(cellphone)
                    loc : Location = meta.to_location(world.player, stage)

                    stage.locations.append(loc)

        ## Events
        if stage.name in EVENTS_INDEX:
            for event in EVENTS_INDEX[stage.name]:
                meta : EventMeta = EventMeta(event)
                loc : Location = meta.to_event_location(world.player, stage)

                if event in world.logic_preference.event_rules:
                    loc.access_rule = world.logic_preference.event_rules[event].condense(world.player)

                stage.locations.append(loc)

    # Handle Shop Regions
    shopping_area: Region = stages[Stage.travel_station_b.value]
    expensive_area : Region = stages[Stage.region_shop_expensive.value]

    if world.options.shoppingsanity != 0:
        ## Handle Shop Items that require specific events
        for region, items in SHOP_EVENT_ACCESS_DIRECTORY.items():
            if region in blacklist:
                continue

            for item in items:
                meta: ShopItemLocation = ShopItemLocation(item)
                loc: Location = meta.to_location(world.player, shopping_area)

                if item in world.shop_rules.item_rules:
                    loc.access_rule = world.shop_rules.item_rules[item].condense(world.player)

                shopping_area.locations.append(loc)

        if not world.options.blacklist_channel.value:
            meta: ShopItemLocation = ShopItemLocation(SHOP_PROGRESSION_75COMPLETION[0])
            loc: Location = meta.to_location(world.player, shopping_area)

            if loc.name in world.shop_rules.item_rules:
                loc.access_rule = world.shop_rules.item_rules[loc.name].condense(world.player)

            shopping_area.locations.append(loc)

        ## Handle Morph Stocks
        if world.options.shoppingsanity != 2:
            stocks_region : Region = stages[Stage.region_shop_morph.value]

            for i, item in enumerate(SHOP_PROGRESSION_MORPH):
                meta : ShopItemLocation = ShopItemLocation(item, 1, i)
                loc : Location = meta.to_location(world.player, shopping_area)

                if item in world.shop_rules.item_rules:
                    loc.access_rule = world.shop_rules.item_rules[item].condense(world.player)

                stocks_region.locations.append(loc)

    ## Handle Shoppingsanity options Enabled/Collection
    if 0 < world.options.shoppingsanity.value < 3:
        shop_locations_meta : list[ShopItemLocation] = []

        if world.options.shoppingsanity.value == 1:
            for item in [*SHOP_PROGRESSION_MASTER]:

                meta : ShopItemLocation = ShopItemLocation(item)
                shop_locations_meta.append(meta)
        else:
            for category_index, category in enumerate(SHOP_COLLECTION_INDEX):
                for offset, item in enumerate(category):
                    meta : ShopItemLocation = ShopItemLocation(item, category_index, offset)
                    shop_locations_meta.append(meta)

        if shop_locations_meta:
            for item in shop_locations_meta:
                loc : Location = item.to_location(world.player, shopping_area)

                if item.name in world.shop_rules.item_rules:
                    loc.access_rule = world.shop_rules.item_rules[item.name].condense(world.player)

                if item in world.shop_rules.cheap_early_items:
                    shopping_area.locations.append(loc)
                else:
                    expensive_area.locations.append(loc)

    ## Handle Shoppingsanity Options Progressive/Restock
    elif 2 < world.options.shoppingsanity.value < 5:
        shop_progression_regions : list[Region] = [region for name, region in stages.items()
                                                   if name in STAGES_SHOP_PROGRESSION]

        for region in shop_progression_regions:
            for location in SHOP_PROGRESSION_DIRECTORY[region.name]:
                meta : ShopItemLocation = ShopItemLocation(location)
                loc : Location = meta.to_location(world.player, region)

                if location in world.shop_rules.item_rules:
                    loc.access_rule = world.shop_rules.item_rules[location].condense(world.player)

                region.locations.append(loc)

    # Send Regions to Archipelago
    world.multiworld.regions.extend(list(stages.values()))

    # shop_locs = [x.name for y in STAGES_SHOP_PROGRESSION for x in stages[y].locations]
    # shop_locs.extend(_.name for _ in shopping_area.locations)
    #
    # print("==================================")
    # for k, v in SHOP_CATEGORIES_COLLECTION_DIRECTORY.items():
    #     print(f"{k}: {len(set(v).intersection(shop_locs))} \t | {set(v).intersection(shop_locs)}")
    #
    # print(len(shop_locs), "\n")

    # # <!> DEBUG
    # # Connection Diagrams
    # from Utils import visualize_regions
    # visualize_regions(world.multiworld.get_region("Menu", world.player), "_region_diagram.puml")