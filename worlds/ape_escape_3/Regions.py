from typing import TYPE_CHECKING, Callable, Dict

from BaseClasses import CollectionState, Entrance, Location, Region

from .data.Stages import STAGES_DIRECTORY, STAGES_MASTER
from .data.Locations import CAMERAS_INDEX, CAMERAS_MASTER, CELLPHONES_INDEX, CameraLocation, CellphoneLocation, \
    MonkeyLocation, MONKEYS_INDEX, EVENTS_INDEX
from .data.Logic import Rulesets
from .data.Rules import RuleType, Casual

if TYPE_CHECKING:
    from . import AE3World

### [< --- HELPERS --- >]
def generate_access_rule(player : int, rulesets : Rulesets) -> Callable[[CollectionState], bool]:
    """Parses a Ruleset and returns a staticmethod for use as an access rule by Archipelago"""
    def access_rule(state: CollectionState) -> bool:
        # Any Critical Rules that return False should immediately mark the item as inaccessible with the current state
        if rulesets.Critical:
            for rule in rulesets.Critical:
                if not rule(state, player):
                    return False

        # At least one set of normal rules (if any) must return true to mark the item as reachable
        if not rulesets.Rules:
            return True

        reachable: bool = False

        for ruleset in rulesets.Rules:
            for rule in ruleset:
                if not rule(state, player):
                    continue

                reachable = True
                break

        return reachable
    return access_rule

def establish_entrances(player : int, parent_region : Region, connections : Dict[Region, Rulesets]):
    """Connects the parent region to its destinations and assigns access rules where present."""
    for destination, ruleset in connections.items():
        entrance : Entrance = Entrance(player, parent_region.name + " <> " + destination.name)
        entrance.parent_region = parent_region

        if ruleset:
            entrance.access_rule = generate_access_rule(player, ruleset)

        parent_region.exits.append(entrance)
        entrance.connect(destination)

def create_regions(world : "AE3World"):
    rule : RuleType = Casual()
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
                loc.access_rule = generate_access_rule(world.player, ruleset)

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

                loc.access_rule = generate_access_rule(world.player, ruleset)

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
                loc : Location = event.to_event_location(world.player, stage)

                stage.locations.append(loc)

    # Send Regions to Archipelago
    world.multiworld.regions.extend(list(stages.values()))

    # <!> DEBUG
     # Connection Diagrams
    from Utils import visualize_regions
    visualize_regions(world.multiworld.get_region("Menu", world.player), "_region_diagram.puml")