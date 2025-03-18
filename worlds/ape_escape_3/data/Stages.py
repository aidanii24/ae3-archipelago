from .Logic import has_keys
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

# Castle
To_Castle_A = StageEntranceMeta(Stage.castle_a.value)
To_Castle_B = StageEntranceMeta(Stage.castle_b.value)
To_Castle_C = StageEntranceMeta(Stage.castle_c.value)
To_Castle_D = StageEntranceMeta(Stage.castle_d.value)
To_Castle_E = StageEntranceMeta(Stage.castle_e.value, AccessRule.MONKEY)
To_Castle_F = StageEntranceMeta(Stage.castle_f.value)

# Monkey White Battle!
To_Boss1 = StageEntranceMeta(Stage.boss1.value, has_keys(1))

# Ciscocity
To_Ciscocity_A = StageEntranceMeta(Stage.ciscocity_a.value, has_keys(2))
To_Ciscocity_B = StageEntranceMeta(Stage.ciscocity_b.value)
To_Ciscocity_C = StageEntranceMeta(Stage.ciscocity_c.value)
To_Ciscocity_D = StageEntranceMeta(Stage.ciscocity_d.value, AccessRule.DASH, AccessRule.RCC)
To_Ciscocity_E = StageEntranceMeta(Stage.ciscocity_e.value, AccessRule.MONKEY)

# Studio
To_Studio_A = StageEntranceMeta(Stage.studio_a.value, AccessRule.SWIM, AccessRule.HERO)
To_Studio_A.rules.Critical.add(has_keys(2))
To_Studio_A_From_D = StageEntranceMeta(Stage.studio_a.value, AccessRule.SHOOT)
To_Studio_B = StageEntranceMeta(Stage.studio_b.value)
To_Studio_C = StageEntranceMeta(Stage.studio_c.value)
To_Studio_D = StageEntranceMeta(Stage.studio_d.value)
To_Studio_E = StageEntranceMeta(Stage.studio_e.value)
To_Studio_F = StageEntranceMeta(Stage.studio_f.value)
To_Studio_G = StageEntranceMeta(Stage.studio_g.value, AccessRule.MONKEY)

# Halloween
To_Halloween_A = StageEntranceMeta(Stage.halloween_a.value, has_keys(2))
To_Halloween_B = StageEntranceMeta(Stage.halloween_b.value)
To_Halloween_C = StageEntranceMeta(Stage.halloween_c.value)
To_Halloween_D = StageEntranceMeta(Stage.halloween_d.value)
To_Halloween_E = StageEntranceMeta(Stage.halloween_e.value, AccessRule.MONKEY)
To_Halloween_F = StageEntranceMeta(Stage.halloween_f.value)

# Western
To_Western_A = StageEntranceMeta(Stage.western_a.value, has_keys(2))
To_Western_B = StageEntranceMeta(Stage.western_b.value)
To_Western_C = StageEntranceMeta(Stage.western_c.value, AccessRule.MONKEY)
To_Western_D = StageEntranceMeta(Stage.western_d.value)
To_Western_E = StageEntranceMeta(Stage.western_e.value)
To_Western_F = StageEntranceMeta(Stage.western_f.value)

# Monkey Blue Battle!
To_Boss2 = StageEntranceMeta(Stage.boss2.value, has_keys(3))



### Stage Table
stage_data : dict[str : list[str]] = {
    # Menu
    Stage.title_screen.value                : [],

    # Hub
    Stage.travel_station_a.value            : [],
    Stage.travel_station_b.value            : [],

    # Zero
    Stage.zero.value                        : [Loc.zero_ukki_pan],

    # Seaside
    Stage.seaside_a.value                   : [Loc.seaside_nessal.value, Loc.seaside_ukki_pia, Loc.seaside_sarubo,
                                               Loc.seaside_salurin, Loc.seaside_ukkitan, Loc.seaside_morella]
}



### [< --- STAGES --- >]

# Menu
Title_Screen = AE3StageMeta(Stage.title_screen.value,
                            [To_Zero, To_Travel_Station_A])

