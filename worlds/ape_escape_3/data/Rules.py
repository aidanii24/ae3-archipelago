from dataclasses import dataclass
from typing import Callable, Sequence, Set

from .Locations import MONKEYS_DIRECTORY
from .Logic import Rulesets, AccessRule, ProgressionMode, event_not_invoked, has_keys, event_invoked
from .Strings import Loc, Stage, Game
from .Stages import AE3EntranceMeta, LEVELS_BY_ORDER, STAGES_DIRECTORY


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
    camera_rules : dict[str, list[str]]
    entrances : dict[str, list[AE3EntranceMeta]]

    default_critical_rule : Set[Callable] = [AccessRule.CATCH]
    final_level_rule : Set[Callable] = {AccessRule.DASH, AccessRule.SWIM, AccessRule.SLING, AccessRule.RCC,
                                        AccessRule.MAGICIAN, AccessRule.KUNGFU, AccessRule.HERO, AccessRule.MONKEY}

    # Set Required Keys for each level depending on the Progression Type
    def get_channel_clear_rules(self, channel_name) -> Rulesets:
        rules : Rulesets = Rulesets()
        if not channel_name in STAGES_DIRECTORY:
            return rules

        # Entrance Rules
        if channel_name in STAGES_DIRECTORY:
            regions: Sequence[str] = STAGES_DIRECTORY[channel_name]
            for region in regions:
                if region in self.entrances:
                    for entrance in self.entrances[region]:
                        rules.Rules.update(entrance.rules.Rules)

                        # Check for critical rules as well
                        if entrance.rules.Critical and entrance.destination != Stage.region_asia_e.value:
                            rules.Critical.update(entrance.rules.Critical)

        # Monkey Rules
        if channel_name in MONKEYS_DIRECTORY:
            rules.Critical.update([AccessRule.CATCH])
            monkeys : Sequence[str] = MONKEYS_DIRECTORY[channel_name]
            for monkey in monkeys:
                if monkey in self.monkey_rules:
                    rules.Rules.update(self.monkey_rules[monkey].rules.Rules)

        return rules

    def set_keys_rules(self, progression : ProgressionMode):
        self.entrances.setdefault(Stage.travel_station_a.value, []).clear()
        self.entrances.setdefault(Stage.travel_station_a.value, []).append(
            AE3EntranceMeta(Stage.travel_station_b.value))

        levels_count = 0
        for sets, levels in enumerate(progression.value):
            extra : int = 0
            if sets < 1:
                extra = 1

            for _ in range(levels + extra):
                access_rule : Callable | frozenset[Callable] | Set[Callable] | None = None

                if sets > 0:
                    access_rule = has_keys(sets)
                elif sets == len(progression.value):
                    access_rule = frozenset({*self.final_level_rule.add(has_keys(sets - 1))})

                entrance : AE3EntranceMeta = AE3EntranceMeta(LEVELS_BY_ORDER[levels_count], access_rule)
                self.entrances.setdefault(Stage.travel_station_a.value, []).append(entrance)

                levels_count += 1

