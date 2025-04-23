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
            Loc.castle_monga.value          : Rulesets(AccessRule.SHOOT, AccessRule.GLIDE)
        })

        self.entrance_rules.update({
            # Seaside
            Stage.entrance_seaside_ac.value : Rulesets(AccessRule.MONKEY),

            # Woods
            Stage.entrance_woods_ad.value   : Rulesets(AccessRule.MONKEY),

            # Castle
            Stage.entrance_castle_aa2.value : Rulesets(event_invoked(Events.event_castle_a2_button.value)),
            Stage.entrance_castle_b1b.value : Rulesets(event_invoked(Events.event_castle_b_clapper.value)),
            Stage.entrance_castle_be.value  : Rulesets(AccessRule.MONKEY)
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
            Loc.castle_sal_1000.value           : Rulesets(AccessRule.HIT)
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
            Loc.castle_sal_1000.value           : Rulesets(AccessRule.ATTACK)
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
        })

