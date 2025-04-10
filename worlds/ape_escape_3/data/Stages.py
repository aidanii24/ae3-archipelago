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
    Stage.region_seaside_a.value,
    Stage.region_woods_a.value,
    Stage.region_castle_a.value,

    Stage.region_boss1.value,

    Stage.region_ciscocity_a.value,
    Stage.region_studio_a.value,
    Stage.region_halloween_a1.value,
    Stage.region_western_a.value,

    Stage.region_boss2.value,

    Stage.region_onsen_a.value,
    Stage.region_snowfesta_a.value,
    Stage.region_edotown_a.value,

    Stage.region_boss3.value,

    Stage.region_heaven_a1.value,
    Stage.region_toyhouse_a.value,
    Stage.region_iceland_a.value,
    Stage.region_arabian_a.value,

    Stage.region_boss4.value,

    Stage.region_asia_a.value,
    Stage.region_plane_a.value,
    Stage.region_hong_a.value,

    Stage.region_boss5.value,

    Stage.region_bay_a.value,
    Stage.region_tomo_a1.value,

    Stage.region_boss6.value,

    Stage.region_space_a.value,

    Stage.region_specter1.value,
    Stage.region_specter2.value
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
    Stage.region_seaside_a.value, Stage.region_seaside_b.value, Stage.region_seaside_c.value
]

STAGES_WOODS : Sequence[str] = [
    Stage.region_woods_a.value, Stage.region_woods_b.value, Stage.region_woods_c.value, Stage.region_woods_d.value
]

STAGES_CASTLE : Sequence[str] = [
    Stage.region_castle_a.value, Stage.region_castle_b.value, Stage.region_castle_c.value, Stage.region_castle_d.value, Stage.region_castle_e.value,
    Stage.region_castle_f.value
]

STAGES_CISCOCITY : Sequence[str] = [
    Stage.region_ciscocity_a.value, Stage.region_ciscocity_b.value, Stage.region_ciscocity_c.value, Stage.region_ciscocity_d.value,
    Stage.region_ciscocity_e.value
]

STAGES_STUDIO : Sequence[str] = [
    Stage.region_studio_a.value, Stage.region_studio_a1.value, Stage.region_studio_b.value, Stage.region_studio_c.value,
    Stage.region_studio_d.value, Stage.region_studio_e.value, Stage.region_studio_f.value, Stage.region_studio_g.value
]

STAGES_HALLOWEEN : Sequence[str] = [
    Stage.region_halloween_a1.value, Stage.region_halloween_a.value, Stage.region_halloween_b.value, Stage.region_halloween_c.value,
    Stage.region_halloween_c1.value, Stage.region_halloween_d.value, Stage.region_halloween_e.value, Stage.region_halloween_e.value,
    Stage.region_halloween_f.value
]

STAGES_WESTERN : Sequence[str] = [
    Stage.region_western_a.value, Stage.region_western_b.value, Stage.region_western_c.value, Stage.region_western_d.value, Stage.region_western_e.value,
    Stage.region_western_f.value
]

STAGES_ONSEN : Sequence[str] = [
    Stage.region_onsen_a.value, Stage.region_onsen_a1.value, Stage.region_onsen_a2.value, Stage.region_onsen_b.value, Stage.region_onsen_b1.value,
    Stage.region_onsen_b.value, Stage.region_onsen_b2.value, Stage.region_onsen_c.value, Stage.region_onsen_d.value, Stage.region_onsen_d1.value,
    Stage.region_onsen_e.value
]

STAGES_SNOWFESTA : Sequence[str] = [
    Stage.region_snowfesta_a.value, Stage.region_snowfesta_b.value, Stage.region_snowfesta_c.value, Stage.region_snowfesta_d.value,
    Stage.region_snowfesta_e.value, Stage.region_snowfesta_f.value, Stage.region_snowfesta_g.value
]

STAGES_EDOTOWN : Sequence[str] = [
    Stage.region_edotown_a.value, Stage.region_edotown_b1.value, Stage.region_edotown_b.value, Stage.region_edotown_c1.value,
    Stage.region_edotown_c.value, Stage.region_edotown_d.value, Stage.region_edotown_e.value, Stage.region_edotown_f.value
]

STAGES_HEAVEN : Sequence[str] = [
    Stage.region_heaven_a.value, Stage.region_heaven_a1.value, Stage.region_heaven_a2.value, Stage.region_heaven_b.value, Stage.region_heaven_c.value,
    Stage.region_heaven_d.value, Stage.region_heaven_e.value
]