# Hub
Travel_Station_A = AE3StageMeta(Stage.travel_station_a.value,
                                [To_Travel_Station_B,
                                 To_Seaside_A, To_Woods_A, To_Castle_A, To_Boss1, To_Ciscocity_A, To_Studio_A,
                                 To_Halloween_A, To_Western_A, To_Boss2])
Travel_Station_B = AE3StageMeta(Stage.travel_station_b.value)

# Zero
# Zero = AE3StageMeta(Stage.zero.value,
#                     To_Travel_Station_A,
#                     Zero_Ukki_Pan)

# Seaside
# Seaside_A = AE3StageMeta(Stage.seaside_a.value,
#                          [To_Seaside_B, To_Seaside_C],
#                          [Seaside_Nessal, Seaside_Ukki_Pia, Seaside_Sarubo, Seaside_Salurin, Seaside_Ukkitan,
#                           Seaside_Morella])
# Seaside_B = AE3StageMeta(Stage.seaside_b.value, None,
#                          [Seaside_Ukki_Ben])
# Seaside_C = AE3StageMeta(Stage.seaside_c.value, None,
#                          [Seaside_Kankichi, Seaside_Tomezo, Seaside_Kamayan, Seaside_Taizo])

# # Woods
# Woods_A = AE3StageMeta(Stage.woods_a.value,
#                        [To_Woods_B, To_Woods_D],
#                        [Woods_Ukki_Pon, Woods_Ukkian, Woods_Ukki_Red, Woods_Rosalin])
# Woods_B = AE3StageMeta(Stage.woods_b.value,
#                        [To_Woods_C],
#                        [Woods_Salubon, Woods_Wolfmon, Woods_Ukiko])
# Woods_C = AE3StageMeta(Stage.woods_c.value, None,
#                        [Woods_Lambymon, Woods_Kreemon, Woods_Ukkilei, Woods_Spork])
# Woods_D = AE3StageMeta(Stage.woods_d.value, None,
#                        [Woods_King_Goat, Woods_Marukichi, Woods_Kikimon, Woods_Kominato])
#
# # Castle
# Castle_A = AE3StageMeta(Stage.castle_a.value,
#                         [To_Castle_D],
#                         [Castle_Ukkido])
# Castle_B = AE3StageMeta(Stage.castle_b.value,
#                         [To_Castle_A, To_Castle_C, To_Castle_E],
#                         [Castle_Pipo_Guard, Castle_Monderella, Castle_Ukki_Ichi, Castle_Ukkinee])
# Castle_C = AE3StageMeta(Stage.castle_c.value, None,
#                         [Castle_Saru_Mon, Castle_Monga, Castle_Ukkiton, Castle_King_Leo])
# Castle_D = AE3StageMeta(Stage.castle_d.value,
#                         [To_Castle_B],
#                         [Castle_Ukkii, Castle_Saluto])
# Castle_E = AE3StageMeta(Stage.castle_e.value,
#                         [To_Castle_F],
#                         [Castle_Kings_Double, Castle_Mattsun, Castle_Miya, Castle_Mon_San])
# Castle_F = AE3StageMeta(Stage.castle_f.value, None,
#                         [Castle_SAL_1000])
#
# # Monkey White Battle!
# Boss1 = AE3StageMeta(Stage.boss1.value, None, [Boss_Monkey_White])

# Ciscocity
Ciscocity_A = AE3StageMeta(Stage.ciscocity_a.value,
                           [To_Ciscocity_B, To_Ciscocity_C, To_Ciscocity_D],
                           [Ciscocity_Ukima, Ciscocity_Monbolo, Ciscocity_Pipo_Mondy, Ciscocity_Ukki_Mattan,
                            Ciscocity_Bemucho, Ciscocity_Ukki_Nader])
Ciscocity_B = AE3StageMeta(Stage.ciscocity_b.value, None,
                           [Ciscocity_Sabu_Sabu, Ciscocity_Ginjiro, Ciscocity_Kichiemon])
