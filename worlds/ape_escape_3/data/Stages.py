from .Locations import *


### [< --- HELPERS --- >]
@dataclass
class AE3EntranceMeta:
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
                 *rules : Callable | frozenset[Callable] | Set[frozenset[Callable]] | Rulesets,
                 critical : set = None):
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

        if isinstance(critical, set):
            self.rules.Critical.update(critical)

### [< --- STAGE GROUPS --- >]
LEVELS_BY_ORDER : Sequence[str] = [
    Stage.seaside_a.value,
    Stage.woods_a.value,
    Stage.castle_a.value,

    Stage.boss1.value,

    Stage.ciscocity_a.value,
    Stage.studio_a.value,
    Stage.halloween_a1.value,
    Stage.western_a.value,

    Stage.boss2.value,

    Stage.onsen_a.value,
    Stage.snowfesta_a.value,
    Stage.edotown_a.value,

    Stage.boss3.value,

    Stage.heaven_a1.value,
    Stage.toyhouse_a.value,
    Stage.iceland_a.value,
    Stage.arabian_a.value,

    Stage.boss4.value,

    Stage.asia_a.value,
    Stage.plane_a.value,
    Stage.hong_a.value,

    Stage.boss5.value,

    Stage.bay_a.value,
    Stage.tomo_a1.value,

    Stage.boss6.value,

    Stage.space_a.value,

    Stage.specter1.value,
    Stage.specter2.value
]

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
    Stage.arabian_e1.value, Stage.arabian_f.value, Stage.arabian_g.value
]

STAGES_ASIA : Sequence[str] = [
    Stage.asia_a.value, Stage.asia_a1.value, Stage.asia_a2.value, Stage.asia_a3.value, Stage.asia_a4.value,
    Stage.asia_a5.value, Stage.asia_b.value, Stage.asia_b1.value, Stage.asia_b2.value, Stage.asia_d.value,
    Stage.asia_d1.value, Stage.asia_d2.value, Stage.asia_e.value, Stage.asia_e1.value, Stage.asia_e2.value,
    Stage.asia_f.value
]

STAGES_PLANE : Sequence[str] = [
    Stage.plane_a.value, Stage.plane_a1.value, Stage.plane_b.value, Stage.plane_b1.value, Stage.plane_c.value,
    Stage.plane_c1.value, Stage.plane_d.value, Stage.plane_e.value, Stage.plane_f.value, Stage.plane_f1.value,
    Stage.plane_g.value, Stage.plane_h.value
]

STAGES_HONG : Sequence[str] = [
    Stage.hong_a.value, Stage.hong_a1.value, Stage.hong_a2.value, Stage.hong_b.value, Stage.hong_b1.value,
    Stage.hong_c.value, Stage.hong_c1.value, Stage.hong_c2.value, Stage.hong_d.value, Stage.hong_e.value,
    Stage.hong_e1.value, Stage.hong_f.value, Stage.hong_g.value, Stage.hong_h.value
]

STAGES_BAY : Sequence[str] = [
    Stage.bay_a.value, Stage.bay_a1.value, Stage.bay_a2.value, Stage.bay_a3.value, Stage.bay_a4.value,
    Stage.bay_a5.value, Stage.bay_b.value, Stage.bay_c.value, Stage.bay_d.value, Stage.bay_d1.value,
    Stage.bay_e.value, Stage.bay_e1.value, Stage.bay_e2.value, Stage.bay_e3.value, Stage.bay_f.value
]

STAGES_TOMO : Sequence[str] = [
    Stage.tomo_a.value, Stage.tomo_a1.value, Stage.tomo_b.value, Stage.tomo_c.value, Stage.tomo_e.value,
    Stage.tomo_e1.value, Stage.tomo_e2.value, Stage.tomo_f.value, Stage.tomo_f1.value, Stage.tomo_f2.value,
    Stage.tomo_g.value, Stage.tomo_g1.value, Stage.tomo_h.value, Stage.tomo_h1.value, Stage.tomo_i.value,
    Stage.tomo_j.value,
]