class Casual(RuleType):
    """
    RuleType for a casual experience. The player is assumed to play the game without any or little advanced or obscure
    knowledge of it.
    """
    monkey_rules = {
        # Seaside
        Loc.seaside_morella.value           : RuleWrap(AccessRule.SHOOT, AccessRule.FLY,
                                                       frozenset({AccessRule.MAGICIAN, AccessRule.CLUB})),

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
        Loc.arabian_minimon.value           : RuleWrap(AccessRule.MAGICIAN),

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
        Loc.plane_mukita.value              : RuleWrap(AccessRule.MAGICIAN),
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
        Loc.tomo_riley.value                : RuleWrap(AccessRule.MAGICIAN),
        Loc.tomo_pipo_ron.value             : RuleWrap(AccessRule.KUNGFU),
        Loc.tomo_sal_13.value               : RuleWrap(AccessRule.ATTACK),
        Loc.tomo_sal_12.value               : RuleWrap(AccessRule.ATTACK),

        # Space
        Loc.space_miluchy.value             : RuleWrap(AccessRule.SHOOT, AccessRule.FLY),
        Loc.space_freet.value               : RuleWrap(AccessRule.ATTACK),
        Loc.space_chico.value               : RuleWrap(AccessRule.ATTACK),
        Loc.space_rokkun.value              : RuleWrap(AccessRule.RCC),
        Loc.space_ukki_love.value           : RuleWrap(AccessRule.MAGICIAN),
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
        Stage.title_screen.value            : [AE3EntranceMeta(Stage.zero.value),
                                               AE3EntranceMeta(Stage.travel_station_a.value)],

        # Level Select
        Stage.travel_station_a.value        : [AE3EntranceMeta(Stage.travel_station_b.value),
                                               AE3EntranceMeta(Stage.region_seaside_a.value),
                                               AE3EntranceMeta(Stage.region_woods_a.value),
                                               AE3EntranceMeta(Stage.region_castle_a.value),

                                               AE3EntranceMeta(Stage.region_boss1.value, has_keys(1)),

                                               AE3EntranceMeta(Stage.region_ciscocity_a.value, has_keys(2)),
                                               AE3EntranceMeta(Stage.region_studio_a.value, has_keys(2)),
                                               AE3EntranceMeta(Stage.region_halloween_a1.value, has_keys(2)),
                                               AE3EntranceMeta(Stage.region_western_a.value, has_keys(2)),

                                               AE3EntranceMeta(Stage.region_boss2.value, has_keys(3)),

                                               AE3EntranceMeta(Stage.region_onsen_a.value, has_keys(4)),
                                               AE3EntranceMeta(Stage.region_snowfesta_a.value, has_keys(4)),
                                               AE3EntranceMeta(Stage.region_edotown_a.value, has_keys(4)),

                                               AE3EntranceMeta(Stage.region_boss3.value, has_keys(5)),

                                               AE3EntranceMeta(Stage.region_heaven_a1.value, has_keys(6)),
                                               AE3EntranceMeta(Stage.region_toyhouse_a.value, has_keys(6)),
                                               AE3EntranceMeta(Stage.region_iceland_a.value, has_keys(6)),
                                               AE3EntranceMeta(Stage.region_arabian_a.value, has_keys(6)),

                                               AE3EntranceMeta(Stage.region_boss4.value, has_keys(7)),

                                               AE3EntranceMeta(Stage.region_asia_a.value, has_keys(8)),
                                               AE3EntranceMeta(Stage.region_plane_a.value, has_keys(8)),
                                               AE3EntranceMeta(Stage.region_hong_a.value, has_keys(8)),

                                               AE3EntranceMeta(Stage.region_boss5.value, has_keys(9)),

                                               AE3EntranceMeta(Stage.region_bay_a.value, has_keys(10)),
                                               AE3EntranceMeta(Stage.region_tomo_a1.value, has_keys(10)),

                                               AE3EntranceMeta(Stage.region_boss6.value, has_keys(11)),

                                               AE3EntranceMeta(Stage.region_space_a.value, has_keys(12)),

                                               AE3EntranceMeta(Stage.region_specter1.value, has_keys(13)),
                                               AE3EntranceMeta(Stage.region_specter2.value, has_keys(13))],

        Stage.travel_station_b.value        : [AE3EntranceMeta(Stage.travel_station_a.value)],

        # Zero
        Stage.zero.value                    : [AE3EntranceMeta(Stage.travel_station_a.value)],

        # Seaside
        Stage.region_seaside_a.value               : [AE3EntranceMeta(Stage.region_seaside_b.value),
                                                      AE3EntranceMeta(Stage.region_seaside_c.value, AccessRule.MONKEY)],
        Stage.region_seaside_b.value               : [AE3EntranceMeta(Stage.region_seaside_a.value)],
        Stage.region_seaside_c.value               : [AE3EntranceMeta(Stage.region_seaside_a.value)],

        # Woods
        Stage.region_woods_a.value                 : [AE3EntranceMeta(Stage.region_woods_b.value),
                                                      AE3EntranceMeta(Stage.region_woods_d.value, AccessRule.MONKEY)],
        Stage.region_woods_b.value                 : [AE3EntranceMeta(Stage.region_woods_a.value),
                                                      AE3EntranceMeta(Stage.region_woods_c.value)],
        Stage.region_woods_c.value                 : [AE3EntranceMeta(Stage.region_woods_b.value)],
        Stage.region_woods_d.value                 : [AE3EntranceMeta(Stage.region_woods_a.value)],

        # Castle
        Stage.region_castle_a.value                : [AE3EntranceMeta(Stage.region_castle_d.value),
                                                      AE3EntranceMeta(Stage.region_castle_b.value)],
        Stage.region_castle_b.value                : [AE3EntranceMeta(Stage.region_castle_a.value),
                                                      AE3EntranceMeta(Stage.region_castle_c.value),
                                                      AE3EntranceMeta(Stage.region_castle_d.value),
                                                      AE3EntranceMeta(Stage.region_castle_e.value, AccessRule.MONKEY)],
        Stage.region_castle_c.value                : [AE3EntranceMeta(Stage.region_castle_b.value)],
        Stage.region_castle_d.value                : [AE3EntranceMeta(Stage.region_castle_a.value),
                                                      AE3EntranceMeta(Stage.region_castle_b.value)],
        Stage.region_castle_e.value                : [AE3EntranceMeta(Stage.region_castle_b.value),
                                                      AE3EntranceMeta(Stage.region_castle_f.value)],
        Stage.region_castle_f.value                : [AE3EntranceMeta(Stage.region_castle_e.value)],

        # Boss1
        Stage.region_boss1.value                   : None,

        # Ciscocity
        Stage.region_ciscocity_a.value             : [AE3EntranceMeta(Stage.region_ciscocity_b.value),
                                                      AE3EntranceMeta(Stage.region_ciscocity_c.value),
                                                      AE3EntranceMeta(Stage.region_ciscocity_d.value)],
        Stage.region_ciscocity_b.value             : [AE3EntranceMeta(Stage.region_ciscocity_a.value)],
        Stage.region_ciscocity_c.value             : [AE3EntranceMeta(Stage.region_ciscocity_a.value),
                                                      AE3EntranceMeta(Stage.region_ciscocity_e.value)],
        Stage.region_ciscocity_d.value             : [AE3EntranceMeta(Stage.region_ciscocity_a.value,
                                                                      AccessRule.DASH, AccessRule.RCC)],
        Stage.region_ciscocity_e.value             : [AE3EntranceMeta(Stage.region_ciscocity_c.value, AccessRule.MONKEY)],

        # Studio
        Stage.region_studio_a.value                : [AE3EntranceMeta(Stage.region_studio_b.value, AccessRule.SHOOT,
                                                                      AccessRule.GLIDE, AccessRule.MAGICIAN),
                                                      AE3EntranceMeta(Stage.region_studio_c.value),
                                                      AE3EntranceMeta(Stage.region_studio_a1.value,
                                                                      event_invoked(Game.shortcut_studio_ad.value)),
                                                      AE3EntranceMeta(Stage.region_studio_e.value)],
        Stage.region_studio_a1.value               : [AE3EntranceMeta(Stage.region_studio_a.value),
                                                      AE3EntranceMeta(Stage.region_studio_d.value)],
        Stage.region_studio_b.value                : [AE3EntranceMeta(Stage.region_studio_a.value),
                                                      AE3EntranceMeta(Stage.region_studio_f.value)],
        Stage.region_studio_c.value                : [AE3EntranceMeta(Stage.region_studio_a.value),
                                                      AE3EntranceMeta(Stage.region_studio_e.value)],
        Stage.region_studio_d.value                : [AE3EntranceMeta(Stage.region_studio_a1.value, AccessRule.SHOOT),
                                                      AE3EntranceMeta(Stage.region_studio_f.value),
                                                      AE3EntranceMeta(Stage.region_studio_g.value, AccessRule.MONKEY)],
        Stage.region_studio_e.value                : [AE3EntranceMeta(Stage.region_studio_a.value),
                                                      AE3EntranceMeta(Stage.region_studio_c.value)],
        Stage.region_studio_f.value                : [AE3EntranceMeta(Stage.region_studio_b.value),
                                                      AE3EntranceMeta(Stage.region_studio_d.value)],
        Stage.region_studio_g.value                : [AE3EntranceMeta(Stage.region_studio_d.value)],

        # Halloween
        Stage.region_halloween_a1.value            : [AE3EntranceMeta(Stage.region_halloween_a.value,
                                                                      AccessRule.SWIM, AccessRule.HERO)],
        Stage.region_halloween_a.value             : [AE3EntranceMeta(Stage.region_halloween_a1.value,
                                                                      AccessRule.SWIM, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_halloween_b.value)],
        Stage.region_halloween_b.value             : [AE3EntranceMeta(Stage.region_halloween_a.value),
                                                      AE3EntranceMeta(Stage.region_halloween_f.value,
                                                                      AccessRule.CLUB, AccessRule.SLING,
                                                                      AccessRule.MORPH_NO_MONKEY)],
        Stage.region_halloween_c.value             : [AE3EntranceMeta(Stage.region_halloween_c1.value),
                                                      AE3EntranceMeta(Stage.region_halloween_d.value)],
        Stage.region_halloween_c1.value            : [AE3EntranceMeta(Stage.region_halloween_c.value,
                                                                      AccessRule.SWIM, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_halloween_f.value)],
        Stage.region_halloween_d.value             : [AE3EntranceMeta(Stage.region_halloween_c.value),
                                                      AE3EntranceMeta(Stage.region_halloween_e.value, AccessRule.MONKEY)],
        Stage.region_halloween_e.value             : [AE3EntranceMeta(Stage.region_halloween_d.value)],
        Stage.region_halloween_f.value             : [AE3EntranceMeta(Stage.region_halloween_b.value),
                                                      AE3EntranceMeta(Stage.region_halloween_c1.value)],

        # Western
        Stage.region_western_a.value               : [AE3EntranceMeta(Stage.region_western_b.value),
                                                      AE3EntranceMeta(Stage.region_western_f.value)],
        Stage.region_western_b.value               : [AE3EntranceMeta(Stage.region_western_a.value)],
        Stage.region_western_c.value               : [AE3EntranceMeta(Stage.region_western_e.value)],
        Stage.region_western_d.value               : [AE3EntranceMeta(Stage.region_western_e.value),
                                                      AE3EntranceMeta(Stage.region_western_f.value)],
        Stage.region_western_e.value               : [AE3EntranceMeta(Stage.region_western_d.value),
                                                      AE3EntranceMeta(Stage.region_western_c.value, AccessRule.MONKEY)],
        Stage.region_western_f.value               : [AE3EntranceMeta(Stage.region_western_a.value),
                                                      AE3EntranceMeta(Stage.region_western_d.value)],

        # Boss2
        Stage.region_boss2.value                   : None,

        # Onsen
        Stage.region_onsen_a.value                 : [AE3EntranceMeta(Stage.region_onsen_a1.value),
                                                      AE3EntranceMeta(Stage.region_onsen_a2.value)],
        Stage.region_onsen_a1.value                : [AE3EntranceMeta(Stage.region_onsen_a.value),
                                                      AE3EntranceMeta(Stage.region_onsen_a2.value,
                                                                      AccessRule.GLIDE, AccessRule.MAGICIAN),
                                                      AE3EntranceMeta(Stage.region_onsen_b1.value,
                                                                      AccessRule.DASH, AccessRule.RCC)],
        Stage.region_onsen_a2.value                : [AE3EntranceMeta(Stage.region_onsen_a.value),
                                                      AE3EntranceMeta(Stage.region_onsen_a1.value,
                                                                      AccessRule.GLIDE, AccessRule.MAGICIAN),
                                                      AE3EntranceMeta(Stage.region_onsen_b1.value,
                                                                      AccessRule.DASH, AccessRule.RCC)],
        Stage.region_onsen_b1.value                : [AE3EntranceMeta(Stage.region_onsen_a1.value),
                                                      AE3EntranceMeta(Stage.region_onsen_a2.value),
                                                      AE3EntranceMeta(Stage.region_onsen_b.value,
                                                               AccessRule.GLIDE, AccessRule.RCC)],
        Stage.region_onsen_b.value                 : [AE3EntranceMeta(Stage.region_onsen_b1.value),
                                                      AE3EntranceMeta(Stage.region_onsen_b2.value, AccessRule.FLY),
                                                      AE3EntranceMeta(Stage.region_onsen_d1.value,
                                                                      AccessRule.SHOOT, AccessRule.RCC),
                                                      AE3EntranceMeta(Stage.region_onsen_e.value)],
        Stage.region_onsen_b2.value                : [AE3EntranceMeta(Stage.region_onsen_b.value),
                                                      AE3EntranceMeta(Stage.region_onsen_d.value)],
        Stage.region_onsen_c.value                 : [AE3EntranceMeta(Stage.region_onsen_d.value)],
        Stage.region_onsen_d.value                 : [AE3EntranceMeta(Stage.region_onsen_b2.value),
                                                      AE3EntranceMeta(Stage.region_onsen_c.value, AccessRule.MONKEY),
                                                      AE3EntranceMeta(Stage.region_onsen_d1.value,
                                                                      AccessRule.DASH, AccessRule.RCC)],
        Stage.region_onsen_d1.value                : [AE3EntranceMeta(Stage.region_onsen_b.value),
                                                      AE3EntranceMeta(Stage.region_onsen_d.value, AccessRule.RCC)],
        Stage.region_onsen_e.value                 : [AE3EntranceMeta(Stage.region_onsen_b.value)],

        # Snowfesta
        Stage.region_snowfesta_a.value             : [AE3EntranceMeta(Stage.region_snowfesta_b.value,
                                                                      AccessRule.DASH, AccessRule.RCC),
                                                      AE3EntranceMeta(Stage.region_snowfesta_c.value),
                                                      AE3EntranceMeta(Stage.region_snowfesta_g.value)],
        Stage.region_snowfesta_b.value             : [AE3EntranceMeta(Stage.region_snowfesta_a.value)],
        Stage.region_snowfesta_c.value             : [AE3EntranceMeta(Stage.region_snowfesta_a.value),
                                                      AE3EntranceMeta(Stage.region_snowfesta_e.value),
                                                      AE3EntranceMeta(Stage.region_snowfesta_f.value)],
        Stage.region_snowfesta_d.value             : [AE3EntranceMeta(Stage.region_snowfesta_g.value)],
        Stage.region_snowfesta_e.value             : [AE3EntranceMeta(Stage.region_snowfesta_c.value)],
        Stage.region_snowfesta_f.value             : [AE3EntranceMeta(Stage.region_snowfesta_c.value)],
        Stage.region_snowfesta_g.value             : [AE3EntranceMeta(Stage.region_snowfesta_a.value, AccessRule.MONKEY),
                                                      AE3EntranceMeta(Stage.region_snowfesta_d.value)],

        # Edotown
        Stage.region_edotown_a.value               : [AE3EntranceMeta(Stage.region_edotown_b1.value)],
        Stage.region_edotown_b1.value              : [AE3EntranceMeta(Stage.region_edotown_a.value),
                                                      AE3EntranceMeta(Stage.region_edotown_b.value, AccessRule.NINJA)],
        Stage.region_edotown_b.value               : [AE3EntranceMeta(Stage.region_edotown_b1.value,
                                                                      AccessRule.NINJA, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_edotown_c1.value),
                                                      AE3EntranceMeta(Stage.region_edotown_e.value,
                                                                      event_invoked(Game.shortcut_edotown_eb.value))],
        Stage.region_edotown_c1.value              : [AE3EntranceMeta(Stage.region_edotown_b.value),
                                                      AE3EntranceMeta(Stage.region_edotown_c.value,
                                                               AccessRule.NINJA, AccessRule.HERO)],
        Stage.region_edotown_c.value               : [AE3EntranceMeta(Stage.region_edotown_c1.value,
                                                                      AccessRule.NINJA, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_edotown_d.value)],
        Stage.region_edotown_d.value               : [AE3EntranceMeta(Stage.region_edotown_c.value),
                                                      AE3EntranceMeta(Stage.region_edotown_e.value),
                                                      AE3EntranceMeta(Stage.region_edotown_f.value, AccessRule.MONKEY)],
        Stage.region_edotown_e.value               : [AE3EntranceMeta(Stage.region_edotown_d.value),
                                                      AE3EntranceMeta(Stage.region_edotown_b.value)],
        Stage.region_edotown_f.value               : [AE3EntranceMeta(Stage.region_edotown_d.value)],

        # Boss3
        Stage.region_boss3.value                   : None,

        # Heaven
        Stage.region_heaven_a1.value               : [AE3EntranceMeta(Stage.region_heaven_a.value, AccessRule.GLIDE)],
        Stage.region_heaven_a.value                : [AE3EntranceMeta(Stage.region_heaven_a1.value, AccessRule.GLIDE),
                                                      AE3EntranceMeta(Stage.region_heaven_a2.value, AccessRule.GLIDE)],
        Stage.region_heaven_a2.value               : [AE3EntranceMeta(Stage.region_heaven_a.value, AccessRule.GLIDE),
                                                      AE3EntranceMeta(Stage.region_heaven_b.value)],
        Stage.region_heaven_b.value                : [AE3EntranceMeta(Stage.region_heaven_a2.value, AccessRule.GLIDE),
                                                      AE3EntranceMeta(Stage.region_heaven_c.value)],
        Stage.region_heaven_c.value                : [AE3EntranceMeta(Stage.region_heaven_b.value),
                                                      AE3EntranceMeta(Stage.region_heaven_d.value),
                                                      AE3EntranceMeta(Stage.region_heaven_e.value, AccessRule.MONKEY)],
        Stage.region_heaven_d.value                : [AE3EntranceMeta(Stage.region_heaven_c.value)],
        Stage.region_heaven_e.value                : [AE3EntranceMeta(Stage.region_heaven_c.value)],

        # Toyhouse
        Stage.region_toyhouse_a.value              : [AE3EntranceMeta(Stage.region_toyhouse_b.value),
                                                      AE3EntranceMeta(Stage.region_toyhouse_c.value),
                                                      AE3EntranceMeta(Stage.region_toyhouse_d.value),
                                                      AE3EntranceMeta(Stage.region_toyhouse_e.value),
                                                      AE3EntranceMeta(Stage.region_toyhouse_g.value)],
        Stage.region_toyhouse_b.value              : [AE3EntranceMeta(Stage.region_toyhouse_a.value)],
        Stage.region_toyhouse_c.value              : [AE3EntranceMeta(Stage.region_toyhouse_a.value)],
        Stage.region_toyhouse_d.value              : [AE3EntranceMeta(Stage.region_toyhouse_a.value),
                                                      AE3EntranceMeta(Stage.region_toyhouse_h.value, AccessRule.MONKEY)],
        Stage.region_toyhouse_e.value              : [AE3EntranceMeta(Stage.region_toyhouse_a.value),
                                                      AE3EntranceMeta(Stage.region_toyhouse_e1.value, AccessRule.NINJA)],
        Stage.region_toyhouse_e1.value             : [AE3EntranceMeta(Stage.region_toyhouse_f.value)],
        Stage.region_toyhouse_f.value              : [AE3EntranceMeta(Stage.region_toyhouse_a.value),
                                                      AE3EntranceMeta(Stage.region_toyhouse_e1.value)],
        Stage.region_toyhouse_g.value              : [AE3EntranceMeta(Stage.region_toyhouse_a.value)],
        Stage.region_toyhouse_h.value              : [AE3EntranceMeta(Stage.region_toyhouse_d.value)],

        # Iceland
        Stage.region_iceland_a.value               : [AE3EntranceMeta(Stage.region_iceland_d.value)],
        Stage.region_iceland_b.value               : [AE3EntranceMeta(Stage.region_iceland_c.value),
                                                      AE3EntranceMeta(Stage.region_iceland_e.value)],
        Stage.region_iceland_c.value               : [AE3EntranceMeta(Stage.region_iceland_b.value,
                                                                      AccessRule.CLUB, AccessRule.SLING,
                                                                      AccessRule.MORPH_NO_MONKEY),
                                                      AE3EntranceMeta(Stage.region_iceland_d.value)],
        Stage.region_iceland_d.value               : [AE3EntranceMeta(Stage.region_iceland_a.value),
                                                      AE3EntranceMeta(Stage.region_iceland_c.value)],
        Stage.region_iceland_e.value               : [AE3EntranceMeta(Stage.region_iceland_a.value,
                                                                      event_invoked(Game.trigger_iceland_e.value)),
                                                      AE3EntranceMeta(Stage.region_iceland_b.value),
                                                      AE3EntranceMeta(Stage.region_iceland_f.value, AccessRule.MONKEY)],
        Stage.region_iceland_f.value               : [AE3EntranceMeta(Stage.region_iceland_e.value)],

        # Arabian
        Stage.region_arabian_a.value               : [AE3EntranceMeta(Stage.region_arabian_c.value,
                                                                      frozenset({AccessRule.SLING, AccessRule.RCC})),
                                                      AE3EntranceMeta(Stage.region_arabian_b.value)],
        Stage.region_arabian_b.value               : [AE3EntranceMeta(Stage.region_arabian_a.value),
                                                      AE3EntranceMeta(Stage.region_arabian_e1.value),
                                                      AE3EntranceMeta(Stage.region_arabian_f.value, AccessRule.MONKEY)],
        Stage.region_arabian_c.value               : [AE3EntranceMeta(Stage.region_arabian_a.value),
                                                      AE3EntranceMeta(Stage.region_arabian_c1.value,
                                                                      event_invoked(Game.trigger_arabian_c.value))],
        Stage.region_arabian_c1.value              : [AE3EntranceMeta(Stage.region_arabian_a.value),
                                                      AE3EntranceMeta(Stage.region_arabian_c.value)],
        Stage.region_arabian_e1.value               : [AE3EntranceMeta(Stage.region_arabian_b.value),
                                                       AE3EntranceMeta(Stage.region_arabian_e.value,
                                                                       AccessRule.MAGICIAN)],
        Stage.region_arabian_e.value               : [AE3EntranceMeta(Stage.region_arabian_e1.value),
                                                      AE3EntranceMeta(Stage.region_arabian_g.value)],
        Stage.region_arabian_f.value               : [AE3EntranceMeta(Stage.region_arabian_b.value)],
        Stage.region_arabian_g.value               : [AE3EntranceMeta(Stage.region_arabian_b.value)],

        # Boss4
        Stage.region_boss4.value                   : None,

        # Asia
        Stage.region_asia_a.value                  : [AE3EntranceMeta(Stage.region_asia_a1.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a3.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a4.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a5.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_b.value,
                                                                      AccessRule.SWIM, AccessRule.HERO)],
        Stage.region_asia_a1.value                 : [AE3EntranceMeta(Stage.region_asia_a.value,
                                                                      AccessRule.SWIM, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_asia_a2.value, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_asia_a3.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a4.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a5.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_b2.value,
                                                                      event_invoked(Game.shortcut_asia_b2b.value)),
                                                      AE3EntranceMeta(Stage.region_asia_e1.value, frozenset({
                                                                     event_invoked(Game.trigger_asia_a1.value),
                                                                     event_invoked(Game.trigger_asia_a2.value)
                                                                 }))],
        Stage.region_asia_a2.value                 : [AE3EntranceMeta(Stage.region_asia_a1.value,
                                                                      AccessRule.SWIM, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_asia_a3.value,
                                                                      AccessRule.SWIM, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_asia_d.value),
                                                      AE3EntranceMeta(Stage.region_asia_e1.value,
                                                                      frozenset({
                                                                     event_invoked(Game.trigger_asia_a1.value),
                                                                     event_invoked(Game.trigger_asia_a2.value)
                                                                 }))],
        Stage.region_asia_a3.value                 : [AE3EntranceMeta(Stage.region_asia_a.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a1.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a4.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a5.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_d1.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_e1.value,
                                                                      frozenset({
                                                                     event_invoked(Game.trigger_asia_a1.value),
                                                                     event_invoked(Game.trigger_asia_a2.value)
                                                                 }))
                                                      ],
        Stage.region_asia_a4.value                 : [AE3EntranceMeta(Stage.region_asia_a.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a1.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a3.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a5.value, AccessRule.SWIM)],
        Stage.region_asia_a5.value                 : [AE3EntranceMeta(Stage.region_asia_a.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a1.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a3.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_a4.value, AccessRule.SWIM)],
        Stage.region_asia_b.value                  : [AE3EntranceMeta(Stage.region_asia_a.value,
                                                                      AccessRule.SWIM, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_asia_b1.value,
                                                                      AccessRule.SHOOT, AccessRule.GLIDE),
                                                      AE3EntranceMeta(Stage.region_asia_b2.value, AccessRule.HERO,
                                                                      event_invoked(Game.shortcut_asia_b2b.value))],
        Stage.region_asia_b1.value                 : [AE3EntranceMeta(Stage.region_asia_b.value),
                                                      AE3EntranceMeta(Stage.region_asia_b2.value, AccessRule.SWIM)],
        Stage.region_asia_b2.value                 : [AE3EntranceMeta(Stage.region_asia_a1.value),
                                                      AE3EntranceMeta(Stage.region_asia_b.value),
                                                      AE3EntranceMeta(Stage.region_asia_b1.value, AccessRule.SWIM)],
        Stage.region_asia_d.value                  : [AE3EntranceMeta(Stage.region_asia_d2.value),
                                                      AE3EntranceMeta(Stage.region_asia_a2.value)],
        Stage.region_asia_d1.value                 : [AE3EntranceMeta(Stage.region_asia_a3.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_asia_d2.value, AccessRule.SWIM)],
        Stage.region_asia_d2.value                 : [AE3EntranceMeta(Stage.region_asia_d.value),
                                                      AE3EntranceMeta(Stage.region_asia_d1.value, AccessRule.SWIM)],
        Stage.region_asia_e.value                  : [AE3EntranceMeta(Stage.region_asia_e2.value, frozenset({
                                                                     AccessRule.SWIM, AccessRule.RCC
                                                                 }),
                                                                      frozenset({
                                                                     AccessRule.SWIM, AccessRule.SHOOT
                                                                 }),

                                                                      critical={AccessRule.FLY})],
        Stage.region_asia_e1.value                 : [AE3EntranceMeta(Stage.region_asia_a1.value),
                                                      AE3EntranceMeta(Stage.region_asia_a2.value),
                                                      AE3EntranceMeta(Stage.region_asia_a3.value),
                                                      AE3EntranceMeta(Stage.region_asia_e.value,
                                                               AccessRule.DASH, AccessRule.FLY,
                                                               critical={
                                                                     event_not_invoked(Game.trigger_asia_e.value)
                                                                 }),
                                                      AE3EntranceMeta(Stage.region_asia_a2.value,
                                                               frozenset({
                                                                     AccessRule.SWIM,
                                                                     event_invoked(Game.trigger_asia_e.value)
                                                                 })),
                                                      AE3EntranceMeta(Stage.region_asia_f.value, AccessRule.MONKEY)],
        Stage.region_asia_e2.value                 : [AE3EntranceMeta(Stage.region_asia_e1.value, AccessRule.SWIM,
                                                                      critical={
                                                                     event_invoked(Game.trigger_asia_e.value)
                                                                 }),
                                                      AE3EntranceMeta(Stage.region_asia_a5.value)],
        Stage.region_asia_f.value                  : [AE3EntranceMeta(Stage.region_asia_e1.value)],

        # Plane
        Stage.region_plane_a.value                 : [AE3EntranceMeta(Stage.region_plane_a1.value, AccessRule.NINJA),
                                                      AE3EntranceMeta(Stage.region_plane_c.value, AccessRule.DASH)],
        Stage.region_plane_a1.value                : [AE3EntranceMeta(Stage.region_plane_a.value)],
        Stage.region_plane_b.value                 : [AE3EntranceMeta(Stage.region_plane_f.value),
                                                      AE3EntranceMeta(Stage.region_plane_h.value)],
        Stage.region_plane_b1.value                : [AE3EntranceMeta(Stage.region_plane_b.value),
                                                      AE3EntranceMeta(Stage.region_plane_f1.value),
                                                      AE3EntranceMeta(Stage.region_plane_h.value)],
        Stage.region_plane_c.value                 : [AE3EntranceMeta(Stage.region_plane_a.value),
                                                      AE3EntranceMeta(Stage.region_plane_c1.value, AccessRule.MAGICIAN),
                                                      AE3EntranceMeta(Stage.region_plane_g.value, AccessRule.MONKEY)],
        Stage.region_plane_c1.value                : [AE3EntranceMeta(Stage.region_plane_c.value),
                                                      AE3EntranceMeta(Stage.region_plane_d.value)],
        Stage.region_plane_d.value                 : [AE3EntranceMeta(Stage.region_plane_c1.value),
                                                      AE3EntranceMeta(Stage.region_plane_e.value)],
        Stage.region_plane_e.value                 : [AE3EntranceMeta(Stage.region_plane_d.value),
                                                      AE3EntranceMeta(Stage.region_plane_f.value)],
        Stage.region_plane_f.value                 : [AE3EntranceMeta(Stage.region_plane_b.value),
                                                      AE3EntranceMeta(Stage.region_plane_e.value)],
        Stage.region_plane_f1.value                : [AE3EntranceMeta(Stage.region_plane_b1.value),
                                                      AE3EntranceMeta(Stage.region_plane_f.value)],
        Stage.region_plane_g.value                 : [AE3EntranceMeta(Stage.region_plane_c.value)],
        Stage.region_plane_h.value                 : [AE3EntranceMeta(Stage.region_plane_b.value),
                                                      AE3EntranceMeta(Stage.region_plane_b1.value)],

        # Hong
        Stage.region_hong_a.value                  : [AE3EntranceMeta(Stage.region_hong_a1.value,
                                                                      AccessRule.KUNGFU, AccessRule.HERO)],
        Stage.region_hong_a1.value                 : [AE3EntranceMeta(Stage.region_hong_a.value),
                                                      AE3EntranceMeta(Stage.region_hong_a2.value)],
        Stage.region_hong_a2.value                 : [AE3EntranceMeta(Stage.region_hong_a.value),
                                                      AE3EntranceMeta(Stage.region_hong_a1.value),
                                                      AE3EntranceMeta(Stage.region_hong_b1.value)],
        Stage.region_hong_b.value                  : [AE3EntranceMeta(Stage.region_hong_b1.value),
                                                      AE3EntranceMeta(Stage.region_hong_c.value, AccessRule.KUNGFU),
                                                      AE3EntranceMeta(Stage.region_hong_f.value, AccessRule.MONKEY)],
        Stage.region_hong_b1.value                 : [AE3EntranceMeta(Stage.region_hong_a2.value),
                                                      AE3EntranceMeta(Stage.region_hong_b.value, AccessRule.KUNGFU)],
        Stage.region_hong_c.value                  : [AE3EntranceMeta(Stage.region_hong_b.value),
                                                      AE3EntranceMeta(Stage.region_hong_c1.value, AccessRule.GLIDE),
                                                      AE3EntranceMeta(Stage.region_hong_d.value),
                                                      AE3EntranceMeta(Stage.region_hong_e.value),
                                                      AE3EntranceMeta(Stage.region_hong_h.value)],
        Stage.region_hong_c1.value                 : [AE3EntranceMeta(Stage.region_hong_c.value),
                                                      AE3EntranceMeta(Stage.region_hong_c2.value,
                                                                      AccessRule.NINJA, AccessRule.HERO)],
        Stage.region_hong_c2.value                 : [AE3EntranceMeta(Stage.region_hong_c.value),
                                                      AE3EntranceMeta(Stage.region_hong_c1.value,
                                                               AccessRule.NINJA, AccessRule.HERO)],
        Stage.region_hong_d.value                  : [AE3EntranceMeta(Stage.region_hong_c.value),
                                                      AE3EntranceMeta(Stage.region_hong_g.value, AccessRule.KUNGFU)],
        Stage.region_hong_e.value                  : [AE3EntranceMeta(Stage.region_hong_c.value),
                                                      AE3EntranceMeta(Stage.region_hong_e1.value, frozenset({
                                                   AccessRule.GLIDE, AccessRule.KUNGFU
                                               }))],
        Stage.region_hong_e1.value                 : [AE3EntranceMeta(Stage.region_hong_e.value)],
        Stage.region_hong_f.value                  : [AE3EntranceMeta(Stage.region_hong_b.value)],
        Stage.region_hong_g.value                  : [AE3EntranceMeta(Stage.region_hong_d.value, AccessRule.KUNGFU)],
        Stage.region_hong_h.value                  : [AE3EntranceMeta(Stage.region_hong_c.value)],

        # boss5
        Stage.region_boss5.value                   : None,

        # Bay
        Stage.region_bay_a.value                   : [AE3EntranceMeta(Stage.region_bay_a1.value,
                                                                      frozenset({AccessRule.SHOOT, AccessRule.SWIM}),
                                                                      AccessRule.HERO)],
        Stage.region_bay_a1.value                  : [AE3EntranceMeta(Stage.region_bay_a.value,
                                                                      AccessRule.SWIM, AccessRule.FLY),
                                                      AE3EntranceMeta(Stage.region_bay_a2.value),
                                                      AE3EntranceMeta(Stage.region_bay_b.value, AccessRule.RCC),
                                                      AE3EntranceMeta(Stage.region_bay_e.value, AccessRule.SWIM)],
        Stage.region_bay_a2.value                  : [AE3EntranceMeta(Stage.region_bay_a.value,
                                                                      AccessRule.SWIM, AccessRule.FLY),
                                                      AE3EntranceMeta(Stage.region_bay_a1.value),
                                                      AE3EntranceMeta(Stage.region_bay_a3.value),
                                                      AE3EntranceMeta(Stage.region_bay_a5.value,
                                                                      event_invoked(Game.trigger_bay_a4.value)),
                                                      AE3EntranceMeta(Stage.region_bay_c.value),
                                                      AE3EntranceMeta(Stage.region_bay_e.value, AccessRule.SWIM)],
        Stage.region_bay_a3.value                  : [AE3EntranceMeta(Stage.region_bay_a2.value),
                                                      AE3EntranceMeta(Stage.region_bay_d1.value, AccessRule.SLING)],
        Stage.region_bay_a4.value                  : [AE3EntranceMeta(Stage.region_bay_a2.value)],
        Stage.region_bay_a5.value                  : [AE3EntranceMeta(Stage.region_bay_a2.value),
                                                      AE3EntranceMeta(Stage.region_bay_f.value, AccessRule.MONKEY)],
        Stage.region_bay_b.value                   : [AE3EntranceMeta(Stage.region_bay_a1.value)],
        Stage.region_bay_c.value                   : [AE3EntranceMeta(Stage.region_bay_a2.value),
                                                      AE3EntranceMeta(Stage.region_bay_a4.value)],
        Stage.region_bay_d.value                   : [AE3EntranceMeta(Stage.region_bay_d1.value)],
        Stage.region_bay_d1.value                  : [AE3EntranceMeta(Stage.region_bay_a3.value),
                                                      AE3EntranceMeta(Stage.region_bay_d.value, AccessRule.KUNGFU)],
        Stage.region_bay_e.value                   : [AE3EntranceMeta(Stage.region_bay_a1.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_bay_a2.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_bay_e1.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_bay_e2.value,
                                                                      event_invoked(Game.trigger_bay_a4.value))],
        Stage.region_bay_e1.value                  : [AE3EntranceMeta(Stage.region_bay_e.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_bay_e2.value,
                                                                      event_invoked(Game.trigger_bay_a4.value))],
        Stage.region_bay_e2.value                  : [AE3EntranceMeta(Stage.region_bay_e.value),
                                                      AE3EntranceMeta(Stage.region_bay_e1.value),
                                                      AE3EntranceMeta(Stage.region_bay_e3.value, AccessRule.FLY)],
        Stage.region_bay_e3.value                  : [AE3EntranceMeta(Stage.region_bay_e2.value)],
        Stage.region_bay_f.value                   : [AE3EntranceMeta(Stage.region_bay_a5.value)],

        # Tomo
        Stage.region_tomo_a1.value                 : [AE3EntranceMeta(Stage.region_tomo_a.value, AccessRule.HERO)],
        Stage.region_tomo_a.value                  : [AE3EntranceMeta(Stage.region_tomo_a1.value, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_tomo_j.value)],
        Stage.region_tomo_b.value                  : [AE3EntranceMeta(Stage.region_tomo_j.value),
                                                      AE3EntranceMeta(Stage.region_tomo_c.value)],
        Stage.region_tomo_c.value                  : [AE3EntranceMeta(Stage.region_tomo_b.value),
                                                      AE3EntranceMeta(Stage.region_tomo_e.value)],
        Stage.region_tomo_e.value                  : [AE3EntranceMeta(Stage.region_tomo_c.value),
                                                      AE3EntranceMeta(Stage.region_tomo_e1.value, AccessRule.RCC),
                                                      AE3EntranceMeta(Stage.region_tomo_i.value, frozenset({
                                                   AccessRule.MONKEY, AccessRule.KNIGHT
                                               }))],
        Stage.region_tomo_e1.value                 : [AE3EntranceMeta(Stage.region_tomo_e.value),
                                                      AE3EntranceMeta(Stage.region_tomo_e2.value, AccessRule.KUNGFU)],
        Stage.region_tomo_e2.value                 : [AE3EntranceMeta(Stage.region_tomo_e1.value),
                                                      AE3EntranceMeta(Stage.region_tomo_f.value)],
        Stage.region_tomo_f.value                  : [AE3EntranceMeta(Stage.region_tomo_e2.value),
                                                      AE3EntranceMeta(Stage.region_tomo_f1.value,
                                                                      AccessRule.NINJA, AccessRule.HERO)],
        Stage.region_tomo_f1.value                 : [AE3EntranceMeta(Stage.region_tomo_f.value,
                                                                      AccessRule.NINJA, AccessRule.HERO),
                                                      AE3EntranceMeta(Stage.region_tomo_g.value)],
        Stage.region_tomo_f2.value                 : [AE3EntranceMeta(Stage.region_tomo_g1.value),
                                                      AE3EntranceMeta(Stage.region_tomo_h.value)],
        Stage.region_tomo_g.value                  : [AE3EntranceMeta(Stage.region_tomo_f1.value),
                                                      AE3EntranceMeta(Stage.region_tomo_g1.value, AccessRule.KUNGFU)],
        Stage.region_tomo_g1.value                 : [AE3EntranceMeta(Stage.region_tomo_g.value),
                                                      AE3EntranceMeta(Stage.region_tomo_f2.value, AccessRule.RCC)],
        Stage.region_tomo_h.value                  : [AE3EntranceMeta(Stage.region_tomo_f2.value),
                                                      AE3EntranceMeta(Stage.region_tomo_h1.value, AccessRule.SHOOT)],
        Stage.region_tomo_h1.value                 : [AE3EntranceMeta(Stage.travel_station_a.value)],
        Stage.region_tomo_i.value                  : [AE3EntranceMeta(Stage.region_tomo_e.value)],
        Stage.region_tomo_j.value                  : [AE3EntranceMeta(Stage.region_tomo_a.value),
                                                      AE3EntranceMeta(Stage.region_tomo_b.value)],

        # boss6
        Stage.region_boss6.value                   : None,

        # Space
        Stage.region_space_a.value                 : [AE3EntranceMeta(Stage.region_space_b.value)],
        Stage.region_space_b.value                 : [AE3EntranceMeta(Stage.region_space_a.value),
                                                      AE3EntranceMeta(Stage.region_space_d.value),
                                                      AE3EntranceMeta(Stage.region_space_e1.value),
                                                      AE3EntranceMeta(Stage.region_space_f.value),
                                                      AE3EntranceMeta(Stage.region_space_g.value),
                                                      AE3EntranceMeta(Stage.region_space_i.value, frozenset({
                                                   event_invoked(Game.trigger_space_e.value),
                                                   event_invoked(Game.trigger_space_f2.value),
                                                   event_invoked(Game.trigger_space_g2.value),
                                               }))],
        Stage.region_space_d.value                 : [AE3EntranceMeta(Stage.region_space_b.value)],
        Stage.region_space_e.value                 : [AE3EntranceMeta(Stage.region_space_e1.value),
                                                      AE3EntranceMeta(Stage.region_space_h.value, AccessRule.MONKEY)],
        Stage.region_space_e1.value                : [AE3EntranceMeta(Stage.region_space_b.value),
                                                      AE3EntranceMeta(Stage.region_space_e.value, frozenset({
                                                   AccessRule.MORPH_NO_MONKEY, AccessRule.SHOOT
                                               }))],
        Stage.region_space_f.value                 : [AE3EntranceMeta(Stage.region_space_b.value),
                                                      AE3EntranceMeta(Stage.region_space_f1.value, AccessRule.GLIDE)],
        Stage.region_space_f1.value                : [AE3EntranceMeta(Stage.region_space_f.value),
                                                      AE3EntranceMeta(Stage.region_space_f2.value, AccessRule.KUNGFU)],
        Stage.region_space_f2.value                : [AE3EntranceMeta(Stage.region_space_f1.value),
                                                      AE3EntranceMeta(Stage.region_space_f.value)],
        Stage.region_space_g.value                 : [AE3EntranceMeta(Stage.region_space_b.value),
                                                      AE3EntranceMeta(Stage.region_space_g1.value, AccessRule.SWIM),
                                                      AE3EntranceMeta(Stage.region_space_g2.value,
                                                                      event_invoked(Game.trigger_space_g1.value))],
        Stage.region_space_g1.value                : [AE3EntranceMeta(Stage.region_space_g1.value)],
        Stage.region_space_g2.value                : [AE3EntranceMeta(Stage.region_space_g.value)],
        Stage.region_space_h.value                 : [AE3EntranceMeta(Stage.region_space_e.value),
                                                      AE3EntranceMeta(Stage.region_space_k.value)],
        Stage.region_space_i.value                 : [AE3EntranceMeta(Stage.region_space_b.value),
                                                      AE3EntranceMeta(Stage.region_space_j.value)],
        Stage.region_space_j.value                 : [AE3EntranceMeta(Stage.region_space_i.value),
                                                      AE3EntranceMeta(Stage.region_space_l.value, AccessRule.GLIDE)],
        Stage.region_space_k.value                 : [AE3EntranceMeta(Stage.region_space_h.value)],
        Stage.region_space_l.value                 : [AE3EntranceMeta(Stage.travel_station_a.value)],

        # Specter
        Stage.region_specter1.value                : None,
        Stage.region_specter2.value                : None
    }
