from typing import TYPE_CHECKING, Callable, Set
from warnings import warn

from BaseClasses import CollectionState

from .Locations import CAMERAS_INDEX, CAMERAS_MASTER, CELLPHONES_INDEX, Cellphone_Name_to_ID, MONKEYS_BOSSES, \
    MONKEYS_BREAK_ROOMS, MONKEYS_INDEX, MONKEYS_MASTER, MONKEYS_PASSWORDS, generate_name_to_id
from .Logic import Rulesets, AccessRule, ProgressionMode, has_keys, event_invoked
from .Strings import Loc, Stage, Events
from .Stages import STAGES_DIRECTORY, ENTRANCES_STAGE_SELECT

if TYPE_CHECKING:
    from ..AE3_Client import AE3Context


class GoalTarget:
    name : str = "Empty Goal"
    description : str = "A Generic Goal Target"

    locations : set[str] = {}
    location_ids : set[int] = {}

    amount : int = 0

    def __init__(self, excluded_stages : list[str] = None, excluded_locations : list[str] = None,
                 additional_locations : list[str] = None):
        if not self.locations:
            return

        if excluded_locations is None:
            excluded_locations = []

        if excluded_stages is None:
            excluded_stages = []

        if additional_locations is None:
            additional_locations = []

        # Add Extra Locations
        self.locations = {*self.locations, *additional_locations}

        # Exclude Specified Locations if any
        locations_excluded : list[str] = excluded_locations if excluded_locations else []
        if excluded_stages:
            for stage in excluded_stages:
                locations_excluded.extend( locations for locations in MONKEYS_INDEX.get(stage, []) )
                locations_excluded.extend( locations for locations in CAMERAS_INDEX.get(stage, []) )
                locations_excluded.extend( locations for locations in CELLPHONES_INDEX.get(stage, []) )

        if locations_excluded:
            actual : str = "Actual:" if self.locations else "[ No Set Locations ] |"
            for location in self.locations:
                actual += f"> {location}"

            self.locations.difference_update(set(locations_excluded))
            if len(self.locations) <= 0:
                excluded : str = "Excluded:"
                for stage in excluded_stages:
                    excluded += f"> {stage}"

                for location in locations_excluded:
                    excluded += f">{location} |"

                raise AssertionError(f"There are no locations to check. Please reduce the excluded locations.",
                                     f"{actual}", f"{excluded}")
            elif len(self.locations) < self.amount:
                warn("Number of Locations required to check for Goal has been reduced due to excluded locations.")
                self.amount = len(self.locations)

        self.location_ids = {generate_name_to_id()[location] for location in self.locations}

        if not self.amount or self.amount is None:
            self.amount = len(self.locations)

    def __bool__(self) -> bool:
        return bool(self.amount)

    def __str__(self):
        return self.name + "\n         [ " + self.description + " ]"

    def exclude(self, locations : list[str] = None):
        if locations is None or not locations:
            self.locations = { location for location in self.locations if location not in locations }
            self.location_ids = {generate_name_to_id()[location] for location in self.locations}

    def append(self, *locations : str):
        self.locations = { * self.locations, *locations }

    async def check(self, ctx : 'AE3Context'):
        checked: set[int] = ctx.locations_checked.union(ctx.checked_locations)

        if len(self.location_ids.intersection(checked)) >= self.amount and not ctx.game_goaled:
            await ctx.goal()

    def get_progress(self, ctx : 'AE3Context') -> int:
        checked: set[int] = ctx.locations_checked.union(ctx.checked_locations)
        progress : int = len(self.location_ids.intersection(checked))

        return progress

    def get_remaining(self, ctx : 'AE3Context') -> list[str]:
        checked: set[int] = ctx.locations_checked.union(ctx.checked_locations)
        progressed : set[int] = self.location_ids.intersection(checked)

        name_to_id : dict[str, int] = generate_name_to_id()
        missing : list[str] = [ l for l in self.locations if name_to_id[l] not in progressed]

        return missing

    def verify(self, state : CollectionState, player : int) -> bool:
        for location in self.locations:
            if not state.can_reach_location(location, player):
                return False

        return True

    def as_access_rule(self) -> Callable[[CollectionState, int], bool]:
        return lambda state, player : self.verify(state, player)

class PostGameAccessRule(GoalTarget):
    name: str = "No Post Game Access Rule"
    description: str = ""

    locations: set[str] = {}
    location_ids: set[int] = {}

    amount: int = 0

    def check(self, ctx : 'AE3Context'):
        checked: set[int] = ctx.locations_checked.union(ctx.checked_locations)

        if ctx.unlocked_channels == 0x1A and len(self.location_ids.intersection(checked)) >= self.amount:
            ctx.unlocked_channels = 0x1B


class LogicPreference:
    """
    Base Class for defined RuleTypes. RuleTypes determine the kinds of access rules locations or regions have
    based on a preferred play style
    """
    monkey_rules : dict[str, Rulesets] = {}
    event_rules : dict[str, Rulesets] = {}
    entrance_rules : dict[str, Rulesets] = {}

    default_critical_rule : Set[Callable] = [AccessRule.CATCH]
    small_starting_channels : list[int] = [6, 15, 18, 20, 22, 23]
    final_level_rule : Set[Callable] = {AccessRule.DASH, AccessRule.SWIM, AccessRule.SLING, AccessRule.RCC,
                                        AccessRule.MAGICIAN, AccessRule.KUNGFU, AccessRule.HERO, AccessRule.MONKEY}

    def __init__(self):
        pass

    # Get all Access Rules within the channel
    def get_channel_clear_rules(self, *regions : str) -> Rulesets:
        rules : Rulesets = Rulesets()
        if not regions in STAGES_DIRECTORY:
            return rules

        for region in regions:
            # Entrance Rules
            if region in self.entrance_rules:
                rules.update(self.entrance_rules[region])

            # Monkey Rules
            rules.critical.update(self.default_critical_rule)
            if region in MONKEYS_INDEX:
                for monkey in MONKEYS_INDEX[region]:
                    if monkey in self.monkey_rules:
                        rules.rules.extend(self.monkey_rules[monkey].rules)

        return rules

    def set_level_progression_rules(self, progression : ProgressionMode, post_game_access_rule_option : int = 0,
                                    post_game_rules : list[Callable] = None):
        if post_game_rules is None:
            post_game_rules = []

        levels_count : int = 0
        for sets, levels in enumerate(progression.progression):
            extra : int = 0
            if sets < 1:
                extra = 1

            for _ in range(levels + extra):
                rule : Rulesets = Rulesets()
                req : int = sets

                if sets <= 0:
                    levels_count += 1
                    continue
                elif sets > 0:
                    rule = Rulesets(has_keys(req))

                if sets == len(progression.progression) - 1:
                    if post_game_access_rule_option < 4:
                        req -= 1

                    final_rule : list[Callable] = [has_keys(req)]
                    final_rule.extend(self.final_level_rule)

                    if post_game_rules:
                        final_rule.append(*post_game_rules)

                    rule = Rulesets(final_rule)

                self.entrance_rules[ENTRANCES_STAGE_SELECT[levels_count].name] = rule
                levels_count += 1