STAGES_SPACE : Sequence[str] = [
    Stage.space_a.value, Stage.space_b.value, Stage.space_d.value, Stage.space_e.value, Stage.space_e1.value,
    Stage.space_f.value, Stage.space_f1.value, Stage.space_f2.value, Stage.space_g.value, Stage.space_g1.value,
    Stage.space_g2.value, Stage.space_h.value, Stage.space_i.value, Stage.space_j.value, Stage.space_k.value,
    Stage.space_l.value,
]

STAGES_BOSSES : Sequence[str] = [
    Stage.boss1.value, Stage.boss2.value, Stage.boss3.value, Stage.boss4.value, Stage.boss5.value, Stage.boss6.value,
    Stage.specter1.value, Stage.specter2.value
]

STAGES_MASTER : Sequence[str] = [
    *STAGES_ZERO, *STAGES_SEASIDE, *STAGES_WOODS, *STAGES_CASTLE, *STAGES_CISCOCITY, *STAGES_STUDIO,
    *STAGES_HALLOWEEN, *STAGES_WESTERN, *STAGES_ONSEN, *STAGES_SNOWFESTA, *STAGES_EDOTOWN, *STAGES_HEAVEN,
    *STAGES_TOYHOUSE, *STAGES_ICELAND, *STAGES_ARABIAN, *STAGES_ASIA, *STAGES_PLANE, *STAGES_HONG,
    *STAGES_BAY, *STAGES_TOMO, *STAGES_SPACE, *STAGES_BOSSES, *STAGES_TITLE, *STAGES_HUB
]

STAGES_INDEX : Sequence[Sequence[str]] = [
    STAGES_MASTER, STAGES_ZERO, STAGES_SEASIDE, STAGES_WOODS, STAGES_CASTLE, STAGES_CISCOCITY, STAGES_STUDIO,
    STAGES_HALLOWEEN, STAGES_WESTERN, STAGES_ONSEN, STAGES_SNOWFESTA, STAGES_EDOTOWN, STAGES_HEAVEN,
    STAGES_TOYHOUSE, STAGES_ICELAND, STAGES_ARABIAN, STAGES_ASIA, STAGES_PLANE, STAGES_HONG, STAGES_BAY,
    STAGES_TOMO, STAGES_BOSSES, STAGES_SPACE, STAGES_TITLE, STAGES_HUB
]

STAGES_DIRECTORY : dict[str, Sequence[str]] = {
    APHelper.zero.value                 : STAGES_ZERO,
    APHelper.seaside.value              : STAGES_SEASIDE,
    APHelper.woods.value                : STAGES_WOODS,
    APHelper.castle.value               : STAGES_CASTLE,
    APHelper.ciscocity.value            : STAGES_CISCOCITY,
    APHelper.studio.value               : STAGES_STUDIO,
    APHelper.halloween.value            : STAGES_HALLOWEEN,
    APHelper.western.value              : STAGES_WESTERN,
    APHelper.onsen.value                : STAGES_ONSEN,
    APHelper.snowfesta.value            : STAGES_SNOWFESTA,
    APHelper.edotown.value              : STAGES_EDOTOWN,
    APHelper.heaven.value               : STAGES_HEAVEN,
    APHelper.toyhouse.value             : STAGES_TOYHOUSE,
    APHelper.iceland.value              : STAGES_ICELAND,
    APHelper.arabian.value              : STAGES_ARABIAN,
    APHelper.asia.value                 : STAGES_ASIA,
    APHelper.plane.value                : STAGES_PLANE,
    APHelper.hong.value                 : STAGES_HONG,
    APHelper.bay.value                  : STAGES_BAY,
    APHelper.tomo.value                 : STAGES_TOMO,
    APHelper.space.value                : STAGES_SPACE,
}