STAGES_TOYHOUSE : Sequence[str] = [
    Stage.region_toyhouse_a.value, Stage.region_toyhouse_b.value, Stage.region_toyhouse_c.value, Stage.region_toyhouse_d.value,
    Stage.region_toyhouse_e.value, Stage.region_toyhouse_e1.value, Stage.region_toyhouse_f.value, Stage.region_toyhouse_g.value,
    Stage.region_toyhouse_h.value
]

STAGES_ICELAND : Sequence[str] = [
    Stage.region_iceland_a.value, Stage.region_iceland_b.value, Stage.region_iceland_c.value, Stage.region_iceland_d.value, Stage.region_iceland_e.value,
    Stage.region_iceland_f.value
]

STAGES_ARABIAN : Sequence[str] = [
    Stage.region_arabian_a.value, Stage.region_arabian_b.value, Stage.region_arabian_c.value, Stage.region_arabian_c1.value, Stage.region_arabian_e.value,
    Stage.region_arabian_e1.value, Stage.region_arabian_f.value, Stage.region_arabian_g.value
]

STAGES_ASIA : Sequence[str] = [
    Stage.region_asia_a.value, Stage.region_asia_a1.value, Stage.region_asia_a2.value, Stage.region_asia_a3.value, Stage.region_asia_a4.value,
    Stage.region_asia_a5.value, Stage.region_asia_b.value, Stage.region_asia_b1.value, Stage.region_asia_b2.value, Stage.region_asia_d.value,
    Stage.region_asia_d1.value, Stage.region_asia_d2.value, Stage.region_asia_e.value, Stage.region_asia_e1.value, Stage.region_asia_e2.value,
    Stage.region_asia_f.value
]

STAGES_PLANE : Sequence[str] = [
    Stage.region_plane_a.value, Stage.region_plane_a1.value, Stage.region_plane_b.value, Stage.region_plane_b1.value, Stage.region_plane_c.value,
    Stage.region_plane_c1.value, Stage.region_plane_d.value, Stage.region_plane_e.value, Stage.region_plane_f.value, Stage.region_plane_f1.value,
    Stage.region_plane_g.value, Stage.region_plane_h.value
]

STAGES_HONG : Sequence[str] = [
    Stage.region_hong_a.value, Stage.region_hong_a1.value, Stage.region_hong_a2.value, Stage.region_hong_b.value, Stage.region_hong_b1.value,
    Stage.region_hong_c.value, Stage.region_hong_c1.value, Stage.region_hong_c2.value, Stage.region_hong_d.value, Stage.region_hong_e.value,
    Stage.region_hong_e1.value, Stage.region_hong_f.value, Stage.region_hong_g.value, Stage.region_hong_h.value
]

STAGES_BAY : Sequence[str] = [
    Stage.region_bay_a.value, Stage.region_bay_a1.value, Stage.region_bay_a2.value, Stage.region_bay_a3.value, Stage.region_bay_a4.value,
    Stage.region_bay_a5.value, Stage.region_bay_b.value, Stage.region_bay_c.value, Stage.region_bay_d.value, Stage.region_bay_d1.value,
    Stage.region_bay_e.value, Stage.region_bay_e1.value, Stage.region_bay_e2.value, Stage.region_bay_e3.value, Stage.region_bay_f.value
]

STAGES_TOMO : Sequence[str] = [
    Stage.region_tomo_a.value, Stage.region_tomo_a1.value, Stage.region_tomo_b.value, Stage.region_tomo_c.value, Stage.region_tomo_e.value,
    Stage.region_tomo_e1.value, Stage.region_tomo_e2.value, Stage.region_tomo_f.value, Stage.region_tomo_f1.value, Stage.region_tomo_f2.value,
    Stage.region_tomo_g.value, Stage.region_tomo_g1.value, Stage.region_tomo_h.value, Stage.region_tomo_h1.value, Stage.region_tomo_i.value,
    Stage.region_tomo_j.value,
]

STAGES_SPACE : Sequence[str] = [
    Stage.region_space_a.value, Stage.region_space_b.value, Stage.region_space_d.value, Stage.region_space_e.value, Stage.region_space_e1.value,
    Stage.region_space_f.value, Stage.region_space_f1.value, Stage.region_space_f2.value, Stage.region_space_g.value, Stage.region_space_g1.value,
    Stage.region_space_g2.value, Stage.region_space_h.value, Stage.region_space_i.value, Stage.region_space_j.value, Stage.region_space_k.value,
    Stage.region_space_l.value,
]

STAGES_BOSSES : Sequence[str] = [
    Stage.region_boss1.value, Stage.region_boss2.value, Stage.region_boss3.value, Stage.region_boss4.value, Stage.region_boss5.value, Stage.region_boss6.value,
    Stage.region_specter1.value, Stage.region_specter2.value
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