from typing import Callable, Set

from .Locations import MONKEYS_INDEX
from .Logic import Rulesets, AccessRule, ProgressionMode, has_keys, event_invoked
from .Strings import Loc, Stage, Events
from .Stages import STAGES_DIRECTORY, ENTRANCES_STAGE_SELECT

class LogicPreference:
    """
    Base Class for defined RuleTypes. RuleTypes determine the kinds of access rules locations or regions have
    based on a preferred play style
    """
    monkey_rules : dict[str, Rulesets] = {}
    event_rules : dict[str, Rulesets] = {}
    entrance_rules : dict[str, Rulesets] = {}

    default_critical_rule : Set[Callable] = [AccessRule.CATCH]
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

    def set_level_progression_rules(self, progression : ProgressionMode):
        levels_count : int = 0
        for sets, levels in enumerate(progression.value):
            extra: int = 0
            if sets < 1:
                extra = 1

            for _ in range(levels + extra):
                rule : Rulesets = Rulesets()

                if sets > 0:
                    rule = Rulesets(has_keys(sets))
                elif sets == len(progression.value):
                    rule = Rulesets(self.final_level_rule.add(has_keys(sets - 1)))

                self.entrance_rules[ENTRANCES_STAGE_SELECT[levels_count].name] = rule

                levels_count += 1

class Hard(LogicPreference):
    """
    RuleType for a hard experience. The player is assumed to play the game with in-depth knowledge of the game,
    except any glitches major oversights.
    """

    def __init__(self):
        super().__init__()

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
        })

        self.entrance_rules.update({
            # Seaside
            Stage.entrance_seaside_ac.value     : Rulesets(AccessRule.MONKEY),

            # Woods
            Stage.entrance_woods_ad.value       : Rulesets(AccessRule.MONKEY),

            # Castle
            Stage.entrance_castle_aa2.value     : Rulesets(event_invoked(Events.event_castle_a2_button.value)),
            Stage.entrance_castle_b1b.value     : Rulesets(event_invoked(Events.event_castle_b_clapper.value)),
            Stage.entrance_castle_be.value      : Rulesets(AccessRule.MONKEY),

            # Ciscocity
            Stage.entrance_ciscocity_ad.value   : Rulesets(AccessRule.DASH, AccessRule.RCC),
            Stage.entrance_ciscocity_ad_2.value : Rulesets(event_invoked(Events.event_ciscocity_d_exit.value)),
            Stage.entrance_ciscocity_ce         : Rulesets(AccessRule.MONKEY),
            Stage.entrance_ciscocity_c1c.value  : Rulesets(event_invoked(Events.event_ciscocity_c_button.value)),
            Stage.entrance_ciscocity_cc1.value  : Rulesets(event_invoked(Events.event_ciscocity_c_button.value)),

            # Studio
            Stage.entrance_studio_aa1.value     : Rulesets(event_invoked(Events.event_studio_a1_button.value)),
            Stage.entrance_studio_aa2.value     : Rulesets(event_invoked(Events.event_studio_a2_button.value)),
            Stage.entrance_studio_b1b.value     : Rulesets(AccessRule.SHOOT, AccessRule.GLIDE, AccessRule.MAGICIAN),
            Stage.entrance_studio_ff1.value     : Rulesets(event_invoked(Events.event_studio_f_tele_robo.value)),
            Stage.entrance_studio_f1f.value     : Rulesets(event_invoked(Events.event_studio_f_tele_robo.value)),
            Stage.entrance_studio_dg.value      : Rulesets(AccessRule.MONKEY),
            Stage.entrance_studio_dd2.value     : Rulesets(AccessRule.SHOOT),

            # Halloween
            Stage.entrance_halloween_aa1.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_a1a.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_bb1.value  : Rulesets(
                event_invoked(Events.event_halloween_b_jumbo_robo.value),
                      event_invoked(Events.event_halloween_b1_jumbo_robo_shoot.value)),
            Stage.entrance_halloween_b1b.value: Rulesets(
                event_invoked(Events.event_halloween_b_jumbo_robo.value),
                event_invoked(Events.event_halloween_b1_jumbo_robo_shoot.value)),
            Stage.entrance_halloween_c1c.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_cc1.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_cc2.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_c2c.value  : Rulesets(AccessRule.SWIM, AccessRule.HERO),
            Stage.entrance_halloween_d1e.value  : Rulesets(AccessRule.MONKEY),

            # Western
            Stage.entrance_western_ec.value     : Rulesets(AccessRule.MONKEY),
        })

class Normal(Hard):
    """
    RuleType for a normal experience. Expectations of accessibility will be the same as the vanilla game.
    """

    def __init__(self):
        super().__init__()

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
            Loc.halloween_bonbon.value          : Rulesets(AccessRule.HIT, event_invoked(
                Events.event_halloween_b_jumbo_robo.value), event_invoked(
                Events.event_halloween_b1_jumbo_robo_shoot.value)),
            Loc.halloween_chichi.value          : Rulesets(AccessRule.HIT, event_invoked(
                Events.event_halloween_b_jumbo_robo.value), event_invoked(
                Events.event_halloween_b1_jumbo_robo_shoot.value)),
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

            # Ciscocity
            Stage.entrance_studio_bb1.value     : Rulesets(AccessRule.SHOOT, AccessRule.GLIDE),

            # Halloween
            Stage.entrance_halloween_d1d2.value : Rulesets(AccessRule.HIT),

            # Western
            Stage.entrance_western_bb1.value    : Rulesets(AccessRule.HIT),
            Stage.entrance_western_dd2.value    : Rulesets(AccessRule.HIT),
            Stage.entrance_western_d1d2.value   : Rulesets(AccessRule.HIT),
            Stage.entrance_western_d2d.value    : Rulesets(AccessRule.HIT),
            Stage.entrance_western_ed1.value    : Rulesets(AccessRule.HIT),
        })

class Casual(Normal):
    """
    RuleType for a casual experience. The player is assumed to play the game without any or little advanced or obscure
    knowledge of it.
    """

    def __init__(self):
        super().__init__()

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
                Events.event_halloween_b_jumbo_robo.value), event_invoked(
                Events.event_halloween_b1_jumbo_robo_shoot.value)),
            Loc.halloween_chichi.value          : Rulesets(AccessRule.ATTACK, event_invoked(
                Events.event_halloween_b_jumbo_robo.value), event_invoked(
                Events.event_halloween_b1_jumbo_robo_shoot.value)),
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
        })

