from collections.abc import Callable
from typing import Dict, Set, List

from BaseClasses import CollectionState, Location, Region

from . import Logic
from .Strings import AE3Locations
from .Logic import Prerequisite

class AE3Location(Location):
    """
        Defines a Location in Ape Escape 3. This refers to points of interest for the randomizer, such as Monkeys,
        Cellphones, Cameras and Points of Interests in the Hub.

        Attributes:
            game : Name of the Game
            prerequisites : List of states required to reach the item.
            Each key or set contains their own set of states needed to satisfy their condition. An item only needs
            one of their sets to have all their conditions met for the item to be considered reachable. Additionally,
            prerequisites under the key named "Global" must also be true, in addition to any additional sets.
    """

    game: str = "Ape Escape 3"
    prerequisites: Dict[str: Set[Callable[[CollectionState, int], bool]]] = {}

    def __init__(self, player : int, name : str, address : int, parent_region : Region ):
        self.prerequisites = prerequisite_table[name]

        super().__init__(player, name, address, parent_region)

location_table = {
    # Monkeys

    ## TV Station/Zero
    AE3Locations.zero_ukki_pan.value : 0,

    ## Seaside Resort
    AE3Locations.seaside_nessal.value : 1,
    AE3Locations.seaside_ukki_pia.value : 2,
    AE3Locations.seaside_sarubo.value : 3,
    AE3Locations.seaside_salurin.value : 4,
    AE3Locations.seaside_ukkitan.value : 5,
    AE3Locations.seaside_morella.value : 6,
    AE3Locations.seaside_ukki_ben.value : 7,
    AE3Locations.seaside_break_kankichi.value : 8,
    AE3Locations.seaside_break_tomezo.value : 9,
    AE3Locations.seaside_break_kamayan.value : 10,
    AE3Locations.seaside_break_taizo.value : 11
}

# Pre-list Prerequisite of Locations. Super
prerequisite_table = {
    # Name

    # Monkeys

    ## TV Station/Zero
    AE3Locations.zero_ukki_pan.value                : { "Global"    : [Prerequisite.catch] },

    ## Seaside Resort
    AE3Locations.seaside_nessal.value               : { "Global"    : [Prerequisite.catch] },
    AE3Locations.seaside_ukki_pia.value             : { "Global"    : [Prerequisite.catch] },
    AE3Locations.seaside_sarubo.value               : { "Global"    : [Prerequisite.catch] },
    AE3Locations.seaside_salurin.value              : { "Global"    : [Prerequisite.catch] },
    AE3Locations.seaside_ukkitan.value              : { "Global"    : [Prerequisite.catch] },
    AE3Locations.seaside_morella.value              : { "Global"    : [Prerequisite.catch],
                                                        "Shoot"     : [Prerequisite.shoot_free]},
    AE3Locations.seaside_ukki_ben.value             : { "Global"    : [Prerequisite.catch] },
    AE3Locations.seaside_break_kankichi.value       : { "Global"    : [Prerequisite.catch],
                                                        "Monkey"    : [Prerequisite.monkey]},
    AE3Locations.seaside_break_tomezo.value         : { "Global"    : [Prerequisite.catch],
                                                        "Monkey"    : [Prerequisite.monkey] },
    AE3Locations.seaside_break_kamayan.value        : { "Global"    : [Prerequisite.catch],
                                                        "Monkey"    : [Prerequisite.monkey] },
    AE3Locations.seaside_break_taizo.value          : { "Global"    : [Prerequisite.catch],
                                                        "Monkey"    : [Prerequisite.monkey] }
}

location_group : Dict[str, Set[str]] = {}

def create_location_groups():
    keys : List[str] = list(location_table)

    # Monkeys
    for location in location_table:
        location_group.setdefault("Monkeys", set()).add(location)