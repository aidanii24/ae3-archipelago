from typing import Callable, Dict, Set, Sequence
from dataclasses import dataclass
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

    game : str = Meta.game
    rules : Rulesets

@dataclass
class AE3LocationMeta(ABC):
    """Base Data Class for all Locations in Ape Escape 3."""

    name : str
    loc_id : int
    address : int
    rules : Rulesets

@dataclass
class MonkeyLocation(AE3LocationMeta):
    """
    Base Data Class for all Monkey Locations

    Parameters:
        name : Name of Location from Strings.py
        rules : Sets of AccessRules for the Location. Can be an AccessRule, Sets of AccessRule, or a full Ruleset.
        Only parameters of type RuleSet can set Critical Rules.
    """

    def __init__(self, name : str, *rules : Callable | frozenset[Callable] | Set[frozenset[Callable]] | Rulesets):
        self.name = name
        self.loc_id = Locations[name]
        self.address = self.loc_id
        self.rules = Rulesets()

        for rule in rules:
            if isinstance(rule, Rulesets):
                self.rules = rule
            else:
                if isinstance(rule, Callable):
                    self.rules.Rules.add(frozenset({rule}))
                elif isinstance(rule, set):
                    self.rules.Rules.update(rule)
                elif isinstance(rules, frozenset):
                    self.rules.Rules.add(rule)

        # For Monkeys, always add CATCH as a Critical Rule
        self.rules.Critical.add(AccessRule.CATCH)

@dataclass
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
                                 AccessRule.SHOOT, AccessRule.FLY)
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