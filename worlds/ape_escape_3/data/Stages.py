from .Logic import has_keys
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
    rules : Rulesets

    def __init__(self, destination : str,
                 *rules : Callable | frozenset[Callable] | Set[frozenset[Callable]] | Rulesets):
        self.destination = destination
        self.rules = Rulesets()

        for rule in rules:
            if isinstance(rule, Rulesets):
                self.rules = rule
            else:
                if isinstance(rule, Callable):
                    self.rules.Rules.add(frozenset({rule}))
                elif isinstance(rule, set):
                    self.rules.Rules.update(frozenset(rule))
                elif isinstance(rule, frozenset):
                    self.rules.Rules.add(rule)

class AE3StageMeta:
    """
    Base Data Class for all the Stages in Ape Escape 3. This will be used as a basis when creating regions.

    Parameters:
        name : Name of Stage from Strings.py
        entrances : List of Entrances (as defined by StageEntranceMeta) this stage has, excluding initial entrance.
        monkeys : List of Monkey Locations that this Stage contains.
        points_of_interest : List of other non-monkey Locations that this stage contains.
    """

    name : str
    entrances : list[StageEntranceMeta]
    monkeys : list[MonkeyLocation]
    points_of_interest : list[AE3LocationMeta]

    def __init__(self, name : str, entrances : StageEntranceMeta | list[StageEntranceMeta] = None,
        monkeys : MonkeyLocation | list[MonkeyLocation] = None,
        pois : AE3LocationMeta | list[AE3LocationMeta] = None):

        self.name = name
        self.entrances = []
        self.monkeys = []
        self.points_of_interest = []

        if isinstance(entrances, StageEntranceMeta):
            self.entrances = [entrances]
        elif isinstance(entrances, list):
            self.entrances = entrances

        if isinstance(monkeys, MonkeyLocation):
            self.monkeys = [monkeys]
        elif isinstance(monkeys, list):
            self.monkeys = monkeys

        if isinstance(pois, AE3LocationMeta):
            self.points_of_interest = [pois]
        elif isinstance(pois, list):
            self.points_of_interest = pois

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

# Woods
To_Woods_A = StageEntranceMeta(Stage.woods_a.value)
To_Woods_B = StageEntranceMeta(Stage.woods_b.value)
To_Woods_C = StageEntranceMeta(Stage.woods_c.value)
To_Woods_D = StageEntranceMeta(Stage.woods_d.value, AccessRule.MONKEY)

To_Castle_A = StageEntranceMeta(Stage.castle_a.value)
To_Castle_B = StageEntranceMeta(Stage.castle_b.value)
To_Castle_C = StageEntranceMeta(Stage.castle_c.value)
To_Castle_D = StageEntranceMeta(Stage.castle_d.value)
To_Castle_E = StageEntranceMeta(Stage.castle_e.value, AccessRule.MONKEY)
To_Castle_F = StageEntranceMeta(Stage.castle_f.value)

To_Boss1 = StageEntranceMeta(Stage.boss1.value, has_keys(1))

### [< --- STAGES --- >]

# Menu
Title_Screen = AE3StageMeta(Stage.title_screen.value,
                            [To_Zero, To_Travel_Station_A])

# Hub
Travel_Station_A = AE3StageMeta(Stage.travel_station_a.value,
                                [To_Travel_Station_B,
                                 To_Seaside_A, To_Woods_A, To_Castle_A, To_Boss1])
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

# Woods
Woods_A = AE3StageMeta(Stage.woods_a.value,
                       [To_Woods_B, To_Woods_D],
                       [Woods_Ukki_Pon, Woods_Ukkian, Woods_Ukki_Red, Woods_Rosalin])
Woods_B = AE3StageMeta(Stage.woods_b.value,
                       [To_Woods_C],
                       [Woods_Salubon, Woods_Wolfmon, Woods_Ukiko])
Woods_C = AE3StageMeta(Stage.woods_c.value, None,
                       [Woods_Lambymon, Woods_Kreemon, Woods_Ukkilei, Woods_Spork])
Woods_D = AE3StageMeta(Stage.woods_d.value, None,
                       [Woods_King_Goat, Woods_Marukichi, Woods_Kikimon, Woods_Kominato])

# Castle
Castle_A = AE3StageMeta(Stage.castle_a.value,
                        [To_Castle_D],
                        [Castle_Ukkido])
Castle_B = AE3StageMeta(Stage.castle_b.value,
                        [To_Castle_A, To_Castle_C, To_Castle_E],
                        [Castle_Pipo_Guard, Castle_Monderella, Castle_Ukki_Ichi, Castle_Ukkinee])
Castle_C = AE3StageMeta(Stage.castle_c.value, None,
                        [Castle_Saru_Mon, Castle_Monga, Castle_Ukkiton, Castle_King_Leo])
Castle_D = AE3StageMeta(Stage.castle_d.value,
                        [To_Castle_B],
                        [Castle_Ukkii, Castle_Saluto])
Castle_E = AE3StageMeta(Stage.castle_e.value,
                        [To_Castle_F],
                        [Castle_Kings_Double, Castle_Mattsun, Castle_Miya, Castle_Mon_San])
Castle_F = AE3StageMeta(Stage.castle_f.value, None,
                        [Castle_SAL_1000])

# Monkey White Battle!
Boss1 = AE3StageMeta(Stage.boss1.value, None, [Boss_Monkey_White])

### [< --- STAGE GROUPS --- >]
HUB : Sequence[AE3StageMeta] = [
    Travel_Station_A, Travel_Station_B
]

SEASIDE : Sequence[AE3StageMeta] = [
    Seaside_A, Seaside_B, Seaside_C
]

WOODS : Sequence[AE3StageMeta] = [
    Woods_A, Woods_B, Woods_C, Woods_D
]

CASTLE : Sequence[AE3StageMeta] = [
    Castle_A, Castle_B, Castle_C, Castle_D, Castle_E, Castle_F
]

BOSS : Sequence[AE3StageMeta] = [
    Boss1
]

MASTER : Sequence[AE3StageMeta] = [
    Title_Screen, Zero, *HUB, *SEASIDE, *WOODS, *CASTLE, *BOSS
]

INDEX : Sequence[Sequence] = [
    MASTER, HUB, SEASIDE, WOODS, CASTLE, BOSS
]