from typing import TYPE_CHECKING

from BaseClasses import Entrance, Location, Region

from .data.Stages import STAGES_BREAK_ROOMS, STAGES_DIRECTORY, STAGES_MASTER, ENTRANCES_MASTER
from .data.Locations import CAMERAS_INDEX, CAMERAS_MASTER, CELLPHONES_INDEX, CameraLocation, CellphoneLocation, \
    EventMeta, MONKEYS_PASSWORDS, MonkeyLocation, MONKEYS_INDEX, EVENTS_INDEX
from .data.Logic import Rulesets
from .data.Rules import LogicPreference, LogicPreferenceOptions

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
    print("PLAYER", world.player)
    rule : LogicPreference = LogicPreferenceOptions[world.options.Logic_Preference]()
    rule.set_level_progression_rules(world.progression, world.options.Post_Game_Access_Rule.value,
     [world.post_game_access_rule.as_access_rule()])

    add_cameras : bool = (world.options.Camerasanity or world.options.Goal_Target == 5 or
                          world.options.Post_Game_Access_Rule == 2)
    add_cellphones : bool = (world.options.Cellphonesanity or world.options.Goal_Target == 6 or
                             world.options.Post_Game_Access_Rule == 3)
    add_break_rooms : bool = bool(world.options.Monkeysanity_BreakRooms) or world.options.Post_Game_Access_Rule == 0

    # Initialize Regions
    stages : dict[str, Region] = { name : Region(name, world.player, world.multiworld) for name in STAGES_MASTER }

    # Connect Regions
    for entrance in [*ENTRANCES_MASTER, *world.progression.level_select_entrances]:
        ruleset : Rulesets = Rulesets()

        if entrance.parent in stages:
            parent = stages[entrance.parent]
        else:
            continue

        if entrance.destination in stages:
            destination = stages[entrance.destination]
        else:
            continue

        if entrance.name in LogicPreference.entrance_rules:
            ruleset = LogicPreference.entrance_rules[entrance.name]

        establish_entrance(world.player, entrance.name, parent, destination, ruleset)

    # Define Regions
    for stage in stages.values():
        # Define Locations

        # Skip stage if Monkeysanity Break Rooms is enabled and the stage is a break room.
        # It should be safe to skip outright since there are no break rooms with Cameras or Cellphones in them.
        if add_break_rooms and stage in STAGES_BREAK_ROOMS:
            continue

        ## Monkeys
        if stage.name in MONKEYS_INDEX:
            for monkeys in MONKEYS_INDEX[stage.name]:
                if not world.options.Monkeysanity_Passwords and monkeys in MONKEYS_PASSWORDS:
                    continue

                meta : MonkeyLocation = MonkeyLocation(monkeys)
                loc : Location = meta.to_location(world.player, stage)

                # Initialize Ruleset for Location
                ruleset : Rulesets = Rulesets()
                if monkeys in rule.monkey_rules.keys():
                    ruleset = rule.monkey_rules[monkeys]

                ruleset.critical.update(rule.default_critical_rule)

                loc.access_rule = ruleset.condense(world.player)

                stage.locations.append(loc)

        ## Cameras
        if add_cameras and stage.name in CAMERAS_INDEX:
            camera : str = CAMERAS_INDEX[stage.name]
            meta : CameraLocation = CameraLocation(camera, CAMERAS_MASTER.index(camera))
            loc : Location = meta.to_location(world.player, stage)

            # Add Access Rule for completing the stage to ensure maximum accessibility,
            # if the player chooses to require the monkey actors for the Cameras,
            # and they did not choose to have early Freeplay
            if world.options.Camerasanity == 1 and not world.options.Early_Free_Play:
                ruleset : Rulesets = Rulesets()
                parent_channel : str = ""
                for channel, regions in STAGES_DIRECTORY.items():
                    if not stage.name in regions:
                        continue

                    parent_channel = channel
                    break

                if parent_channel:
                    ruleset = rule.get_channel_clear_rules(parent_channel)

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

                if event in rule.event_rules:
                    loc.access_rule = rule.event_rules[event].condense(world.player)

                stage.locations.append(loc)

    # Send Regions to Archipelago
    world.multiworld.regions.extend(list(stages.values()))

    # # <!> DEBUG
    # # Connection Diagrams
    from Utils import visualize_regions
    visualize_regions(world.multiworld.get_region("Menu", world.player), "_region_diagram.puml")