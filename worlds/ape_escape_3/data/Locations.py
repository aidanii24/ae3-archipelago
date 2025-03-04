from typing import Callable, Dict, Set, Sequence
from abc import ABC

from BaseClasses import Location

from .Addresses import Locations, Pointers
from .Logic import AccessRule, Rulesets
from .Strings import Loc, Meta


### [< --- HELPERS --- >]
class AE3Location(Location):
    """
    Defines a Location in Ape Escape 3. This refers to points of interest for the randomizer, such as Monkeys,
    Cellphones, Cameras and Points of Interests in the Hub.

    Attributes:
        game : Name of the Game
        rules : Sets of AccessRules to check if the Location is reachable
    """

    game : str = Meta.game.value
    rules : Rulesets = None


class AE3LocationMeta(ABC):
    """Base Data Class for all Locations in Ape Escape 3."""

    name : str
    loc_id : int
    address : int
    rules : Rulesets = None

class MonkeyLocation(AE3LocationMeta):
    """
    Base Data Class for all Monkey Locations

    Parameters:
        name : Name of Location from Strings.py
        rules : Sets of AccessRules for the Location. Can be an AccessRule, Sets of AccessRule, or a full Ruleset.
        Only parameters of type RuleSet can set Critical Rules.
    """

    def __init__(self, name : str, rules : Callable | Set[Callable] | Set[frozenset[Callable]] | Rulesets = None):
        self.name = name
        self.loc_id = Locations[name]
        self.address = self.loc_id

        if rules is Rulesets:
            self.rules = rules
        else:
            self.rules = Rulesets()

            if rules is Callable:
                self.rules.Rules.add(frozenset({rules}))
            elif rules is Set[Callable]:
                self.rules.Rules.add(frozenset(rules))
            elif rules is Set[Set[Callable]]:
                self.rules.Rules.update(rules)

        # For Monkeys, always add CATCH as a Critical Rule
        self.rules.Critical.add(AccessRule.CATCH)

    def add_rules(self, rules : Set[frozenset[Callable]]):
        self.rules.Rules.update(frozenset(s) for s in rules)

class CameraLocation(AE3LocationMeta):
    """Base Data Class for all Camera Locations"""

    ptrs : Sequence[int]

    def __init__(self, name : str):
        self.name = name
        self.loc_id = Locations[name]    # Equipment can be assumed to always be in Addresses.Items.
        self.address = self.loc_id

        if self.address in Pointers:
            self.ptrs = Pointers[self.address]

### [< --- LOCATIONS --- >]
# Zero
Zero_Ukki_Pan = MonkeyLocation(Loc.zero_ukki_pan.value)

# Seaside
Seaside_Nessal = MonkeyLocation(Loc.seaside_nessal.value)
Seaside_Ukki_Pia = MonkeyLocation(Loc.seaside_ukki_pia.value)
Seaside_Sarubo = MonkeyLocation(Loc.seaside_sarubo.value)
Seaside_Salurin = MonkeyLocation(Loc.seaside_salurin.value)
Seaside_Ukkitan = MonkeyLocation(Loc.seaside_ukkitan.value)
Seaside_Morella = MonkeyLocation(Loc.seaside_morella.value,
                                 {frozenset({AccessRule.SLING}), frozenset({AccessRule.FLY})})
Seaside_Ukki_Ben = MonkeyLocation(Loc.seaside_ukki_ben.value)
Seaside_Kankichi = MonkeyLocation(Loc.seaside_kankichi.value)
Seaside_Tomezo = MonkeyLocation(Loc.seaside_tomezo.value)
Seaside_Kamayan = MonkeyLocation(Loc.seaside_kamayan.value)
Seaside_Taizo = MonkeyLocation(Loc.seaside_taizo.value)

### [< --- LOCATION GROUPS --- >]
SEASIDE_MONKEYS : Sequence[MonkeyLocation] = [
    Seaside_Nessal, Seaside_Ukki_Pia, Seaside_Sarubo, Seaside_Salurin, Seaside_Ukkitan, Seaside_Morella,
    Seaside_Ukki_Ben, Seaside_Kankichi, Seaside_Tomezo, Seaside_Kamayan, Seaside_Taizo
]

