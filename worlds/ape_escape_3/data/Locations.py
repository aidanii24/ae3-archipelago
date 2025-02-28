from typing import Dict, Set

from BaseClasses import Location, Region

from .Strings import AE3Locations
from .Logic import AccessRules, LocationRules
from .Addresses import Address

# TODO - Create Tables by category first, then add them all to a master table

class AE3Location(Location):
    """
        Defines a Location in Ape Escape 3. This refers to points of interest for the randomizer, such as Monkeys,
        Cellphones, Cameras and Points of Interests in the Hub.

        Attributes:
            game : Name of the Game
            rules : Set of LocationRules to check if the Location is reachable
    """

    game: str = "Ape Escape 3"
    rules: LocationRules = None

    def __init__(self, player : int, name : str, address : int, parent_region : Region ):
        self.rules = rules_table[name]

        super().__init__(player, name, address, parent_region)

location_table = {
    # Monkeys

    ## TV Station/Zero
    AE3Locations.zero_ukki_pan.value :                  Address.locations[AE3Locations.zero_ukki_pan.value],

    ## Seaside Resort
    AE3Locations.seaside_nessal.value :                 Address.locations[AE3Locations.seaside_nessal.value],
    AE3Locations.seaside_ukki_pia.value :               Address.locations[AE3Locations.seaside_ukki_pia.value],
    AE3Locations.seaside_sarubo.value :                 Address.locations[AE3Locations.seaside_sarubo.value],
    AE3Locations.seaside_salurin.value :                Address.locations[AE3Locations.seaside_salurin.value],
    AE3Locations.seaside_ukkitan.value :                Address.locations[AE3Locations.seaside_ukkitan.value],
    AE3Locations.seaside_morella.value :                Address.locations[AE3Locations.seaside_morella.value],
    AE3Locations.seaside_ukki_ben.value :               Address.locations[AE3Locations.seaside_ukki_ben.value],
    AE3Locations.seaside_break_kankichi.value :         Address.locations[AE3Locations.seaside_break_kankichi.value],
    AE3Locations.seaside_break_tomezo.value :           Address.locations[AE3Locations.seaside_break_tomezo.value],
    AE3Locations.seaside_break_kamayan.value :          Address.locations[AE3Locations.seaside_break_kamayan.value],
    AE3Locations.seaside_break_taizo.value :            Address.locations[AE3Locations.seaside_break_taizo.value]
}

# Pre-list Prerequisite of Locations
## TODO - Could Move these to Rules.py
rules_table = {
    # Name

    # Monkeys

    ## TV Station/Zero
    AE3Locations.zero_ukki_pan.value                : LocationRules( {AccessRules.CATCH} ),

    ## Seaside Resort
    AE3Locations.seaside_nessal.value               : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_ukki_pia.value             : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_sarubo.value               : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_salurin.value              : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_ukkitan.value              : LocationRules( {AccessRules.CATCH} ),
    AE3Locations.seaside_morella.value              : LocationRules( {AccessRules.CATCH},
                                                                     {frozenset({AccessRules.SHOOT_FREE})}),
    AE3Locations.seaside_ukki_ben.value             : LocationRules( {AccessRules.CATCH} ),

    AE3Locations.seaside_break_kankichi.value       : LocationRules( {AccessRules.CATCH},
                                                                     {frozenset({AccessRules.MONKEY})}),
    AE3Locations.seaside_break_tomezo.value         : LocationRules( {AccessRules.CATCH},
                                                                     {frozenset({AccessRules.MONKEY})}),
    AE3Locations.seaside_break_kamayan.value        : LocationRules( {AccessRules.CATCH},
                                                                     {frozenset({AccessRules.MONKEY})}),
    AE3Locations.seaside_break_taizo.value          : LocationRules( {AccessRules.CATCH},
                                                                     {frozenset({AccessRules.MONKEY})})
}

location_group : Dict[str, Set[str]] = {}

def create_location_groups():
    # Monkeys
    for location in location_table.keys():
        location_group.setdefault("Monkeys", set()).add(location)