from typing import Sequence
from Strings import APHelper

RATES0: dict[str, float] = {
    APHelper.nothing.value              : 70.0,
    APHelper.hint_filler.value          : 15.0,
    APHelper.hint_progressive.value     : 5.5,
    APHelper.check_filler.value         : 5.25,
    APHelper.check_progressive.value    : 3.0,
    APHelper.check_pgc.value            : 0.25,
    APHelper.check_gt.value             : 0.1,
}

RATES1: dict[str, float] = {
    APHelper.nothing.value              : 40.0,
    APHelper.hint_filler.value          : 25.0,
    APHelper.hint_progressive.value     : 13,
    APHelper.check_filler.value         : 12.245,
    APHelper.check_progressive.value    : 8.0,
    APHelper.check_pgc.value            : 1.2,
    APHelper.check_gt.value             : 0.525,
    APHelper.bypass_pgc.value           : 0.025,
    APHelper.instant_goal.value         : 0.005,
}

CONSOLATION_RATES: Sequence[dict[str, float]] = [
    RATES0,
    RATES1,
]