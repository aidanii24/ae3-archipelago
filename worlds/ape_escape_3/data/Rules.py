from typing import Callable, Set
from dataclasses import dataclass

from .Logic import Rulesets, AccessRule, event_not_invoked, has_keys, event_invoked
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

        # Woods
        Loc.woods_kreemon.value             : RuleWrap(AccessRule.ATTACK),

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
        Loc.onsen_mujakin.value             : RuleWrap(AccessRule.ATTACK),
        Loc.onsen_fuji_chan.value           : RuleWrap(AccessRule.SHOOT, AccessRule.NINJA),

        # Snowfesta
        Loc.snowfesta_kimisuke.value        : RuleWrap(AccessRule.SHOOT),
        Loc.snowfesta_mitsuro.value         : RuleWrap(AccessRule.SHOOT),

        # Edotown
        Loc.edotown_walter.value            : RuleWrap(AccessRule.NINJA),
        Loc.edotown_monkibeth.value         : RuleWrap(AccessRule.NINJA),

        # Heaven
        Loc.heaven_chomon.value             : RuleWrap(AccessRule.RCC),
        Loc.heaven_tami.value               : RuleWrap(AccessRule.ATTACK),

        # Toyhouse
        Loc.toyhouse_monto.value            : RuleWrap(AccessRule.SHOOT, AccessRule.NINJA),
        Loc.toyhouse_mokitani.value         : RuleWrap(AccessRule.RCC),

        # Iceland
        Loc.iceland_jolly_mon.value         : RuleWrap(event_invoked(Game.trigger_iceland_e.value)),
        Loc.iceland_hikkori.value           : RuleWrap(event_invoked(Game.trigger_iceland_e.value)),
        Loc.iceland_rammy.value             : RuleWrap(event_invoked(Game.trigger_iceland_e.value)),

        # Arabian
        Loc.arabian_minimon.value           : RuleWrap(AccessRule.GENIE),

        # Asia
        Loc.asia_baku.value                 : RuleWrap(frozenset({AccessRule.SHOOT, AccessRule.SWIM})),
        Loc.asia_mohcha.value               : RuleWrap(AccessRule.RCC),
        Loc.asia_gimchin.value              : RuleWrap(AccessRule.FLY, AccessRule.SHOOT),
        Loc.asia_takumon.value              : RuleWrap(AccessRule.SWIM, AccessRule.NINJA, AccessRule.HERO,
                                                       AccessRule.COWBOY),
        Loc.asia_ukki_ether.value           : RuleWrap(AccessRule.SWIM),

        # Plane
        Loc.plane_pont.value                : RuleWrap(AccessRule.RCC, AccessRule.HERO),
        Loc.plane_gamish.value              : RuleWrap(AccessRule.RCC, AccessRule.HERO),
        Loc.plane_mukita.value              : RuleWrap(AccessRule.GENIE),
        Loc.plane_jeloh.value               : RuleWrap(AccessRule.ATTACK),
        Loc.plane_bongo.value               : RuleWrap(AccessRule.ATTACK),

        # Hong
        Loc.hong_ukki_chan.value            : RuleWrap(AccessRule.SHOOT),
        Loc.hong_uki_uki.value              : RuleWrap(AccessRule.SHOOT, AccessRule.FLY),
        Loc.hong_muki_muki.value            : RuleWrap(AccessRule.SHOOT, AccessRule.FLY),
        Loc.hong_bankan.value               : RuleWrap(AccessRule.NINJA, AccessRule.HERO),
        Loc.hong_sukei.value                : RuleWrap(AccessRule.SHOOT, AccessRule.NINJA),
        Loc.hong_block_master.value         : RuleWrap(frozenset({AccessRule.GLIDE, AccessRule.KUNGFU})),

        # Bay
        Loc.bay_shiny_pete.value            : RuleWrap(AccessRule.SHOOT),
        Loc.bay_gimo.value                  : RuleWrap(AccessRule.SHOOT),
        Loc.bay_nakabi.value                : RuleWrap(AccessRule.ATTACK),
        Loc.bay_gimi_gimi.value             : RuleWrap(AccessRule.ATTACK),
        Loc.bay_pokkini.value               : RuleWrap(AccessRule.ATTACK),
        Loc.bay_jimo.value                  : RuleWrap(AccessRule.SWIM),

        # Tomo
        Loc.tomo_kichibeh.value             : RuleWrap(AccessRule.ATTACK),
        Loc.tomo_bonchicchi.value           : RuleWrap(AccessRule.ATTACK),
        Loc.tomo_mikibon.value              : RuleWrap(AccessRule.ATTACK),
        Loc.tomo_chimpy.value               : RuleWrap(AccessRule.NINJA),
        Loc.tomo_kajitan.value              : RuleWrap(AccessRule.NINJA),
        Loc.tomo_uka_uka.value              : RuleWrap(AccessRule.NINJA),
        Loc.tomo_mil_mil.value              : RuleWrap(AccessRule.NINJA),
        Loc.tomo_tomio.value                : RuleWrap(AccessRule.ATTACK),
        Loc.tomo_gario.value                : RuleWrap(AccessRule.ATTACK),
        Loc.tomo_riley.value                : RuleWrap(AccessRule.GENIE),
        Loc.tomo_pipo_ron.value             : RuleWrap(AccessRule.KUNGFU),
        Loc.tomo_sal_13.value               : RuleWrap(AccessRule.ATTACK),
        Loc.tomo_sal_12.value               : RuleWrap(AccessRule.ATTACK),

        # Space
        Loc.space_miluchy.value             : RuleWrap(AccessRule.SHOOT, AccessRule.FLY),
        Loc.space_freet.value               : RuleWrap(AccessRule.ATTACK),
        Loc.space_chico.value               : RuleWrap(AccessRule.ATTACK),
        Loc.space_rokkun.value              : RuleWrap(AccessRule.RCC),
        Loc.space_ukki_love.value           : RuleWrap(AccessRule.GENIE),
        Loc.space_sal_10.value              : RuleWrap(AccessRule.ATTACK),
        Loc.space_sal_11.value              : RuleWrap(AccessRule.ATTACK),
        Loc.space_sal_3000.value            : RuleWrap(AccessRule.ATTACK),

        # Bosses
        Loc.boss_monkey_white.value         : RuleWrap(AccessRule.ATTACK),
        Loc.boss_monkey_blue.value          : RuleWrap(AccessRule.ATTACK),
        Loc.boss_monkey_yellow.value        : RuleWrap(AccessRule.ATTACK),
        Loc.boss_monkey_pink.value          : RuleWrap(AccessRule.ATTACK),
        Loc.boss_monkey_red.value           : RuleWrap(AccessRule.ATTACK),
        Loc.boss_specter.value              : RuleWrap(AccessRule.SHOOT),
        Loc.boss_specter_final.value        : RuleWrap(AccessRule.ATTACK),
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

                                               StageEntranceMeta(Stage.boss3.value, has_keys(5)),

                                               StageEntranceMeta(Stage.heaven_a1.value, has_keys(6)),
                                               StageEntranceMeta(Stage.toyhouse_a.value, has_keys(6)),
                                               StageEntranceMeta(Stage.iceland_a.value, has_keys(6)),
                                               StageEntranceMeta(Stage.arabian_a.value, has_keys(6)),

                                               StageEntranceMeta(Stage.boss4.value, has_keys(7)),

                                               StageEntranceMeta(Stage.asia_a.value, has_keys(8)),
                                               StageEntranceMeta(Stage.plane_a.value, has_keys(8)),
                                               StageEntranceMeta(Stage.hong_a.value, has_keys(8)),

                                               StageEntranceMeta(Stage.boss5.value, has_keys(9)),

                                               StageEntranceMeta(Stage.bay_a.value, has_keys(10)),
                                               StageEntranceMeta(Stage.tomo_a1.value, has_keys(10)),

                                               StageEntranceMeta(Stage.boss6.value, has_keys(11)),

                                               StageEntranceMeta(Stage.space_a.value, has_keys(12)),

                                               StageEntranceMeta(Stage.specter1.value, has_keys(13)),
                                               StageEntranceMeta(Stage.specter2.value, has_keys(13))],

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
                                               StageEntranceMeta(Stage.halloween_f.value,
                                                                 AccessRule.CLUB, AccessRule.SLING,
                                                                 AccessRule.MORPH_NO_MONKEY)],
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
        Stage.boss3.value                   : None,

        # Heaven
        Stage.heaven_a1.value               : [StageEntranceMeta(Stage.heaven_a.value, AccessRule.GLIDE)],
        Stage.heaven_a.value                : [StageEntranceMeta(Stage.heaven_a1.value, AccessRule.GLIDE),
                                               StageEntranceMeta(Stage.heaven_a2.value, AccessRule.GLIDE)],
        Stage.heaven_a2.value               : [StageEntranceMeta(Stage.heaven_a.value, AccessRule.GLIDE),
                                               StageEntranceMeta(Stage.heaven_b.value)],
        Stage.heaven_b.value                : [StageEntranceMeta(Stage.heaven_a2.value, AccessRule.GLIDE),
                                               StageEntranceMeta(Stage.heaven_c.value)],
        Stage.heaven_c.value                : [StageEntranceMeta(Stage.heaven_b.value),
                                               StageEntranceMeta(Stage.heaven_d.value),
                                               StageEntranceMeta(Stage.heaven_e.value, AccessRule.MONKEY)],
        Stage.heaven_d.value                : [StageEntranceMeta(Stage.heaven_c.value)],
        Stage.heaven_e.value                : [StageEntranceMeta(Stage.heaven_c.value)],

        # Toyhouse
        Stage.toyhouse_a.value              : [StageEntranceMeta(Stage.toyhouse_b.value),
                                               StageEntranceMeta(Stage.toyhouse_c.value),
                                               StageEntranceMeta(Stage.toyhouse_d.value),
                                               StageEntranceMeta(Stage.toyhouse_e.value),
                                               StageEntranceMeta(Stage.toyhouse_g.value)],
        Stage.toyhouse_b.value              : [StageEntranceMeta(Stage.toyhouse_a.value)],
        Stage.toyhouse_c.value              : [StageEntranceMeta(Stage.toyhouse_a.value)],
        Stage.toyhouse_d.value              : [StageEntranceMeta(Stage.toyhouse_a.value),
                                               StageEntranceMeta(Stage.toyhouse_h.value, AccessRule.MONKEY)],
        Stage.toyhouse_e.value              : [StageEntranceMeta(Stage.toyhouse_a.value),
                                               StageEntranceMeta(Stage.toyhouse_e1.value, AccessRule.NINJA)],
        Stage.toyhouse_e1.value             : [StageEntranceMeta(Stage.toyhouse_f.value)],
        Stage.toyhouse_f.value              : [StageEntranceMeta(Stage.toyhouse_a.value),
                                               StageEntranceMeta(Stage.toyhouse_e1.value)],
        Stage.toyhouse_g.value              : [StageEntranceMeta(Stage.toyhouse_a.value)],
        Stage.toyhouse_h.value              : [StageEntranceMeta(Stage.toyhouse_d.value)],

        # Iceland
        Stage.iceland_a.value               : [StageEntranceMeta(Stage.iceland_d.value)],
        Stage.iceland_b.value               : [StageEntranceMeta(Stage.iceland_c.value),
                                               StageEntranceMeta(Stage.iceland_e.value)],
        Stage.iceland_c.value               : [StageEntranceMeta(Stage.iceland_b.value,
                                                                 AccessRule.CLUB, AccessRule.SLING,
                                                                 AccessRule.MORPH_NO_MONKEY),
                                               StageEntranceMeta(Stage.iceland_d.value)],
        Stage.iceland_d.value               : [StageEntranceMeta(Stage.iceland_a.value),
                                               StageEntranceMeta(Stage.iceland_c.value)],
        Stage.iceland_e.value               : [StageEntranceMeta(Stage.iceland_a.value,
                                                                 event_invoked(Game.trigger_iceland_e.value)),
                                               StageEntranceMeta(Stage.iceland_b.value),
                                               StageEntranceMeta(Stage.iceland_f.value, AccessRule.MONKEY)],
        Stage.iceland_f.value               : [StageEntranceMeta(Stage.iceland_e.value)],

        # Arabian
        Stage.arabian_a.value               : [StageEntranceMeta(Stage.arabian_c.value,
                                                                 frozenset({AccessRule.SLING, AccessRule.RCC})),
                                               StageEntranceMeta(Stage.arabian_b.value)],
        Stage.arabian_b.value               : [StageEntranceMeta(Stage.arabian_a.value),
                                               StageEntranceMeta(Stage.arabian_e1.value),
                                               StageEntranceMeta(Stage.arabian_f.value, AccessRule.MONKEY)],
        Stage.arabian_c.value               : [StageEntranceMeta(Stage.arabian_a.value),
                                               StageEntranceMeta(Stage.arabian_c1.value,
                                                                 event_invoked(Game.trigger_arabian_c.value))],
        Stage.arabian_c1.value              : [StageEntranceMeta(Stage.arabian_a.value),
                                               StageEntranceMeta(Stage.arabian_c.value)],
        Stage.arabian_e1.value               : [StageEntranceMeta(Stage.arabian_b.value),
                                                StageEntranceMeta(Stage.arabian_e.value,
                                                                  AccessRule.GENIE)],
        Stage.arabian_e.value               : [StageEntranceMeta(Stage.arabian_e1.value)],
        Stage.arabian_f.value               : [StageEntranceMeta(Stage.arabian_b.value)],

        # Boss4
        Stage.boss4.value                   : None,

        # Asia
        Stage.asia_a.value                  : [StageEntranceMeta(Stage.asia_a1.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a3.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a4.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a5.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_b.value,
                                                                 AccessRule.SWIM, AccessRule.HERO)],
        Stage.asia_a1.value                 : [StageEntranceMeta(Stage.asia_a.value,
                                                                 AccessRule.SWIM, AccessRule.HERO),
                                               StageEntranceMeta(Stage.asia_a2.value, AccessRule.HERO),
                                               StageEntranceMeta(Stage.asia_a3.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a4.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a5.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_b2.value,
                                                                 event_invoked(Game.shortcut_asia_b2b.value)),
                                               StageEntranceMeta(Stage.asia_e1.value,frozenset({
                                                                     event_invoked(Game.trigger_asia_a1.value),
                                                                     event_invoked(Game.trigger_asia_a2.value)
                                                                 }))],
        Stage.asia_a2.value                 : [StageEntranceMeta(Stage.asia_a1.value,
                                                                 AccessRule.SWIM, AccessRule.HERO),
                                               StageEntranceMeta(Stage.asia_a3.value,
                                                                 AccessRule.SWIM, AccessRule.HERO),
                                               StageEntranceMeta(Stage.asia_d.value),
                                               StageEntranceMeta(Stage.asia_e1.value,
                                                                 frozenset({
                                                                     event_invoked(Game.trigger_asia_a1.value),
                                                                     event_invoked(Game.trigger_asia_a2.value)
                                                                 }))],
        Stage.asia_a3.value                 : [StageEntranceMeta(Stage.asia_a.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a1.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a4.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a5.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_d1.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_e1.value,
                                                                 frozenset({
                                                                     event_invoked(Game.trigger_asia_a1.value),
                                                                     event_invoked(Game.trigger_asia_a2.value)
                                                                 }))
                                               ],
        Stage.asia_a4.value                 : [StageEntranceMeta(Stage.asia_a.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a1.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a3.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a5.value, AccessRule.SWIM)],
        Stage.asia_a5.value                 : [StageEntranceMeta(Stage.asia_a.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a1.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a3.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_a4.value, AccessRule.SWIM)],
        Stage.asia_b.value                  : [StageEntranceMeta(Stage.asia_a.value,
                                                                 AccessRule.SWIM, AccessRule.HERO),
                                               StageEntranceMeta(Stage.asia_b1.value,
                                                                 AccessRule.SHOOT, AccessRule.GLIDE),
                                               StageEntranceMeta(Stage.asia_b2.value, AccessRule.HERO,
                                                                 event_invoked(Game.shortcut_asia_b2b.value))],
        Stage.asia_b1.value                 : [StageEntranceMeta(Stage.asia_b.value),
                                               StageEntranceMeta(Stage.asia_b2.value, AccessRule.SWIM)],
        Stage.asia_b2.value                 : [StageEntranceMeta(Stage.asia_a1.value),
                                               StageEntranceMeta(Stage.asia_b.value),
                                               StageEntranceMeta(Stage.asia_b1.value, AccessRule.SWIM)],
        Stage.asia_d.value                  : [StageEntranceMeta(Stage.asia_d2.value),
                                               StageEntranceMeta(Stage.asia_a2.value)],
        Stage.asia_d1.value                 : [StageEntranceMeta(Stage.asia_a3.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.asia_d2.value, AccessRule.SWIM)],
        Stage.asia_d2.value                 : [StageEntranceMeta(Stage.asia_d.value),
                                               StageEntranceMeta(Stage.asia_d1.value, AccessRule.SWIM)],
        Stage.asia_e.value                  : [StageEntranceMeta(Stage.asia_e2.value,frozenset({
                                                                     AccessRule.SWIM, AccessRule.RCC
                                                                 }),
                                                                 frozenset({
                                                                     AccessRule.SWIM, AccessRule.SHOOT
                                                                 }),

                                                                 critical={AccessRule.FLY})],
        Stage.asia_e1.value                 : [StageEntranceMeta(Stage.asia_a1.value),
                                               StageEntranceMeta(Stage.asia_a2.value),
                                               StageEntranceMeta(Stage.asia_a3.value),
                                               StageEntranceMeta(Stage.asia_e.value,
                                                                 AccessRule.DASH, AccessRule.FLY,
                                                                 critical={
                                                                     event_not_invoked(Game.trigger_asia_e.value)
                                                                 }),
                                               StageEntranceMeta(Stage.asia_a2.value,
                                                                 frozenset({
                                                                     AccessRule.SWIM,
                                                                     event_invoked(Game.trigger_asia_e.value)
                                                                 })),
                                               StageEntranceMeta(Stage.asia_f.value, AccessRule.MONKEY)],
        Stage.asia_e2.value                 : [StageEntranceMeta(Stage.asia_e1.value, AccessRule.SWIM,
                                                                 critical={
                                                                     event_invoked(Game.trigger_asia_e.value)
                                                                 }),
                                               StageEntranceMeta(Stage.asia_a5.value)],
        Stage.asia_f.value                  : [StageEntranceMeta(Stage.asia_e1.value)],

        # Plane
        Stage.plane_a.value                 : [StageEntranceMeta(Stage.plane_a1.value, AccessRule.NINJA),
                                               StageEntranceMeta(Stage.plane_c.value, AccessRule.DASH)],
        Stage.plane_a1.value                : [StageEntranceMeta(Stage.plane_a.value)],
        Stage.plane_b.value                 : [StageEntranceMeta(Stage.plane_f.value),
                                               StageEntranceMeta(Stage.plane_h.value)],
        Stage.plane_b1.value                : [StageEntranceMeta(Stage.plane_b.value),
                                               StageEntranceMeta(Stage.plane_f1.value),
                                               StageEntranceMeta(Stage.plane_h.value)],
        Stage.plane_c.value                 : [StageEntranceMeta(Stage.plane_a.value),
                                               StageEntranceMeta(Stage.plane_c1.value, AccessRule.GENIE),
                                               StageEntranceMeta(Stage.plane_g.value, AccessRule.MONKEY)],
        Stage.plane_c1.value                : [StageEntranceMeta(Stage.plane_c.value),
                                               StageEntranceMeta(Stage.plane_d.value)],
        Stage.plane_d.value                 : [StageEntranceMeta(Stage.plane_c1.value),
                                               StageEntranceMeta(Stage.plane_e.value)],
        Stage.plane_e.value                 : [StageEntranceMeta(Stage.plane_d.value),
                                               StageEntranceMeta(Stage.plane_f.value)],
        Stage.plane_f.value                 : [StageEntranceMeta(Stage.plane_b.value),
                                               StageEntranceMeta(Stage.plane_e.value)],
        Stage.plane_f1.value                : [StageEntranceMeta(Stage.plane_b1.value),
                                               StageEntranceMeta(Stage.plane_f.value)],
        Stage.plane_g.value                 : [StageEntranceMeta(Stage.plane_c.value)],
        Stage.plane_h.value                 : [StageEntranceMeta(Stage.plane_b.value),
                                               StageEntranceMeta(Stage.plane_b1.value)],

        # Hong
        Stage.hong_a.value                  : [StageEntranceMeta(Stage.hong_a1.value,
                                                                 AccessRule.KUNGFU, AccessRule.HERO)],
        Stage.hong_a1.value                 : [StageEntranceMeta(Stage.hong_a.value),
                                               StageEntranceMeta(Stage.hong_a2.value)],
        Stage.hong_a2.value                 : [StageEntranceMeta(Stage.hong_a.value),
                                               StageEntranceMeta(Stage.hong_a1.value),
                                               StageEntranceMeta(Stage.hong_b1.value)],
        Stage.hong_b.value                  : [StageEntranceMeta(Stage.hong_b1.value),
                                               StageEntranceMeta(Stage.hong_c.value, AccessRule.KUNGFU),
                                               StageEntranceMeta(Stage.hong_f.value, AccessRule.MONKEY)],
        Stage.hong_b1.value                 : [StageEntranceMeta(Stage.hong_a2.value),
                                               StageEntranceMeta(Stage.hong_b.value, AccessRule.KUNGFU)],
        Stage.hong_c.value                  : [StageEntranceMeta(Stage.hong_b.value),
                                               StageEntranceMeta(Stage.hong_c1.value, AccessRule.GLIDE),
                                               StageEntranceMeta(Stage.hong_d.value),
                                               StageEntranceMeta(Stage.hong_e.value),
                                               StageEntranceMeta(Stage.hong_h.value)],
        Stage.hong_c1.value                 : [StageEntranceMeta(Stage.hong_c.value),
                                               StageEntranceMeta(Stage.hong_c2.value,
                                                                 AccessRule.NINJA, AccessRule.HERO)],
        Stage.hong_c2.value                 : [StageEntranceMeta(Stage.hong_c.value),
                                               StageEntranceMeta(Stage.hong_c1.value,
                                                                 AccessRule.NINJA, AccessRule.HERO)],
        Stage.hong_d.value                  : [StageEntranceMeta(Stage.hong_c.value),
                                               StageEntranceMeta(Stage.hong_g.value, AccessRule.KUNGFU)],
        Stage.hong_e.value                  : [StageEntranceMeta(Stage.hong_c.value),
                                               StageEntranceMeta(Stage.hong_e1.value, frozenset({
                                                   AccessRule.GLIDE, AccessRule.KUNGFU
                                               }))],
        Stage.hong_e1.value                 : [StageEntranceMeta(Stage.hong_e.value)],
        Stage.hong_f.value                  : [StageEntranceMeta(Stage.hong_b.value)],
        Stage.hong_g.value                  : [StageEntranceMeta(Stage.hong_d.value, AccessRule.KUNGFU)],
        Stage.hong_h.value                  : [StageEntranceMeta(Stage.hong_c.value)],

        # boss5
        Stage.boss5.value                   : None,

        # Bay
        Stage.bay_a.value                   : [StageEntranceMeta(Stage.bay_a1.value,
                                                                 frozenset({AccessRule.SHOOT, AccessRule.SWIM}),
                                                                 AccessRule.HERO)],
        Stage.bay_a1.value                  : [StageEntranceMeta(Stage.bay_a.value,
                                                                 AccessRule.SWIM, AccessRule.FLY),
                                               StageEntranceMeta(Stage.bay_a2.value),
                                               StageEntranceMeta(Stage.bay_b.value, AccessRule.RCC),
                                               StageEntranceMeta(Stage.bay_e.value, AccessRule.SWIM)],
        Stage.bay_a2.value                  : [StageEntranceMeta(Stage.bay_a.value,
                                                                 AccessRule.SWIM, AccessRule.FLY),
                                               StageEntranceMeta(Stage.bay_a1.value),
                                               StageEntranceMeta(Stage.bay_a3.value),
                                               StageEntranceMeta(Stage.bay_a5.value,
                                                                 event_invoked(Game.trigger_bay_a4.value)),
                                               StageEntranceMeta(Stage.bay_c.value),
                                               StageEntranceMeta(Stage.bay_e.value, AccessRule.SWIM)],
        Stage.bay_a3.value                  : [StageEntranceMeta(Stage.bay_a2.value),
                                               StageEntranceMeta(Stage.bay_d1.value, AccessRule.SLING)],
        Stage.bay_a4.value                  : [StageEntranceMeta(Stage.bay_a2.value)],
        Stage.bay_a5.value                  : [StageEntranceMeta(Stage.bay_a2.value),
                                               StageEntranceMeta(Stage.bay_f.value, AccessRule.MONKEY)],
        Stage.bay_b.value                   : [StageEntranceMeta(Stage.bay_a1.value)],
        Stage.bay_c.value                   : [StageEntranceMeta(Stage.bay_a2.value),
                                               StageEntranceMeta(Stage.bay_a4.value)],
        Stage.bay_d.value                   : [StageEntranceMeta(Stage.bay_d1.value)],
        Stage.bay_d1.value                  : [StageEntranceMeta(Stage.bay_a3.value),
                                               StageEntranceMeta(Stage.bay_d.value, AccessRule.KUNGFU)],
        Stage.bay_e.value                   : [StageEntranceMeta(Stage.bay_a1.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.bay_a2.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.bay_e1.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.bay_e2.value,
                                                                 event_invoked(Game.trigger_bay_a4.value))],
        Stage.bay_e1.value                  : [StageEntranceMeta(Stage.bay_e.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.bay_e2.value,
                                                                 event_invoked(Game.trigger_bay_a4.value))],
        Stage.bay_e2.value                  : [StageEntranceMeta(Stage.bay_e.value),
                                               StageEntranceMeta(Stage.bay_e1.value),
                                               StageEntranceMeta(Stage.bay_e3.value, AccessRule.FLY)],
        Stage.bay_e3.value                  : [StageEntranceMeta(Stage.bay_e2.value)],
        Stage.bay_f.value                   : [StageEntranceMeta(Stage.bay_a5.value)],

        # Tomo
        Stage.tomo_a1.value                 : [StageEntranceMeta(Stage.tomo_a.value, AccessRule.HERO)],
        Stage.tomo_a.value                  : [StageEntranceMeta(Stage.tomo_a1.value, AccessRule.HERO),
                                               StageEntranceMeta(Stage.tomo_j.value)],
        Stage.tomo_b.value                  : [StageEntranceMeta(Stage.tomo_j.value),
                                               StageEntranceMeta(Stage.tomo_c.value)],
        Stage.tomo_c.value                  : [StageEntranceMeta(Stage.tomo_b.value),
                                               StageEntranceMeta(Stage.tomo_e.value)],
        Stage.tomo_e.value                  : [StageEntranceMeta(Stage.tomo_c.value),
                                               StageEntranceMeta(Stage.tomo_e1.value, AccessRule.RCC),
                                               StageEntranceMeta(Stage.tomo_i.value, frozenset({
                                                   AccessRule.MONKEY, AccessRule.KNIGHT
                                               }))],
        Stage.tomo_e1.value                 : [StageEntranceMeta(Stage.tomo_e.value),
                                               StageEntranceMeta(Stage.tomo_e2.value, AccessRule.KUNGFU)],
        Stage.tomo_e2.value                 : [StageEntranceMeta(Stage.tomo_e1.value),
                                               StageEntranceMeta(Stage.tomo_f.value)],
        Stage.tomo_f.value                  : [StageEntranceMeta(Stage.tomo_e2.value),
                                               StageEntranceMeta(Stage.tomo_f1.value,
                                                                 AccessRule.NINJA, AccessRule.HERO)],
        Stage.tomo_f1.value                 : [StageEntranceMeta(Stage.tomo_f.value,
                                                                 AccessRule.NINJA, AccessRule.HERO),
                                               StageEntranceMeta(Stage.tomo_g.value)],
        Stage.tomo_f2.value                 : [StageEntranceMeta(Stage.tomo_g1.value),
                                               StageEntranceMeta(Stage.tomo_h.value)],
        Stage.tomo_g.value                  : [StageEntranceMeta(Stage.tomo_f1.value),
                                               StageEntranceMeta(Stage.tomo_g1.value, AccessRule.KUNGFU)],
        Stage.tomo_g1.value                 : [StageEntranceMeta(Stage.tomo_g.value),
                                               StageEntranceMeta(Stage.tomo_f2.value, AccessRule.RCC)],
        Stage.tomo_h.value                  : [StageEntranceMeta(Stage.tomo_f2.value),
                                               StageEntranceMeta(Stage.tomo_h1.value, AccessRule.SHOOT)],
        Stage.tomo_h1.value                 : [StageEntranceMeta(Stage.travel_station_a.value)],
        Stage.tomo_i.value                  : [StageEntranceMeta(Stage.tomo_e.value)],
        Stage.tomo_j.value                  : [StageEntranceMeta(Stage.tomo_a.value),
                                               StageEntranceMeta(Stage.tomo_b.value)],

        # boss6
        Stage.boss6.value                   : None,

        # Space
        Stage.space_a.value                 : [StageEntranceMeta(Stage.space_b.value)],
        Stage.space_b.value                 : [StageEntranceMeta(Stage.space_a.value),
                                               StageEntranceMeta(Stage.space_d.value),
                                               StageEntranceMeta(Stage.space_e1.value),
                                               StageEntranceMeta(Stage.space_f.value),
                                               StageEntranceMeta(Stage.space_g.value),
                                               StageEntranceMeta(Stage.space_i.value, frozenset({
                                                   event_invoked(Game.trigger_space_e.value),
                                                   event_invoked(Game.trigger_space_f2.value),
                                                   event_invoked(Game.trigger_space_g2.value),
                                               }))],
        Stage.space_d.value                 : [StageEntranceMeta(Stage.space_b.value)],
        Stage.space_e.value                 : [StageEntranceMeta(Stage.space_e1.value),
                                               StageEntranceMeta(Stage.space_h.value, AccessRule.MONKEY)],
        Stage.space_e1.value                : [StageEntranceMeta(Stage.space_b.value),
                                               StageEntranceMeta(Stage.space_e.value, frozenset({
                                                   AccessRule.MORPH_NO_MONKEY, AccessRule.SHOOT
                                               }))],
        Stage.space_f.value                 : [StageEntranceMeta(Stage.space_b.value),
                                               StageEntranceMeta(Stage.space_f1.value, AccessRule.GLIDE)],
        Stage.space_f1.value                : [StageEntranceMeta(Stage.space_f.value),
                                               StageEntranceMeta(Stage.space_f2.value, AccessRule.KUNGFU)],
        Stage.space_f2.value                : [StageEntranceMeta(Stage.space_f1.value),
                                               StageEntranceMeta(Stage.space_f.value)],
        Stage.space_g.value                 : [StageEntranceMeta(Stage.space_b.value),
                                               StageEntranceMeta(Stage.space_g1.value, AccessRule.SWIM),
                                               StageEntranceMeta(Stage.space_g2.value,
                                                                 event_invoked(Game.trigger_space_g1.value))],
        Stage.space_g1.value                : [StageEntranceMeta(Stage.space_g1.value)],
        Stage.space_g2.value                : [StageEntranceMeta(Stage.space_g.value)],
        Stage.space_h.value                 : [StageEntranceMeta(Stage.space_e.value),
                                               StageEntranceMeta(Stage.space_k.value)],
        Stage.space_i.value                 : [StageEntranceMeta(Stage.space_b.value),
                                               StageEntranceMeta(Stage.space_j.value)],
        Stage.space_j.value                 : [StageEntranceMeta(Stage.space_i.value),
                                               StageEntranceMeta(Stage.space_l.value, AccessRule.GLIDE)],
        Stage.space_k.value                 : [StageEntranceMeta(Stage.space_h.value)],
        Stage.space_l.value                 : [StageEntranceMeta(Stage.travel_station_a.value)],

        # Specter
        Stage.specter1.value                : None,
        Stage.specter2.value                : None
    }
