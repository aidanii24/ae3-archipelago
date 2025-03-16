from typing import Callable, Set
from dataclasses import dataclass

from .Logic import Rulesets, AccessRule, has_keys, event_invoked
from .Strings import Loc, Stage, Game
from .Stages import StageEntranceMeta


@dataclass
class RuleWrap:
    """Container for Rulesets for easy parsing when generating locations"""
    rules : Rulesets = Rulesets()

    def __init__(self, *rules : Callable | frozenset[Callable] | Set[frozenset[Callable]] | Rulesets):
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

class RuleType:
    """
    Base Class for defined RuleTypes. RuleTypes determine the kinds of access rules locations or regions have
    based on a preferred play style
    """
    monkey_rules : dict[str, RuleWrap]
    entrances : dict[str, list[StageEntranceMeta]]

    default_critical_rule : Set[Callable] = [AccessRule.CATCH]

class Casual(RuleType):
    """
    RuleType for a casual experience. The player is assumed to play the game without any or little advanced or obscure
    knowledge of it.
    """
    monkey_rules = {
        Loc.seaside_morella.value           : RuleWrap(AccessRule.SHOOT, AccessRule.FLY,
                                                       frozenset({AccessRule.GENIE, AccessRule.CLUB})),
        Loc.castle_monga.value              : RuleWrap(AccessRule.SHOOT, AccessRule.FLY)
    }

    entrances = {
        Stage.title_screen.value            : [StageEntranceMeta(Stage.zero.value),
                                               StageEntranceMeta(Stage.travel_station_a.value)],

        # Level Select
        Stage.travel_station_a.value        : [StageEntranceMeta(Stage.travel_station_b.value),
                                               StageEntranceMeta(Stage.seaside_a.value),
                                               StageEntranceMeta(Stage.woods_a.value),
                                               StageEntranceMeta(Stage.castle_a.value),

                                               StageEntranceMeta(Stage.boss1.value, has_keys(1)),

                                               StageEntranceMeta(Stage.ciscocity_a.value, has_keys(2)),
                                               StageEntranceMeta(Stage.studio_a.value, has_keys(2))],

        Stage.travel_station_b.value        : [StageEntranceMeta(Stage.travel_station_a.value)],

        # Zero
        Stage.zero.value                    : [StageEntranceMeta(Stage.travel_station_a.value)],

        # Seaside
        Stage.seaside_a.value               : [StageEntranceMeta(Stage.seaside_b.value),
                                               StageEntranceMeta(Stage.seaside_c.value, AccessRule.MONKEY)],
        Stage.seaside_b.value               : [StageEntranceMeta(Stage.seaside_a.value)],
        Stage.seaside_c.value               : [StageEntranceMeta(Stage.seaside_a.value)],

        # Woods
        Stage.woods_a.value                 : [StageEntranceMeta(Stage.woods_b.value),
                                               StageEntranceMeta(Stage.woods_d.value, AccessRule.MONKEY)],
        Stage.woods_b.value                 : [StageEntranceMeta(Stage.woods_a.value),
                                               StageEntranceMeta(Stage.woods_c.value)],
        Stage.woods_c.value                 : [StageEntranceMeta(Stage.woods_b.value)],
        Stage.woods_d.value                 : [StageEntranceMeta(Stage.woods_a.value)],

        # Castle
        Stage.castle_a.value                : [StageEntranceMeta(Stage.castle_d.value),
                                               StageEntranceMeta(Stage.castle_b.value)],
        Stage.castle_b.value                : [StageEntranceMeta(Stage.castle_a.value),
                                               StageEntranceMeta(Stage.castle_c.value),
                                               StageEntranceMeta(Stage.castle_d.value),
                                               StageEntranceMeta(Stage.castle_e.value, AccessRule.MONKEY)],
        Stage.castle_c.value                : [StageEntranceMeta(Stage.castle_b.value)],
        Stage.castle_d.value                : [StageEntranceMeta(Stage.castle_a.value),
                                               StageEntranceMeta(Stage.castle_b.value)],
        Stage.castle_e.value                : [StageEntranceMeta(Stage.castle_b.value),
                                               StageEntranceMeta(Stage.castle_f.value)],
        Stage.castle_f.value                : [StageEntranceMeta(Stage.castle_e.value)],

        # Boss1
        Stage.boss1.value                   : None,

        # Ciscocity
        Stage.ciscocity_a.value             : [StageEntranceMeta(Stage.ciscocity_b.value),
                                               StageEntranceMeta(Stage.ciscocity_c.value),
                                               StageEntranceMeta(Stage.ciscocity_d.value),],
        Stage.ciscocity_b.value             : [StageEntranceMeta(Stage.ciscocity_a.value)],
        Stage.ciscocity_c.value             : [StageEntranceMeta(Stage.ciscocity_a.value),
                                               StageEntranceMeta(Stage.ciscocity_e.value),],
        Stage.ciscocity_d.value             : [StageEntranceMeta(Stage.ciscocity_a.value,
                                                                 AccessRule.DASH, AccessRule.RCC)],
        Stage.ciscocity_e.value             : [StageEntranceMeta(Stage.ciscocity_c.value, AccessRule.MONKEY)],

        # Studio
        Stage.studio_a.value                : [StageEntranceMeta(Stage.studio_b.value, AccessRule.SHOOT,
                                                                 AccessRule.GLIDE, AccessRule.GENIE),
                                               StageEntranceMeta(Stage.studio_c.value),
                                               StageEntranceMeta(Stage.studio_a1.value,
                                                                 event_invoked(Game.shortcut_studio_ad.value)),
                                               StageEntranceMeta(Stage.studio_e.value)],
        Stage.studio_a1.value               : [StageEntranceMeta(Stage.studio_a.value),
                                               StageEntranceMeta(Stage.studio_d.value)],
        Stage.studio_b.value                : [StageEntranceMeta(Stage.studio_a.value),
                                               StageEntranceMeta(Stage.studio_f.value)],
        Stage.studio_c.value                : [StageEntranceMeta(Stage.studio_a.value),
                                               StageEntranceMeta(Stage.studio_e.value)],
        Stage.studio_d.value                : [StageEntranceMeta(Stage.studio_a1.value, AccessRule.SHOOT),
                                               StageEntranceMeta(Stage.studio_f.value),
                                               StageEntranceMeta(Stage.studio_g.value, AccessRule.MONKEY)],
        Stage.studio_e.value                : [StageEntranceMeta(Stage.studio_a.value),
                                               StageEntranceMeta(Stage.studio_c.value)],
        Stage.studio_f.value                : [StageEntranceMeta(Stage.studio_b.value),
                                               StageEntranceMeta(Stage.studio_d.value)],
        Stage.studio_g.value                : [StageEntranceMeta(Stage.studio_d.value)]
    }