MONKEYS : Sequence[MonkeyLocation] = [
    Zero_Ukki_Pan, *SEASIDE_MONKEYS
]

MASTER : Sequence[AE3LocationMeta] = [
    *MONKEYS
]

INDEX : Sequence[Sequence] = [
    MASTER, MONKEYS, SEASIDE_MONKEYS
]

### [< --- METHODS --- >]
def generate_name_to_id() -> Dict[str, int]:
    """Get a Dictionary of all Items in Name-ID pairs"""
    i: AE3LocationMeta
    return {i.name: i.loc_id for i in MASTER}



# # TODO - @Deprecated
# location_table = {
#     # Monkeys
#
#     ## TV Station/Zero
#     Loc.zero_ukki_pan.value :                   Locations[Loc.zero_ukki_pan.value].value,
#
#     ## Seaside Resort
#     Loc.seaside_nessal.value :                  Locations[Loc.seaside_nessal.value].value,
#     Loc.seaside_ukki_pia.value :                Locations[Loc.seaside_ukki_pia.value].value,
#     Loc.seaside_sarubo.value :                  Locations[Loc.seaside_sarubo.value].value,
#     Loc.seaside_salurin.value :                 Locations[Loc.seaside_salurin.value].value,
#     Loc.seaside_ukkitan.value :                 Locations[Loc.seaside_ukkitan.value].value,
#     Loc.seaside_morella.value :                 Locations[Loc.seaside_morella.value].value,
#     Loc.seaside_ukki_ben.value :                Locations[Loc.seaside_ukki_ben.value].value,
#     Loc.seaside_kankichi.value :                Locations[Loc.seaside_kankichi.value].value,
#     Loc.seaside_tomezo.value :                  Locations[Loc.seaside_tomezo.value].value,
#     Loc.seaside_kamayan.value :                 Locations[Loc.seaside_kamayan.value].value,
#     Loc.seaside_taizo.value :                   Locations[Loc.seaside_taizo.value].value
# }
#
# # Pre-list Prerequisite of Locations
# ## TODO - Could Move these to Rules.py
# rules_table = {
#     # Name
#
#     # Monkeys
#
#     ## TV Station/Zero
#     Loc.zero_ukki_pan.value                 : Rulesets( {AccessRule.CATCH} ),
#
#     ## Seaside Resort
#     Loc.seaside_nessal.value                : Rulesets( {AccessRule.CATCH} ),
#     Loc.seaside_ukki_pia.value              : Rulesets( {AccessRule.CATCH} ),
#     Loc.seaside_sarubo.value                : Rulesets( {AccessRule.CATCH} ),
#     Loc.seaside_salurin.value               : Rulesets( {AccessRule.CATCH} ),
#     Loc.seaside_ukkitan.value               : Rulesets( {AccessRule.CATCH} ),
#     Loc.seaside_morella.value               : Rulesets( {AccessRule.CATCH},
#                                                                      {frozenset({AccessRule.SLING})}),
#     Loc.seaside_ukki_ben.value              : Rulesets( {AccessRule.CATCH} ),
#
#     Loc.seaside_kankichi.value              : Rulesets( {AccessRule.CATCH},
#                                                                      {frozenset({AccessRule.MONKEY})}),
#     Loc.seaside_tomezo.value                : Rulesets( {AccessRule.CATCH},
#                                                                      {frozenset({AccessRule.MONKEY})}),
#     Loc.seaside_kamayan.value               : Rulesets( {AccessRule.CATCH},
#                                                                      {frozenset({AccessRule.MONKEY})}),
#     Loc.seaside_taizo.value                 : Rulesets( {AccessRule.CATCH},
#                                                                      {frozenset({AccessRule.MONKEY})})
# }
#
# location_group : Dict[str, Set[str]] = {}
#
# def create_location_groups():
#     # Monkeys
#     for location in location_table.keys():
#         location_group.setdefault("Monkeys", set()).add(location)