Ciscocity_C = AE3StageMeta(Stage.ciscocity_c.value,
                           [To_Ciscocity_E],
                           [Ciscocity_Ukkilun])
Ciscocity_D = AE3StageMeta(Stage.ciscocity_d.value, None,
                           [Ciscocity_Bully_Mon, Ciscocity_Ukki_Joe, Ciscocity_Tamaki, Ciscocity_Mickey_Oou])
Ciscocity_E = AE3StageMeta(Stage.ciscocity_e.value, None,
                           [Ciscocity_Sally_Kokoroe, Ciscocity_Monkey_Manager, Ciscocity_Supervisor_Chimp,
                            Ciscocity_Boss_Ape])

# Studio
Studio_A = AE3StageMeta(Stage.studio_a.value,
                        [To_Studio_B, To_Studio_E],
                        [Studio_Ukki_Yan])
Studio_B = AE3StageMeta(Stage.studio_b.value,
                        [To_Studio_F],
                        [Studio_Ukkipuss, Studio_Minoh, Studio_Monta])
Studio_C = AE3StageMeta(Stage.studio_c.value,
                        [To_Studio_A],
                        [Studio_Pipopam, Studio_Monpii_Ukkichi, Studio_Gabimon])
Studio_D = AE3StageMeta(Stage.studio_d.value,
                        [To_Studio_A_From_D, To_Studio_G],
                        [Studio_Bananamon, Studio_Mokinza])
Studio_E = AE3StageMeta(Stage.studio_e.value,
                        [To_Studio_C],
                        [Studio_Ukki_Lee_Ukki, Studio_Ukkida_Jiro, Studio_Sal_Ukindo])
Studio_F = AE3StageMeta(Stage.studio_f.value,
                        [To_Studio_D],
                        [Studio_Gimminey, Studio_Hant, Studio_Chippino])
Studio_G = AE3StageMeta(Stage.studio_d.value, None,
                        [Studio_Ukki_Paul, Studio_Sally_Mon, Studio_Bonly, Studio_Monly])

# Halloween
Halloween_A = AE3StageMeta(Stage.halloween_a.value,
                           [To_Halloween_B],
                           [Halloween_Monkichiro, Halloween_Leomon, Halloween_Uikkun, Halloween_Take_Ukita])
Halloween_B = AE3StageMeta(Stage.halloween_b.value,
                           [To_Halloween_F],
                           [Halloween_Bonbon, Halloween_Chichi])
Halloween_C = AE3StageMeta(Stage.halloween_c.value,
                           [To_Halloween_D],
                           [Halloween_Ukkisuke, Halloween_Chibi_Sally, Halloween_Ukkison])
Halloween_D = AE3StageMeta(Stage.halloween_d.value,
                           [To_Halloween_E],
                           [Halloween_Saruhotep, Halloween_Ukkito, Halloween_Monzally, Halloween_Ukkiami])
Halloween_E = AE3StageMeta(Stage.halloween_e.value, None,
                           [Halloween_Monjan, Halloween_Nattchan, Halloween_Kabochin, Halloween_Ukki_Mon])
Halloween_F = AE3StageMeta(Stage.halloween_f.value,
                           [To_Halloween_C],
                           [Halloween_Mumpkin])

# Western
Western_A = AE3StageMeta(Stage.western_a.value,
                         [To_Western_B, To_Western_F],
                         [Western_Morrey, Western_Jomi, Western_Tammy])
Western_B = AE3StageMeta(Stage.western_b.value, None,
                         [Western_Ukki_Gigolo, Western_Monboron, Western_West_Ukki])
Western_C = AE3StageMeta(Stage.western_c.value, None,
                         [Western_Lucky_Woo, Western_Pamela, Western_Ukki_Monber, Western_Gaukichi])
Western_D = AE3StageMeta(Stage.western_d.value,
                         [To_Western_E],
                         [Western_Shaluron, Western_Jay_Mohn, Western_Munkee_Joe, Western_Saru_Chison,
                          Western_Jaja_Jamo])
