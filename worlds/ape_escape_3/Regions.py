from typing import TYPE_CHECKING, Dict

from BaseClasses import Entrance, Location, Region

from .data.Stages import STAGES_DIRECTORY, STAGES_MASTER
from .data.Locations import CAMERAS_INDEX, CAMERAS_MASTER, CELLPHONES_INDEX, CameraLocation, CellphoneLocation, \
    EventMeta, MonkeyLocation, MONKEYS_INDEX, EVENTS_INDEX
from .data.Logic import Rulesets
from .data.Rules import LogicPreference, Casual

if TYPE_CHECKING:
    from . import AE3World

### [< --- HELPERS --- >]
def establish_entrances(player : int, parent_region : Region, connections : Dict[Region, Rulesets]):
    """Connects the parent region to its destinations and assigns access rules where present."""
    for destination, ruleset in connections.items():
        entrance : Entrance = Entrance(player, parent_region.name + " <> " + destination.name)
        entrance.parent_region = parent_region

        if ruleset:
            entrance.access_rule = ruleset.condense(player)

        parent_region.exits.append(entrance)
        entrance.connect(destination)

def create_regions(world : "AE3World"):
    rule : LogicPreference = Casual()
    rule.set_keys_rules(world.progression)

    # Initialize Regions
    stages : dict[str, Region] = { name : Region(name, world.player, world.multiworld) for name in STAGES_MASTER }

    # Define Regions
    for stage in stages.values():
        connections : dict[Region, Rulesets] = {}
        if rule.entrances[stage.name]:
            for entrance in rule.entrances[stage.name]:
                connections.setdefault(stages[entrance.destination], entrance.rules)

        if connections:
            establish_entrances(world.player, stage, connections)

        # Define Locations
        ## Monkeys
        if stage.name in MONKEYS_INDEX:
            for monkeys in MONKEYS_INDEX[stage.name]:
                meta : MonkeyLocation = MonkeyLocation(monkeys)
                loc : Location = meta.to_location(world.player, stage)

                # Initialize Ruleset for Location
                ruleset : Rulesets = Rulesets()
                if monkeys in rule.monkey_rules.keys():
                    ruleset = rule.monkey_rules[monkeys].rules

                ruleset.Critical.update(rule.default_critical_rule)

                # Generate Access Rule from Ruleset
                loc.access_rule = ruleset.condense(world.player)

                stage.locations.append(loc)

        ## Cameras
        if world.options.Camerasanity and stage.name in CAMERAS_INDEX:
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
        if world.options.Cellphonesanity:
            if stage.name in CELLPHONES_INDEX:
                for cellphone in CELLPHONES_INDEX[stage.name]:
                    meta : CellphoneLocation = CellphoneLocation(cellphone)
                    loc : Location = meta.to_location(world.player, stage)

                    stage.locations.append(loc)

        ## Events
        if stage.name in EVENTS_INDEX:
            for event in EVENTS_INDEX[stage.name]:
                if event in rule.event_rules:
                    meta : EventMeta = EventMeta(event)
                    loc : Location = meta.to_event_location(world.player, stage)
                    loc.access_rule = rule.event_rules[event].rules.condense()

                    stage.locations.append(loc)

    # Send Regions to Archipelago
    world.multiworld.regions.extend(list(stages.values()))

    # <!> DEBUG
     # Connection Diagrams
    from Utils import visualize_regions
    visualize_regions(world.multiworld.get_region("Menu", world.player), "_region_diagram.puml")