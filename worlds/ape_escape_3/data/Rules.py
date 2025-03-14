from dataclasses import dataclass
from typing import TYPE_CHECKING

from .Strings import Stage
from .Locations import *
from .Stages import StageEntranceMeta

if TYPE_CHECKING:
    from .. import AE3World


@dataclass
class RuleWrap:
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
    monkey_rules : dict[str, RuleWrap]
    entrances : dict[str, list[StageEntranceMeta]]

    default_critical_rule : Set[Callable] = [AccessRule.CATCH]

class Casual(RuleType):
    monkey_rules = {
        Loc.seaside_morella.value           : RuleWrap(AccessRule.SHOOT, AccessRule.FLY, AccessRule.GENIE)
    }

    entrances = {
        Stage.title_screen.value            : [StageEntranceMeta(Stage.zero.value),
                                               StageEntranceMeta(Stage.travel_station_a.value)],
        Stage.travel_station_a.value        : [StageEntranceMeta(Stage.travel_station_b.value),
                                               StageEntranceMeta(Stage.seaside_a.value)],
        Stage.travel_station_b.value        : [StageEntranceMeta(Stage.travel_station_a.value)],

        # Zero
        Stage.zero.value                    : [StageEntranceMeta(Stage.travel_station_a.value)],

        # Seaside
        Stage.seaside_a.value               : [StageEntranceMeta(Stage.seaside_b.value),
                                               StageEntranceMeta(Stage.seaside_c.value, AccessRule.MONKEY)],
        Stage.seaside_b.value               : [StageEntranceMeta(Stage.seaside_a.value)],
        Stage.seaside_c.value               : [StageEntranceMeta(Stage.seaside_a.value)],
    }
