from typing import Callable, Sequence
from dataclasses import dataclass

from .Strings import Stage, APHelper
from .Logic import Rulesets


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
    name : str
    parent : str
    destination : str
    rules : Rulesets

    def __init__(self, name : str, parent : str, destination : str,
                 *rules : Callable | list[Callable] | list[list[Callable]] | Rulesets | None,
                 critical : set = None):
        self.name = name
        self.parent = parent
        self.destination = destination
        self.rules = Rulesets()

        for rule in rules:
            if isinstance(rule, Rulesets):
                self.rules = rule
            else:
                self.rules = Rulesets(*rules, critical=critical)

### [< --- STAGE GROUPS --- >]
LEVELS_BY_ORDER : Sequence[str] = [
    Stage.region_seaside_a.value,
    Stage.region_woods_a.value,
    Stage.region_castle_a1.value,

    Stage.region_boss1.value,

    Stage.region_ciscocity_a.value,
    Stage.region_studio_a.value,
    Stage.region_halloween_a1.value,
    Stage.region_western_a.value,

    Stage.region_boss2.value,

    Stage.region_onsen_a.value,
    Stage.region_snowfesta_a.value,
    Stage.region_edotown_a1.value,

    Stage.region_boss3.value,

    Stage.region_heaven_a1.value,
    Stage.region_toyhouse_a.value,
    Stage.region_iceland_a1.value,
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
    Stage.region_specter2.value,

    Stage.zero.value,
]

STAGES_TITLE : Sequence[str] = [
    Stage.title_screen.value
]

STAGES_HUB : Sequence[str] = [
    Stage.travel_station_a.value,
    Stage.travel_station_b.value
]

STAGES_ZERO : Sequence[str] = [
    Stage.zero.value
]

STAGES_SEASIDE : Sequence[str] = [
    Stage.region_seaside_a.value,
    Stage.region_seaside_b.value,
    Stage.region_seaside_c.value
]

STAGES_WOODS : Sequence[str] = [
    Stage.region_woods_a.value,
    Stage.region_woods_b.value,
    Stage.region_woods_c.value,
    Stage.region_woods_d.value
]

STAGES_CASTLE : Sequence[str] = [
    Stage.region_castle_a1.value,
    Stage.region_castle_a2.value,
    Stage.region_castle_a.value,
    Stage.region_castle_b.value,
    Stage.region_castle_b1.value,
    Stage.region_castle_c.value,
    Stage.region_castle_d.value,
    Stage.region_castle_d1.value,
    Stage.region_castle_e.value,
    Stage.region_castle_f.value
]

STAGES_CISCOCITY : Sequence[str] = [
    Stage.region_ciscocity_a.value,
    Stage.region_ciscocity_b.value,
    Stage.region_ciscocity_c.value,
    Stage.region_ciscocity_c1.value,
    Stage.region_ciscocity_d.value,
    Stage.region_ciscocity_e.value
]

STAGES_STUDIO : Sequence[str] = [
    Stage.region_studio_a.value,
    Stage.region_studio_a1.value,
    Stage.region_studio_a2.value,
    Stage.region_studio_b.value,
    Stage.region_studio_b1.value,
    Stage.region_studio_b2.value,
    Stage.region_studio_c.value,
    Stage.region_studio_d.value,
    Stage.region_studio_d1.value,
    Stage.region_studio_d2.value,
    Stage.region_studio_e.value,
    Stage.region_studio_f.value,
    Stage.region_studio_f1.value,
    Stage.region_studio_g.value
]

STAGES_HALLOWEEN : Sequence[str] = [
    Stage.region_halloween_a.value,
    Stage.region_halloween_a1.value,
    Stage.region_halloween_b.value,
    Stage.region_halloween_b1.value,
    Stage.region_halloween_c.value,
    Stage.region_halloween_c1.value,
    Stage.region_halloween_c2.value,
    Stage.region_halloween_d.value,
    Stage.region_halloween_d1.value,
    Stage.region_halloween_d2.value,
    Stage.region_halloween_e.value,
    Stage.region_halloween_f.value
]

STAGES_WESTERN : Sequence[str] = [
    Stage.region_western_a.value,
    Stage.region_western_b.value,
    Stage.region_western_b1.value,
    Stage.region_western_c.value,
    Stage.region_western_d.value,
    Stage.region_western_d1.value,
    Stage.region_western_d2.value,
    Stage.region_western_d3.value,
    Stage.region_western_e.value,
    Stage.region_western_e1.value,
    Stage.region_western_f.value
]

STAGES_ONSEN : Sequence[str] = [
    Stage.region_onsen_a.value,
    Stage.region_onsen_a1.value,
    Stage.region_onsen_a2.value,
    Stage.region_onsen_b.value,
    Stage.region_onsen_b1.value,
    Stage.region_onsen_c.value,
    Stage.region_onsen_d.value,
    Stage.region_onsen_d1.value,
    Stage.region_onsen_e.value
]

STAGES_SNOWFESTA : Sequence[str] = [
    Stage.region_snowfesta_a.value,
    Stage.region_snowfesta_b.value,
    Stage.region_snowfesta_c.value,
    Stage.region_snowfesta_d.value,
    Stage.region_snowfesta_e.value,
    Stage.region_snowfesta_f.value,
    Stage.region_snowfesta_g.value
]

STAGES_EDOTOWN : Sequence[str] = [
    Stage.region_edotown_a.value,
    Stage.region_edotown_a1.value,
    Stage.region_edotown_b.value,
    Stage.region_edotown_b1.value,
    Stage.region_edotown_b2.value,
    Stage.region_edotown_c.value,
    Stage.region_edotown_c1.value,
    Stage.region_edotown_c2.value,
    Stage.region_edotown_d.value,
    Stage.region_edotown_e.value,
    Stage.region_edotown_f.value
]

STAGES_HEAVEN : Sequence[str] = [
    Stage.region_heaven_a.value,
    Stage.region_heaven_a1.value,
    Stage.region_heaven_b.value,
    Stage.region_heaven_b1.value,
    Stage.region_heaven_c.value,
    Stage.region_heaven_d.value,
    Stage.region_heaven_e.value
]

STAGES_TOYHOUSE : Sequence[str] = [
    Stage.region_toyhouse_a.value,
    Stage.region_toyhouse_b.value,
    Stage.region_toyhouse_b1.value,
    Stage.region_toyhouse_c.value,
    Stage.region_toyhouse_d.value,
    Stage.region_toyhouse_e.value,
    Stage.region_toyhouse_f.value,
    Stage.region_toyhouse_g.value,
    Stage.region_toyhouse_g1.value,
    Stage.region_toyhouse_h.value
]

STAGES_ICELAND : Sequence[str] = [
    Stage.region_iceland_a.value,
    Stage.region_iceland_a1.value,
    Stage.region_iceland_a2.value,
    Stage.region_iceland_b.value,
    Stage.region_iceland_c.value,
    Stage.region_iceland_d.value,
    Stage.region_iceland_e.value,
    Stage.region_iceland_f.value
]

STAGES_ARABIAN : Sequence[str] = [
    Stage.region_arabian_a.value,
    Stage.region_arabian_b.value,
    Stage.region_arabian_c1.value,
    Stage.region_arabian_c.value,
    Stage.region_arabian_e.value,
    Stage.region_arabian_e1.value,
    Stage.region_arabian_f.value,
    Stage.region_arabian_g.value
]

STAGES_ASIA : Sequence[str] = [
    Stage.region_asia_a.value,
    Stage.region_asia_a1.value,
    Stage.region_asia_a2.value,
    Stage.region_asia_a3.value,
    Stage.region_asia_a4.value,
    Stage.region_asia_a5.value,
    Stage.region_asia_a6.value,
    Stage.region_asia_b.value,
    Stage.region_asia_b1.value,
    Stage.region_asia_b2.value,
    Stage.region_asia_d.value,
    Stage.region_asia_d1.value,
    Stage.region_asia_d2.value,
    Stage.region_asia_e.value,
    Stage.region_asia_e1.value,
    Stage.region_asia_e2.value,
    Stage.region_asia_f.value
]

STAGES_PLANE : Sequence[str] = [
    Stage.region_plane_a.value,
    Stage.region_plane_a1.value,
    Stage.region_plane_b.value,
    Stage.region_plane_b1.value,
    Stage.region_plane_b2.value,
    Stage.region_plane_c.value,
    Stage.region_plane_c1.value,
    Stage.region_plane_d.value,
    Stage.region_plane_e.value,
    Stage.region_plane_f.value,
    Stage.region_plane_f1.value,
    Stage.region_plane_g.value,
    Stage.region_plane_h.value
]

STAGES_HONG : Sequence[str] = [
    Stage.region_hong_a.value,
    Stage.region_hong_a1.value,
    Stage.region_hong_a2.value,
    Stage.region_hong_b.value,
    Stage.region_hong_b1.value,
    Stage.region_hong_b2.value,
    Stage.region_hong_c.value,
    Stage.region_hong_c1.value,
    Stage.region_hong_c2.value,
    Stage.region_hong_d.value,
    Stage.region_hong_e.value,
    Stage.region_hong_e1.value,
    Stage.region_hong_f.value,
    Stage.region_hong_g.value,
    Stage.region_hong_h.value
]

STAGES_BAY : Sequence[str] = [
    Stage.region_bay_a.value,
    Stage.region_bay_a1.value,
    Stage.region_bay_a2.value,
    Stage.region_bay_a3.value,
    Stage.region_bay_a4.value,
    Stage.region_bay_a5.value,
    Stage.region_bay_a6.value,
    Stage.region_bay_a7.value,
    Stage.region_bay_b.value,
    Stage.region_bay_c.value,
    Stage.region_bay_c1.value,
    Stage.region_bay_d.value,
    Stage.region_bay_d1.value,
    Stage.region_bay_e.value,
    Stage.region_bay_e1.value,
    Stage.region_bay_e2.value,
    Stage.region_bay_f.value
]

STAGES_TOMO : Sequence[str] = [
    Stage.region_tomo_a.value,
    Stage.region_tomo_a1.value,
    Stage.region_tomo_b.value,
    Stage.region_tomo_c.value,
    Stage.region_tomo_e.value,
    Stage.region_tomo_e1.value,
    Stage.region_tomo_e2.value,
    Stage.region_tomo_e3.value,
    Stage.region_tomo_f.value,
    Stage.region_tomo_f1.value,
    Stage.region_tomo_f2.value,
    Stage.region_tomo_g.value,
    Stage.region_tomo_g1.value,
    Stage.region_tomo_h.value,
    Stage.region_tomo_h1.value,
    Stage.region_tomo_i.value,
    Stage.region_tomo_j.value
]

STAGES_SPACE : Sequence[str] = [
    Stage.region_space_a.value,
    Stage.region_space_b.value,
    Stage.region_space_d.value,
    Stage.region_space_e.value,
    Stage.region_space_e1.value,
    Stage.region_space_f.value,
    Stage.region_space_f1.value,
    Stage.region_space_f2.value,
    Stage.region_space_g.value,
    Stage.region_space_g1.value,
    Stage.region_space_h.value,
    Stage.region_space_i.value,
    Stage.region_space_j.value,
    Stage.region_space_j1.value,
    Stage.region_space_k.value
]

STAGES_BOSSES : Sequence[str] = [
    Stage.region_boss1.value,
    Stage.region_boss2.value,
    Stage.region_boss3.value,
    Stage.region_boss4.value,
    Stage.region_boss5.value,
    Stage.region_boss6.value,
    Stage.region_specter1.value,
    Stage.region_specter2.value
]