Western_E = AE3StageMeta(Stage.western_e.value,
                         [To_Western_A, To_Western_C],
                         [Western_Chammy_Mo, Western_Golon_Moe, Western_Golozo])
Western_F = AE3StageMeta(Stage.western_f.value,
                         [To_Western_D],
                         [Western_Ukkia_Munbo, Western_Mon_Johny])

# Monkey Blue Battle!
Boss2 = AE3StageMeta(Stage.boss2.value, None, [Boss_Monkey_Blue])

### [< --- STAGE GROUPS --- >]
# HUB : Sequence[AE3StageMeta] = [
#     Travel_Station_A, Travel_Station_B
#]

# SEASIDE : Sequence[AE3StageMeta] = [
#     Seaside_A, Seaside_B, Seaside_C
# ]

# WOODS : Sequence[AE3StageMeta] = [
#     Woods_A, Woods_B, Woods_C, Woods_D
# ]
#
# CASTLE : Sequence[AE3StageMeta] = [
#     Castle_A, Castle_B, Castle_C, Castle_D, Castle_E, Castle_F
# ]

CISCOCITY : Sequence[AE3StageMeta] = [
    Ciscocity_A, Ciscocity_B, Ciscocity_C, Ciscocity_D, Ciscocity_E
]

STUDIO : Sequence[AE3StageMeta] = [
    Studio_A, Studio_B, Studio_C, Studio_D, Studio_E, Studio_F, Studio_G
]

HALLOWEEN : Sequence[AE3StageMeta] = [
    Halloween_A, Halloween_B, Halloween_C, Halloween_D, Halloween_E, Halloween_F
]

WESTERN : Sequence[AE3StageMeta] = [
    Western_A, Western_B, Western_C, Western_D, Western_E, Western_F
]

# BOSS : Sequence[AE3StageMeta] = [
#     Boss1, Boss2
# ]

# MASTER : Sequence[AE3StageMeta] = [
#     Title_Screen, Zero, *HUB, *SEASIDE, *WOODS, *CASTLE, *CISCOCITY, *STUDIO, *HALLOWEEN, *WESTERN, *BOSS
# ]
#
# INDEX : Sequence[Sequence] = [
#     MASTER, HUB, SEASIDE, WOODS, CASTLE, CISCOCITY, STUDIO, HALLOWEEN, WESTERN, BOSS
# ]




### [< --- REFACTORED STAGE GROUPS --- >]
STAGES_TITLE : Sequence[str] = [
    Stage.title_screen.value
]

STAGES_HUB : Sequence[str] = [
    Stage.travel_station_a.value, Stage.travel_station_b.value
]

STAGES_ZERO : Sequence[str] = [
    Stage.zero.value
]

STAGES_SEASIDE : Sequence[str] = [
    Stage.seaside_a.value, Stage.seaside_b.value, Stage.seaside_c.value
]

STAGES_WOODS : Sequence[str] = [
    Stage.woods_a.value, Stage.woods_b.value, Stage.woods_c.value, Stage.woods_d.value
]

STAGES_CASTLE : Sequence[str] = [
    Stage.castle_a.value, Stage.castle_b.value, Stage.castle_c.value, Stage.castle_d.value, Stage.castle_e.value,
    Stage.castle_f.value
]

STAGES_CISCOCITY : Sequence[str] = [
    Stage.ciscocity_a.value, Stage.ciscocity_b.value, Stage.ciscocity_c.value, Stage.ciscocity_d.value,
    Stage.ciscocity_e.value
]

STAGES_STUDIO : Sequence[str] = [
    Stage.studio_a.value, Stage.studio_a1.value, Stage.studio_b.value, Stage.studio_c.value,
    Stage.studio_d.value, Stage.studio_e.value, Stage.studio_f.value, Stage.studio_g.value
]

STAGES_HALLOWEEN : Sequence[str] = [
    Stage.halloween_a1.value, Stage.halloween_a.value, Stage.halloween_b.value, Stage.halloween_c.value,
    Stage.halloween_c1.value, Stage.halloween_d.value, Stage.halloween_e.value, Stage.halloween_e.value,
    Stage.halloween_f.value
]

