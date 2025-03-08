from typing import Callable, Dict, Set, Sequence
from dataclasses import dataclass
from abc import ABC

from BaseClasses import Location

#from .Addresses import Locations, Pointers
from .Addresses import NTSCU
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
        # Locations can be assumed to always be in Addresses.Locations. NTSCU version will be used as basis for the ID.
        self.loc_id = NTSCU.Locations[name]
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

Woods_Ukki_Pon = MonkeyLocation(Loc.woods_ukki_pon.value)
Woods_Ukkian = MonkeyLocation(Loc.woods_ukkian.value)
Woods_Ukki_Red = MonkeyLocation(Loc.woods_ukki_red.value)
Woods_Rosalin = MonkeyLocation(Loc.woods_rosalin.value)
Woods_Salubon = MonkeyLocation(Loc.woods_salubon.value)
Woods_Wolfmon = MonkeyLocation(Loc.woods_wolfmon.value)
Woods_Ukiko = MonkeyLocation(Loc.woods_ukiko.value)
Woods_Lambymon = MonkeyLocation(Loc.woods_lambymon.value)
Woods_Kreemon = MonkeyLocation(Loc.woods_kreemon.value)
Woods_Ukkilei = MonkeyLocation(Loc.woods_ukkilei.value)
Woods_Spork = MonkeyLocation(Loc.woods_spork.value)
Woods_King_Goat = MonkeyLocation(Loc.woods_king_goat.value)
Woods_Marukichi = MonkeyLocation(Loc.woods_marukichi.value)
Woods_Kikimon = MonkeyLocation(Loc.woods_kikimon.value)
Woods_Kominato = MonkeyLocation(Loc.woods_kominato.value)

# Woods

### [< --- LOCATION GROUPS --- >]
SEASIDE_MONKEYS : Sequence[MonkeyLocation] = [
    Seaside_Nessal, Seaside_Ukki_Pia, Seaside_Sarubo, Seaside_Salurin, Seaside_Ukkitan, Seaside_Morella,
    Seaside_Ukki_Ben, Seaside_Kankichi, Seaside_Tomezo, Seaside_Kamayan, Seaside_Taizo
]

WOODS_MONKEYS : Sequence[MonkeyLocation] = [
    Woods_Ukki_Pon, Woods_Ukkian, Woods_Ukki_Red, Woods_Rosalin, Woods_Salubon, Woods_Wolfmon, Woods_Ukiko,
    Woods_Lambymon, Woods_Kreemon, Woods_Ukkilei, Woods_Spork, Woods_King_Goat, Woods_Marukichi, Woods_Kikimon,
    Woods_Kominato
]

MONKEYS : Sequence[MonkeyLocation] = [
    Zero_Ukki_Pan, *SEASIDE_MONKEYS, *WOODS_MONKEYS
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