STAGES_BREAK_ROOMS : Sequence[str] = [
    Stage.region_seaside_c.value,
    Stage.region_woods_d.value,
    Stage.region_castle_e.value,
    Stage.region_ciscocity_e.value,
    Stage.region_studio_g.value,
    Stage.region_halloween_e.value,
    Stage.region_western_c.value,
    Stage.region_onsen_c.value,
    Stage.region_snowfesta_g.value,
    Stage.region_edotown_f.value,
    Stage.region_heaven_e.value,
    Stage.region_toyhouse_h.value,
    Stage.region_iceland_f.value,
    Stage.region_arabian_f.value,
    Stage.region_asia_f.value,
    Stage.region_plane_g.value,
    Stage.region_hong_f.value,
    Stage.region_bay_f.value,
    Stage.region_tomo_i.value,
    Stage.region_space_h.value,
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

### [< --- VANILLA ENTRANCES --- >]
ENTRANCES_MAIN : list[AE3EntranceMeta] = [
    # Seaside
    AE3EntranceMeta(Stage.entrance_seaside_ab.value, Stage.region_seaside_a.value, Stage.region_seaside_b.value),
    AE3EntranceMeta(Stage.entrance_seaside_ac.value, Stage.region_seaside_a.value, Stage.region_seaside_c.value),
    AE3EntranceMeta(Stage.entrance_seaside_ba.value, Stage.region_seaside_b.value, Stage.region_seaside_a.value),
    AE3EntranceMeta(Stage.entrance_seaside_ca.value, Stage.region_seaside_c.value, Stage.region_seaside_a.value),

    # Woods
    AE3EntranceMeta(Stage.entrance_woods_ab.value, Stage.region_woods_a.value, Stage.region_woods_b.value),
    AE3EntranceMeta(Stage.entrance_woods_ad.value, Stage.region_woods_a.value, Stage.region_woods_d.value),
    AE3EntranceMeta(Stage.entrance_woods_ba.value, Stage.region_woods_b.value, Stage.region_woods_a.value),
    AE3EntranceMeta(Stage.entrance_woods_bc.value, Stage.region_woods_b.value, Stage.region_woods_c.value),
    AE3EntranceMeta(Stage.entrance_woods_cb.value, Stage.region_woods_c.value, Stage.region_woods_b.value),
    AE3EntranceMeta(Stage.entrance_woods_da.value, Stage.region_woods_d.value, Stage.region_woods_a.value),

    # Castle
    AE3EntranceMeta(Stage.entrance_castle_ad.value, Stage.region_castle_a.value, Stage.region_castle_d.value),
    AE3EntranceMeta(Stage.entrance_castle_a2b.value, Stage.region_castle_a2.value,Stage.region_castle_b.value),
    AE3EntranceMeta(Stage.entrance_castle_da.value, Stage.region_castle_d.value, Stage.region_castle_a.value),
    AE3EntranceMeta(Stage.entrance_castle_d1b.value, Stage.region_castle_d1.value, Stage.region_castle_b.value),
    AE3EntranceMeta(Stage.entrance_castle_ba2.value, Stage.region_castle_b.value, Stage.region_castle_a2.value),
    AE3EntranceMeta(Stage.entrance_castle_bd1.value, Stage.region_castle_b.value, Stage.region_castle_d1.value),
    AE3EntranceMeta(Stage.entrance_castle_be.value, Stage.region_castle_b.value, Stage.region_castle_e.value),
    AE3EntranceMeta(Stage.entrance_castle_b1c.value, Stage.region_castle_b1.value, Stage.region_castle_c.value),
    AE3EntranceMeta(Stage.entrance_castle_cb1.value, Stage.region_castle_c.value, Stage.region_castle_b1.value),
    AE3EntranceMeta(Stage.entrance_castle_eb.value, Stage.region_castle_e.value, Stage.region_castle_b.value),
    AE3EntranceMeta(Stage.entrance_castle_ef.value, Stage.region_castle_e.value, Stage.region_castle_f.value),
    AE3EntranceMeta(Stage.entrance_castle_fe.value, Stage.region_castle_f.value, Stage.region_castle_e.value),

    # Ciscocity
    AE3EntranceMeta(Stage.entrance_ciscocity_ac1.value, Stage.region_ciscocity_a.value,
                    Stage.region_ciscocity_c1.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_ab.value, Stage.region_ciscocity_a.value, Stage.region_ciscocity_b.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_ad.value, Stage.region_ciscocity_a.value, Stage.region_ciscocity_d.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_ad_2.value, Stage.region_ciscocity_a.value,
                    Stage.region_ciscocity_d.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_c1a.value, Stage.region_ciscocity_c1.value,
                    Stage.region_ciscocity_a.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_ce.value, Stage.region_ciscocity_c.value, Stage.region_ciscocity_e.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_ec.value, Stage.region_ciscocity_e.value, Stage.region_ciscocity_c.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_ba.value, Stage.region_ciscocity_b.value, Stage.region_ciscocity_a.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_da.value, Stage.region_ciscocity_d.value, Stage.region_ciscocity_a.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_da_2.value, Stage.region_ciscocity_d.value,
                    Stage.region_ciscocity_a.value),

    # Studio
    AE3EntranceMeta(Stage.entrance_studio_ab1.value, Stage.region_studio_a.value, Stage.region_studio_b1.value),
    AE3EntranceMeta(Stage.entrance_studio_ae.value, Stage.region_studio_a.value, Stage.region_studio_e.value),
    AE3EntranceMeta(Stage.entrance_studio_a2c.value, Stage.region_studio_a2.value, Stage.region_studio_c.value),
    AE3EntranceMeta(Stage.entrance_studio_a1d2.value, Stage.region_studio_a1.value, Stage.region_studio_d2.value),
    AE3EntranceMeta(Stage.entrance_studio_b1a.value, Stage.region_studio_b1.value, Stage.region_studio_a.value),
    AE3EntranceMeta(Stage.entrance_studio_bf.value, Stage.region_studio_b.value, Stage.region_studio_f.value),
    AE3EntranceMeta(Stage.entrance_studio_fb.value, Stage.region_studio_f.value, Stage.region_studio_b.value),
    AE3EntranceMeta(Stage.entrance_studio_f1d1.value, Stage.region_studio_f1.value, Stage.region_studio_d1.value),
    AE3EntranceMeta(Stage.entrance_studio_d1f1.value, Stage.region_studio_d1.value, Stage.region_studio_f1.value),
    AE3EntranceMeta(Stage.entrance_studio_dg.value, Stage.region_studio_d.value, Stage.region_studio_g.value),
    AE3EntranceMeta(Stage.entrance_studio_d2a1.value, Stage.region_studio_d2.value, Stage.region_studio_a1.value),
    AE3EntranceMeta(Stage.entrance_studio_gd.value, Stage.region_studio_g.value, Stage.region_studio_d.value),
    AE3EntranceMeta(Stage.entrance_studio_ea.value, Stage.region_studio_e.value, Stage.region_studio_a.value),
    AE3EntranceMeta(Stage.entrance_studio_ec.value, Stage.region_studio_e.value, Stage.region_studio_c.value),
    AE3EntranceMeta(Stage.entrance_studio_ce.value, Stage.region_studio_c.value, Stage.region_studio_e.value),
    AE3EntranceMeta(Stage.entrance_studio_ca2.value, Stage.region_studio_c.value, Stage.region_studio_a2.value),

    # Halloween
    AE3EntranceMeta(Stage.entrance_halloween_ab.value, Stage.region_halloween_a.value, Stage.region_halloween_b.value),
    AE3EntranceMeta(Stage.entrance_halloween_ba.value, Stage.region_halloween_b.value, Stage.region_halloween_a.value),
    AE3EntranceMeta(Stage.entrance_halloween_b1f.value, Stage.region_halloween_b1.value,
                    Stage.region_halloween_f.value),
    AE3EntranceMeta(Stage.entrance_halloween_fb1.value, Stage.region_halloween_f.value,
                    Stage.region_halloween_b1.value),
    AE3EntranceMeta(Stage.entrance_halloween_fc1.value, Stage.region_halloween_f.value,
                    Stage.region_halloween_c1.value),
    AE3EntranceMeta(Stage.entrance_halloween_c1f.value, Stage.region_halloween_c1.value,
                    Stage.region_halloween_f.value),
    AE3EntranceMeta(Stage.entrance_halloween_c2d1.value, Stage.region_halloween_c2.value,
                    Stage.region_halloween_d1.value),
    AE3EntranceMeta(Stage.entrance_halloween_dc2.value, Stage.region_halloween_d.value,
                    Stage.region_halloween_c2.value),
    AE3EntranceMeta(Stage.entrance_halloween_d1e.value, Stage.region_halloween_d1.value,
                    Stage.region_halloween_e.value),
    AE3EntranceMeta(Stage.entrance_halloween_ed1.value, Stage.region_halloween_e.value,
                    Stage.region_halloween_d1.value),

    # Western
    AE3EntranceMeta(Stage.entrance_western_ab.value, Stage.region_western_a.value, Stage.region_western_b.value),
    AE3EntranceMeta(Stage.entrance_western_af.value, Stage.region_western_a.value, Stage.region_western_f.value),
    AE3EntranceMeta(Stage.entrance_western_ba.value, Stage.region_western_b.value, Stage.region_western_a.value),
    AE3EntranceMeta(Stage.entrance_western_fa.value, Stage.region_western_f.value, Stage.region_western_a.value),
    AE3EntranceMeta(Stage.entrance_western_fd2.value, Stage.region_western_f.value, Stage.region_western_d2.value),
    AE3EntranceMeta(Stage.entrance_western_de.value, Stage.region_western_d.value, Stage.region_western_e.value),
    AE3EntranceMeta(Stage.entrance_western_d1f.value, Stage.region_western_d1.value, Stage.region_western_f.value),
    AE3EntranceMeta(Stage.entrance_western_ed1.value, Stage.region_western_e.value, Stage.region_western_d1.value),
    AE3EntranceMeta(Stage.entrance_western_ec.value, Stage.region_western_e.value, Stage.region_western_c.value),
    AE3EntranceMeta(Stage.entrance_western_cf.value, Stage.region_western_c.value, Stage.region_western_f.value),

    # Onsen
    AE3EntranceMeta(Stage.entrance_onsen_a1b1.value, Stage.region_onsen_a1.value, Stage.region_onsen_b1.value),
    AE3EntranceMeta(Stage.entrance_onsen_a2b1.value, Stage.region_onsen_a2.value, Stage.region_onsen_b1.value),
    AE3EntranceMeta(Stage.entrance_onsen_b1a1.value, Stage.region_onsen_b1.value, Stage.region_onsen_a1.value),
    AE3EntranceMeta(Stage.entrance_onsen_b1a2.value, Stage.region_onsen_b1.value, Stage.region_onsen_a2.value),
    AE3EntranceMeta(Stage.entrance_onsen_be_2.value, Stage.region_onsen_b.value, Stage.region_onsen_e.value),
    AE3EntranceMeta(Stage.entrance_onsen_bd1.value, Stage.region_onsen_b.value, Stage.region_onsen_d1.value),
    AE3EntranceMeta(Stage.entrance_onsen_bd.value, Stage.region_onsen_b.value, Stage.region_onsen_d.value),
    AE3EntranceMeta(Stage.entrance_onsen_be.value, Stage.region_onsen_b.value, Stage.region_onsen_e.value),
    AE3EntranceMeta(Stage.entrance_onsen_d1b.value, Stage.region_onsen_d1.value, Stage.region_onsen_b.value),
    AE3EntranceMeta(Stage.entrance_onsen_db.value, Stage.region_onsen_d.value, Stage.region_onsen_b.value),
    AE3EntranceMeta(Stage.entrance_onsen_dc.value, Stage.region_onsen_d.value, Stage.region_onsen_c.value),
    AE3EntranceMeta(Stage.entrance_onsen_cd.value, Stage.region_onsen_c.value, Stage.region_onsen_d.value),
    AE3EntranceMeta(Stage.entrance_onsen_eb.value, Stage.region_onsen_e.value, Stage.region_onsen_b.value),
    AE3EntranceMeta(Stage.entrance_onsen_eb_2.value, Stage.region_onsen_e.value, Stage.region_onsen_b.value),

    # Snowfesta
    AE3EntranceMeta(Stage.entrance_snowfesta_ab.value, Stage.region_snowfesta_a.value, Stage.region_snowfesta_b.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_ag.value, Stage.region_snowfesta_a.value, Stage.region_snowfesta_g.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_ac.value, Stage.region_snowfesta_a.value, Stage.region_snowfesta_c.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_ba.value, Stage.region_snowfesta_b.value, Stage.region_snowfesta_a.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_ga.value, Stage.region_snowfesta_g.value, Stage.region_snowfesta_a.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_gd.value, Stage.region_snowfesta_g.value, Stage.region_snowfesta_d.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_dg.value, Stage.region_snowfesta_d.value, Stage.region_snowfesta_g.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_ca.value, Stage.region_snowfesta_c.value, Stage.region_snowfesta_a.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_cf.value, Stage.region_snowfesta_c.value, Stage.region_snowfesta_f.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_ce.value, Stage.region_snowfesta_c.value, Stage.region_snowfesta_e.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_ce_2.value, Stage.region_snowfesta_c.value,
                    Stage.region_snowfesta_e.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_fc.value, Stage.region_snowfesta_f.value, Stage.region_snowfesta_c.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_ec.value, Stage.region_snowfesta_e.value, Stage.region_snowfesta_c.value),
    AE3EntranceMeta(Stage.entrance_snowfesta_ec_2.value, Stage.region_snowfesta_e.value,
                    Stage.region_snowfesta_c.value),

    # Edotown
    AE3EntranceMeta(Stage.entrance_edotown_ab1.value, Stage.region_edotown_a.value, Stage.region_edotown_b1.value),
    AE3EntranceMeta(Stage.entrance_edotown_b1a.value, Stage.region_edotown_b1.value, Stage.region_edotown_a.value),
    AE3EntranceMeta(Stage.entrance_edotown_be.value, Stage.region_edotown_b.value, Stage.region_edotown_e.value),
    AE3EntranceMeta(Stage.entrance_edotown_c1b.value, Stage.region_edotown_c1.value, Stage.region_edotown_b.value),
    AE3EntranceMeta(Stage.entrance_edotown_c2d.value, Stage.region_edotown_c2.value, Stage.region_edotown_d.value),
    AE3EntranceMeta(Stage.entrance_edotown_dc2.value, Stage.region_edotown_d.value, Stage.region_edotown_c2.value),
    AE3EntranceMeta(Stage.entrance_edotown_de.value, Stage.region_edotown_d.value, Stage.region_edotown_e.value),
    AE3EntranceMeta(Stage.entrance_edotown_df.value, Stage.region_edotown_d.value, Stage.region_edotown_f.value),
    AE3EntranceMeta(Stage.entrance_edotown_fd.value, Stage.region_edotown_f.value, Stage.region_edotown_d.value),
    AE3EntranceMeta(Stage.entrance_edotown_ed.value, Stage.region_edotown_e.value, Stage.region_edotown_d.value),
    AE3EntranceMeta(Stage.entrance_edotown_eb.value, Stage.region_edotown_e.value, Stage.region_edotown_b.value),

    # Heaven
    AE3EntranceMeta(Stage.entrance_heaven_ab.value, Stage.region_heaven_a.value, Stage.region_heaven_b.value),
    AE3EntranceMeta(Stage.entrance_heaven_ba.value, Stage.region_heaven_b.value, Stage.region_heaven_a.value),
    AE3EntranceMeta(Stage.entrance_heaven_b1c.value, Stage.region_heaven_b1.value, Stage.region_heaven_c.value),
    AE3EntranceMeta(Stage.entrance_heaven_cb1.value, Stage.region_heaven_c.value, Stage.region_heaven_b1.value),
    AE3EntranceMeta(Stage.entrance_heaven_ce.value, Stage.region_heaven_c.value, Stage.region_heaven_e.value),
    AE3EntranceMeta(Stage.entrance_heaven_cd.value, Stage.region_heaven_c.value, Stage.region_heaven_d.value),
    AE3EntranceMeta(Stage.entrance_heaven_ec.value, Stage.region_heaven_e.value, Stage.region_heaven_c.value),
    AE3EntranceMeta(Stage.entrance_heaven_dc.value, Stage.region_heaven_d.value, Stage.region_heaven_c.value),

    # Toyhouse
    AE3EntranceMeta(Stage.entrance_toyhouse_ab.value, Stage.region_toyhouse_a.value, Stage.region_toyhouse_b.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_ad.value, Stage.region_toyhouse_a.value, Stage.region_toyhouse_d.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_ag.value, Stage.region_toyhouse_a.value, Stage.region_toyhouse_g.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_ae.value, Stage.region_toyhouse_a.value, Stage.region_toyhouse_e.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_ac.value, Stage.region_toyhouse_a.value, Stage.region_toyhouse_c.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_ba.value, Stage.region_toyhouse_b.value, Stage.region_toyhouse_a.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_da.value, Stage.region_toyhouse_d.value, Stage.region_toyhouse_a.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_dh.value, Stage.region_toyhouse_d.value, Stage.region_toyhouse_h.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_hd.value, Stage.region_toyhouse_h.value, Stage.region_toyhouse_d.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_ga.value, Stage.region_toyhouse_g.value, Stage.region_toyhouse_a.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_g1a.value, Stage.region_toyhouse_g1.value, Stage.region_toyhouse_a.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_ea.value, Stage.region_toyhouse_e.value, Stage.region_toyhouse_a.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_ef.value, Stage.region_toyhouse_e.value, Stage.region_toyhouse_f.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_fe.value, Stage.region_toyhouse_f.value, Stage.region_toyhouse_e.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_fa.value, Stage.region_toyhouse_f.value, Stage.region_toyhouse_a.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_ca.value, Stage.region_toyhouse_c.value, Stage.region_toyhouse_a.value),

    # Iceland
    AE3EntranceMeta(Stage.entrance_iceland_ad.value, Stage.region_iceland_a.value, Stage.region_iceland_d.value),
    AE3EntranceMeta(Stage.entrance_iceland_a2e.value, Stage.region_iceland_a2.value, Stage.region_iceland_e.value),
    AE3EntranceMeta(Stage.entrance_iceland_da.value, Stage.region_iceland_d.value, Stage.region_iceland_a.value),
    AE3EntranceMeta(Stage.entrance_iceland_dc.value, Stage.region_iceland_d.value, Stage.region_iceland_c.value),
    AE3EntranceMeta(Stage.entrance_iceland_cd.value, Stage.region_iceland_c.value, Stage.region_iceland_d.value),
    AE3EntranceMeta(Stage.entrance_iceland_cb.value, Stage.region_iceland_c.value, Stage.region_iceland_b.value),
    AE3EntranceMeta(Stage.entrance_iceland_bc.value, Stage.region_iceland_b.value, Stage.region_iceland_c.value),
    AE3EntranceMeta(Stage.entrance_iceland_be.value, Stage.region_iceland_b.value, Stage.region_iceland_e.value),
    AE3EntranceMeta(Stage.entrance_iceland_eb.value, Stage.region_iceland_e.value, Stage.region_iceland_b.value),
    AE3EntranceMeta(Stage.entrance_iceland_ef.value, Stage.region_iceland_e.value, Stage.region_iceland_f.value),
    AE3EntranceMeta(Stage.entrance_iceland_ea2.value, Stage.region_iceland_e.value, Stage.region_iceland_a2.value),

    # Arabian
    AE3EntranceMeta(Stage.entrance_arabian_ac.value, Stage.region_arabian_a.value, Stage.region_arabian_c.value),
    AE3EntranceMeta(Stage.entrance_arabian_ac1.value, Stage.region_arabian_a.value, Stage.region_arabian_c1.value),
    AE3EntranceMeta(Stage.entrance_arabian_ab.value, Stage.region_arabian_a.value, Stage.region_arabian_b.value),
    AE3EntranceMeta(Stage.entrance_arabian_ca.value, Stage.region_arabian_c.value, Stage.region_arabian_a.value),
    AE3EntranceMeta(Stage.entrance_arabian_c1a.value, Stage.region_arabian_c1.value, Stage.region_arabian_a.value),
    AE3EntranceMeta(Stage.entrance_arabian_ba.value, Stage.region_arabian_b.value, Stage.region_arabian_a.value),
    AE3EntranceMeta(Stage.entrance_arabian_bg.value, Stage.region_arabian_b.value, Stage.region_arabian_g.value),
    AE3EntranceMeta(Stage.entrance_arabian_bf.value, Stage.region_arabian_b.value, Stage.region_arabian_f.value),
    AE3EntranceMeta(Stage.entrance_arabian_be1.value, Stage.region_arabian_b.value, Stage.region_arabian_e1.value),
    AE3EntranceMeta(Stage.entrance_arabian_fb.value, Stage.region_arabian_f.value, Stage.region_arabian_b.value),
    AE3EntranceMeta(Stage.entrance_arabian_e1b.value, Stage.region_arabian_e1.value, Stage.region_arabian_b.value),
    AE3EntranceMeta(Stage.entrance_arabian_eg.value, Stage.region_arabian_e.value, Stage.region_arabian_g.value),
    AE3EntranceMeta(Stage.entrance_arabian_ge.value, Stage.region_arabian_g.value, Stage.region_arabian_e.value),
    AE3EntranceMeta(Stage.entrance_arabian_gb.value, Stage.region_arabian_g.value, Stage.region_arabian_b.value),

    # Asia
    AE3EntranceMeta(Stage.entrance_asia_ab.value, Stage.region_asia_a.value, Stage.region_asia_b.value),
    AE3EntranceMeta(Stage.entrance_asia_a1b1.value, Stage.region_asia_a1.value, Stage.region_asia_b1.value),
    AE3EntranceMeta(Stage.entrance_asia_a2d2.value, Stage.region_asia_a2.value, Stage.region_asia_d2.value),
    AE3EntranceMeta(Stage.entrance_asia_a3e.value, Stage.region_asia_a3.value, Stage.region_asia_e.value),
    AE3EntranceMeta(Stage.entrance_asia_a4d1.value, Stage.region_asia_a4.value, Stage.region_asia_d1.value),
    AE3EntranceMeta(Stage.entrance_asia_ba.value, Stage.region_asia_b.value, Stage.region_asia_a.value),
    AE3EntranceMeta(Stage.entrance_asia_b2a2.value, Stage.region_asia_b2.value, Stage.region_asia_a2.value),
    AE3EntranceMeta(Stage.entrance_asia_d1a4.value, Stage.region_asia_d1.value, Stage.region_asia_a4.value),
    AE3EntranceMeta(Stage.entrance_asia_d2a2.value, Stage.region_asia_d2.value, Stage.region_asia_a2.value),
    AE3EntranceMeta(Stage.entrance_asia_ea3.value, Stage.region_asia_e.value, Stage.region_asia_a3.value),
    AE3EntranceMeta(Stage.entrance_asia_ef.value, Stage.region_asia_e.value, Stage.region_asia_f.value),
    AE3EntranceMeta(Stage.entrance_asia_fe.value, Stage.region_asia_f.value, Stage.region_asia_e.value),
    AE3EntranceMeta(Stage.entrance_asia_e2a5.value, Stage.region_asia_e2.value, Stage.region_asia_a5.value),

    # Plane
    AE3EntranceMeta(Stage.entrance_plane_ac.value, Stage.region_plane_a.value, Stage.region_plane_c.value),
    AE3EntranceMeta(Stage.entrance_plane_ca.value, Stage.region_plane_c.value, Stage.region_plane_a.value),
    AE3EntranceMeta(Stage.entrance_plane_cg.value, Stage.region_plane_c.value, Stage.region_plane_g.value),
    AE3EntranceMeta(Stage.entrance_plane_gc.value, Stage.region_plane_g.value, Stage.region_plane_c.value),
    AE3EntranceMeta(Stage.entrance_plane_c1d.value, Stage.region_plane_c1.value, Stage.region_plane_d.value),
    AE3EntranceMeta(Stage.entrance_plane_dc1.value, Stage.region_plane_d.value, Stage.region_plane_c1.value),
    AE3EntranceMeta(Stage.entrance_plane_de.value, Stage.region_plane_d.value, Stage.region_plane_e.value),
    AE3EntranceMeta(Stage.entrance_plane_ed.value, Stage.region_plane_e.value, Stage.region_plane_d.value),
    AE3EntranceMeta(Stage.entrance_plane_ef.value, Stage.region_plane_e.value, Stage.region_plane_f.value),
    AE3EntranceMeta(Stage.entrance_plane_fe.value, Stage.region_plane_f.value, Stage.region_plane_e.value),
    AE3EntranceMeta(Stage.entrance_plane_fb.value, Stage.region_plane_f.value, Stage.region_plane_b.value),
    AE3EntranceMeta(Stage.entrance_plane_bf.value, Stage.region_plane_b.value, Stage.region_plane_f.value),
    AE3EntranceMeta(Stage.entrance_plane_bh.value, Stage.region_plane_b.value, Stage.region_plane_h.value),
    AE3EntranceMeta(Stage.entrance_plane_b1h.value, Stage.region_plane_b1.value, Stage.region_plane_h.value),
    AE3EntranceMeta(Stage.entrance_plane_b2f1.value, Stage.region_plane_b2.value, Stage.region_plane_f1.value),
    AE3EntranceMeta(Stage.entrance_plane_f1b1.value, Stage.region_plane_f1.value, Stage.region_plane_b1.value),
    AE3EntranceMeta(Stage.entrance_plane_hb.value, Stage.region_plane_h.value, Stage.region_plane_b.value),
    AE3EntranceMeta(Stage.entrance_plane_hb1.value, Stage.region_plane_h.value, Stage.region_plane_b1.value),

    # Hong
    AE3EntranceMeta(Stage.entrance_hong_a2b.value, Stage.region_hong_a2.value, Stage.region_hong_b.value),
    AE3EntranceMeta(Stage.entrance_hong_ba2.value, Stage.region_hong_b.value, Stage.region_hong_a2.value),
    AE3EntranceMeta(Stage.entrance_hong_b1f.value, Stage.region_hong_b1.value, Stage.region_hong_f.value),
    AE3EntranceMeta(Stage.entrance_hong_b1c.value, Stage.region_hong_b1.value, Stage.region_hong_c.value),
    AE3EntranceMeta(Stage.entrance_hong_b2d.value, Stage.region_hong_b2.value, Stage.region_hong_d.value),
    AE3EntranceMeta(Stage.entrance_hong_fb1.value, Stage.region_hong_f.value, Stage.region_hong_b1.value),
    AE3EntranceMeta(Stage.entrance_hong_cb1.value, Stage.region_hong_c.value, Stage.region_hong_b1.value),
    AE3EntranceMeta(Stage.entrance_hong_ce.value, Stage.region_hong_c.value, Stage.region_hong_e.value),
    AE3EntranceMeta(Stage.entrance_hong_cd.value, Stage.region_hong_c.value, Stage.region_hong_d.value),
    AE3EntranceMeta(Stage.entrance_hong_ch.value, Stage.region_hong_c.value, Stage.region_hong_h.value),
    AE3EntranceMeta(Stage.entrance_hong_hc.value, Stage.region_hong_h.value, Stage.region_hong_c.value),
    AE3EntranceMeta(Stage.entrance_hong_ec.value, Stage.region_hong_e.value, Stage.region_hong_c.value),
    AE3EntranceMeta(Stage.entrance_hong_dc.value, Stage.region_hong_d.value, Stage.region_hong_c.value),
    AE3EntranceMeta(Stage.entrance_hong_dg.value, Stage.region_hong_d.value, Stage.region_hong_g.value),
    AE3EntranceMeta(Stage.entrance_hong_eb2.value, Stage.region_hong_e.value, Stage.region_hong_b2.value),
    AE3EntranceMeta(Stage.entrance_hong_gd.value, Stage.region_hong_g.value, Stage.region_hong_d.value),

    # Bay
    AE3EntranceMeta(Stage.entrance_bay_a1b.value, Stage.region_bay_a1.value, Stage.region_bay_b.value),
    AE3EntranceMeta(Stage.entrance_bay_a2e.value, Stage.region_bay_a2.value, Stage.region_bay_e.value),
    AE3EntranceMeta(Stage.entrance_bay_a3c.value, Stage.region_bay_a3.value, Stage.region_bay_c.value),
    AE3EntranceMeta(Stage.entrance_bay_a4d1.value, Stage.region_bay_a4.value, Stage.region_bay_d1.value),
    AE3EntranceMeta(Stage.entrance_bay_a6f.value, Stage.region_bay_a6.value, Stage.region_bay_f.value),
    AE3EntranceMeta(Stage.entrance_bay_ba1.value, Stage.region_bay_b.value, Stage.region_bay_a1.value),
    AE3EntranceMeta(Stage.entrance_bay_ca3.value, Stage.region_bay_c.value, Stage.region_bay_a3.value),
    AE3EntranceMeta(Stage.entrance_bay_c1a7.value, Stage.region_bay_c1.value, Stage.region_bay_a7.value),
    AE3EntranceMeta(Stage.entrance_bay_d1a4.value, Stage.region_bay_d1.value, Stage.region_bay_a4.value),
    AE3EntranceMeta(Stage.entrance_bay_ea2.value, Stage.region_bay_e.value, Stage.region_bay_a2.value),
    AE3EntranceMeta(Stage.entrance_bay_fa6.value, Stage.region_bay_f.value, Stage.region_bay_a6.value),

    # Tomo
    AE3EntranceMeta(Stage.entrance_tomo_aj.value, Stage.region_tomo_a.value, Stage.region_tomo_j.value),
    AE3EntranceMeta(Stage.entrance_tomo_ja.value, Stage.region_tomo_j.value, Stage.region_tomo_a.value),
    AE3EntranceMeta(Stage.entrance_tomo_jb.value, Stage.region_tomo_j.value, Stage.region_tomo_b.value),
    AE3EntranceMeta(Stage.entrance_tomo_bj.value, Stage.region_tomo_b.value, Stage.region_tomo_j.value),
    AE3EntranceMeta(Stage.entrance_tomo_bc.value, Stage.region_tomo_b.value, Stage.region_tomo_c.value),
    AE3EntranceMeta(Stage.entrance_tomo_cb.value, Stage.region_tomo_c.value, Stage.region_tomo_b.value),
    AE3EntranceMeta(Stage.entrance_tomo_ce.value, Stage.region_tomo_c.value, Stage.region_tomo_e.value),
    AE3EntranceMeta(Stage.entrance_tomo_ec.value, Stage.region_tomo_e.value, Stage.region_tomo_c.value),
    AE3EntranceMeta(Stage.entrance_tomo_e1i.value, Stage.region_tomo_e1.value, Stage.region_tomo_i.value),
    AE3EntranceMeta(Stage.entrance_tomo_e3f1.value, Stage.region_tomo_e3.value, Stage.region_tomo_f1.value),
    AE3EntranceMeta(Stage.entrance_tomo_f1e3.value, Stage.region_tomo_f1.value, Stage.region_tomo_e3.value),
    AE3EntranceMeta(Stage.entrance_tomo_f2g.value, Stage.region_tomo_f2.value, Stage.region_tomo_g.value),
    AE3EntranceMeta(Stage.entrance_tomo_fg1.value, Stage.region_tomo_f.value, Stage.region_tomo_g1.value),
    AE3EntranceMeta(Stage.entrance_tomo_fh1.value, Stage.region_tomo_f.value, Stage.region_tomo_h1.value),
    AE3EntranceMeta(Stage.entrance_tomo_gf2.value, Stage.region_tomo_g.value, Stage.region_tomo_f2.value),
    AE3EntranceMeta(Stage.entrance_tomo_g1f.value, Stage.region_tomo_g1.value, Stage.region_tomo_f.value),
    AE3EntranceMeta(Stage.entrance_tomo_h1f.value, Stage.region_tomo_h1.value, Stage.region_tomo_f.value),
    AE3EntranceMeta(Stage.entrance_tomo_ha.value, Stage.region_tomo_h.value, Stage.travel_station_a.value),
    AE3EntranceMeta(Stage.entrance_tomo_ie1.value, Stage.region_tomo_i.value, Stage.region_tomo_e1.value),

    # Space
    AE3EntranceMeta(Stage.entrance_space_ab.value, Stage.region_space_a.value, Stage.region_space_b.value),
    AE3EntranceMeta(Stage.entrance_space_ba.value, Stage.region_space_b.value, Stage.region_space_a.value),
    AE3EntranceMeta(Stage.entrance_space_be1.value, Stage.region_space_b.value, Stage.region_space_e1.value),
    AE3EntranceMeta(Stage.entrance_space_bg.value, Stage.region_space_b.value, Stage.region_space_g.value),
    AE3EntranceMeta(Stage.entrance_space_bf.value, Stage.region_space_b.value, Stage.region_space_f.value),
    AE3EntranceMeta(Stage.entrance_space_bd.value, Stage.region_space_b.value, Stage.region_space_d.value),
    AE3EntranceMeta(Stage.entrance_space_bi.value, Stage.region_space_b.value, Stage.region_space_i.value),
    AE3EntranceMeta(Stage.entrance_space_e1b.value, Stage.region_space_e1.value, Stage.region_space_b.value),
    AE3EntranceMeta(Stage.entrance_space_eh.value, Stage.region_space_e.value, Stage.region_space_h.value),
    AE3EntranceMeta(Stage.entrance_space_gb.value, Stage.region_space_g.value, Stage.region_space_g1.value),
    AE3EntranceMeta(Stage.entrance_space_fb.value, Stage.region_space_f.value, Stage.region_space_b.value),
    AE3EntranceMeta(Stage.entrance_space_db.value, Stage.region_space_d.value, Stage.region_space_b.value),
    AE3EntranceMeta(Stage.entrance_space_ib.value, Stage.region_space_i.value, Stage.region_space_b.value),
    AE3EntranceMeta(Stage.entrance_space_ij.value, Stage.region_space_i.value, Stage.region_space_j.value),
    AE3EntranceMeta(Stage.entrance_space_ji.value, Stage.region_space_j.value, Stage.region_space_i.value),
    AE3EntranceMeta(Stage.entrance_space_j1a.value, Stage.region_space_j1.value, Stage.travel_station_a.value),
    AE3EntranceMeta(Stage.entrance_space_he.value, Stage.region_space_h.value, Stage.region_space_e.value),
    AE3EntranceMeta(Stage.entrance_space_hk.value, Stage.region_space_h.value, Stage.region_space_k.value),
    AE3EntranceMeta(Stage.entrance_space_kh.value, Stage.region_space_k.value, Stage.region_space_h.value)
]

## Entrances between subregions (Regions within the same Room/Stage)
ENTRANCES_SUBREGIONS : list[AE3EntranceMeta] = [
    # Preliminary
    AE3EntranceMeta(Stage.entrance_ng.value, Stage.title_screen.value, Stage.zero.value),
    AE3EntranceMeta(Stage.entrance_tutorial_clear.value, Stage.title_screen.value, Stage.travel_station_a.value),
    AE3EntranceMeta(Stage.entrance_continue.value, Stage.zero.value, Stage.travel_station_a.value),

    AE3EntranceMeta(Stage.entrance_travel_ab.value, Stage.travel_station_a.value, Stage.travel_station_b.value),
    AE3EntranceMeta(Stage.entrance_travel_ba.value, Stage.travel_station_b.value, Stage.travel_station_a.value),

    # Castle
    AE3EntranceMeta(Stage.entrance_castle_aa2.value, Stage.region_castle_a.value, Stage.region_castle_a2.value),
    AE3EntranceMeta(Stage.entrance_castle_a2a.value, Stage.region_castle_a2.value, Stage.region_castle_a.value),
    AE3EntranceMeta(Stage.entrance_castle_a1a.value, Stage.region_castle_a1.value, Stage.region_castle_a.value),
    AE3EntranceMeta(Stage.entrance_castle_aa1.value, Stage.region_castle_a.value, Stage.region_castle_a1.value),
    AE3EntranceMeta(Stage.entrance_castle_dd1.value, Stage.region_castle_d.value, Stage.region_castle_d1.value),
    AE3EntranceMeta(Stage.entrance_castle_d1d.value, Stage.region_castle_d1.value, Stage.region_castle_d.value),
    AE3EntranceMeta(Stage.entrance_castle_bb1.value, Stage.region_castle_b.value, Stage.region_castle_b1.value),
    AE3EntranceMeta(Stage.entrance_castle_b1b.value, Stage.region_castle_b1.value, Stage.region_castle_b.value),

    # Ciscocity
    AE3EntranceMeta(Stage.entrance_ciscocity_c1c.value, Stage.region_ciscocity_c1.value,
                    Stage.region_ciscocity_c.value),
    AE3EntranceMeta(Stage.entrance_ciscocity_cc1.value, Stage.region_ciscocity_c.value,
                    Stage.region_ciscocity_c1.value),

    # Studio
    AE3EntranceMeta(Stage.entrance_studio_aa2.value, Stage.region_studio_a.value, Stage.region_studio_a2.value),
    AE3EntranceMeta(Stage.entrance_studio_aa1.value, Stage.region_studio_a.value, Stage.region_studio_a1.value),
    AE3EntranceMeta(Stage.entrance_studio_a2a.value, Stage.region_studio_a2.value, Stage.region_studio_a.value),
    AE3EntranceMeta(Stage.entrance_studio_a1a.value, Stage.region_studio_a1.value, Stage.region_studio_a.value),
    AE3EntranceMeta(Stage.entrance_studio_b1b2.value, Stage.region_studio_b1.value, Stage.region_studio_b2.value),
    AE3EntranceMeta(Stage.entrance_studio_b2b1.value, Stage.region_studio_b2.value, Stage.region_studio_b1.value),
    AE3EntranceMeta(Stage.entrance_studio_b2b.value, Stage.region_studio_b2.value, Stage.region_studio_b.value),
    AE3EntranceMeta(Stage.entrance_studio_bb2.value, Stage.region_studio_b.value, Stage.region_studio_b2.value),
    AE3EntranceMeta(Stage.entrance_studio_ff1.value, Stage.region_studio_f.value, Stage.region_studio_f1.value),
    AE3EntranceMeta(Stage.entrance_studio_f1f.value, Stage.region_studio_f1.value, Stage.region_studio_f.value),
    AE3EntranceMeta(Stage.entrance_studio_d1d.value, Stage.region_studio_d1.value, Stage.region_studio_d.value),
    AE3EntranceMeta(Stage.entrance_studio_dd1.value, Stage.region_studio_d.value, Stage.region_studio_d1.value),
    AE3EntranceMeta(Stage.entrance_studio_dd2.value, Stage.region_studio_d.value, Stage.region_studio_d2.value),
    AE3EntranceMeta(Stage.entrance_studio_d2d.value, Stage.region_studio_d2.value, Stage.region_studio_d.value),

    # Halloween
    AE3EntranceMeta(Stage.entrance_halloween_a1a.value, Stage.region_halloween_a1.value,
                    Stage.region_halloween_a.value),
    AE3EntranceMeta(Stage.entrance_halloween_aa1.value, Stage.region_halloween_a.value,
                    Stage.region_halloween_a1.value),
    AE3EntranceMeta(Stage.entrance_halloween_bb1.value, Stage.region_halloween_b.value,
                    Stage.region_halloween_b1.value),
    AE3EntranceMeta(Stage.entrance_halloween_b1b.value, Stage.region_halloween_b1.value,
                    Stage.region_halloween_b.value),
    AE3EntranceMeta(Stage.entrance_halloween_c1c.value, Stage.region_halloween_c1.value,
                    Stage.region_halloween_c.value),
    AE3EntranceMeta(Stage.entrance_halloween_cc1.value, Stage.region_halloween_c.value,
                    Stage.region_halloween_c1.value),
    AE3EntranceMeta(Stage.entrance_halloween_cc2.value, Stage.region_halloween_c.value,
                    Stage.region_halloween_c2.value),
    AE3EntranceMeta(Stage.entrance_halloween_c2c.value, Stage.region_halloween_c2.value,
                    Stage.region_halloween_c.value),
    AE3EntranceMeta(Stage.entrance_halloween_dd1.value, Stage.region_halloween_d.value,
                    Stage.region_halloween_d1.value),
    AE3EntranceMeta(Stage.entrance_halloween_d1d.value, Stage.region_halloween_d1.value,
                    Stage.region_halloween_d.value),
    AE3EntranceMeta(Stage.entrance_halloween_d1d2.value, Stage.region_halloween_d1.value,
                    Stage.region_halloween_d2.value),
    AE3EntranceMeta(Stage.entrance_halloween_d2d1.value, Stage.region_halloween_d2.value,
                    Stage.region_halloween_d1.value),

    # Western
    AE3EntranceMeta(Stage.entrance_western_bb1.value, Stage.region_western_b.value, Stage.region_western_b1.value),
    AE3EntranceMeta(Stage.entrance_western_b1b.value, Stage.region_western_b1.value, Stage.region_western_b.value),
    AE3EntranceMeta(Stage.entrance_western_dd2.value, Stage.region_western_d.value, Stage.region_western_d2.value),
    AE3EntranceMeta(Stage.entrance_western_dd3.value, Stage.region_western_d.value, Stage.region_western_d3.value),
    AE3EntranceMeta(Stage.entrance_western_d1d2.value, Stage.region_western_d1.value, Stage.region_western_d2.value),
    AE3EntranceMeta(Stage.entrance_western_d1d3.value, Stage.region_western_d1.value, Stage.region_western_d3.value),
    AE3EntranceMeta(Stage.entrance_western_d2d.value, Stage.region_western_d2.value, Stage.region_western_d.value),
    AE3EntranceMeta(Stage.entrance_western_ee1.value, Stage.region_western_e.value, Stage.region_western_e1.value),
    AE3EntranceMeta(Stage.entrance_western_e1e.value, Stage.region_western_e1.value, Stage.region_western_e.value),

    # Onsen
    AE3EntranceMeta(Stage.entrance_onsen_aa1.value, Stage.region_onsen_a.value, Stage.region_onsen_a1.value),
    AE3EntranceMeta(Stage.entrance_onsen_aa2.value, Stage.region_onsen_a.value, Stage.region_onsen_a2.value),
    AE3EntranceMeta(Stage.entrance_onsen_a1a.value, Stage.region_onsen_a1.value, Stage.region_onsen_a.value),
    AE3EntranceMeta(Stage.entrance_onsen_a1a2.value, Stage.region_onsen_a1.value, Stage.region_onsen_a2.value),
    AE3EntranceMeta(Stage.entrance_onsen_a2a.value, Stage.region_onsen_a2.value, Stage.region_onsen_a.value),
    AE3EntranceMeta(Stage.entrance_onsen_a2a1.value, Stage.region_onsen_a2.value, Stage.region_onsen_a1.value),
    AE3EntranceMeta(Stage.entrance_onsen_b1b.value, Stage.region_onsen_b1.value, Stage.region_onsen_b.value),
    AE3EntranceMeta(Stage.entrance_onsen_bb1.value, Stage.region_onsen_b.value, Stage.region_onsen_b1.value),
    AE3EntranceMeta(Stage.entrance_onsen_d1d.value, Stage.region_onsen_d1.value, Stage.region_onsen_d.value),
    AE3EntranceMeta(Stage.entrance_onsen_dd1.value, Stage.region_onsen_d.value, Stage.region_onsen_d1.value),

    # Edotown
    AE3EntranceMeta(Stage.entrance_edotown_a1a.value, Stage.region_edotown_a1.value, Stage.region_edotown_a.value),
    AE3EntranceMeta(Stage.entrance_edotown_aa1.value, Stage.region_edotown_a.value, Stage.region_edotown_a1.value),
    AE3EntranceMeta(Stage.entrance_edotown_b1b2.value, Stage.region_edotown_b1.value, Stage.region_edotown_b2.value),
    AE3EntranceMeta(Stage.entrance_edotown_b2b1.value, Stage.region_edotown_b2.value, Stage.region_edotown_b1.value),
    AE3EntranceMeta(Stage.entrance_edotown_b2b.value, Stage.region_edotown_b2.value, Stage.region_edotown_b.value),
    AE3EntranceMeta(Stage.entrance_edotown_bb2.value, Stage.region_edotown_b.value, Stage.region_edotown_b2.value),
    AE3EntranceMeta(Stage.entrance_edotown_bc1.value, Stage.region_edotown_b.value, Stage.region_edotown_c1.value),
    AE3EntranceMeta(Stage.entrance_edotown_c1c.value, Stage.region_edotown_c1.value, Stage.region_edotown_c.value),
    AE3EntranceMeta(Stage.entrance_edotown_cc1.value, Stage.region_edotown_c.value, Stage.region_edotown_c1.value),
    AE3EntranceMeta(Stage.entrance_edotown_cc2.value, Stage.region_edotown_c.value, Stage.region_edotown_c2.value),
    AE3EntranceMeta(Stage.entrance_edotown_c2c.value, Stage.region_edotown_c2.value, Stage.region_edotown_c.value),

    # Heaven
    AE3EntranceMeta(Stage.entrance_heaven_a1a.value, Stage.region_heaven_a1.value, Stage.region_heaven_a.value),
    AE3EntranceMeta(Stage.entrance_heaven_aa1.value, Stage.region_heaven_a.value, Stage.region_heaven_a1.value),
    AE3EntranceMeta(Stage.entrance_heaven_bb1.value, Stage.region_heaven_b.value, Stage.region_heaven_b1.value),
    AE3EntranceMeta(Stage.entrance_heaven_b1b.value, Stage.region_heaven_b1.value, Stage.region_heaven_b.value),

    # Toyhouse
    AE3EntranceMeta(Stage.entrance_toyhouse_bb1.value, Stage.region_toyhouse_b.value, Stage.region_toyhouse_b1.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_b1b.value, Stage.region_toyhouse_b1.value, Stage.region_toyhouse_b.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_gg1.value, Stage.region_toyhouse_g.value, Stage.region_toyhouse_g1.value),
    AE3EntranceMeta(Stage.entrance_toyhouse_g1g.value, Stage.region_toyhouse_g1.value, Stage.region_toyhouse_g.value),

    # Iceland
    AE3EntranceMeta(Stage.entrance_iceland_a1a.value, Stage.region_iceland_a1.value, Stage.region_iceland_a.value),
    AE3EntranceMeta(Stage.entrance_iceland_aa1.value, Stage.region_iceland_a.value, Stage.region_iceland_a1.value),
    AE3EntranceMeta(Stage.entrance_iceland_aa2.value, Stage.region_iceland_a.value, Stage.region_iceland_a2.value),
    AE3EntranceMeta(Stage.entrance_iceland_a2a.value, Stage.region_iceland_a2.value, Stage.region_iceland_a.value),

    # Arabian
    AE3EntranceMeta(Stage.entrance_arabian_cc1.value, Stage.region_arabian_c.value, Stage.region_arabian_c1.value),
    AE3EntranceMeta(Stage.entrance_arabian_c1c.value, Stage.region_arabian_c1.value, Stage.region_arabian_c.value),
    AE3EntranceMeta(Stage.entrance_arabian_e1e.value, Stage.region_arabian_e1.value, Stage.region_arabian_e.value),
    AE3EntranceMeta(Stage.entrance_arabian_ee1.value, Stage.region_arabian_e.value, Stage.region_arabian_e1.value),

    # Asia
    AE3EntranceMeta(Stage.entrance_asia_aa1.value, Stage.region_asia_a.value, Stage.region_asia_a1.value),
    AE3EntranceMeta(Stage.entrance_asia_aa5.value, Stage.region_asia_a.value, Stage.region_asia_a5.value),
    AE3EntranceMeta(Stage.entrance_asia_a1a.value, Stage.region_asia_a1.value, Stage.region_asia_a.value),
    AE3EntranceMeta(Stage.entrance_asia_a1a2.value, Stage.region_asia_a1.value, Stage.region_asia_a2.value),
    AE3EntranceMeta(Stage.entrance_asia_a1a3.value, Stage.region_asia_a1.value, Stage.region_asia_a3.value),
    AE3EntranceMeta(Stage.entrance_asia_a1a4.value, Stage.region_asia_a1.value, Stage.region_asia_a4.value),
    AE3EntranceMeta(Stage.entrance_asia_a2a1.value, Stage.region_asia_a2.value, Stage.region_asia_a1.value),
    AE3EntranceMeta(Stage.entrance_asia_a2a3.value, Stage.region_asia_a2.value, Stage.region_asia_a3.value),
    AE3EntranceMeta(Stage.entrance_asia_a2a4.value, Stage.region_asia_a2.value, Stage.region_asia_a4.value),
    AE3EntranceMeta(Stage.entrance_asia_a3a1.value, Stage.region_asia_a3.value, Stage.region_asia_a1.value),
    AE3EntranceMeta(Stage.entrance_asia_a3a4.value, Stage.region_asia_a3.value, Stage.region_asia_a4.value),
    AE3EntranceMeta(Stage.entrance_asia_a3a2.value, Stage.region_asia_a3.value, Stage.region_asia_a2.value),
    AE3EntranceMeta(Stage.entrance_asia_a4a1.value, Stage.region_asia_a4.value, Stage.region_asia_a1.value),
    AE3EntranceMeta(Stage.entrance_asia_a4a3.value, Stage.region_asia_a4.value, Stage.region_asia_a3.value),
    AE3EntranceMeta(Stage.entrance_asia_a4a5.value, Stage.region_asia_a4.value, Stage.region_asia_a5.value),
    AE3EntranceMeta(Stage.entrance_asia_a5a6.value, Stage.region_asia_a5.value, Stage.region_asia_a6.value),
    AE3EntranceMeta(Stage.entrance_asia_a6a5.value, Stage.region_asia_a6.value, Stage.region_asia_a5.value),
    AE3EntranceMeta(Stage.entrance_asia_bb1.value, Stage.region_asia_b.value, Stage.region_asia_b1.value),
    AE3EntranceMeta(Stage.entrance_asia_bb2.value, Stage.region_asia_b.value, Stage.region_asia_b2.value),
    AE3EntranceMeta(Stage.entrance_asia_b1b.value, Stage.region_asia_b1.value, Stage.region_asia_b.value),
    AE3EntranceMeta(Stage.entrance_asia_b1b2.value, Stage.region_asia_b1.value, Stage.region_asia_b2.value),
    AE3EntranceMeta(Stage.entrance_asia_b2b1.value, Stage.region_asia_b2.value, Stage.region_asia_b1.value),
    AE3EntranceMeta(Stage.entrance_asia_b2b.value, Stage.region_asia_b2.value, Stage.region_asia_b.value),
    AE3EntranceMeta(Stage.entrance_asia_d1d.value, Stage.region_asia_d1.value, Stage.region_asia_d.value),
    AE3EntranceMeta(Stage.entrance_asia_dd2.value, Stage.region_asia_d.value, Stage.region_asia_d2.value),
    AE3EntranceMeta(Stage.entrance_asia_d2d.value, Stage.region_asia_d2.value, Stage.region_asia_d.value),
    AE3EntranceMeta(Stage.entrance_asia_ee1.value, Stage.region_asia_e.value, Stage.region_asia_e1.value),
    AE3EntranceMeta(Stage.entrance_asia_e1e.value, Stage.region_asia_e1.value, Stage.region_asia_e.value),
    AE3EntranceMeta(Stage.entrance_asia_e1e2.value, Stage.region_asia_e1.value, Stage.region_asia_e2.value),
    AE3EntranceMeta(Stage.entrance_asia_e2e.value, Stage.region_asia_e2.value, Stage.region_asia_e.value),

    # Plane
    AE3EntranceMeta(Stage.entrance_plane_aa1.value, Stage.region_plane_a.value, Stage.region_plane_a1.value),
    AE3EntranceMeta(Stage.entrance_plane_a1a.value, Stage.region_plane_a1.value, Stage.region_plane_a.value),
    AE3EntranceMeta(Stage.entrance_plane_cc1.value, Stage.region_plane_c.value, Stage.region_plane_c1.value),
    AE3EntranceMeta(Stage.entrance_plane_c1c.value, Stage.region_plane_c1.value, Stage.region_plane_c.value),
    AE3EntranceMeta(Stage.entrance_plane_b1b2.value, Stage.region_plane_b1.value, Stage.region_plane_b2.value),
    AE3EntranceMeta(Stage.entrance_plane_b2b1.value, Stage.region_plane_b2.value, Stage.region_plane_b1.value),

    # Hong
    AE3EntranceMeta(Stage.entrance_hong_aa1.value, Stage.region_hong_a.value, Stage.region_hong_a1.value),
    AE3EntranceMeta(Stage.entrance_hong_a1a.value, Stage.region_hong_a1.value, Stage.region_hong_a.value),
    AE3EntranceMeta(Stage.entrance_hong_a1a2.value, Stage.region_hong_a1.value, Stage.region_hong_a2.value),
    AE3EntranceMeta(Stage.entrance_hong_a2a1.value, Stage.region_hong_a2.value, Stage.region_hong_a1.value),
    AE3EntranceMeta(Stage.entrance_hong_bb1.value, Stage.region_hong_b.value, Stage.region_hong_b1.value),
    AE3EntranceMeta(Stage.entrance_hong_bb2.value, Stage.region_hong_b.value, Stage.region_hong_b2.value),
    AE3EntranceMeta(Stage.entrance_hong_b1b.value, Stage.region_hong_b1.value, Stage.region_hong_b.value),
    AE3EntranceMeta(Stage.entrance_hong_b2b.value, Stage.region_hong_b2.value, Stage.region_hong_b.value),
    AE3EntranceMeta(Stage.entrance_hong_cc1.value, Stage.region_hong_c.value, Stage.region_hong_c1.value),
    AE3EntranceMeta(Stage.entrance_hong_c1c.value, Stage.region_hong_c1.value, Stage.region_hong_c.value),
    AE3EntranceMeta(Stage.entrance_hong_c1c2.value, Stage.region_hong_c1.value, Stage.region_hong_c2.value),
    AE3EntranceMeta(Stage.entrance_hong_c2c.value, Stage.region_hong_c2.value, Stage.region_hong_c.value),
    AE3EntranceMeta(Stage.entrance_hong_ee1.value, Stage.region_hong_e.value, Stage.region_hong_e1.value),
    AE3EntranceMeta(Stage.entrance_hong_e1e.value, Stage.region_hong_e1.value, Stage.region_hong_e.value),

    # Bay
    AE3EntranceMeta(Stage.entrance_bay_aa1.value, Stage.region_bay_a.value, Stage.region_bay_a1.value),
    AE3EntranceMeta(Stage.entrance_bay_a1a.value, Stage.region_bay_a1.value, Stage.region_bay_a.value),
    AE3EntranceMeta(Stage.entrance_bay_a1a5.value, Stage.region_bay_a1.value, Stage.region_bay_a5.value),
    AE3EntranceMeta(Stage.entrance_bay_a1a2.value, Stage.region_bay_a1.value, Stage.region_bay_a2.value),
    AE3EntranceMeta(Stage.entrance_bay_a2a1.value, Stage.region_bay_a2.value, Stage.region_bay_a1.value),
    AE3EntranceMeta(Stage.entrance_bay_a2a3.value, Stage.region_bay_a2.value, Stage.region_bay_a3.value),
    AE3EntranceMeta(Stage.entrance_bay_a3a2.value, Stage.region_bay_a3.value, Stage.region_bay_a2.value),
    AE3EntranceMeta(Stage.entrance_bay_a3a6.value, Stage.region_bay_a3.value, Stage.region_bay_a6.value),
    AE3EntranceMeta(Stage.entrance_bay_a3a5.value, Stage.region_bay_a3.value, Stage.region_bay_a5.value),
    AE3EntranceMeta(Stage.entrance_bay_a3a4.value, Stage.region_bay_a3.value, Stage.region_bay_a4.value),
    AE3EntranceMeta(Stage.entrance_bay_a4a3.value, Stage.region_bay_a4.value, Stage.region_bay_a3.value),
    AE3EntranceMeta(Stage.entrance_bay_a5a1.value, Stage.region_bay_a5.value, Stage.region_bay_a1.value),
    AE3EntranceMeta(Stage.entrance_bay_a5a3.value, Stage.region_bay_a5.value, Stage.region_bay_a3.value),
    AE3EntranceMeta(Stage.entrance_bay_a6a3.value, Stage.region_bay_a6.value, Stage.region_bay_a3.value),
    AE3EntranceMeta(Stage.entrance_bay_a7a3.value, Stage.region_bay_a7.value, Stage.region_bay_a3.value),
    AE3EntranceMeta(Stage.entrance_bay_cc1.value, Stage.region_bay_c.value, Stage.region_bay_c1.value),
    AE3EntranceMeta(Stage.entrance_bay_c1c.value, Stage.region_bay_c1.value, Stage.region_bay_c.value),
    AE3EntranceMeta(Stage.entrance_bay_d1d.value, Stage.region_bay_d1.value, Stage.region_bay_d.value),
    AE3EntranceMeta(Stage.entrance_bay_dd1.value, Stage.region_bay_d.value, Stage.region_bay_d1.value),
    AE3EntranceMeta(Stage.entrance_bay_ee1.value, Stage.region_bay_e.value, Stage.region_bay_e1.value),
    AE3EntranceMeta(Stage.entrance_bay_ee2.value, Stage.region_bay_e.value, Stage.region_bay_e2.value),
    AE3EntranceMeta(Stage.entrance_bay_e1e2.value, Stage.region_bay_e1.value, Stage.region_bay_e2.value),
    AE3EntranceMeta(Stage.entrance_bay_e2e.value, Stage.region_bay_e2.value, Stage.region_bay_e.value),

    # Tomo
    AE3EntranceMeta(Stage.entrance_tomo_a1a.value, Stage.region_tomo_a1.value, Stage.region_tomo_a.value),
    AE3EntranceMeta(Stage.entrance_tomo_aa1.value, Stage.region_tomo_a.value, Stage.region_tomo_a1.value),
    AE3EntranceMeta(Stage.entrance_tomo_ee1.value, Stage.region_tomo_e.value, Stage.region_tomo_e1.value),
    AE3EntranceMeta(Stage.entrance_tomo_e1e.value, Stage.region_tomo_e1.value, Stage.region_tomo_e.value),
    AE3EntranceMeta(Stage.entrance_tomo_ee2.value, Stage.region_tomo_e.value, Stage.region_tomo_e2.value),
    AE3EntranceMeta(Stage.entrance_tomo_e2e.value, Stage.region_tomo_e2.value, Stage.region_tomo_e.value),
    AE3EntranceMeta(Stage.entrance_tomo_e2e3.value, Stage.region_tomo_e2.value, Stage.region_tomo_e3.value),
    AE3EntranceMeta(Stage.entrance_tomo_e3e2.value, Stage.region_tomo_e3.value, Stage.region_tomo_e2.value),
    AE3EntranceMeta(Stage.entrance_tomo_f1f2.value, Stage.region_tomo_f1.value, Stage.region_tomo_f2.value),
    AE3EntranceMeta(Stage.entrance_tomo_f2f1.value, Stage.region_tomo_f2.value, Stage.region_tomo_f1.value),
    AE3EntranceMeta(Stage.entrance_tomo_ff2.value, Stage.region_tomo_f.value, Stage.region_tomo_f2.value),
    AE3EntranceMeta(Stage.entrance_tomo_ff1.value, Stage.region_tomo_f.value, Stage.region_tomo_f1.value),
    AE3EntranceMeta(Stage.entrance_tomo_gg1.value, Stage.region_tomo_g.value, Stage.region_tomo_g1.value),
    AE3EntranceMeta(Stage.entrance_tomo_g1g.value, Stage.region_tomo_g1.value, Stage.region_tomo_g.value),
    AE3EntranceMeta(Stage.entrance_tomo_h1h.value, Stage.region_tomo_h1.value, Stage.region_tomo_h.value),
    AE3EntranceMeta(Stage.entrance_tomo_hh1.value, Stage.region_tomo_h.value, Stage.region_tomo_h1.value),

    # Space
    AE3EntranceMeta(Stage.entrance_space_e1e.value, Stage.region_space_e1.value, Stage.region_space_e.value),
    AE3EntranceMeta(Stage.entrance_space_e1e_2.value, Stage.region_space_e1.value, Stage.region_space_e.value),
    AE3EntranceMeta(Stage.entrance_space_ee1.value, Stage.region_space_e.value, Stage.region_space_e1.value),
    AE3EntranceMeta(Stage.entrance_space_ee1_2.value, Stage.region_space_e.value, Stage.region_space_b.value),
    AE3EntranceMeta(Stage.entrance_space_gg1.value, Stage.region_space_g.value, Stage.region_space_g1.value),
    AE3EntranceMeta(Stage.entrance_space_gg1_2.value, Stage.region_space_g.value, Stage.region_space_g1.value),
    AE3EntranceMeta(Stage.entrance_space_g1g.value, Stage.region_space_g.value, Stage.region_space_g.value),
    AE3EntranceMeta(Stage.entrance_space_g1g_2.value, Stage.region_space_g.value, Stage.region_space_g.value),
    AE3EntranceMeta(Stage.entrance_space_ff2.value, Stage.region_space_f.value, Stage.region_space_f2.value),
    AE3EntranceMeta(Stage.entrance_space_ff1.value, Stage.region_space_f.value, Stage.region_space_f1.value),
    AE3EntranceMeta(Stage.entrance_space_f1f.value, Stage.region_space_f1.value, Stage.region_space_f.value),
    AE3EntranceMeta(Stage.entrance_space_f1f2.value, Stage.region_space_f1.value, Stage.region_space_f2.value),
    AE3EntranceMeta(Stage.entrance_space_f2f1.value, Stage.region_space_f2.value, Stage.region_space_f1.value),
    AE3EntranceMeta(Stage.entrance_space_f2f.value, Stage.region_space_f2.value, Stage.region_space_f.value),
    AE3EntranceMeta(Stage.entrance_space_dd.value, Stage.region_space_d.value, Stage.region_space_d.value),
    AE3EntranceMeta(Stage.entrance_space_dd_2.value, Stage.region_space_d.value, Stage.region_space_d.value),
    AE3EntranceMeta(Stage.entrance_space_jj1.value, Stage.region_space_j.value, Stage.region_space_j1.value),
    AE3EntranceMeta(Stage.entrance_space_j1j.value, Stage.region_space_j1.value, Stage.region_space_j.value),
]

## Entrances for selecting a stage
ENTRANCES_STAGE_SELECT : list[AE3EntranceMeta] = [
    AE3EntranceMeta(Stage.entrance_level_1.value, Stage.travel_station_a.value, Stage.region_seaside_a.value),
    AE3EntranceMeta(Stage.entrance_level_2.value, Stage.travel_station_a.value, Stage.region_woods_a.value),
    AE3EntranceMeta(Stage.entrance_level_3.value, Stage.travel_station_a.value, Stage.region_castle_a1.value),

    AE3EntranceMeta(Stage.entrance_level_4.value, Stage.travel_station_a.value, Stage.region_boss1.value),

    AE3EntranceMeta(Stage.entrance_level_5.value, Stage.travel_station_a.value, Stage.region_ciscocity_a.value),
    AE3EntranceMeta(Stage.entrance_level_6.value, Stage.travel_station_a.value, Stage.region_studio_a.value),
    AE3EntranceMeta(Stage.entrance_level_7.value, Stage.travel_station_a.value, Stage.region_halloween_a1.value),
    AE3EntranceMeta(Stage.entrance_level_8.value, Stage.travel_station_a.value, Stage.region_western_a.value),

    AE3EntranceMeta(Stage.entrance_level_9.value, Stage.travel_station_a.value, Stage.region_boss2.value),

    AE3EntranceMeta(Stage.entrance_level_10.value, Stage.travel_station_a.value, Stage.region_onsen_a.value),
    AE3EntranceMeta(Stage.entrance_level_11.value, Stage.travel_station_a.value, Stage.region_snowfesta_a.value),
    AE3EntranceMeta(Stage.entrance_level_12.value, Stage.travel_station_a.value, Stage.region_edotown_a1.value),

    AE3EntranceMeta(Stage.entrance_level_13.value, Stage.travel_station_a.value, Stage.region_boss3.value),

    AE3EntranceMeta(Stage.entrance_level_14.value, Stage.travel_station_a.value, Stage.region_heaven_a1.value),
    AE3EntranceMeta(Stage.entrance_level_15.value, Stage.travel_station_a.value, Stage.region_toyhouse_a.value),
    AE3EntranceMeta(Stage.entrance_level_16.value, Stage.travel_station_a.value, Stage.region_iceland_a1.value),
    AE3EntranceMeta(Stage.entrance_level_17.value, Stage.travel_station_a.value, Stage.region_arabian_a.value),

    AE3EntranceMeta(Stage.entrance_level_18.value, Stage.travel_station_a.value, Stage.region_boss4.value),

    AE3EntranceMeta(Stage.entrance_level_19.value, Stage.travel_station_a.value, Stage.region_asia_a.value),
    AE3EntranceMeta(Stage.entrance_level_20.value, Stage.travel_station_a.value, Stage.region_plane_a.value),
    AE3EntranceMeta(Stage.entrance_level_21.value, Stage.travel_station_a.value, Stage.region_hong_a.value),

    AE3EntranceMeta(Stage.entrance_level_22.value, Stage.travel_station_a.value, Stage.region_boss5.value),

    AE3EntranceMeta(Stage.entrance_level_23.value, Stage.travel_station_a.value, Stage.region_bay_a.value),
    AE3EntranceMeta(Stage.entrance_level_24.value, Stage.travel_station_a.value, Stage.region_tomo_a1.value),

    AE3EntranceMeta(Stage.entrance_level_25.value, Stage.travel_station_a.value, Stage.region_boss6.value),

    AE3EntranceMeta(Stage.entrance_level_26.value, Stage.travel_station_a.value, Stage.region_space_a.value),

    AE3EntranceMeta(Stage.entrance_level_27.value, Stage.travel_station_a.value, Stage.region_specter1.value),
    AE3EntranceMeta(Stage.entrance_level_28.value, Stage.travel_station_a.value, Stage.region_specter2.value),

    AE3EntranceMeta(Stage.entrance_level_29.value, Stage.travel_station_a.value, Stage.zero.value)
]

ENTRANCES_MASTER : list[AE3EntranceMeta] = [
    *ENTRANCES_MAIN, *ENTRANCES_SUBREGIONS, *ENTRANCES_STAGE_SELECT
]

### [< --- VANILLA ENTRANCES GROUPS --- >]
ENTRANCES_SEASIDE : list[str] = [
    Stage.entrance_seaside_ab.value,
    Stage.entrance_seaside_ac.value,
    Stage.entrance_seaside_ba.value,
    Stage.entrance_seaside_ca.value
]

ENTRANCES_WOODS : list[str] = [
    Stage.entrance_woods_ab.value,
    Stage.entrance_woods_ad.value,
    Stage.entrance_woods_ba.value,
    Stage.entrance_woods_bc.value,
    Stage.entrance_woods_cb.value,
    Stage.entrance_woods_da.value
]

ENTRANCES_CASTLE : list[str] = [
    Stage.entrance_castle_ad.value,
    Stage.entrance_castle_a2b.value,
    Stage.entrance_castle_da.value,
    Stage.entrance_castle_d1b.value,
    Stage.entrance_castle_ba2.value,
    Stage.entrance_castle_bd1.value,
    Stage.entrance_castle_be.value,
    Stage.entrance_castle_b1c.value,
    Stage.entrance_castle_cb1.value,
    Stage.entrance_castle_eb.value,
    Stage.entrance_castle_ef.value,
    Stage.entrance_castle_fe.value,

    Stage.entrance_castle_aa2.value,
    Stage.entrance_castle_a2a.value,
    Stage.entrance_castle_a1a.value,
    Stage.entrance_castle_aa1.value,
    Stage.entrance_castle_dd1.value,
    Stage.entrance_castle_d1d.value,
    Stage.entrance_castle_bb1.value,
    Stage.entrance_castle_b1b.value
]

ENTRANCES_CISCOCITY : list[str] = [
    Stage.entrance_ciscocity_ac1.value,
    Stage.entrance_ciscocity_ab.value,
    Stage.entrance_ciscocity_ad.value,
    Stage.entrance_ciscocity_ad_2.value,
    Stage.entrance_ciscocity_c1a.value,
    Stage.entrance_ciscocity_c1c.value,
    Stage.entrance_ciscocity_cc1.value,
    Stage.entrance_ciscocity_ce.value,
    Stage.entrance_ciscocity_ec.value,
    Stage.entrance_ciscocity_ba.value,
    Stage.entrance_ciscocity_da.value,
    Stage.entrance_ciscocity_da_2.value
]

ENTRANCES_STUDIO : list[str] = [
    Stage.entrance_studio_ab1.value,
    Stage.entrance_studio_aa2.value,
    Stage.entrance_studio_aa1.value,
    Stage.entrance_studio_ae.value,
    Stage.entrance_studio_a2a.value,
    Stage.entrance_studio_a2c.value,
    Stage.entrance_studio_a1a.value,
    Stage.entrance_studio_a1d2.value,
    Stage.entrance_studio_b1a.value,
    Stage.entrance_studio_b1b2.value,
    Stage.entrance_studio_b2b1.value,
    Stage.entrance_studio_bf.value,
    Stage.entrance_studio_fb.value,
    Stage.entrance_studio_ff1.value,
    Stage.entrance_studio_f1f.value,
    Stage.entrance_studio_f1d1.value,
    Stage.entrance_studio_d1f1.value,
    Stage.entrance_studio_d1d.value,
    Stage.entrance_studio_dd1.value,
    Stage.entrance_studio_dg.value,
    Stage.entrance_studio_dd2.value,
    Stage.entrance_studio_d2d.value,
    Stage.entrance_studio_d2a1.value,
    Stage.entrance_studio_gd.value,
    Stage.entrance_studio_ea.value,
    Stage.entrance_studio_ec.value,
    Stage.entrance_studio_ce.value,
    Stage.entrance_studio_ca2.value
]

ENTRANCES_HALLOWEEN : list[str] = [
    Stage.entrance_halloween_a1a.value,
    Stage.entrance_halloween_aa1.value,
    Stage.entrance_halloween_ab.value,
    Stage.entrance_halloween_ba.value,
    Stage.entrance_halloween_bb1.value,
    Stage.entrance_halloween_b1b.value,
    Stage.entrance_halloween_b1f.value,
    Stage.entrance_halloween_fb1.value,
    Stage.entrance_halloween_fc1.value,
    Stage.entrance_halloween_c1f.value,
    Stage.entrance_halloween_c1c.value,
    Stage.entrance_halloween_cc1.value,
    Stage.entrance_halloween_cc2.value,
    Stage.entrance_halloween_c2c.value,
    Stage.entrance_halloween_c2d1.value,
    Stage.entrance_halloween_dc2.value,
    Stage.entrance_halloween_dd1.value,
    Stage.entrance_halloween_d1d.value,
    Stage.entrance_halloween_d1e.value,
    Stage.entrance_halloween_d1d2.value,
    Stage.entrance_halloween_d2d1.value,
    Stage.entrance_halloween_ed1.value
]

ENTRANCES_WESTERN : list[str] = [
    Stage.entrance_western_ab.value,
    Stage.entrance_western_af.value,
    Stage.entrance_western_ba.value,
    Stage.entrance_western_bb1.value,
    Stage.entrance_western_b1b.value,
    Stage.entrance_western_fa.value,
    Stage.entrance_western_fd2.value,
    Stage.entrance_western_de.value,
    Stage.entrance_western_dd2.value,
    Stage.entrance_western_dd3.value,
    Stage.entrance_western_d1f.value,
    Stage.entrance_western_d1d2.value,
    Stage.entrance_western_d1d3.value,
    Stage.entrance_western_d2d.value,
    Stage.entrance_western_ed1.value,
    Stage.entrance_western_ec.value,
    Stage.entrance_western_ee1.value,
    Stage.entrance_western_e1e.value,
    Stage.entrance_western_cf.value
]

ENTRANCES_ONSEN : list[str] = [
    Stage.entrance_onsen_aa1.value,
    Stage.entrance_onsen_aa2.value,
    Stage.entrance_onsen_a1a.value,
    Stage.entrance_onsen_a1a2.value,
    Stage.entrance_onsen_a1b1.value,
    Stage.entrance_onsen_a2a.value,
    Stage.entrance_onsen_a2a1.value,
    Stage.entrance_onsen_a2b1.value,
    Stage.entrance_onsen_b1a1.value,
    Stage.entrance_onsen_b1a2.value,
    Stage.entrance_onsen_b1b.value,
    Stage.entrance_onsen_bb1.value,
    Stage.entrance_onsen_be_2.value,
    Stage.entrance_onsen_bd1.value,
    Stage.entrance_onsen_bd.value,
    Stage.entrance_onsen_be.value,
    Stage.entrance_onsen_d1b.value,
    Stage.entrance_onsen_d1d.value,
    Stage.entrance_onsen_dd1.value,
    Stage.entrance_onsen_db.value,
    Stage.entrance_onsen_dc.value,
    Stage.entrance_onsen_cd.value,
    Stage.entrance_onsen_eb.value,
    Stage.entrance_onsen_eb_2.value
]

ENTRANCES_SNOWFESTA : list[str] = [
    Stage.entrance_snowfesta_ab.value,
    Stage.entrance_snowfesta_ag.value,
    Stage.entrance_snowfesta_ac.value,
    Stage.entrance_snowfesta_ba.value,
    Stage.entrance_snowfesta_ga.value,
    Stage.entrance_snowfesta_gd.value,
    Stage.entrance_snowfesta_dg.value,
    Stage.entrance_snowfesta_ca.value,
    Stage.entrance_snowfesta_cf.value,
    Stage.entrance_snowfesta_ce.value,
    Stage.entrance_snowfesta_ce_2.value,
    Stage.entrance_snowfesta_fc.value,
    Stage.entrance_snowfesta_ec.value,
    Stage.entrance_snowfesta_ec_2.value
]

ENTRANCES_EDOTOWN : list[str] = [
    Stage.entrance_edotown_a1a.value,
    Stage.entrance_edotown_aa1.value,
    Stage.entrance_edotown_ab1.value,
    Stage.entrance_edotown_b1a.value,
    Stage.entrance_edotown_b1b2.value,
    Stage.entrance_edotown_b2b1.value,
    Stage.entrance_edotown_b2b.value,
    Stage.entrance_edotown_bb2.value,
    Stage.entrance_edotown_bc1.value,
    Stage.entrance_edotown_be.value,
    Stage.entrance_edotown_c1b.value,
    Stage.entrance_edotown_c1c.value,
    Stage.entrance_edotown_cc1.value,
    Stage.entrance_edotown_cc2.value,
    Stage.entrance_edotown_c2c.value,
    Stage.entrance_edotown_c2d.value,
    Stage.entrance_edotown_dc2.value,
    Stage.entrance_edotown_de.value,
    Stage.entrance_edotown_df.value,
    Stage.entrance_edotown_fd.value,
    Stage.entrance_edotown_ed.value,
    Stage.entrance_edotown_eb.value
]

ENTRANCES_HEAVEN : list[str] = [
    Stage.entrance_heaven_a1a.value,
    Stage.entrance_heaven_aa1.value,
    Stage.entrance_heaven_ab.value,
    Stage.entrance_heaven_ba.value,
    Stage.entrance_heaven_bb1.value,
    Stage.entrance_heaven_b1b.value,
    Stage.entrance_heaven_b1c.value,
    Stage.entrance_heaven_cb1.value,
    Stage.entrance_heaven_ce.value,
    Stage.entrance_heaven_cd.value,
    Stage.entrance_heaven_ec.value,
    Stage.entrance_heaven_dc.value
]

ENTRANCES_TOYHOUSE : list[str] = [
    Stage.entrance_toyhouse_bb1.value,
    Stage.entrance_toyhouse_b1b.value,
    Stage.entrance_toyhouse_gg1.value,
    Stage.entrance_toyhouse_g1g.value,
    Stage.entrance_toyhouse_ab.value,
    Stage.entrance_toyhouse_ad.value,
    Stage.entrance_toyhouse_ag.value,
    Stage.entrance_toyhouse_ae.value,
    Stage.entrance_toyhouse_ac.value,
    Stage.entrance_toyhouse_ba.value,
    Stage.entrance_toyhouse_da.value,
    Stage.entrance_toyhouse_dh.value,
    Stage.entrance_toyhouse_hd.value,
    Stage.entrance_toyhouse_ga.value,
    Stage.entrance_toyhouse_g1a.value,
    Stage.entrance_toyhouse_ea.value,
    Stage.entrance_toyhouse_ef.value,
    Stage.entrance_toyhouse_fe.value,
    Stage.entrance_toyhouse_fa.value,
    Stage.entrance_toyhouse_ca.value
]

ENTRANCES_ICELAND : list[str] = [
    Stage.entrance_iceland_a1a.value,
    Stage.entrance_iceland_aa1.value,
    Stage.entrance_iceland_aa2.value,
    Stage.entrance_iceland_ad.value,
    Stage.entrance_iceland_a2a.value,
    Stage.entrance_iceland_a2e.value,
    Stage.entrance_iceland_da.value,
    Stage.entrance_iceland_dc.value,
    Stage.entrance_iceland_cd.value,
    Stage.entrance_iceland_cb.value,
    Stage.entrance_iceland_bc.value,
    Stage.entrance_iceland_be.value,
    Stage.entrance_iceland_eb.value,
    Stage.entrance_iceland_ef.value,
    Stage.entrance_iceland_ea2.value
]

ENTRANCES_ARABIAN : list[str] = [
    Stage.entrance_arabian_ac.value,
    Stage.entrance_arabian_ac1.value,
    Stage.entrance_arabian_ab.value,
    Stage.entrance_arabian_ca.value,
    Stage.entrance_arabian_cc1.value,
    Stage.entrance_arabian_c1c.value,
    Stage.entrance_arabian_c1a.value,
    Stage.entrance_arabian_ba.value,
    Stage.entrance_arabian_bg.value,
    Stage.entrance_arabian_bf.value,
    Stage.entrance_arabian_be1.value,
    Stage.entrance_arabian_fb.value,
    Stage.entrance_arabian_e1b.value,
    Stage.entrance_arabian_e1e.value,
    Stage.entrance_arabian_ee1.value,
    Stage.entrance_arabian_eg.value,
    Stage.entrance_arabian_ge.value,
    Stage.entrance_arabian_gb.value
]

ENTRANCES_ASIA : list[str] = [
    Stage.entrance_asia_ab.value,
    Stage.entrance_asia_aa1.value,
    Stage.entrance_asia_aa5.value,
    Stage.entrance_asia_a1a.value,
    Stage.entrance_asia_a1b1.value,
    Stage.entrance_asia_a1a2.value,
    Stage.entrance_asia_a1a3.value,
    Stage.entrance_asia_a1a4.value,
    Stage.entrance_asia_a2a1.value,
    Stage.entrance_asia_a2d2.value,
    Stage.entrance_asia_a2a3.value,
    Stage.entrance_asia_a2a4.value,
    Stage.entrance_asia_a3a1.value,
    Stage.entrance_asia_a3a4.value,
    Stage.entrance_asia_a3a2.value,
    Stage.entrance_asia_a3e.value,
    Stage.entrance_asia_a4a1.value,
    Stage.entrance_asia_a4a3.value,
    Stage.entrance_asia_a4a5.value,
    Stage.entrance_asia_a4d1.value,
    Stage.entrance_asia_a5a6.value,
    Stage.entrance_asia_a6a5.value,
    Stage.entrance_asia_ba.value,
    Stage.entrance_asia_bb1.value,
    Stage.entrance_asia_bb2.value,
    Stage.entrance_asia_b1b.value,
    Stage.entrance_asia_b1b2.value,
    Stage.entrance_asia_b2b1.value,
    Stage.entrance_asia_b2b.value,
    Stage.entrance_asia_b2a2.value,
    Stage.entrance_asia_d1a4.value,
    Stage.entrance_asia_d1d.value,
    Stage.entrance_asia_dd1.value,
    Stage.entrance_asia_dd2.value,
    Stage.entrance_asia_d2d.value,
    Stage.entrance_asia_d2a2.value,
    Stage.entrance_asia_ea3.value,
    Stage.entrance_asia_ee1.value,
    Stage.entrance_asia_ef.value,
    Stage.entrance_asia_fe.value,
    Stage.entrance_asia_e1e.value,
    Stage.entrance_asia_e1e2.value,
    Stage.entrance_asia_e2e.value,
    Stage.entrance_asia_e2a5.value,
]

ENTRANCES_PLANE : list[str] = [
    Stage.entrance_plane_aa1.value,
    Stage.entrance_plane_ac.value,
    Stage.entrance_plane_a1a.value,
    Stage.entrance_plane_ca.value,
    Stage.entrance_plane_cc1.value,
    Stage.entrance_plane_cg.value,
    Stage.entrance_plane_gc.value,
    Stage.entrance_plane_c1c.value,
    Stage.entrance_plane_c1d.value,
    Stage.entrance_plane_dc1.value,
    Stage.entrance_plane_de.value,
    Stage.entrance_plane_ed.value,
    Stage.entrance_plane_ef.value,
    Stage.entrance_plane_fe.value,
    Stage.entrance_plane_fb.value,
    Stage.entrance_plane_bf.value,
    Stage.entrance_plane_bh.value,
    Stage.entrance_plane_b1h.value,
    Stage.entrance_plane_b1b2.value,
    Stage.entrance_plane_b2b1.value,
    Stage.entrance_plane_b2f1.value,
    Stage.entrance_plane_f1b1.value,
    Stage.entrance_plane_hb.value,
    Stage.entrance_plane_hb1.value,
]

ENTRANCES_HONG : list[str] = [
    Stage.entrance_hong_aa1.value,
    Stage.entrance_hong_a1a.value,
    Stage.entrance_hong_a1a2.value,
    Stage.entrance_hong_a2a1.value,
    Stage.entrance_hong_a2b.value,
    Stage.entrance_hong_ba2.value,
    Stage.entrance_hong_bb1.value,
    Stage.entrance_hong_bb2.value,
    Stage.entrance_hong_b1b.value,
    Stage.entrance_hong_b1f.value,
    Stage.entrance_hong_b1c.value,
    Stage.entrance_hong_b2b.value,
    Stage.entrance_hong_b2d.value,
    Stage.entrance_hong_fb1.value,
    Stage.entrance_hong_cb1.value,
    Stage.entrance_hong_cc1.value,
    Stage.entrance_hong_ce.value,
    Stage.entrance_hong_cd.value,
    Stage.entrance_hong_ch.value,
    Stage.entrance_hong_hc.value,
    Stage.entrance_hong_c1c.value,
    Stage.entrance_hong_c1c2.value,
    Stage.entrance_hong_c2c.value,
    Stage.entrance_hong_ec.value,
    Stage.entrance_hong_ee1.value,
    Stage.entrance_hong_e1e.value,
    Stage.entrance_hong_dc.value,
    Stage.entrance_hong_dg.value,
    Stage.entrance_hong_eb2.value,
    Stage.entrance_hong_gd.value,
]

ENTRANCES_BAY : list[str] = [
    Stage.entrance_bay_aa1.value,
    Stage.entrance_bay_a1a.value,
    Stage.entrance_bay_a1b.value,
    Stage.entrance_bay_a1a5.value,
    Stage.entrance_bay_a1a2.value,
    Stage.entrance_bay_a2a1.value,
    Stage.entrance_bay_a2a3.value,
    Stage.entrance_bay_a2e.value,
    Stage.entrance_bay_a3a2.value,
    Stage.entrance_bay_a3c.value,
    Stage.entrance_bay_a3a6.value,
    Stage.entrance_bay_a3a5.value,
    Stage.entrance_bay_a3a4.value,
    Stage.entrance_bay_a4a3.value,
    Stage.entrance_bay_a4d1.value,
    Stage.entrance_bay_a5a1.value,
    Stage.entrance_bay_a5a3.value,
    Stage.entrance_bay_a6a3.value,
    Stage.entrance_bay_a6f.value,
    Stage.entrance_bay_a7a3.value,
    Stage.entrance_bay_ba1.value,
    Stage.entrance_bay_ca3.value,
    Stage.entrance_bay_cc1.value,
    Stage.entrance_bay_c1c.value,
    Stage.entrance_bay_c1a7.value,
    Stage.entrance_bay_d1a4.value,
    Stage.entrance_bay_d1d.value,
    Stage.entrance_bay_dd1.value,
    Stage.entrance_bay_ea2.value,
    Stage.entrance_bay_ee1.value,
    Stage.entrance_bay_ee2.value,
    Stage.entrance_bay_e1e2.value,
    Stage.entrance_bay_e2e.value,
    Stage.entrance_bay_fa6.value
]

ENTRANCES_TOMO : list[str] = [
    Stage.entrance_tomo_a1a.value,
    Stage.entrance_tomo_aa1.value,
    Stage.entrance_tomo_aj.value,
    Stage.entrance_tomo_ja.value,
    Stage.entrance_tomo_jb.value,
    Stage.entrance_tomo_bj.value,
    Stage.entrance_tomo_bc.value,
    Stage.entrance_tomo_cb.value,
    Stage.entrance_tomo_ce.value,
    Stage.entrance_tomo_ec.value,
    Stage.entrance_tomo_ee1.value,
    Stage.entrance_tomo_e1e.value,
    Stage.entrance_tomo_e1i.value,
    Stage.entrance_tomo_ee2.value,
    Stage.entrance_tomo_e2e.value,
    Stage.entrance_tomo_e2e3.value,
    Stage.entrance_tomo_e3e2.value,
    Stage.entrance_tomo_e3f1.value,
    Stage.entrance_tomo_f1e3.value,
    Stage.entrance_tomo_f1f2.value,
    Stage.entrance_tomo_f2f1.value,
    Stage.entrance_tomo_f2g.value,
    Stage.entrance_tomo_ff2.value,
    Stage.entrance_tomo_ff1.value,
    Stage.entrance_tomo_fg1.value,
    Stage.entrance_tomo_fh1.value,
    Stage.entrance_tomo_gf2.value,
    Stage.entrance_tomo_gg1.value,
    Stage.entrance_tomo_g1g.value,
    Stage.entrance_tomo_g1f.value,
    Stage.entrance_tomo_h1f.value,
    Stage.entrance_tomo_h1h.value,
    Stage.entrance_tomo_hh1.value,
    Stage.entrance_tomo_ha.value,
    Stage.entrance_tomo_ie1.value
]

ENTRANCES_SPACE : list[str] = [
    Stage.entrance_space_ab.value,
    Stage.entrance_space_ba.value,
    Stage.entrance_space_be1.value,
    Stage.entrance_space_bg.value,
    Stage.entrance_space_bf.value,
    Stage.entrance_space_bd.value,
    Stage.entrance_space_bi.value,
    Stage.entrance_space_e1b.value,
    Stage.entrance_space_e1e.value,
    Stage.entrance_space_e1e_2.value,
    Stage.entrance_space_eh.value,
    Stage.entrance_space_ee1.value,
    Stage.entrance_space_ee1_2.value,
    Stage.entrance_space_gb.value,
    Stage.entrance_space_gg1.value,
    Stage.entrance_space_gg1_2.value,
    Stage.entrance_space_g1g.value,
    Stage.entrance_space_g1g_2.value,
    Stage.entrance_space_fb.value,
    Stage.entrance_space_ff2.value,
    Stage.entrance_space_ff1.value,
    Stage.entrance_space_f1f.value,
    Stage.entrance_space_f1f2.value,
    Stage.entrance_space_f2f1.value,
    Stage.entrance_space_f2f.value,
    Stage.entrance_space_db.value,
    Stage.entrance_space_dd.value,
    Stage.entrance_space_dd_2.value,
    Stage.entrance_space_ib.value,
    Stage.entrance_space_ij.value,
    Stage.entrance_space_ji.value,
    Stage.entrance_space_jj1.value,
    Stage.entrance_space_j1j.value,
    Stage.entrance_space_j1a.value,
    Stage.entrance_space_he.value,
    Stage.entrance_space_hk.value,
    Stage.entrance_space_kh.value
]

ENTRANCES_INDEX : dict[str, list[str]] = {
    APHelper.seaside.value              : ENTRANCES_SEASIDE,
    APHelper.woods.value                : ENTRANCES_WOODS,
    APHelper.castle.value               : ENTRANCES_CASTLE,
    APHelper.ciscocity.value            : ENTRANCES_CISCOCITY,
    APHelper.studio.value               : ENTRANCES_STUDIO,
    APHelper.halloween.value            : ENTRANCES_HALLOWEEN,
    APHelper.western.value              : ENTRANCES_WESTERN,
    APHelper.onsen.value                : ENTRANCES_ONSEN,
    APHelper.snowfesta.value            : ENTRANCES_SNOWFESTA,
    APHelper.edotown.value              : ENTRANCES_EDOTOWN,
    APHelper.heaven.value               : ENTRANCES_HEAVEN,
    APHelper.toyhouse.value             : ENTRANCES_TOYHOUSE,
    APHelper.iceland.value              : ENTRANCES_ICELAND,
    APHelper.arabian.value              : ENTRANCES_ARABIAN,
    APHelper.asia.value                 : ENTRANCES_ASIA,
    APHelper.plane.value                : ENTRANCES_PLANE,
    APHelper.hong.value                 : ENTRANCES_HONG,
    APHelper.bay.value                  : ENTRANCES_BAY,
    APHelper.tomo.value                 : ENTRANCES_TOMO,
    APHelper.space.value                : ENTRANCES_SPACE,
}