STAGES_WESTERN : Sequence[str] = [
    Stage.western_a.value, Stage.western_b.value, Stage.western_c.value, Stage.western_d.value, Stage.western_e.value,
    Stage.western_f.value
]

STAGES_ONSEN : Sequence[str] = [
    Stage.onsen_a.value, Stage.onsen_a1.value, Stage.onsen_a2.value, Stage.onsen_b.value, Stage.onsen_b1.value,
    Stage.onsen_b.value, Stage.onsen_b2.value, Stage.onsen_c.value, Stage.onsen_d.value, Stage.onsen_d1.value,
    Stage.onsen_e.value
]

STAGES_SNOWFESTA : Sequence[str] = [
    Stage.snowfesta_a.value, Stage.snowfesta_b.value, Stage.snowfesta_c.value, Stage.snowfesta_d.value,
    Stage.snowfesta_e.value, Stage.snowfesta_f.value, Stage.snowfesta_g.value
]

STAGES_EDOTOWN : Sequence[str] = [
    Stage.edotown_a.value, Stage.edotown_b1.value, Stage.edotown_b.value, Stage.edotown_c1.value,
    Stage.edotown_c.value, Stage.edotown_d.value, Stage.edotown_e.value, Stage.edotown_f.value
]

STAGES_HEAVEN : Sequence[str] = [
    Stage.heaven_a.value, Stage.heaven_a1.value, Stage.heaven_a2.value, Stage.heaven_b.value, Stage.heaven_c.value,
    Stage.heaven_d.value, Stage.heaven_e.value
]

STAGES_TOYHOUSE : Sequence[str] = [
    Stage.toyhouse_a.value, Stage.toyhouse_b.value, Stage.toyhouse_c.value, Stage.toyhouse_d.value,
    Stage.toyhouse_e.value, Stage.toyhouse_e1.value, Stage.toyhouse_f.value, Stage.toyhouse_g.value,
    Stage.toyhouse_h.value
]

STAGES_ICELAND : Sequence[str] = [
    Stage.iceland_a.value, Stage.iceland_b.value, Stage.iceland_c.value, Stage.iceland_d.value, Stage.iceland_e.value,
    Stage.iceland_f.value
]

STAGES_ARABIAN : Sequence[str] = [
    Stage.arabian_a.value, Stage.arabian_b.value, Stage.arabian_c.value, Stage.arabian_c1.value, Stage.arabian_e.value,
    Stage.arabian_e1.value, Stage.arabian_f.value
]

STAGES_BOSSES : Sequence[str] = [
    Stage.boss1.value, Stage.boss2.value, Stage.boss3.value, Stage.boss4.value
]

STAGES_MASTER : Sequence[str] = [
    *STAGES_ZERO, *STAGES_SEASIDE, *STAGES_WOODS, *STAGES_CASTLE, *STAGES_CISCOCITY, *STAGES_STUDIO,
    *STAGES_HALLOWEEN, *STAGES_WESTERN, *STAGES_ONSEN, *STAGES_SNOWFESTA, *STAGES_EDOTOWN, *STAGES_HEAVEN,
    *STAGES_TOYHOUSE, *STAGES_ICELAND, *STAGES_ARABIAN, *STAGES_BOSSES, *STAGES_TITLE, *STAGES_HUB
]

STAGES_INDEX : Sequence[Sequence[str]] = [
    STAGES_MASTER, STAGES_ZERO, STAGES_SEASIDE, STAGES_WOODS, STAGES_CASTLE, STAGES_CISCOCITY, STAGES_STUDIO,
    STAGES_HALLOWEEN, STAGES_WESTERN, STAGES_ONSEN, STAGES_SNOWFESTA, STAGES_EDOTOWN, STAGES_HEAVEN,
    STAGES_TOYHOUSE, STAGES_ICELAND, STAGES_ARABIAN, STAGES_BOSSES, STAGES_TITLE, STAGES_HUB,
]