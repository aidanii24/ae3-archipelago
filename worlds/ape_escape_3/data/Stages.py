from typing_extensions import NamedTuple
from dataclasses import dataclass

from .Strings import Stage
from .Locations import *


### [< --- HELPERS --- >]
@dataclass
class StageEntranceMeta:
    """
    Base Data Class for the entrances of various Stages.

    Parameters:
        destination : Name of Stage Destination in Strings.py
        rules : Sets of AccessRules for the Entrance. Can be an AccessRule, Set of AccessRule, or a full Ruleset.
        Passing callables will add them as Normal Rules. To assign critical rules, pass a Ruleset instead.
    """
    destination : str
    rules : Rulesets = None

    def __init__(self, destination : str, rules : Callable | Set[Callable] | Rulesets = None):
        self.destination = destination

        if rules is Rulesets:
            self.rules = rules
        else:
            self.rules = Rulesets()

            if rules is Callable:
                self.rules.Rules.add(frozenset({rules}))
            if rules is Set[Callable]:
                self.rules.Rules.add(frozenset(rules))

class AE3StageMeta(NamedTuple):
    """
    Base Data Class for all the Stages in Ape Escape 3. This will be used as a basis when creating regions.

    Parameters:
        name : Name of Stage from Strings.py
        entrances : List of Entrances (as defined by StageEntranceMeta) this stage has, excluding initial entrance.
        monkeys : List of Monkey Locations that this Stage contains.
        points_of_interest : List of other non-monkey Locations that this stage contains
    """

    name : str
    entrances : List[StageEntranceMeta] = None
    monkeys : List[MonkeyLocation] = None
    points_of_interest : List[AE3LocationMeta] = None

    def __new__(cls, name : str, entrances : StageEntranceMeta | List[StageEntranceMeta] = None,
                monkeys : MonkeyLocation | List[MonkeyLocation] = None,
                pois : AE3LocationMeta | List[AE3LocationMeta] = None):
        cls.name = name

        if entrances is StageEntranceMeta:
            cls.locations = [entrances]
        elif entrances is List[StageEntranceMeta]:
            cls.locations = entrances

        if monkeys is MonkeyLocation:
            cls.locations = [monkeys]
        elif monkeys is List[MonkeyLocation]:
            cls.locations = monkeys

        if pois is AE3LocationMeta:
            cls.locations = [pois]
        elif pois is List[AE3LocationMeta]:
            cls.locations = pois

### [< --- ENTRANCES --- >]

# Hub
To_Travel_Station_A = StageEntranceMeta(Stage.travel_station_a.value)
To_Travel_Station_B = StageEntranceMeta(Stage.travel_station_b.value)

# Zero
To_Zero = StageEntranceMeta(Stage.zero.value)

# Seaside
To_Seaside_A = StageEntranceMeta(Stage.seaside_a.value)
To_Seaside_B = StageEntranceMeta(Stage.seaside_b.value)
To_Seaside_C = StageEntranceMeta(Stage.seaside_c.value, AccessRule.MONKEY)

### [< --- STAGES --- >]

# Menu
Title_Screen = AE3StageMeta(Stage.title_screen.value,
                            [To_Zero, To_Travel_Station_A])

# Hub
Travel_Station_A = AE3StageMeta(Stage.travel_station_a.value,
                                [To_Seaside_A])
Travel_Station_B = AE3StageMeta(Stage.travel_station_b.value)

# Zero
Zero = AE3StageMeta(Stage.zero.value,
                    To_Travel_Station_A,
                    Zero_Ukki_Pan)

# Seaside
Seaside_A = AE3StageMeta(Stage.seaside_a.value,
                         [To_Seaside_B, To_Seaside_C],
                         [Seaside_Nessal, Seaside_Ukki_Pia, Seaside_Sarubo, Seaside_Salurin, Seaside_Ukkitan,
                          Seaside_Morella])
Seaside_B = AE3StageMeta(Stage.seaside_b.value, None,
                         [Seaside_Ukki_Ben])
Seaside_C = AE3StageMeta(Stage.seaside_c.value, None,
                         [Seaside_Kankichi, Seaside_Tomezo, Seaside_Kamayan, Seaside_Taizo])

### [< --- STAGE GROUPS --- >]
HUB : Sequence[AE3StageMeta] = [
    Travel_Station_A, Travel_Station_B
]

SEASIDE : Sequence[AE3StageMeta] = [
    Seaside_A, Seaside_B, Seaside_C
]

MASTER : Sequence[AE3StageMeta] = [
    Title_Screen, Zero, *HUB, *SEASIDE
]

INDEX : Sequence[Sequence] = [
    MASTER, HUB, SEASIDE
]