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
        # Seaside
        Loc.seaside_morella.value           : RuleWrap(AccessRule.SHOOT, AccessRule.FLY,
                                                       frozenset({AccessRule.GENIE, AccessRule.CLUB})),

        # Castle
        Loc.castle_monga.value              : RuleWrap(AccessRule.SHOOT, AccessRule.FLY),

        # Ciscocity
        Loc.ciscocity_ukkilun.value         : RuleWrap(AccessRule.DASH, AccessRule.RCC, AccessRule.SHOOT),

        # Studio
        Loc.studio_minoh.value              : RuleWrap(AccessRule.SHOOT, AccessRule.FLY),
        Loc.studio_monta.value              : RuleWrap(AccessRule.SHOOT, AccessRule.FLY),

        # Halloween
        Loc.halloween_ukkisuke.value        : RuleWrap(AccessRule.SWIM, AccessRule.HERO),
        Loc.halloween_chibi_sally.value     : RuleWrap(AccessRule.SWIM, AccessRule.HERO),

        # Onsen
        Loc.onsen_chabimon.value            : RuleWrap(AccessRule.RCC),
        Loc.onsen_mujakin.value             : RuleWrap(AccessRule.SWIM, AccessRule.HERO, AccessRule.NINJA),
        Loc.onsen_fuji_chan.value           : RuleWrap(AccessRule.SHOOT, AccessRule.NINJA),

        # Snowfesta
        Loc.snowfesta_kimisuke.value        : RuleWrap(AccessRule.SHOOT),
        Loc.snowfesta_mitsuro.value         : RuleWrap(AccessRule.SHOOT),

        # Edotown
        Loc.edotown_walter.value            : RuleWrap(AccessRule.NINJA),
        Loc.edotown_monkibeth.value         : RuleWrap(AccessRule.NINJA),

        # Heaven
        Loc.heaven_chomon.value             : RuleWrap(AccessRule.RCC),

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
                                               StageEntranceMeta(Stage.studio_a.value, has_keys(2)),
                                               StageEntranceMeta(Stage.halloween_a1.value, has_keys(2)),
                                               StageEntranceMeta(Stage.western_a.value, has_keys(2)),

                                               StageEntranceMeta(Stage.boss2.value, has_keys(3)),

                                               StageEntranceMeta(Stage.onsen_a.value, has_keys(4)),
                                               StageEntranceMeta(Stage.snowfesta_a.value, has_keys(4)),
                                               StageEntranceMeta(Stage.edotown_a.value, has_keys(4)),

                                               StageEntranceMeta(Stage.boss3.value, has_keys(5))],

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
        Stage.studio_g.value                : [StageEntranceMeta(Stage.studio_d.value)],

        # Halloween
        Stage.halloween_a1.value            : [StageEntranceMeta(Stage.halloween_a.value,
                                                                 AccessRule.SWIM, AccessRule.HERO)],
        Stage.halloween_a.value             : [StageEntranceMeta(Stage.halloween_a1.value,
                                                                 AccessRule.SWIM, AccessRule.HERO),
                                               StageEntranceMeta(Stage.halloween_b.value)],
        Stage.halloween_b.value             : [StageEntranceMeta(Stage.halloween_a.value),
                                               StageEntranceMeta(Stage.halloween_f.value)],
        Stage.halloween_c.value             : [StageEntranceMeta(Stage.halloween_c1.value),
                                               StageEntranceMeta(Stage.halloween_d.value)],
        Stage.halloween_c1.value            : [StageEntranceMeta(Stage.halloween_c.value,
                                                                 AccessRule.SWIM, AccessRule.HERO),
                                               StageEntranceMeta(Stage.halloween_f.value)],
        Stage.halloween_d.value             : [StageEntranceMeta(Stage.halloween_c.value),
                                               StageEntranceMeta(Stage.halloween_e.value, AccessRule.MONKEY)],
        Stage.halloween_e.value             : [StageEntranceMeta(Stage.halloween_d.value)],
        Stage.halloween_f.value             : [StageEntranceMeta(Stage.halloween_b.value),
                                               StageEntranceMeta(Stage.halloween_c1.value)],

        # Western
        Stage.western_a.value               : [StageEntranceMeta(Stage.western_b.value),
                                               StageEntranceMeta(Stage.western_f.value)],
        Stage.western_b.value               : [StageEntranceMeta(Stage.western_a.value)],
        Stage.western_c.value               : [StageEntranceMeta(Stage.western_e.value)],
        Stage.western_d.value               : [StageEntranceMeta(Stage.western_e.value),
                                               StageEntranceMeta(Stage.western_f.value)],
        Stage.western_e.value               : [StageEntranceMeta(Stage.western_d.value),
                                               StageEntranceMeta(Stage.western_c.value, AccessRule.MONKEY)],
        Stage.western_f.value               : [StageEntranceMeta(Stage.western_a.value),
                                               StageEntranceMeta(Stage.western_d.value)],

        # Boss2
        Stage.boss2.value                   : None,

        # Onsen
        Stage.onsen_a.value                 : [StageEntranceMeta(Stage.onsen_a1.value),
                                               StageEntranceMeta(Stage.onsen_a2.value)],
        Stage.onsen_a1.value                : [StageEntranceMeta(Stage.onsen_a.value),
                                               StageEntranceMeta(Stage.onsen_a2.value,
                                                                 AccessRule.GLIDE, AccessRule.GENIE),
                                               StageEntranceMeta(Stage.onsen_b1.value,
                                                                 AccessRule.DASH, AccessRule.RCC)],
        Stage.onsen_a2.value                : [StageEntranceMeta(Stage.onsen_a.value),
                                               StageEntranceMeta(Stage.onsen_a1.value,
                                                                 AccessRule.GLIDE, AccessRule.GENIE),
                                               StageEntranceMeta(Stage.onsen_b1.value,
                                                                 AccessRule.DASH, AccessRule.RCC),],
        Stage.onsen_b1.value                : [StageEntranceMeta(Stage.onsen_a1.value),
                                               StageEntranceMeta(Stage.onsen_a2.value),
                                               StageEntranceMeta(Stage.onsen_b.value,
                                                                 AccessRule.GLIDE, AccessRule.RCC)],
        Stage.onsen_b.value                 : [StageEntranceMeta(Stage.onsen_b1.value),
                                               StageEntranceMeta(Stage.onsen_b2.value, AccessRule.FLY),
                                               StageEntranceMeta(Stage.onsen_d1.value,
                                                                 AccessRule.SHOOT, AccessRule.RCC),
                                               StageEntranceMeta(Stage.onsen_e.value)],
        Stage.onsen_b2.value                : [StageEntranceMeta(Stage.onsen_b.value),
                                               StageEntranceMeta(Stage.onsen_d.value),],
        Stage.onsen_c.value                 : [StageEntranceMeta(Stage.onsen_d.value)],
        Stage.onsen_d.value                 : [StageEntranceMeta(Stage.onsen_b2.value),
                                               StageEntranceMeta(Stage.onsen_c.value, AccessRule.MONKEY),
                                               StageEntranceMeta(Stage.onsen_d1.value,
                                                                 AccessRule.DASH, AccessRule.RCC)],
        Stage.onsen_d1.value                : [StageEntranceMeta(Stage.onsen_b.value),
                                               StageEntranceMeta(Stage.onsen_d.value, AccessRule.RCC)],
        Stage.onsen_e.value                 : [StageEntranceMeta(Stage.onsen_b.value)],

        # Snowfesta
        Stage.snowfesta_a.value             : [StageEntranceMeta(Stage.snowfesta_b.value,
                                                                 AccessRule.DASH, AccessRule.RCC),
                                               StageEntranceMeta(Stage.snowfesta_c.value),
                                               StageEntranceMeta(Stage.snowfesta_g.value)],
        Stage.snowfesta_b.value             : [StageEntranceMeta(Stage.snowfesta_a.value)],
        Stage.snowfesta_c.value             : [StageEntranceMeta(Stage.snowfesta_a.value),
                                               StageEntranceMeta(Stage.snowfesta_e.value),
                                               StageEntranceMeta(Stage.snowfesta_f.value)],
        Stage.snowfesta_d.value             : [StageEntranceMeta(Stage.snowfesta_g.value)],
        Stage.snowfesta_e.value             : [StageEntranceMeta(Stage.snowfesta_c.value)],
        Stage.snowfesta_f.value             : [StageEntranceMeta(Stage.snowfesta_c.value)],
        Stage.snowfesta_g.value             : [StageEntranceMeta(Stage.snowfesta_a.value, AccessRule.MONKEY),
                                               StageEntranceMeta(Stage.snowfesta_d.value)],

        # Edotown
        Stage.edotown_a.value               : [StageEntranceMeta(Stage.edotown_b1.value)],
        Stage.edotown_b1.value              : [StageEntranceMeta(Stage.edotown_a.value),
                                               StageEntranceMeta(Stage.edotown_b.value, AccessRule.NINJA)],
        Stage.edotown_b.value               : [StageEntranceMeta(Stage.edotown_b1.value,
                                                                 AccessRule.NINJA, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.edotown_c1.value),
                                               StageEntranceMeta(Stage.edotown_e.value,
                                                                 event_invoked(Game.shortcut_edotown_eb.value))],
        Stage.edotown_c1.value              : [StageEntranceMeta(Stage.edotown_b.value),
                                               StageEntranceMeta(Stage.edotown_c.value,
                                                                 AccessRule.NINJA, AccessRule.HERO)],
        Stage.edotown_c.value               : [StageEntranceMeta(Stage.edotown_c1.value,
                                                                 AccessRule.NINJA, AccessRule.HERO),
                                               StageEntranceMeta(Stage.edotown_d.value)],
        Stage.edotown_d.value               : [StageEntranceMeta(Stage.edotown_c.value),
                                               StageEntranceMeta(Stage.edotown_e.value),
                                               StageEntranceMeta(Stage.edotown_f.value, AccessRule.MONKEY)],
        Stage.edotown_e.value               : [StageEntranceMeta(Stage.edotown_d.value),
                                               StageEntranceMeta(Stage.edotown_b.value)],
        Stage.edotown_f.value               : [StageEntranceMeta(Stage.edotown_d.value)],

        # Boss3
        Stage.boss3.value                   : None
    }
