from collections.abc import Callable
from typing import Dict, Set, List

from BaseClasses import CollectionState, Location, Region

from .Strings import AE3Locations
from .Logic import AccessRules, LocationRules


# TODO
# Create Location() objects directly instead of making Tables of its data first

class AE3Location(Location):
    """
        Defines a Location in Ape Escape 3. This refers to points of interest for the randomizer, such as Monkeys,
        Cellphones, Cameras and Points of Interests in the Hub.

        Attributes:
            game : Name of the Game
            rules : Set of LocationRules to check if the Location is reachable
    """

    game: str = "Ape Escape 3"
    rules: LocationRules

    def __init__(self, player : int, name : str, address : int, parent_region : Region ):
        self.rules = rules_table[name]

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

# Pre-list Prerequisite of Locations
## TODO - Could Move these to Rules.py
rules_table : Dict[str : Set[Callable[[CollectionState, int], bool]]] = {
    # Name

    # Monkeys

    ## TV Station/Zero
    AE3Locations.zero_ukki_pan.value                : LocationRules( {AccessRules.CATCH}, ),

    ## Seaside Resort
    AE3Locations.seaside_nessal.value               : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_ukki_pia.value             : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_sarubo.value               : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_salurin.value              : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_ukkitan.value              : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_morella.value              : LocationRules( {AccessRules.CATCH},
                                                                     {{AccessRules.SHOOT_FREE}}),
    AE3Locations.seaside_ukki_ben.value             : LocationRules( {AccessRules.CATCH} ),

    AE3Locations.seaside_break_kankichi.value       : LocationRules( {AccessRules.CATCH},
                                                                     {{AccessRules.MONKEY}}),
    AE3Locations.seaside_break_tomezo.value         : LocationRules( {AccessRules.CATCH},
                                                                     {{AccessRules.MONKEY}}),
    AE3Locations.seaside_break_kamayan.value        : LocationRules( {AccessRules.CATCH},
                                                                     {{AccessRules.MONKEY}}),
    AE3Locations.seaside_break_taizo.value          : LocationRules( {AccessRules.CATCH},
                                                                     {{AccessRules.MONKEY}})
}

location_group : Dict[str, Set[str]] = {}

def create_location_groups():
    keys : List[str] = list(location_table)

    # Monkeys
    for location in location_table:
        location_group.setdefault("Monkeys", set()).add(location)