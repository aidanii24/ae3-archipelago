from typing import TYPE_CHECKING, Callable, Dict

from BaseClasses import CollectionState, Entrance, Location, Region

from .data.Stages import AE3StageMeta, MASTER
from .data.Locations import AE3Location
from .data.Logic import Rulesets

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

### [< --- GENERATION --- >]
def create_regions(world : "AE3World"):
    # Cache Data
    meta_cache : Dict[str, AE3StageMeta] = { r.name : r for r in MASTER }
    regions_dir : Dict[str, Region] = {}

    # Initialize Regions
    for stage in MASTER:

        region : Region = Region(stage.name, world.player, world.multiworld)
        regions_dir.setdefault(region.name, region)

    # Define Regions
    for region in regions_dir.values():
        meta : AE3StageMeta = meta_cache[region.name]

        # Connect Regions
        connections : Dict[Region, Rulesets] = {}
        if meta.entrances:
            for entrance in meta.entrances:
                connections.setdefault(regions_dir[entrance.destination], entrance.rules)

        establish_entrances(world.player, region, connections)

        # Define Locations
        if meta.monkeys:
            for loc in [*meta.monkeys]:
                location : Location = AE3Location(world.player, loc.name, loc.address, region)

                if loc.rules:
                    location.access_rule = generate_access_rule(world.player, loc.rules)

                region.locations.append(location)

    # Send Regions to Archipelago
    world.multiworld.regions.extend(list(regions_dir.values()))

    # <!> DEBUG
    # Connection Diagrams
    from Utils import visualize_regions
    visualize_regions(world.multiworld.get_region("Menu", world.player), "_region_diagram.puml")