# [<--- LOGIC PREFERENCES --->]
class Hard(LogicPreference):
    """
    RuleType for a hard experience. The player is assumed to play the game with in-depth knowledge of the game,
    except any glitches major oversights.
    """

    def __init__(self):
        super().__init__()

        self.small_starting_areas = [6, 18, 20, 22, 23]

        self.monkey_rules.update({
            # Seaside
            Loc.seaside_morella.value       : Rulesets(AccessRule.SHOOT, AccessRule.FLY, AccessRule.MAGICIAN),

            # Woods
            Loc.woods_kreemon.value         : Rulesets(AccessRule.ATTACK),

            # Castle
            Loc.castle_monga.value          : Rulesets(AccessRule.SHOOT, AccessRule.GLIDE),

            # Studio
            Loc.studio_minoh.value          : Rulesets(AccessRule.SHOOT, AccessRule.GLIDE),
            Loc.studio_monta.value          : Rulesets(AccessRule.SHOOT, AccessRule.GLIDE),

            # Onsen
            Loc.onsen_chabimon.value        : Rulesets(AccessRule.RCC),
            Loc.onsen_fuji_chan.value       : Rulesets(AccessRule.SHOOT, AccessRule.NINJA),

            # Snowfesta
            Loc.snowfesta_kimisuke.value    : Rulesets(AccessRule.SHOOT),
            Loc.snowfesta_mitsuro.value     : Rulesets(AccessRule.SHOOT),

            # Heaven
            Loc.heaven_chomon.value         : Rulesets(AccessRule.RCC),

            # Toyhouse
            Loc.toyhouse_monto.value        : Rulesets(AccessRule.SHOOT, AccessRule.FLY),
            Loc.toyhouse_mokitani.value     : Rulesets(AccessRule.RCC),

            # Iceland
            Loc.iceland_jolly_mon.value     : Rulesets(AccessRule.SLING),
            Loc.iceland_hikkori.value       : Rulesets(AccessRule.SLING),
            Loc.iceland_rammy.value         : Rulesets(AccessRule.SLING),

            # Arabian
            Loc.arabian_minimon.value       : Rulesets(AccessRule.MAGICIAN, [AccessRule.DASH,
                                                                             AccessRule.SHOOT_BOOM]),

            # Asia
            Loc.bay_kazuo.value             : Rulesets(AccessRule.NINJA, AccessRule.HERO,
                                                       [AccessRule.SHOOT, AccessRule.SWIM]),
            Loc.asia_mohcha.value           : Rulesets(AccessRule.RCC),
            Loc.asia_takumon.value          : Rulesets(AccessRule.SWIM, AccessRule.CATCH_LONG,
                                                       [AccessRule.KUNGFU, AccessRule.RCC],
                                                       [AccessRule.KUNGFU, AccessRule.CLUB],
                                                       [AccessRule.KUNGFU, AccessRule.SHOOT],),
            Loc.asia_ukki_ether.value       : Rulesets(AccessRule.SWIM, AccessRule.HERO),

            # Plane
            Loc.plane_mukita.value          : Rulesets(AccessRule.MAGICIAN),

            # Hong
            Loc.hong_ukki_chan.value        : Rulesets(AccessRule.SHOOT),
            Loc.hong_uki_uki.value          : Rulesets(AccessRule.SHOOT, AccessRule.FLY),
            Loc.hong_muki_muki.value        : Rulesets(AccessRule.SHOOT, AccessRule.FLY),
            Loc.hong_bankan.value           : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Loc.hong_sukei.value            : Rulesets(AccessRule.SHOOT, AccessRule.NINJA),

            # Bay
            Loc.bay_shiny_pete.value        : Rulesets(AccessRule.SHOOT),
            Loc.bay_gimo.value              : Rulesets(AccessRule.SHOOT),
            Loc.bay_jimo.value              : Rulesets([AccessRule.FLY, AccessRule.KUNGFU, AccessRule.SWIM]),

            # Tomo
            Loc.tomo_riley.value            : Rulesets(AccessRule.MAGICIAN),
            Loc.tomo_pipo_ron.value         : Rulesets(AccessRule.KUNGFU),

            # Space
            Loc.space_rokkun.value          : Rulesets(AccessRule.RCC),
            Loc.space_sal_3000.value        : Rulesets(AccessRule.SHOOT),
        })

        self.event_rules.update({
            # Studio
            Events.studio_b1_button.value               : Rulesets(AccessRule.SHOOT, AccessRule.GLIDE,
                                                                   AccessRule.MAGICIAN),

            # Halloween
            Events.halloween_b1_jumbo_robo_shoot.value  : Rulesets(AccessRule.SHOOT),

            # Edotown
            Events.edotown_e_scroll.value               : Rulesets(AccessRule.CLUB, AccessRule.HOOP,
                                                                   AccessRule.MORPH),

            # Iceland
            Events.iceland_e_button.value               : Rulesets(AccessRule.SLING),

            # Arabian
            Events.arabian_c_golden_mon.value           : Rulesets(AccessRule.CATCH),

            # Asia
            Events.asia_e1_button.value                 : Rulesets(AccessRule.RCC, AccessRule.SHOOT,
                                                                   critical={AccessRule.FLY}),

            # Hong
            Events.hong_b_kungfu.value                  : Rulesets(AccessRule.KUNGFU),

            # Bay
            Events.bay_e1_button.value                  : Rulesets(AccessRule.SHOOT),

            # Tomo
            Events.tomo_e2_kungfu.value                 : Rulesets(AccessRule.KUNGFU),
            Events.tomo_g_button.value                  : Rulesets(AccessRule.RCC),

            # Space
            Events.space_g_button.value                 : Rulesets(AccessRule.SWIM),
            Events.space_f1_kungfu.value                : Rulesets(AccessRule.KUNGFU),
        })

        self.entrance_rules.update({
            # Seaside
            Stage.entrance_seaside_ac.value     : Rulesets(AccessRule.MONKEY),

            # Woods
            Stage.entrance_woods_ad.value       : Rulesets(AccessRule.MONKEY),

            # Castle
            Stage.entrance_castle_aa2.value     : Rulesets(event_invoked(Events.castle_a2_button.value)),
            Stage.entrance_castle_b1b.value     : Rulesets(event_invoked(Events.castle_b_clapper.value)),
            Stage.entrance_castle_be.value      : Rulesets(AccessRule.MONKEY),

            # Ciscocity
            Stage.entrance_ciscocity_ad.value   : Rulesets(AccessRule.DASH, AccessRule.RCC),
            Stage.entrance_ciscocity_ad_2.value : Rulesets(event_invoked(Events.ciscocity_d_exit.value)),
            Stage.entrance_ciscocity_ce         : Rulesets(AccessRule.MONKEY),
            Stage.entrance_ciscocity_c1c.value  : Rulesets(event_invoked(Events.ciscocity_c_button.value)),
            Stage.entrance_ciscocity_cc1.value  : Rulesets(event_invoked(Events.ciscocity_c_button.value)),

            # Studio
            Stage.entrance_studio_aa1.value     : Rulesets(event_invoked(Events.studio_a1_button.value)),
            Stage.entrance_studio_aa2.value     : Rulesets(event_invoked(Events.studio_a2_button.value)),
            Stage.entrance_studio_b1b2.value    : Rulesets(event_invoked(Events.studio_b1_button.value)),
            Stage.entrance_studio_b2b.value     : Rulesets(event_invoked(Events.studio_b1_button.value)),
            Stage.entrance_studio_bb2.value     : Rulesets(event_invoked(Events.studio_b1_button.value)),
            Stage.entrance_studio_ff1.value     : Rulesets(event_invoked(Events.studio_f_tele_robo.value)),
            Stage.entrance_studio_f1f.value     : Rulesets(event_invoked(Events.studio_f_tele_robo.value)),
            Stage.entrance_studio_dg.value      : Rulesets(AccessRule.MONKEY),
            Stage.entrance_studio_dd2.value     : Rulesets(AccessRule.SHOOT),

            # Halloween
            Stage.entrance_halloween_aa1.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_a1a.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_bb1.value  : Rulesets(
                event_invoked(Events.halloween_b_jumbo_robo.value),
                      event_invoked(Events.halloween_b1_jumbo_robo_shoot.value)),
            Stage.entrance_halloween_b1b.value: Rulesets(
                event_invoked(Events.halloween_b_jumbo_robo.value),
                event_invoked(Events.halloween_b1_jumbo_robo_shoot.value)),
            Stage.entrance_halloween_c1c.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_cc1.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_cc2.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_c2c.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_d1e.value  : Rulesets(AccessRule.MONKEY),

            # Western
            Stage.entrance_western_ec.value     : Rulesets(AccessRule.MONKEY),

            # Onsen
            Stage.entrance_onsen_a1a.value      : Rulesets(event_invoked(Events.onsen_a_button.value)),
            Stage.entrance_onsen_a2a.value      : Rulesets(event_invoked(Events.onsen_a_button.value)),
            Stage.entrance_onsen_be.value       : Rulesets(AccessRule.FLY),
            Stage.entrance_onsen_bd1.value      : Rulesets(AccessRule.SHOOT, [AccessRule.RCC, AccessRule.ATTACK]),
            Stage.entrance_onsen_bd.value       : Rulesets(AccessRule.FLY),
            Stage.entrance_onsen_dd1.value      : Rulesets(AccessRule.RCC, AccessRule.DASH),
            Stage.entrance_onsen_d1d.value      : Rulesets(AccessRule.RCC),
            Stage.entrance_onsen_dc.value       : Rulesets(AccessRule.MONKEY),

            # Snowfesta
            Stage.entrance_snowfesta_ab.value   : Rulesets(AccessRule.RCC, AccessRule.DASH),
            Stage.entrance_snowfesta_ag.value   : Rulesets(AccessRule.MONKEY),
            Stage.entrance_snowfesta_ce_2.value : Rulesets(event_invoked(Events.snowfesta_e_bell.value)),
            Stage.entrance_snowfesta_ec.value   : Rulesets(event_invoked(Events.snowfesta_e_bell.value)),

            # Edotown
            Stage.entrance_edotown_b1b2.value   : Rulesets(AccessRule.NINJA),
            Stage.entrance_edotown_b2b1.value   : Rulesets([event_invoked(Events.edotown_b1_button.value),
                                                            AccessRule.NINJA], AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_edotown_be.value     : Rulesets(event_invoked(Events.edotown_e_scroll.value)),
            Stage.entrance_edotown_df.value     : Rulesets(AccessRule.MONKEY),
            Stage.entrance_edotown_eb.value     : Rulesets(event_invoked(Events.edotown_e_scroll.value)),

            # Heaven
            Stage.entrance_heaven_ab.value      : Rulesets(AccessRule.GLIDE),
            Stage.entrance_heaven_ba.value      : Rulesets(AccessRule.GLIDE),
            Stage.entrance_heaven_b1b.value     : Rulesets(event_invoked(Events.heaven_b_clapper.value)),
            Stage.entrance_heaven_ce.value      : Rulesets(AccessRule.MONKEY),

            # Toyhouse
            Stage.entrance_toyhouse_ae.value    : Rulesets(AccessRule.NINJA),
            Stage.entrance_toyhouse_ea.value    : Rulesets(AccessRule.NINJA),
            Stage.entrance_toyhouse_dh.value    : Rulesets(AccessRule.MONKEY),

            # Iceland
            Stage.entrance_iceland_a2e.value    : Rulesets(event_invoked(Events.iceland_e_button.value)),
            Stage.entrance_iceland_ea2.value    : Rulesets(event_invoked(Events.iceland_e_button.value)),
            Stage.entrance_iceland_ef.value     : Rulesets(AccessRule.MONKEY),
            Stage.entrance_iceland_cb.value     : Rulesets(event_invoked(Events.iceland_c_jumbo_robo.value)),

            # Arabian
            Stage.entrance_arabian_ac.value     : Rulesets([AccessRule.RCC, AccessRule.SHOOT]),
            Stage.entrance_arabian_ac1.value    : Rulesets(event_invoked(Events.arabian_c1_exit.value)),
            Stage.entrance_arabian_cc1.value    : Rulesets(event_invoked(Events.arabian_c_golden_mon.value)),
            Stage.entrance_arabian_c1c.value    : Rulesets(event_invoked(Events.arabian_c_golden_mon.value)),
            Stage.entrance_arabian_bg.value     : Rulesets(event_invoked(Events.arabian_g_exit.value)),
            Stage.entrance_arabian_bf.value     : Rulesets(event_invoked(Events.arabian_g_exit.value)),
            Stage.entrance_arabian_e1e.value    : Rulesets(AccessRule.MAGICIAN),

            # Asia
            Stage.entrance_asia_ab.value        : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_asia_ba.value        : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_asia_aa1.value       : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_aa5.value       : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a1a.value       : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_asia_a1b1.value      : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_asia_a1a2.value      : Rulesets(AccessRule.HERO),
            Stage.entrance_asia_a1a3.value      : Rulesets(AccessRule.SWIM, [AccessRule.HERO,
                                                            event_invoked(Events.asia_a2_block.value)]),
            Stage.entrance_asia_a1a4.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a2a1.value      : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_asia_a2a3.value      : Rulesets([event_invoked(Events.asia_a_block.value),
                                                            event_invoked(Events.asia_a1_block.value),
                                                            event_invoked(Events.asia_a2_block.value)],
                                                           AccessRule.HERO),
            Stage.entrance_asia_a2a4.value      : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_asia_a3a1.value      : Rulesets(AccessRule.SWIM, [AccessRule.HERO,
                                                            event_invoked(Events.asia_a2_block.value)]),
            Stage.entrance_asia_a3a4.value      : Rulesets(AccessRule.SWIM, [AccessRule.HERO,
                                                            event_invoked(Events.asia_a2_block.value)]),
            Stage.entrance_asia_a3a2.value      : Rulesets([event_invoked(Events.asia_a_block.value),
                                                            event_invoked(Events.asia_a1_block.value),
                                                            event_invoked(Events.asia_a2_block.value)],
                                                           AccessRule.HERO),
            Stage.entrance_asia_a3e.value       : Rulesets([event_invoked(Events.asia_a_block.value),
                                                            event_invoked(Events.asia_a1_block.value),
                                                            event_invoked(Events.asia_a2_block.value)]),
            Stage.entrance_asia_a4a1.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a4a3.value      : Rulesets(AccessRule.SWIM, [AccessRule.HERO,
                                                            event_invoked(Events.asia_a2_block.value)]),
            Stage.entrance_asia_a4a5.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a5a6.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a6a5.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_bb1.value       : Rulesets(AccessRule.SHOOT, AccessRule.FLY),
            Stage.entrance_asia_bb2.value       : Rulesets(AccessRule.HERO,
                                                           event_invoked(Events.asia_b2_button.value)),
            Stage.entrance_asia_b1b2.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_b2b1.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_d1a4.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_dd1.value       : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_ee1.value       : Rulesets([AccessRule.DASH, AccessRule.RCC]),
            Stage.entrance_asia_ef.value        : Rulesets(AccessRule.MONKEY),
            Stage.entrance_asia_e1e.value       : Rulesets(AccessRule.GLIDE),
            Stage.entrance_asia_e1e2.value      : Rulesets(AccessRule.SHOOT, [AccessRule.ATTACK, AccessRule.RCC],
                                                           critical={AccessRule.FLY}),
            Stage.entrance_asia_e2e.value       : Rulesets([event_invoked(Events.asia_e1_button.value),
                                                            AccessRule.SWIM]),

            # Plane
            Stage.entrance_plane_aa1.value      : Rulesets(AccessRule.NINJA),
            Stage.entrance_plane_ac.value       : Rulesets(AccessRule.RCC, AccessRule.DASH),
            Stage.entrance_plane_cc1.value      : Rulesets(AccessRule.MAGICIAN),
            Stage.entrance_plane_cg.value       : Rulesets(AccessRule.MONKEY),
            Stage.entrance_plane_ed.value       : Rulesets(event_invoked(Events.plane_d_clapper.value)),

            # Hong
            Stage.entrance_hong_aa1.value       : Rulesets(AccessRule.KUNGFU, AccessRule.HERO),
            Stage.entrance_hong_a1a2.value      : Rulesets(AccessRule.HIT),
            Stage.entrance_hong_bb1.value       : Rulesets(AccessRule.KUNGFU),
            Stage.entrance_hong_b1b.value       : Rulesets(event_invoked(Events.hong_b_kungfu.value)),
            Stage.entrance_hong_bb2.value       : Rulesets(event_invoked(Events.hong_b2_button.value)),
            Stage.entrance_hong_b1f.value       : Rulesets(AccessRule.MONKEY),
            Stage.entrance_hong_b2b.value       : Rulesets(event_invoked(Events.hong_b2_button.value)),
            Stage.entrance_hong_cc1.value       : Rulesets(AccessRule.GLIDE),
            Stage.entrance_hong_c1c.value       : Rulesets(AccessRule.GLIDE),
            Stage.entrance_hong_c1c2.value      : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_hong_ee1.value       : Rulesets(AccessRule.KUNGFU),
            Stage.entrance_hong_dg.value        : Rulesets(AccessRule.KUNGFU),

            # Bay
            Stage.entrance_bay_aa1.value        : Rulesets(AccessRule.SHOOT, AccessRule.HERO),
            Stage.entrance_bay_a1a.value        : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_bay_a1b.value        : Rulesets(AccessRule.RCC),
            Stage.entrance_bay_a1a2.value       : Rulesets(AccessRule.SWIM),
            Stage.entrance_bay_a2a1.value       : Rulesets(AccessRule.SWIM),
            Stage.entrance_bay_a2a3.value       : Rulesets(AccessRule.SWIM),
            Stage.entrance_bay_a2e.value        : Rulesets(AccessRule.SWIM),
            Stage.entrance_bay_a3a2.value       : Rulesets(AccessRule.SWIM),
            Stage.entrance_bay_a3a6.value       : Rulesets(event_invoked(Events.bay_a7_button.value)),
            Stage.entrance_bay_a4d1.value       : Rulesets(AccessRule.SLING),
            Stage.entrance_bay_a6f.value        : Rulesets(AccessRule.MONKEY),
            Stage.entrance_bay_d1d.value        : Rulesets(AccessRule.KUNGFU),
            Stage.entrance_bay_ea2.value        : Rulesets(AccessRule.SWIM),
            Stage.entrance_bay_ee1.value        : Rulesets(AccessRule.SHOOT),
            Stage.entrance_bay_ee2.value        : Rulesets(event_invoked(Events.bay_e1_button.value)),
            Stage.entrance_bay_e1e2.value       : Rulesets(AccessRule.HIT),

            # Tomo
            Stage.entrance_tomo_aa1.value       : Rulesets(AccessRule.HERO, AccessRule.NINJA),
            Stage.entrance_tomo_a1a.value       : Rulesets(AccessRule.HERO, AccessRule.NINJA),
            Stage.entrance_tomo_e1i.value       : Rulesets(AccessRule.MONKEY),
            Stage.entrance_tomo_e2e3.value      : Rulesets(AccessRule.KUNGFU),
            Stage.entrance_tomo_e3e2.value      : Rulesets(event_invoked(Events.tomo_e2_kungfu.value)),
            Stage.entrance_tomo_f1f2.value      : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_tomo_f2f1.value      : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_tomo_gg1.value       : Rulesets(AccessRule.KUNGFU),
            Stage.entrance_tomo_g1f.value       : Rulesets(event_invoked(Events.tomo_g_button.value)),
            Stage.entrance_tomo_h1h.value       : Rulesets(AccessRule.GLIDE),
            Stage.entrance_tomo_ha.value        : Rulesets(AccessRule.SHOOT),

            # Space
            Stage.entrance_space_bi.value       : Rulesets([event_invoked(Events.space_e_button.value),
                                                            event_invoked(Events.space_f2_button.value),
                                                            event_invoked(Events.space_g1_button.value),
                                                            event_invoked(Events.space_d_button.value)]),
            Stage.entrance_space_e1e.value      : Rulesets(event_invoked(Events.space_e_button.value)),
            Stage.entrance_space_ee1_2.value    : Rulesets(event_invoked(Events.space_e_button.value)),
            Stage.entrance_space_e1e_2.value    : Rulesets([AccessRule.RCC, AccessRule.MORPH_NO_MONKEY]),
            Stage.entrance_space_ee1.value      : Rulesets(event_invoked(Events.space_e_button.value)),
            Stage.entrance_space_eh.value       : Rulesets(AccessRule.MONKEY),
            Stage.entrance_space_gg1.value      : Rulesets(event_invoked(Events.space_g1_button.value)),
            Stage.entrance_space_gg1_2.value    : Rulesets(AccessRule.SWIM),
            Stage.entrance_space_g1g.value      : Rulesets(event_invoked(Events.space_g_button.value)),
            Stage.entrance_space_g1g_2.value    : Rulesets(event_invoked(Events.space_g1_button.value)),
            Stage.entrance_space_ff2.value      : Rulesets(event_invoked(Events.space_f2_button.value)),
            Stage.entrance_space_ff1.value      : Rulesets(AccessRule.GLIDE),
            Stage.entrance_space_f1f2.value     : Rulesets(AccessRule.KUNGFU),
            Stage.entrance_space_f2f1.value     : Rulesets(event_invoked(Events.space_f1_kungfu.value)),
            Stage.entrance_space_f2f.value      : Rulesets(event_invoked(Events.space_f2_button.value)),
            Stage.entrance_space_dd.value       : Rulesets(AccessRule.ATTACK),
            Stage.entrance_space_dd_2.value     : Rulesets(AccessRule.ATTACK),
            Stage.entrance_space_ib.value       : Rulesets([event_invoked(Events.space_e_button.value),
                                                     event_invoked(Events.space_f2_button.value),
                                                     event_invoked(Events.space_g1_button.value),
                                                     event_invoked(Events.space_d_button.value)]),
            Stage.entrance_space_jj1.value      : Rulesets(AccessRule.GLIDE),
            Stage.entrance_space_j1j.value      : Rulesets(AccessRule.GLIDE),
        })

class Normal(Hard):
    """
    RuleType for a normal experience. Expectations of accessibility will be the same as the vanilla game.
    """

    def __init__(self):
        super().__init__()

        self.small_starting_areas = [6, 9, 11, 15, 18, 20, 22, 23]

        self.monkey_rules.update({
            # Seaside
            Loc.seaside_morella.value           : Rulesets(AccessRule.SHOOT, AccessRule.FLY),

            # Woods
            Loc.woods_salubon.value             : Rulesets(AccessRule.HIT),
            Loc.woods_ukkilei.value             : Rulesets(AccessRule.HIT),

            # Castle
            Loc.castle_pipo_guard.value         : Rulesets(AccessRule.HIT),
            Loc.castle_ukkii.value              : Rulesets(AccessRule.HIT),
            Loc.castle_sal_1000.value           : Rulesets(AccessRule.HIT),

            # Ciscocity
            Loc.ciscocity_pipo_mondy.value      : Rulesets(AccessRule.DASH),

            # Studio
            Loc.studio_monpii_ukkichi.value     : Rulesets(AccessRule.HIT),

            # Halloween
            Loc.halloween_uikkun.value          : Rulesets(AccessRule.HIT),
            Loc.halloween_bonbon.value          : Rulesets(AccessRule.HIT,
                                                           event_invoked(Events.halloween_b_jumbo_robo.value),
                                                           event_invoked(Events.halloween_b1_jumbo_robo_shoot.value)),
            Loc.halloween_chichi.value          : Rulesets(AccessRule.HIT,
                                                           event_invoked(Events.halloween_b_jumbo_robo.value),
                                                           event_invoked(Events.halloween_b1_jumbo_robo_shoot.value)),
            Loc.halloween_ukkito.value          : Rulesets(AccessRule.HIT),
            Loc.halloween_ukkiami.value         : Rulesets(AccessRule.HIT),
            Loc.halloween_kabochin.value        : Rulesets(AccessRule.HIT),
            Loc.halloween_mumpkin.value         : Rulesets(AccessRule.HIT),

            # Western
            Loc.western_jay_mohn.value          : Rulesets(AccessRule.HIT),
            Loc.western_jaja_jamo.value         : Rulesets(AccessRule.ATTACK, AccessRule.HOOP),
            Loc.western_chammy_mo.value         : Rulesets(AccessRule.HIT),
            Loc.western_golozo.value            : Rulesets(AccessRule.HIT),
            Loc.western_golon_moe.value         : Rulesets(AccessRule.ATTACK),

            # Onsen
            Loc.onsen_domobeh.value             : Rulesets(AccessRule.SWIM, AccessRule.CATCH_LONG),
            Loc.onsen_mujakin.value             : Rulesets(AccessRule.SWIM, AccessRule.CATCH_LONG),
            Loc.onsen_fuji_chan.value           : Rulesets(AccessRule.SHOOT),

            # Snofesta
            Loc.snowfesta_konkichi.value        : Rulesets(AccessRule.RADAR),
            Loc.snowfesta_pipotron_yellow.value : Rulesets(AccessRule.DASH),
            Loc.snowfesta_ukki_jii.value        : Rulesets(AccessRule.HIT),

            # Edotown
            Loc.edotown_fatty_mcfats.value      : Rulesets(AccessRule.HIT),
            Loc.edotown_walter.value            : Rulesets(AccessRule.NINJA),

            # Heaven
            Loc.heaven_ukkido.value             : Rulesets(AccessRule.ATTACK),
            Loc.heaven_tami.value               : Rulesets(AccessRule.HIT),
            Loc.heaven_valuccha.value           : Rulesets(AccessRule.ATTACK),

            # Toyhouse
            Loc.toyhouse_monto.value            : Rulesets(AccessRule.SHOOT, AccessRule.NINJA),
            Loc.toyhouse_golonero.value         : Rulesets(AccessRule.HIT),

            # Iceland
            Loc.iceland_kushachin.value         : Rulesets(AccessRule.HIT),
            Loc.iceland_malikko.value           : Rulesets(AccessRule.HIT),
            Loc.iceland_bolikko.value           : Rulesets(AccessRule.HIT),
            Loc.iceland_iceymon.value           : Rulesets(AccessRule.HIT),

            # Arabian
            Loc.arabian_minimon.value           : Rulesets(AccessRule.MAGICIAN),
            Loc.arabian_cup_o_mon.value         : Rulesets(AccessRule.HIT),

            # Asia
            Loc.asia_baku.value                 : Rulesets([AccessRule.SHOOT, AccessRule.SWIM], AccessRule.NINJA),
            Loc.asia_takumon.value              : Rulesets(AccessRule.SWIM, AccessRule.CATCH_LONG),
            Loc.asia_ukki_ether.value           : Rulesets(AccessRule.SWIM),

            # Plane
            Loc.plane_jeloh.value               : Rulesets(AccessRule.HIT),
            Loc.plane_bongo.value               : Rulesets(AccessRule.HIT),

            # Bay
            Loc.bay_nadamon.value               : Rulesets(AccessRule.HIT),
            Loc.bay_nakabi.value                : Rulesets(AccessRule.HIT),
            Loc.bay_gimi_gimi.value             : Rulesets(AccessRule.HIT),
            Loc.bay_pokkini.value               : Rulesets(AccessRule.HIT),

            # Tomo
            Loc.tomo_kichibeh.value             : Rulesets(AccessRule.HIT),
            Loc.tomo_bonchicchi.value           : Rulesets(AccessRule.HIT),
            Loc.tomo_mikibon.value              : Rulesets(AccessRule.HIT),
            Loc.tomo_chimpy.value               : Rulesets(AccessRule.MORPH_NO_MONKEY),
            Loc.tomo_kajitan.value              : Rulesets(AccessRule.MORPH_NO_MONKEY),
            Loc.tomo_uka_uka.value              : Rulesets(AccessRule.MORPH_NO_MONKEY),
            Loc.tomo_mil_mil.value              : Rulesets(AccessRule.MORPH_NO_MONKEY),
            Loc.tomo_tomio.value                : Rulesets(AccessRule.HIT),
            Loc.tomo_gario.value                : Rulesets(AccessRule.HIT),
            Loc.tomo_sal_13.value               : Rulesets(AccessRule.HIT),
            Loc.tomo_sal_12.value               : Rulesets(AccessRule.HIT),

            # Space
            Loc.space_freet.value               : Rulesets(AccessRule.HIT),
            Loc.space_chico.value               : Rulesets(AccessRule.HIT),
            Loc.space_ukki_love.value           : Rulesets(AccessRule.MAGICIAN),
            Loc.space_sal_10.value              : Rulesets(AccessRule.HIT),
            Loc.space_sal_11.value              : Rulesets(AccessRule.HIT),

            # Bosses
            Loc.boss_monkey_white.value         : Rulesets(AccessRule.HIT),
            Loc.boss_monkey_blue.value          : Rulesets(AccessRule.HIT),
            Loc.boss_monkey_yellow.value        : Rulesets(AccessRule.HIT),
            Loc.boss_monkey_pink.value          : Rulesets(AccessRule.HIT),
            Loc.boss_monkey_red.value           : Rulesets(AccessRule.HIT),
            Loc.boss_specter.value              : Rulesets(AccessRule.HIT),
            Loc.boss_specter_final.value        : Rulesets(AccessRule.HIT)
        })

        self.event_rules.update({
            # Castle
            Events.castle_b_clapper.value               : Rulesets(AccessRule.HIT),
            Events.castle_a2_button.value               : Rulesets(AccessRule.HIT),

            # Ciscocity
            Events.ciscocity_c_button.value             : Rulesets(AccessRule.SHOOT, AccessRule.DASH, AccessRule.RCC),

            # Studio
            Events.studio_a1_button.value               : Rulesets(AccessRule.HIT),
            Events.studio_a2_button.value               : Rulesets(AccessRule.HIT),
            Events.studio_b1_button.value               : Rulesets(AccessRule.SHOOT, AccessRule.GLIDE),

            # Halloween
            Events.halloween_b_jumbo_robo.value         : Rulesets(AccessRule.HIT),

            # Onsen
            Events.onsen_a_button.value                 : Rulesets(AccessRule.HIT),

            # Snowfesta
            Events.snowfesta_e_bell.value               : Rulesets(AccessRule.HIT),

            # Edotown
            Events.edotown_b1_button.value              : Rulesets(AccessRule.HIT),

            # Heaven
            Events.heaven_b_clapper.value               : Rulesets(AccessRule.HIT),

            # Iceland
            Events.iceland_c_jumbo_robo.value           : Rulesets(AccessRule.HIT),

            # Asia
            Events.asia_b2_button.value                 : Rulesets(AccessRule.HIT),

            # Plane
            Events.plane_d_clapper.value                : Rulesets(AccessRule.HIT),

            # Hong
            Events.hong_b2_button.value                 : Rulesets(AccessRule.HIT),

            # Bay
            Events.bay_a7_button.value                  : Rulesets(AccessRule.HIT),

            # Space
            Events.space_e_button.value                : Rulesets(AccessRule.ATTACK),
            Events.space_g1_button.value                : Rulesets(AccessRule.ATTACK),
            Events.space_f2_button.value                : Rulesets(AccessRule.ATTACK),
        })

        self.entrance_rules.update({
            # Seaside
            Stage.entrance_seaside_ab.value     : Rulesets(AccessRule.HIT),

            # Woods
            Stage.entrance_woods_bc.value       : Rulesets(AccessRule.HIT),

            # Castle
            Stage.entrance_castle_aa1.value     : Rulesets(AccessRule.HIT),
            Stage.entrance_castle_a1a.value     : Rulesets(AccessRule.HIT),
            Stage.entrance_castle_bb1.value     : Rulesets(AccessRule.HIT),

            # Halloween
            Stage.entrance_halloween_d1d2.value : Rulesets(AccessRule.HIT),

            # Western
            Stage.entrance_western_bb1.value    : Rulesets(AccessRule.HIT),
            Stage.entrance_western_dd2.value    : Rulesets(AccessRule.HIT),
            Stage.entrance_western_d1d2.value   : Rulesets(AccessRule.HIT),
            Stage.entrance_western_d2d.value    : Rulesets(AccessRule.HIT),
            Stage.entrance_western_ed1.value    : Rulesets(AccessRule.HIT),

            # Onsen
            Stage.entrance_onsen_aa1.value      : Rulesets(AccessRule.HIT),
            Stage.entrance_onsen_aa2.value      : Rulesets(AccessRule.HIT),
            Stage.entrance_onsen_a1a2.value     : Rulesets(AccessRule.GLIDE, AccessRule.MAGICIAN),
            Stage.entrance_onsen_a2a1.value     : Rulesets(AccessRule.GLIDE, AccessRule.MAGICIAN),
            Stage.entrance_onsen_b1b.value      : Rulesets(AccessRule.GLIDE, [AccessRule.RCC, AccessRule.SWIM]),

            # Edotown
            Stage.entrance_edotown_a1a.value    : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_edotown_aa1.value    : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_edotown_ab1.value    : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_edotown_b1a.value    : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_edotown_b2b.value    : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_edotown_bb2.value    : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_edotown_bc1.value    : Rulesets(AccessRule.HIT),
            Stage.entrance_edotown_c1c.value    : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_edotown_cc1.value    : Rulesets(AccessRule.NINJA, AccessRule.HERO),
            Stage.entrance_edotown_cc2.value    : Rulesets(AccessRule.HIT),

            # Heaven
            Stage.entrance_heaven_bb1.value     : Rulesets(AccessRule.HIT),

            # Toyhouse
            Stage.entrance_toyhouse_bb1.value   : Rulesets(AccessRule.HIT),
            Stage.entrance_toyhouse_ef.value    : Rulesets(AccessRule.HIT),
            Stage.entrance_toyhouse_fe.value    : Rulesets(AccessRule.HIT),
            Stage.entrance_toyhouse_fa.value    : Rulesets(AccessRule.HIT),

            # Iceland
            Stage.entrance_iceland_a1a.value    : Rulesets(AccessRule.HIT),

            # Asia
            Stage.entrance_asia_a4d1.value      : Rulesets(AccessRule.HIT),
            Stage.entrance_asia_bb2.value       : Rulesets(event_invoked(Events.asia_b2_button.value)),
            Stage.entrance_asia_b2b.value       : Rulesets(AccessRule.HIT),

            # Plane
            Stage.entrance_plane_de.value       : Rulesets(AccessRule.HIT),

            # Bay
            Stage.entrance_bay_cc1.value        : Rulesets(AccessRule.HIT),

            # Tomo
            Stage.entrance_tomo_ee1.value       : Rulesets(AccessRule.KNIGHT),
            Stage.entrance_tomo_ee2.value       : Rulesets(AccessRule.RCC),
        })

class Casual(Normal):
    """
    RuleType for a casual experience. The player is assumed to play the game without any or little advanced or obscure
    knowledge of it.
    """

    def __init__(self):
        super().__init__()

        self.small_starting_areas = [6, 9, 11, 13, 15, 18, 20, 22, 23]

        self.monkey_rules.update({
            # Woods
            Loc.woods_salubon.value             : Rulesets([AccessRule.RADAR, AccessRule.ATTACK]),
            Loc.woods_ukkilei.value             : Rulesets(AccessRule.ATTACK),

            # Castle
            Loc.castle_pipo_guard.value         : Rulesets(AccessRule.ATTACK),
            Loc.castle_monga.value              : Rulesets(AccessRule.SHOOT),
            Loc.castle_ukkii.value              : Rulesets(AccessRule.ATTACK),
            Loc.castle_sal_1000.value           : Rulesets(AccessRule.ATTACK),

            # Ciscocity
            Loc.ciscocity_ukima.value           : Rulesets(AccessRule.DASH),
            Loc.ciscocity_pipo_mondy.value      : Rulesets([AccessRule.ATTACK, AccessRule.DASH]),

            # Studio
            Loc.studio_minoh.value              : Rulesets(AccessRule.SHOOT),
            Loc.studio_monta.value              : Rulesets(AccessRule.SHOOT),
            Loc.studio_monpii_ukkichi.value     : Rulesets(AccessRule.ATTACK),

            # Halloween
            Loc.halloween_monkichiro.value      : Rulesets(AccessRule.SWIM),
            Loc.halloween_uikkun.value          : Rulesets(AccessRule.ATTACK),
            Loc.halloween_bonbon.value          : Rulesets(AccessRule.ATTACK, event_invoked(
                Events.halloween_b_jumbo_robo.value), event_invoked(
                Events.halloween_b1_jumbo_robo_shoot.value)),
            Loc.halloween_chichi.value          : Rulesets(AccessRule.ATTACK, event_invoked(
                Events.halloween_b_jumbo_robo.value), event_invoked(
                Events.halloween_b1_jumbo_robo_shoot.value)),
            Loc.halloween_ukkito.value          : Rulesets(AccessRule.ATTACK),
            Loc.halloween_ukkiami.value         : Rulesets(AccessRule.ATTACK),
            Loc.halloween_kabochin.value        : Rulesets(AccessRule.ATTACK),
            Loc.halloween_mumpkin.value         : Rulesets(AccessRule.ATTACK),

            # Western
            Loc.western_jay_mohn.value          : Rulesets(AccessRule.ATTACK),
            Loc.western_jaja_jamo.value         : Rulesets(AccessRule.ATTACK, AccessRule.HOOP),
            Loc.western_chammy_mo.value         : Rulesets(AccessRule.ATTACK),
            Loc.western_golozo.value            : Rulesets(AccessRule.ATTACK),
            Loc.western_golon_moe.value         : Rulesets(AccessRule.MORPH_NO_MONKEY),

            # Onsen
            Loc.onsen_saru_sam.value            : Rulesets(AccessRule.ATTACK),
            Loc.onsen_tome_san.value            : Rulesets(AccessRule.ATTACK),
            Loc.onsen_domobeh.value             : Rulesets(AccessRule.SWIM),
            Loc.onsen_kimi_san.value            : Rulesets(AccessRule.ATTACK),
            Loc.onsen_mujakin.value             : Rulesets(AccessRule.SWIM),

            # Snowfesta
            Loc.snowfesta_konkichi.value        : Rulesets([AccessRule.ATTACK, AccessRule.RADAR]),
            Loc.snowfesta_pipotron_yellow.value : Rulesets(AccessRule.ATTACK),
            Loc.snowfesta_ukki_jii.value        : Rulesets(AccessRule.ATTACK),

            # Edotown
            Loc.edotown_yosio.value             : Rulesets(AccessRule.DASH),
            Loc.edotown_fatty_mcfats.value      : Rulesets(AccessRule.ATTACK),
            Loc.edotown_golota.value            : Rulesets(AccessRule.ATTACK),

            # Heaven
            Loc.heaven_ukkido.value             : Rulesets(AccessRule.SHOOT),
            Loc.heaven_tami.value               : Rulesets(AccessRule.ATTACK),
            Loc.heaven_kicchino.value           : Rulesets(AccessRule.MORPH_NO_MONKEY),
            Loc.heaven_kimurin.value            : Rulesets(AccessRule.MORPH_NO_MONKEY),
            Loc.heaven_valuccha.value           : Rulesets(AccessRule.SHOOT),

            # Toyhouse
            Loc.toyhouse_monto.value            : Rulesets(AccessRule.SHOOT),
            Loc.toyhouse_pipotron_red.value     : Rulesets(AccessRule.MORPH_NO_MONKEY),
            Loc.toyhouse_golonero.value         : Rulesets(AccessRule.ATTACK),

            # Iceland
            Loc.iceland_kushachin.value         : Rulesets(AccessRule.ATTACK),
            Loc.iceland_malikko.value           : Rulesets(AccessRule.ATTACK),
            Loc.iceland_bolikko.value           : Rulesets(AccessRule.ATTACK),
            Loc.iceland_iceymon.value           : Rulesets(AccessRule.ATTACK),

            # Arabian
            Loc.arabian_cup_o_mon.value         : Rulesets(AccessRule.ATTACK),

            # Asia
            Loc.asia_baku.value                 : Rulesets([AccessRule.SHOOT, AccessRule.SWIM]),
            Loc.asia_takumon.value              : Rulesets(AccessRule.SWIM),

            # Plane
            Loc.plane_temko.value               : Rulesets(AccessRule.DASH),
            Loc.plane_pipotron_blue.value       : Rulesets(AccessRule.MORPH_NO_MONKEY),
            Loc.plane_jeloh.value               : Rulesets(AccessRule.ATTACK),
            Loc.plane_bongo.value               : Rulesets(AccessRule.ATTACK),

            # Hong
            Loc.hong_uki_uki.value              : Rulesets(AccessRule.SHOOT),
            Loc.hong_muki_muki.value            : Rulesets(AccessRule.SHOOT),
            Loc.hong_bassili_ukki.value         : Rulesets(AccessRule.DASH),
            Loc.hong_bankan.value               : Rulesets(AccessRule.NINJA),
            Loc.hong_sukei.value                : Rulesets(AccessRule.SHOOT),

            # Bay
            Loc.bay_nadamon.value               : Rulesets(AccessRule.ATTACK),
            Loc.bay_nakabi.value                : Rulesets(AccessRule.ATTACK),
            Loc.bay_gimi_gimi.value             : Rulesets(AccessRule.ATTACK),
            Loc.bay_pokkini.value               : Rulesets(AccessRule.ATTACK),

            # Tomo
            Loc.tomo_kichibeh.value             : Rulesets(AccessRule.ATTACK),
            Loc.tomo_bonchicchi.value           : Rulesets(AccessRule.ATTACK),
            Loc.tomo_mikibon.value              : Rulesets(AccessRule.ATTACK),
            Loc.tomo_dj_tamo.value              : Rulesets(AccessRule.DASH),
            Loc.tomo_chimpy.value               : Rulesets(AccessRule.KUNGFU, AccessRule.NINJA),
            Loc.tomo_kajitan.value              : Rulesets(AccessRule.KUNGFU, AccessRule.NINJA),
            Loc.tomo_uka_uka.value              : Rulesets(AccessRule.KUNGFU, AccessRule.NINJA),
            Loc.tomo_mil_mil.value              : Rulesets(AccessRule.KUNGFU, AccessRule.NINJA),
            Loc.tomo_goro_san.value             : Rulesets(AccessRule.KNIGHT),
            Loc.tomo_tomio.value                : Rulesets(AccessRule.ATTACK),
            Loc.tomo_gario.value                : Rulesets(AccessRule.ATTACK),
            Loc.tomo_dj_pari.value              : Rulesets(AccessRule.DASH),
            Loc.tomo_sal_13.value               : Rulesets(AccessRule.ATTACK),
            Loc.tomo_sal_12.value               : Rulesets(AccessRule.ATTACK),

            # Space
            Loc.space_miluchy.value             : Rulesets(AccessRule.SHOOT, AccessRule.FLY),
            Loc.space_freet.value               : Rulesets(AccessRule.ATTACK),
            Loc.space_chico.value               : Rulesets(AccessRule.ATTACK),
            Loc.space_sal_10.value              : Rulesets(AccessRule.ATTACK),
            Loc.space_sal_11.value              : Rulesets(AccessRule.ATTACK),

            # Bosses
            Loc.boss_monkey_white.value         : Rulesets(AccessRule.ATTACK),
            Loc.boss_monkey_blue.value          : Rulesets(AccessRule.ATTACK),
            Loc.boss_monkey_yellow.value        : Rulesets(AccessRule.NINJA),
            Loc.boss_monkey_pink.value          : Rulesets(AccessRule.MORPH_NO_MONKEY),
            Loc.boss_monkey_red.value           : Rulesets(AccessRule.ATTACK),
            Loc.boss_specter.value              : Rulesets(AccessRule.ATTACK),
            Loc.boss_specter_final.value        : Rulesets(AccessRule.ATTACK, AccessRule.SWIM)
        })

        self.event_rules.update({
            # Castle
            Events.castle_b_clapper.value               : Rulesets(AccessRule.ATTACK),
            Events.castle_a2_button.value               : Rulesets(AccessRule.ATTACK),

            # Ciscocity
            Events.ciscocity_c_button.value             : Rulesets(AccessRule.SHOOT, AccessRule.DASH, AccessRule.RCC),

            # Studio
            Events.studio_a1_button.value               : Rulesets(AccessRule.ATTACK),
            Events.studio_a2_button.value               : Rulesets(AccessRule.ATTACK),

            # Halloween
            Events.halloween_b_jumbo_robo.value         : Rulesets(AccessRule.ATTACK),

            # Onsen
            Events.onsen_a_button.value                 : Rulesets(AccessRule.ATTACK),

            # Snowfesta
            Events.snowfesta_e_bell.value               : Rulesets(AccessRule.ATTACK),

            # Edotown
            Events.edotown_b1_button.value              : Rulesets(AccessRule.ATTACK),
            Events.edotown_e_scroll.value               : Rulesets(AccessRule.CLUB, AccessRule.KNIGHT,
                                                                   AccessRule.NINJA, AccessRule.MAGICIAN,
                                                                   AccessRule.KUNGFU),

            # Heaven
            Events.heaven_b_clapper.value               : Rulesets(AccessRule.ATTACK),

            # Iceland
            Events.iceland_c_jumbo_robo.value           : Rulesets(AccessRule.ATTACK),

            # Asia
            Events.asia_b2_button.value                 : Rulesets(AccessRule.ATTACK),

            # Plane
            Events.plane_d_clapper.value                 : Rulesets(AccessRule.ATTACK),

            # Hong
            Events.hong_b2_button.value                 : Rulesets(AccessRule.ATTACK),

            # Bay
            Events.bay_a7_button.value                  : Rulesets(AccessRule.ATTACK),
        })

        self.entrance_rules.update({
            # Seaside
            Stage.entrance_seaside_ab.value     : Rulesets(AccessRule.ATTACK),

            # Woods
            Stage.entrance_woods_bc.value       : Rulesets(AccessRule.ATTACK),

            # Castle
            Stage.entrance_castle_aa1.value     : Rulesets(AccessRule.ATTACK),
            Stage.entrance_castle_a1a.value     : Rulesets(AccessRule.ATTACK),
            Stage.entrance_castle_dd1.value     : Rulesets(AccessRule.KNIGHT),
            Stage.entrance_castle_d1d.value     : Rulesets(AccessRule.KNIGHT),
            Stage.entrance_castle_bb1.value     : Rulesets(AccessRule.ATTACK),

            # Ciscocity
            Stage.entrance_ciscocity_ab.value   : Rulesets(AccessRule.ATTACK),
            Stage.entrance_ciscocity_ce.value   : Rulesets([AccessRule.MONKEY, AccessRule.MONKEY]),

            # Studio
            Stage.entrance_studio_d1d.value     : Rulesets(AccessRule.ATTACK, AccessRule.GLIDE),
            Stage.entrance_studio_d2d.value     : Rulesets(AccessRule.ATTACK),

            # Halloween
            Stage.entrance_halloween_a1a.value  : Rulesets(AccessRule.SWIM),
            Stage.entrance_halloween_aa1.value  : Rulesets(AccessRule.SWIM),
            Stage.entrance_halloween_c1c.value  : Rulesets(AccessRule.SWIM),
            Stage.entrance_halloween_cc1.value  : Rulesets(AccessRule.SWIM),
            Stage.entrance_halloween_cc2.value  : Rulesets(AccessRule.SWIM),
            Stage.entrance_halloween_c2c.value  : Rulesets(AccessRule.SWIM),
            Stage.entrance_halloween_dd1.value  : Rulesets(AccessRule.KNIGHT),
            Stage.entrance_halloween_d1d.value  : Rulesets(AccessRule.KNIGHT),
            Stage.entrance_halloween_d1d2.value : Rulesets(AccessRule.ATTACK),

            # Western
            Stage.entrance_western_bb1.value    : Rulesets(AccessRule.ATTACK),
            Stage.entrance_western_fd2.value    : Rulesets(AccessRule.ATTACK),
            Stage.entrance_western_dd2.value    : Rulesets(AccessRule.ATTACK),
            Stage.entrance_western_d1d2.value   : Rulesets(AccessRule.ATTACK),
            Stage.entrance_western_d2d.value    : Rulesets(AccessRule.ATTACK),
            Stage.entrance_western_ed1.value    : Rulesets(AccessRule.ATTACK),

            # Onsen
            Stage.entrance_onsen_aa1.value      : Rulesets(AccessRule.ATTACK),
            Stage.entrance_onsen_aa2.value      : Rulesets(AccessRule.ATTACK),
            Stage.entrance_onsen_a1a2.value     : Rulesets(AccessRule.GLIDE, AccessRule.MAGICIAN),
            Stage.entrance_onsen_a2a1.value     : Rulesets(AccessRule.GLIDE, AccessRule.MAGICIAN),
            Stage.entrance_onsen_b1b.value      : Rulesets([AccessRule.RCC, AccessRule.SWIM]),
            Stage.entrance_onsen_bd1.value      : Rulesets(AccessRule.SHOOT),
            Stage.entrance_onsen_dd1.value      : Rulesets(AccessRule.RCC),

            # Edotown
            Stage.entrance_edotown_a1a.value    : Rulesets(AccessRule.NINJA),
            Stage.entrance_edotown_aa1.value    : Rulesets(AccessRule.NINJA),
            Stage.entrance_edotown_ab1.value    : Rulesets(AccessRule.GLIDE),
            Stage.entrance_edotown_b1a.value    : Rulesets(AccessRule.GLIDE),
            Stage.entrance_edotown_b2b1.value   : Rulesets([event_invoked(Events.edotown_b1_button.value),
                                                            AccessRule.NINJA], AccessRule.SWIM),
            Stage.entrance_edotown_b2b.value    : Rulesets(AccessRule.NINJA),
            Stage.entrance_edotown_bb2.value    : Rulesets(AccessRule.NINJA),
            Stage.entrance_edotown_bc1.value    : Rulesets(AccessRule.ATTACK),
            Stage.entrance_edotown_c1c.value    : Rulesets(AccessRule.NINJA),
            Stage.entrance_edotown_cc1.value    : Rulesets(AccessRule.NINJA),
            Stage.entrance_edotown_cc2.value    : Rulesets(AccessRule.ATTACK),

            # Heaven
            Stage.entrance_heaven_a1a.value     : Rulesets(AccessRule.GLIDE),
            Stage.entrance_heaven_aa1.value     : Rulesets(AccessRule.GLIDE),
            Stage.entrance_heaven_ab.value      : Rulesets(AccessRule.NINJA, AccessRule.HERO, [AccessRule.FLYER,
                                                            AccessRule.HOOP]),
            Stage.entrance_heaven_bb1.value     : Rulesets(AccessRule.ATTACK),

            # Toyhouse
            Stage.entrance_toyhouse_bb1.value   : Rulesets(AccessRule.ATTACK),
            Stage.entrance_toyhouse_ef.value    : Rulesets(AccessRule.ATTACK),
            Stage.entrance_toyhouse_fe.value    : Rulesets(AccessRule.ATTACK),
            Stage.entrance_toyhouse_fa.value    : Rulesets(AccessRule.ATTACK),

            # Iceland
            Stage.entrance_iceland_a1a.value    : Rulesets(AccessRule.ATTACK),
            Stage.entrance_iceland_aa2.value    : Rulesets(AccessRule.GLIDE),
            Stage.entrance_iceland_a2a.value    : Rulesets(AccessRule.GLIDE),
            Stage.entrance_iceland_be.value     : Rulesets(AccessRule.DASH),

            # Asia
            Stage.entrance_asia_ab.value        : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_ba.value        : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a1a.value       : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a1b1.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a1a3.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a2a1.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a2a3.value      : Rulesets([event_invoked(Events.asia_a_block.value),
                                                      event_invoked(Events.asia_a1_block.value),
                                                      event_invoked(Events.asia_a2_block.value)]),
            Stage.entrance_asia_a2a4.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a3a1.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a3a4.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a3a2.value      : Rulesets([event_invoked(Events.asia_a_block.value),
                                                      event_invoked(Events.asia_a1_block.value),
                                                      event_invoked(Events.asia_a2_block.value)]),
            Stage.entrance_asia_a4a3.value      : Rulesets(AccessRule.SWIM),
            Stage.entrance_asia_a4d1.value      : Rulesets(AccessRule.ATTACK),
            Stage.entrance_asia_b2b.value       : Rulesets(AccessRule.ATTACK),
            Stage.entrance_asia_dd1.value       : Rulesets([AccessRule.SWIM, AccessRule.FLY]),

            # Plane
            Stage.entrance_plane_de.value       : Rulesets(AccessRule.ATTACK),
            Stage.entrance_plane_b1h.value      : Rulesets(AccessRule.RCC, AccessRule.HERO),
            Stage.entrance_plane_hb1.value      : Rulesets(AccessRule.RCC, AccessRule.HERO),
            Stage.entrance_plane_b1b2.value     : Rulesets(AccessRule.RCC, AccessRule.HERO),
            Stage.entrance_plane_b2b1.value     : Rulesets(AccessRule.RCC, AccessRule.HERO),

            # Hong
            Stage.entrance_hong_aa1.value       : Rulesets(AccessRule.KUNGFU),
            Stage.entrance_hong_a1a2.value      : Rulesets(AccessRule.ATTACK),
            Stage.entrance_hong_cc1.value       : Rulesets([AccessRule.ATTACK, AccessRule.GLIDE]),
            Stage.entrance_hong_c1c.value       : Rulesets([AccessRule.ATTACK, AccessRule.GLIDE]),

            # Bay
            Stage.entrance_bay_aa1.value        : Rulesets([AccessRule.ATTACK, AccessRule.SHOOT, AccessRule.SWIM]),
            Stage.entrance_bay_a1a.value        : Rulesets(AccessRule.SWIM),
            Stage.entrance_bay_a3a4.value       : Rulesets(AccessRule.RCC),
            Stage.entrance_bay_cc1.value        : Rulesets([AccessRule.ATTACK, AccessRule.FLY]),
            Stage.entrance_bay_e1e2.value       : Rulesets(AccessRule.ATTACK),

            # Tomo
            Stage.entrance_tomo_bc.value        : Rulesets(AccessRule.GLIDE),

            # Space
            Stage.entrance_space_gg1.value      : Rulesets([AccessRule.ATTACK, AccessRule.ATTACK]),
        })

LogicPreferenceOptions : list = [
    Casual,
    Normal,
    Hard
]

# [<--- GOAL TARGETS --->]
class Specter(GoalTarget):
    name = "Specter"
    description = "Capture Specter by clearing \"Specter Battle!\""

    locations = {Loc.boss_specter.value}


class SpecterFinal(Specter):
    name = "Specter Final"
    description = "Capture Specter a second time by clearing \"Specter's Final Battle!\""

    locations = {Loc.boss_specter_final.value}


class TripleThreat(GoalTarget):
    name = "Triple Threat"
    description = "Defeat at least 3 bosses!"

    locations = {*MONKEYS_BOSSES}

    amount = 3


class PlaySpike(GoalTarget):
    name = "Play Spike"
    description = "Go and Capture 204 Pipo Monkeys!"

    locations = {monkey for monkey in MONKEYS_MASTER if monkey != Loc.boss_tomoki.value and monkey not in
                MONKEYS_PASSWORDS}

    amount = 204

    def verify(self, state: CollectionState, player: int) -> bool:
        minimum_equipment : list[Callable] = [AccessRule.DASH, AccessRule.SWIM, AccessRule.SLING, AccessRule.RCC,
                                              AccessRule.MAGICIAN, AccessRule.KUNGFU, AccessRule.HERO]

        if any(monkey in MONKEYS_BREAK_ROOMS for monkey in self.locations):
            minimum_equipment.append(AccessRule.MONKEY)

        for rule in minimum_equipment:
            if not rule(state, player):
                return False

        return True


class PlayJimmy(PlaySpike):
    name = "Play Jimmy"
    description = "Go and Capture 300 Pipo Monkeys!"

    amount = 300


class DirectorsCut(GoalTarget):
    name = "Director's Cut"
    description = "Capture all Monkey Films across all the channels!"

    locations = {*CAMERAS_MASTER}


class PhoneCheck(DirectorsCut):
    name = "Phone Check"
    description = "Activate all Cellphones scattered across the channels!"

    locations = {*Cellphone_Name_to_ID.values()}


class PasswordHunt(DirectorsCut):
    name = "Password Hunt"

    locations = {*MONKEYS_PASSWORDS}


GoalTargetOptions : list[Callable] = [
    Specter, SpecterFinal, TripleThreat, PlaySpike, PlayJimmy, DirectorsCut, PhoneCheck, PasswordHunt
]

class Vanilla(PostGameAccessRule):
    name = "Vanilla"
    description = "Capture all Base and Break Room Monkeys"

    locations = {monkey for monkey in MONKEYS_MASTER
                 if monkey != Loc.boss_tomoki.value and monkey not in MONKEYS_PASSWORDS }

    def verify(self, state : CollectionState, player : int) -> bool:
        for rule in [AccessRule.DASH, AccessRule.SWIM, AccessRule.SLING, AccessRule.RCC, AccessRule.MAGICIAN,
                     AccessRule.KUNGFU, AccessRule.HERO]:
            if not rule(state, player):
                return False

        return True

class ActiveMonkeys(PostGameAccessRule):
    name = "Active Monkeys"
    description = "Capture all Active Monkeys (marked as locations)"

    locations = {monkey for monkey in MONKEYS_MASTER if monkey != Loc.boss_tomoki.value }

    def verify(self, state: CollectionState, player: int) -> bool:
        minimum_equipment : list[Callable] = [AccessRule.DASH, AccessRule.SWIM, AccessRule.SLING, AccessRule.RCC,
                                              AccessRule.MAGICIAN, AccessRule.KUNGFU, AccessRule.HERO]

        if any(monkey in MONKEYS_BREAK_ROOMS for monkey in self.locations):
            minimum_equipment.append(AccessRule.MONKEY)

        for rule in minimum_equipment:
            if not rule(state, player):
                return False

        return True

class AllCameras(PostGameAccessRule):
    name = "All Cameras"
    description = "Capture all Monkey Films"

    locations = { *CAMERAS_MASTER }

class AllCellphones(PostGameAccessRule):
    name = "All Cellphones"
    description = "Activate all Cellphones"

    locations = { *Cellphone_Name_to_ID.values() }

class ChannelKey(PostGameAccessRule):
    name = "Channel Key"
    description = "Find the extra Channel Key"

    locations = { Loc.boss_specter.value }

    def get_progress(self, ctx : 'AE3Context') -> int:
        all_keys = len(ctx.progression.progression) - 1
        if ctx.post_game_access_rule_option < 4:
            all_keys -= 1

        return int(ctx.keys / all_keys)

    def verify(self, state : CollectionState, player : int) -> bool:
        return state.can_reach_location(Loc.boss_specter.value, player)

class AfterEnd(ChannelKey):
    name = "After End"
    description = "Defeat Specter in Specter's Battle!"

    locations = { Loc.boss_specter.value }

PostGameAccessRuleOptions : list[Callable] = [
    Vanilla, ActiveMonkeys, AllCameras, AllCellphones, ChannelKey, AfterEnd
]