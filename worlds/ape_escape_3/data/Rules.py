from dataclasses import dataclass
from typing import TYPE_CHECKING

from .Strings import Loc, Stage
from .Locations import *
from .Stages import StageEntranceMeta

if TYPE_CHECKING:
    from .. import AE3World

@dataclass
class RuleType:
    monkey_rules : dict[str, set[AccessRule] | AccessRule]
    entrances : dict[str, list[StageEntranceMeta]]

class Casual(RuleType):
    monkey_rules = {
        Loc.seaside_morella.value           : [AccessRule.SHOOT, AccessRule.FLY]
    }

    entrances = {
        Stage.title_screen.value            : [StageEntranceMeta(Stage.zero.value),
                                               StageEntranceMeta(Stage.travel_station_a.value)],
        Stage.travel_station_a.value        : [StageEntranceMeta(Stage.travel_station_b.value),
                                               [StageEntranceMeta(Stage.seaside_a.value)]],
        Stage.travel_station_b.value        : [StageEntranceMeta(Stage.travel_station_b.value)],

        # Zero
        Stage.zero.value                    : [StageEntranceMeta(Stage.seaside_a.value)],

        # Seaside
        Stage.seaside_a.value               : [StageEntranceMeta(Stage.seaside_b.value),
                                               StageEntranceMeta(Stage.seaside_c.value, AccessRule.MONKEY)],
        Stage.seaside_b.value               : [StageEntranceMeta(Stage.seaside_a.value)],
        Stage.seaside_c.value               : [StageEntranceMeta(Stage.seaside_a.value)],
    }
