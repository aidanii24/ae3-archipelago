from typing import Callable, Set, Sequence
from dataclasses import dataclass
from abc import ABC

from BaseClasses import Location, Region, ItemClassification

from .Strings import Loc, Stage, Game, Meta
from .Logic import AccessRule, Rulesets
from .Addresses import NTSCU
from .Items import AE3Item


### [< --- HELPERS --- >]
class AE3Location(Location):
    """
    Defines a Location in Ape Escape 3. This refers to points of interest for the randomizer, such as Monkeys,
    Cellphones, Cameras and Points of Interests in the Hub.

    Attributes:
        game : Name of the Game
        rules : Sets of AccessRules to check if the Location is reachable
    """

    game : str = Meta.game
    rules : Rulesets

@dataclass
class AE3LocationMeta(ABC):
    """Base Data Class for all Locations in Ape Escape 3."""

    name : str
    loc_id : int
    address : int
    rules : Rulesets

@dataclass
class MonkeyLocation(AE3LocationMeta):
    """
    Base Data Class for all Monkey Locations

    Parameters:
        name : Name of Location from Strings.py
        rules : Sets of AccessRules for the Location. Can be an AccessRule, Sets of AccessRule, or a full Ruleset.
        Only parameters of type RuleSet can set Critical Rules.
    """

    def __init__(self, name : str, *rules : Callable | frozenset[Callable] | Set[frozenset[Callable]] | Rulesets):
        self.name = name
        # Locations can be assumed to always be in Addresses.Locations. NTSCU version will be used as basis for the ID.
        self.loc_id = NTSCU.Locations[name]
        self.address = self.loc_id
        self.rules = Rulesets()

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

        # For Monkeys, always add CATCH as a Critical Rule
        self.rules.Critical.add(AccessRule.CATCH)

    def to_location(self, player : int, parent : Region) -> Location:
        return Location(player, self.name, self.loc_id, parent)

class EventMeta(AE3LocationMeta):
    """Base Class for all events."""
    def __init__(self, name : str, *rules : Callable | frozenset[Callable] | Set[frozenset[Callable]] | Rulesets):
        self.name = name
        self.loc_id = 0x0
        self.address = 0x0

        self.rules = Rulesets()

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

    def to_event_location(self, player : int, parent : Region) -> Location:
        event : Location = Location(player, self.name, None, parent)
        item : AE3Item = AE3Item(self.name, ItemClassification.progression, None, player)

        event.place_locked_item(item)

        return event

# ### [< --- LOCATIONS --- >]
# # Zero
# Zero_Ukki_Pan = MonkeyLocation(Loc.zero_ukki_pan.value)
#
# # Seaside
# Seaside_Nessal = MonkeyLocation(Loc.seaside_nessal.value)
# Seaside_Ukki_Pia = MonkeyLocation(Loc.seaside_ukki_pia.value)
# Seaside_Sarubo = MonkeyLocation(Loc.seaside_sarubo.value)
# Seaside_Salurin = MonkeyLocation(Loc.seaside_salurin.value)
# Seaside_Ukkitan = MonkeyLocation(Loc.seaside_ukkitan.value)
# Seaside_Morella = MonkeyLocation(Loc.seaside_morella.value,
#                                  AccessRule.SHOOT, AccessRule.FLY)
# Seaside_Ukki_Ben = MonkeyLocation(Loc.seaside_ukki_ben.value)
# Seaside_Kankichi = MonkeyLocation(Loc.seaside_kankichi.value)
# Seaside_Tomezo = MonkeyLocation(Loc.seaside_tomezo.value)
# Seaside_Kamayan = MonkeyLocation(Loc.seaside_kamayan.value)
# Seaside_Taizo = MonkeyLocation(Loc.seaside_taizo.value)

# # Woods
# Woods_Ukki_Pon = MonkeyLocation(Loc.woods_ukki_pon.value)
# Woods_Ukkian = MonkeyLocation(Loc.woods_ukkian.value)
# Woods_Ukki_Red = MonkeyLocation(Loc.woods_ukki_red.value)
# Woods_Rosalin = MonkeyLocation(Loc.woods_rosalin.value)
# Woods_Salubon = MonkeyLocation(Loc.woods_salubon.value)
# Woods_Wolfmon = MonkeyLocation(Loc.woods_wolfmon.value)
# Woods_Ukiko = MonkeyLocation(Loc.woods_ukiko.value)
# Woods_Lambymon = MonkeyLocation(Loc.woods_lambymon.value)
# Woods_Kreemon = MonkeyLocation(Loc.woods_kreemon.value)
# Woods_Ukkilei = MonkeyLocation(Loc.woods_ukkilei.value)
# Woods_Spork = MonkeyLocation(Loc.woods_spork.value)
# Woods_King_Goat = MonkeyLocation(Loc.woods_king_goat.value)
# Woods_Marukichi = MonkeyLocation(Loc.woods_marukichi.value)
# Woods_Kikimon = MonkeyLocation(Loc.woods_kikimon.value)
# Woods_Kominato = MonkeyLocation(Loc.woods_kominato.value)
#
# # Castle
# Castle_Ukkido = MonkeyLocation(Loc.castle_ukkido.value)
# Castle_Pipo_Guard = MonkeyLocation(Loc.castle_pipo_guard.value)
# Castle_Monderella = MonkeyLocation(Loc.castle_monderella.value)
# Castle_Ukki_Ichi = MonkeyLocation(Loc.castle_ukki_ichi.value)
# Castle_Ukkinee = MonkeyLocation(Loc.castle_ukkinee.value)
# Castle_Saru_Mon = MonkeyLocation(Loc.castle_saru_mon.value)
# Castle_Monga = MonkeyLocation(Loc.castle_monga.value,
#                               AccessRule.SHOOT, AccessRule.GLIDE)
# Castle_Ukkiton = MonkeyLocation(Loc.castle_ukkiton.value)
# Castle_King_Leo = MonkeyLocation(Loc.castle_king_leo.value)
# Castle_Ukkii = MonkeyLocation(Loc.castle_ukkii.value)
# Castle_Saluto = MonkeyLocation(Loc.castle_saluto.value)
# Castle_Kings_Double = MonkeyLocation(Loc.castle_kings_double.value)
# Castle_Mattsun = MonkeyLocation(Loc.castle_mattsun.value)
# Castle_Miya = MonkeyLocation(Loc.castle_miya.value)
# Castle_Mon_San = MonkeyLocation(Loc.castle_mon_san.value)
# Castle_SAL_1000 = MonkeyLocation(Loc.castle_sal_1000.value)
#
# ## Monkey White Battle!
# Boss_Monkey_White = MonkeyLocation(Loc.boss_monkey_white.value)

## The Big City
Ciscocity_Ukima = MonkeyLocation(Loc.ciscocity_ukima.value)
Ciscocity_Monbolo = MonkeyLocation(Loc.ciscocity_monbolo.value)
Ciscocity_Pipo_Mondy = MonkeyLocation(Loc.ciscocity_pipo_mondy.value)
Ciscocity_Ukki_Mattan = MonkeyLocation(Loc.ciscocity_ukki_mattan.value)
Ciscocity_Bemucho = MonkeyLocation(Loc.ciscocity_bemucho.value)
Ciscocity_Ukki_Nader = MonkeyLocation(Loc.ciscocity_ukki_nader.value)
Ciscocity_Sabu_Sabu = MonkeyLocation(Loc.ciscocity_sabu_sabu.value)
Ciscocity_Ginjiro = MonkeyLocation(Loc.ciscocity_ginjiro.value)
Ciscocity_Kichiemon = MonkeyLocation(Loc.ciscocity_kichiemon.value)
Ciscocity_Ukkilun = MonkeyLocation(Loc.ciscocity_ukkilun.value)
Ciscocity_Bully_Mon = MonkeyLocation(Loc.ciscocity_bully_mon.value)
Ciscocity_Ukki_Joe = MonkeyLocation(Loc.ciscocity_ukki_joe.value)
Ciscocity_Tamaki = MonkeyLocation(Loc.ciscocity_tamaki.value)
Ciscocity_Mickey_Oou = MonkeyLocation(Loc.ciscocity_mickey_oou.value)
Ciscocity_Sally_Kokoroe = MonkeyLocation(Loc.ciscocity_sally_kokoroe.value)
Ciscocity_Monkey_Manager = MonkeyLocation(Loc.ciscocity_monkey_manager.value)
Ciscocity_Supervisor_Chimp = MonkeyLocation(Loc.ciscocity_supervisor_chimp.value)
Ciscocity_Boss_Ape = MonkeyLocation(Loc.ciscocity_boss_ape.value)

## Specter TV Studio
Studio_Ukki_Yan = MonkeyLocation(Loc.studio_ukki_yan.value)
Studio_Ukkipuss = MonkeyLocation(Loc.studio_ukkipuss.value)
Studio_Minoh = MonkeyLocation(Loc.studio_minoh.value)
Studio_Monta = MonkeyLocation(Loc.studio_monta.value)
Studio_Pipopam = MonkeyLocation(Loc.studio_pipopam.value)
Studio_Monpii_Ukkichi = MonkeyLocation(Loc.studio_monpii_ukkichi.value)
Studio_Gabimon = MonkeyLocation(Loc.studio_gabimon.value)
Studio_Bananamon = MonkeyLocation(Loc.studio_bananamon.value)
Studio_Mokinza = MonkeyLocation(Loc.studio_mokinza.value)
Studio_Ukki_Lee_Ukki = MonkeyLocation(Loc.studio_ukki_lee_ukki.value)
Studio_Ukkida_Jiro = MonkeyLocation(Loc.studio_ukkida_jiro.value)
Studio_Sal_Ukindo = MonkeyLocation(Loc.studio_sal_ukindo.value)
Studio_Gimminey = MonkeyLocation(Loc.studio_gimminey.value)
Studio_Hant = MonkeyLocation(Loc.studio_hant.value)
Studio_Chippino = MonkeyLocation(Loc.studio_chippino.value)
Studio_Ukki_Paul = MonkeyLocation(Loc.studio_ukki_paul.value)
Studio_Sally_Mon = MonkeyLocation(Loc.studio_sally_mon.value)
Studio_Bonly = MonkeyLocation(Loc.studio_bonly.value)
Studio_Monly = MonkeyLocation(Loc.studio_monly.value)

## Bootown
Halloween_Monkichiro = MonkeyLocation(Loc.halloween_monkichiro.value)
Halloween_Leomon = MonkeyLocation(Loc.halloween_leomon.value)
Halloween_Uikkun = MonkeyLocation(Loc.halloween_uikkun.value)
Halloween_Take_Ukita = MonkeyLocation(Loc.halloween_take_ukita.value)
Halloween_Bonbon = MonkeyLocation(Loc.halloween_bonbon.value)
Halloween_Chichi = MonkeyLocation(Loc.halloween_chichi.value)
Halloween_Ukkisuke = MonkeyLocation(Loc.halloween_ukkisuke.value)
Halloween_Chibi_Sally = MonkeyLocation(Loc.halloween_chibi_sally.value)
Halloween_Ukkison = MonkeyLocation(Loc.halloween_ukkison.value)
Halloween_Saruhotep = MonkeyLocation(Loc.halloween_saruhotep.value)
Halloween_Ukkito = MonkeyLocation(Loc.halloween_ukkito.value)
Halloween_Monzally = MonkeyLocation(Loc.halloween_monzally.value)
Halloween_Ukkiami = MonkeyLocation(Loc.halloween_ukkiami.value)
Halloween_Monjan = MonkeyLocation(Loc.halloween_monjan.value)
Halloween_Nattchan = MonkeyLocation(Loc.halloween_nattchan.value)
Halloween_Kabochin = MonkeyLocation(Loc.halloween_kabochin.value)
Halloween_Ukki_Mon = MonkeyLocation(Loc.halloween_ukki_mon.value)
Halloween_Mumpkin = MonkeyLocation(Loc.halloween_mumpkin.value)

## Wild West Town
Western_Morrey = MonkeyLocation(Loc.western_morrey.value)
Western_Jomi = MonkeyLocation(Loc.western_jomi.value)
Western_Tammy = MonkeyLocation(Loc.western_tammy.value)
Western_Ukki_Gigolo = MonkeyLocation(Loc.western_ukki_gigolo.value)
Western_Monboron = MonkeyLocation(Loc.western_monboron.value)
Western_West_Ukki = MonkeyLocation(Loc.western_west_ukki.value)
Western_Lucky_Woo = MonkeyLocation(Loc.western_lucky_woo.value)
Western_Pamela = MonkeyLocation(Loc.western_pamela.value)
Western_Ukki_Monber = MonkeyLocation(Loc.western_ukki_monber.value)
Western_Gaukichi = MonkeyLocation(Loc.western_gaukichi.value)
Western_Shaluron = MonkeyLocation(Loc.western_shaluron.value)
Western_Jay_Mohn = MonkeyLocation(Loc.western_jay_mohn.value)
Western_Munkee_Joe = MonkeyLocation(Loc.western_munkee_joe.value)
Western_Saru_Chison = MonkeyLocation(Loc.western_saru_chison.value)
Western_Jaja_Jamo = MonkeyLocation(Loc.western_jaja_jamo.value)
Western_Chammy_Mo = MonkeyLocation(Loc.western_chammy_mo.value)
Western_Golon_Moe = MonkeyLocation(Loc.western_golon_moe.value)
Western_Golozo = MonkeyLocation(Loc.western_golozo.value)
Western_Ukkia_Munbo = MonkeyLocation(Loc.western_ukkia_munbo.value)
Western_Mon_Johny = MonkeyLocation(Loc.western_mon_johny.value)

## Monkey Blue Battle!
Boss_Monkey_Blue = MonkeyLocation(Loc.boss_monkey_blue.value)

### [< --- LOCATION GROUPS --- >]
# SEASIDE_MONKEYS : Sequence[MonkeyLocation] = [
#     Seaside_Nessal, Seaside_Ukki_Pia, Seaside_Sarubo, Seaside_Salurin, Seaside_Ukkitan, Seaside_Morella,
#     Seaside_Ukki_Ben, Seaside_Kankichi, Seaside_Tomezo, Seaside_Kamayan, Seaside_Taizo
# ]
#
# WOODS_MONKEYS : Sequence[MonkeyLocation] = [
#     Woods_Ukki_Pon, Woods_Ukkian, Woods_Ukki_Red, Woods_Rosalin, Woods_Salubon, Woods_Wolfmon, Woods_Ukiko,
#     Woods_Lambymon, Woods_Kreemon, Woods_Ukkilei, Woods_Spork, Woods_King_Goat, Woods_Marukichi, Woods_Kikimon,
#     Woods_Kominato
# ]
#
# CASTLE_MONKEYS : Sequence[MonkeyLocation] = [
#     Castle_Ukkido, Castle_Pipo_Guard, Castle_Monderella, Castle_Ukki_Ichi, Castle_Ukkinee, Castle_Saru_Mon,
#     Castle_Monga, Castle_Ukkiton, Castle_King_Leo, Castle_Ukkii, Castle_Saluto, Castle_Kings_Double,
#     Castle_Mattsun, Castle_Miya, Castle_Mon_San, Castle_SAL_1000
# ]

CISCOCITY_MONKEYS : Sequence[MonkeyLocation] = [
    Ciscocity_Ukima, Ciscocity_Monbolo, Ciscocity_Pipo_Mondy, Ciscocity_Ukki_Mattan, Ciscocity_Bemucho,
    Ciscocity_Ukki_Nader, Ciscocity_Sabu_Sabu, Ciscocity_Ginjiro, Ciscocity_Kichiemon, Ciscocity_Ukkilun,
    Ciscocity_Bully_Mon, Ciscocity_Ukki_Joe, Ciscocity_Tamaki, Ciscocity_Mickey_Oou, Ciscocity_Sally_Kokoroe,
    Ciscocity_Monkey_Manager, Ciscocity_Supervisor_Chimp, Ciscocity_Boss_Ape
]

STUDIO_MONKEYS : Sequence[MonkeyLocation] = [
    Studio_Ukki_Yan, Studio_Ukkipuss, Studio_Minoh, Studio_Monta, Studio_Pipopam, Studio_Monpii_Ukkichi,
    Studio_Gabimon, Studio_Bananamon, Studio_Mokinza, Studio_Bananamon, Studio_Ukki_Lee_Ukki, Studio_Ukkida_Jiro,
    Studio_Sal_Ukindo, Studio_Gimminey, Studio_Hant, Studio_Chippino, Studio_Ukki_Paul, Studio_Sally_Mon,
    Studio_Bonly, Studio_Monly
]

HALLOWEEN_MONKEYS : Sequence[MonkeyLocation] = [
    Halloween_Monkichiro, Halloween_Leomon, Halloween_Uikkun, Halloween_Take_Ukita, Halloween_Bonbon, Halloween_Chichi,
    Halloween_Ukkisuke, Halloween_Chibi_Sally, Halloween_Ukkison, Halloween_Saruhotep, Halloween_Ukkito,
    Halloween_Monzally, Halloween_Ukkiami, Halloween_Monjan, Halloween_Nattchan, Halloween_Kabochin, Halloween_Ukki_Mon,
    Halloween_Mumpkin
]

WESTERN_MONKEYS : Sequence[MonkeyLocation] = [
    Western_Morrey, Western_Jomi, Western_Tammy, Western_Ukki_Gigolo, Western_Monboron, Western_West_Ukki,
    Western_Lucky_Woo, Western_Pamela, Western_Ukki_Monber, Western_Gaukichi, Western_Shaluron, Western_Jay_Mohn,
    Western_Munkee_Joe, Western_Saru_Chison, Western_Jaja_Jamo, Western_Chammy_Mo, Western_Golon_Moe, Western_Golozo,
    Western_Ukkia_Munbo, Western_Mon_Johny
]

# BOSS_MONKEYS : Sequence[MonkeyLocation] = [
#     Boss_Monkey_White, Boss_Monkey_Blue
# ]

# MONKEYS : Sequence[MonkeyLocation] = [
#     Zero_Ukki_Pan, *SEASIDE_MONKEYS, *WOODS_MONKEYS, *CASTLE_MONKEYS, *CISCOCITY_MONKEYS, *STUDIO_MONKEYS,
#     *HALLOWEEN_MONKEYS, *WESTERN_MONKEYS, *BOSS_MONKEYS
# ]

# MASTER : Sequence[AE3LocationMeta] = [
#     *MONKEYS
# ]

# INDEX : Sequence[Sequence] = [
#     MASTER, MONKEYS, SEASIDE_MONKEYS, WOODS_MONKEYS, CASTLE_MONKEYS, CISCOCITY_MONKEYS, STUDIO_MONKEYS,
#     HALLOWEEN_MONKEYS, WESTERN_MONKEYS, BOSS_MONKEYS
# ]

### [< --- METHODS --- >]
# def generate_name_to_id() -> Dict[str, int]:
#     """Get a Dictionary of all Items in Name-ID pairs"""
#     i: AE3LocationMeta
#     return {i.name: i.loc_id for i in MASTER}



### [< --- STAGE GROUPS --- >]

# Zero
MONKEYS_ZERO : Sequence[str] = [
    Loc.zero_ukki_pan.value
]

# Seaside
MONKEYS_SEASIDE_A : Sequence[str] = [
    Loc.seaside_nessal.value, Loc.seaside_ukki_pia.value, Loc.seaside_sarubo.value, Loc.seaside_salurin.value,
    Loc.seaside_ukkitan.value, Loc.seaside_morella.value
]

MONKEYS_SEASIDE_B : Sequence[str] = [
    Loc.seaside_ukki_ben.value
]

MONKEYS_SEASIDE_C : Sequence[str] = [
    Loc.seaside_kankichi.value, Loc.seaside_tomezo.value, Loc.seaside_kamayan.value, Loc.seaside_taizo.value
]

MONKEYS_SEASIDE : Sequence[str] = [
    *MONKEYS_SEASIDE_A, *MONKEYS_SEASIDE_B, *MONKEYS_SEASIDE_C
]

# Woods
MONKEYS_WOODS_A : Sequence[str] = [
    Loc.woods_ukki_pon.value, Loc.woods_ukkian.value, Loc.woods_ukki_red.value, Loc.woods_rosalin.value
]

MONKEYS_WOODS_B : Sequence[str] = [
    Loc.woods_salubon.value, Loc.woods_wolfmon.value, Loc.woods_ukiko.value
]

MONKEYS_WOODS_C : Sequence[str] = [
    Loc.woods_lambymon.value, Loc.woods_kreemon.value, Loc.woods_ukkilei.value, Loc.woods_spork.value
]

MONKEYS_WOODS_D : Sequence[str] = [
    Loc.woods_king_goat.value, Loc.woods_marukichi.value, Loc.woods_kikimon.value, Loc.woods_kominato.value
]

MONKEYS_WOODS : Sequence[str] = [
    *MONKEYS_WOODS_A, *MONKEYS_WOODS_B, *MONKEYS_WOODS_C, *MONKEYS_WOODS_D
]

# Castle
MONKEYS_CASTLE_A : Sequence[str] = [
    Loc.castle_ukkido.value
]

MONKEYS_CASTLE_B : Sequence[str] = [
    Loc.castle_pipo_guard.value, Loc.castle_monderella.value, Loc.castle_ukki_ichi.value, Loc.castle_ukkinee.value
]

MONKEYS_CASTLE_C : Sequence[str] = [
    Loc.castle_saru_mon.value, Loc.castle_monga.value, Loc.castle_ukkiton.value, Loc.castle_king_leo.value
]

MONKEYS_CASTLE_D : Sequence[str] = [
    Loc.castle_ukkii.value, Loc.castle_saluto.value
]

MONKEYS_CASTLE_E : Sequence[str] = [
    Loc.castle_kings_double.value, Loc.castle_mattsun.value, Loc.castle_miya.value, Loc.castle_mon_san.value
]

MONKEYS_CASTLE_F : Sequence[str] = [
    Loc.castle_sal_1000.value
]

MONKEYS_CASTLE : Sequence[str] = [
    *MONKEYS_CASTLE_A, *MONKEYS_CASTLE_B, *MONKEYS_CASTLE_C, *MONKEYS_CASTLE_D, *MONKEYS_CASTLE_E, *MONKEYS_CASTLE_F
]

# Boss1
MONKEYS_BOSS1 : Sequence[str] = [ Loc.boss_monkey_white.value ]

# Ciscocity
MONKEYS_CISCOCITY_A : Sequence[str] = [
    Loc.ciscocity_ukima.value, Loc.ciscocity_monbolo.value, Loc.ciscocity_pipo_mondy.value,
    Loc.ciscocity_ukki_mattan.value, Loc.ciscocity_bemucho.value, Loc.ciscocity_ukki_nader.value
]

MONKEYS_CISCOCITY_B : Sequence[str] = [
    Loc.ciscocity_sabu_sabu.value, Loc.ciscocity_ginjiro.value, Loc.ciscocity_kichiemon.value
]

MONKEYS_CISCOCITY_C : Sequence[str] = [
    Loc.ciscocity_ukkilun.value
]

MONKEYS_CISCOCITY_D : Sequence[str] = [
    Loc.ciscocity_bully_mon.value, Loc.ciscocity_ukki_joe.value, Loc.ciscocity_tamaki.value,
    Loc.ciscocity_mickey_oou.value
]

MONKEYS_CISCOCITY_E : Sequence[str] = [
    Loc.ciscocity_sally_kokoroe.value, Loc.ciscocity_monkey_manager.value, Loc.ciscocity_supervisor_chimp.value,
    Loc.ciscocity_boss_ape.value
]

MONKEYS_CISCOCITY : Sequence[str] = [
    *MONKEYS_CISCOCITY_A, *MONKEYS_CISCOCITY_B, *MONKEYS_CISCOCITY_C, *MONKEYS_CISCOCITY_D, *MONKEYS_CISCOCITY_E,
]

# Studio
MONKEYS_STUDIO_A : Sequence[str] = [
    Loc.studio_ukki_yan.value
]

MONKEYS_STUDIO_B : Sequence[str] = [
    Loc.studio_ukkipuss.value, Loc.studio_minoh.value, Loc.studio_monta.value
]

MONKEYS_STUDIO_C : Sequence[str] = [
    Loc.studio_pipopam.value, Loc.studio_monpii_ukkichi.value, Loc.studio_gabimon.value
]

MONKEYS_STUDIO_D : Sequence[str] = [
    Loc.studio_bananamon.value, Loc.studio_mokinza.value
]

MONKEYS_STUDIO_E : Sequence[str] = [
    Loc.studio_ukki_lee_ukki.value, Loc.studio_ukkida_jiro.value, Loc.studio_sal_ukindo.value
]

MONKEYS_STUDIO_F : Sequence[str] = [
    Loc.studio_gimminey.value, Loc.studio_hant.value, Loc.studio_chippino.value
]

MONKEYS_STUDIO_G : Sequence[str] = [
    Loc.studio_ukki_paul.value, Loc.studio_sally_mon.value, Loc.studio_bonly.value, Loc.studio_monly.value
]

MONKEYS_STUDIO : Sequence[str] = [
    *MONKEYS_STUDIO_A, *MONKEYS_STUDIO_B, *MONKEYS_STUDIO_C, *MONKEYS_STUDIO_D, *MONKEYS_STUDIO_E, *MONKEYS_STUDIO_F,
    *MONKEYS_STUDIO_G,
]

# Halloween
MONKEYS_HALLOWEEN_A1 : Sequence[str] = [
    Loc.halloween_monkichiro.value
]

MONKEYS_HALLOWEEN_A : Sequence[str] = [
    Loc.halloween_leomon.value, Loc.halloween_uikkun.value, Loc.halloween_take_ukita.value
]

MONKEYS_HALLOWEEN_B : Sequence[str] = [
    Loc.halloween_bonbon.value, Loc.halloween_chichi.value
]

MONKEYS_HALLOWEEN_C : Sequence[str] = [
    Loc.halloween_ukkisuke.value, Loc.halloween_chibi_sally.value, Loc.halloween_ukkison.value
]

MONKEYS_HALLOWEEN_D : Sequence[str] = [
    Loc.halloween_saruhotep.value, Loc.halloween_ukkito.value, Loc.halloween_monzally.value,
    Loc.halloween_ukkiami.value
]

MONKEYS_HALLOWEEN_E : Sequence[str] = [
    Loc.halloween_monjan.value, Loc.halloween_nattchan.value, Loc.halloween_kabochin.value,
    Loc.halloween_ukki_mon.value
]

MONKEYS_HALLOWEEN_F : Sequence[str] = [
    Loc.halloween_mumpkin.value
]

MONKEYS_HALLOWEEN : Sequence[str] = [
    *MONKEYS_HALLOWEEN_A1, *MONKEYS_HALLOWEEN_A, *MONKEYS_HALLOWEEN_B, *MONKEYS_HALLOWEEN_C, *MONKEYS_HALLOWEEN_D,
    *MONKEYS_HALLOWEEN_E,  *MONKEYS_HALLOWEEN_F
]

# Western
MONKEYS_WESTERN_A : Sequence[str] = [
    Loc.western_morrey.value, Loc.western_jomi.value, Loc.western_tammy.value
]

MONKEYS_WESTERN_B : Sequence[str] = [
    Loc.western_ukki_gigolo.value, Loc.western_monboron.value, Loc.western_west_ukki.value
]

MONKEYS_WESTERN_C : Sequence[str] = [
    Loc.western_lucky_woo.value, Loc.western_pamela.value, Loc.western_ukki_monber.value, Loc.western_gaukichi.value
]

MONKEYS_WESTERN_D : Sequence[str] = [
    Loc.western_shaluron.value, Loc.western_jay_mohn.value, Loc.western_munkee_joe.value, Loc.western_saru_chison.value,
    Loc.western_jaja_jamo.value
]

MONKEYS_WESTERN_E : Sequence[str] = [
    Loc.western_chammy_mo.value, Loc.western_golon_moe.value, Loc.western_golozo.value
]

MONKEYS_WESTERN_F : Sequence[str] = [
    Loc.western_ukkia_munbo.value, Loc.western_mon_johny.value
]

MONKEYS_WESTERN : Sequence[str] = [
    *MONKEYS_WESTERN_A, *MONKEYS_WESTERN_B, *MONKEYS_WESTERN_C, *MONKEYS_WESTERN_D, *MONKEYS_WESTERN_E,
    *MONKEYS_WESTERN_F,
]

# Boss2
MONKEYS_BOSS2 : Sequence[str] = [
    Loc.boss_monkey_blue.value
]

# Onsen
MONKEYS_ONSEN_A : Sequence[str] = [
    Loc.onsen_chabimon.value, Loc.onsen_ukki_ichiro.value
]

MONKEYS_ONSEN_A1 : Sequence[str] = [
    Loc.onsen_michiyan.value, Loc.onsen_tome_san.value
]

MONKEYS_ONSEN_A2 : Sequence[str] = [
    Loc.onsen_kiichiro.value, Loc.onsen_saru_sam.value
]

MONKEYS_ONSEN_B : Sequence[str] = [
    Loc.onsen_ukki_emon.value, Loc.onsen_moki.value, Loc.onsen_ukimi.value, Loc.onsen_domobeh.value
]

MONKEYS_ONSEN_C : Sequence[str] = [
    Loc.onsen_sam_san.value, Loc.onsen_donkichi.value, Loc.onsen_minokichi.value, Loc.onsen_tatabo.value
]

MONKEYS_ONSEN_D : Sequence[str] = [
    Loc.onsen_michiro.value, Loc.onsen_gen_san.value
]

MONKEYS_ONSEN_D1 : Sequence[str] = [
    Loc.onsen_kimi_san.value
]

MONKEYS_ONSEN_E : Sequence[str] = [
    Loc.onsen_mujakin.value, Loc.onsen_mihachin.value, Loc.onsen_fuji_chan.value
]

MONKEYS_ONSEN : Sequence[str] = [
    *MONKEYS_ONSEN_A, *MONKEYS_ONSEN_A1, *MONKEYS_ONSEN_A2, *MONKEYS_ONSEN_B, *MONKEYS_ONSEN_C, *MONKEYS_ONSEN_D,
    *MONKEYS_ONSEN_D1, *MONKEYS_ONSEN_E
]

# Snowfesta
MONKEYS_SNOWFESTA_A : Sequence[str] = [
    Loc.snowfesta_kimisuke.value, Loc.snowfesta_konzo.value, Loc.snowfesta_saburota.value, Loc.snowfesta_mitsuro.value,
    Loc.snowfesta_takuo.value, Loc.snowfesta_konkichi.value
]

MONKEYS_SNOWFESTA_B : Sequence[str] = [
    Loc.snowfesta_fumikichi.value, Loc.snowfesta_pipotron_yellow.value
]

MONKEYS_SNOWFESTA_C : Sequence[str] = [
    Loc.snowfesta_tamubeh.value, Loc.snowfesta_kimikichi.value, Loc.snowfesta_gonbeh.value
]

MONKEYS_SNOWFESTA_D : Sequence[str] = [
    Loc.snowfesta_shimmy.value
]

MONKEYS_SNOWFESTA_E : Sequence[str] = [
    Loc.snowfesta_mako.value, Loc.snowfesta_miko.value, Loc.snowfesta_tamio.value, Loc.snowfesta_jeitan.value,
    Loc.snowfesta_ukki_jii.value
]

MONKEYS_SNOWFESTA_F : Sequence[str] = [
    Loc.snowfesta_akki_bon.value
]

MONKEYS_SNOWFESTA_G : Sequence[str] = [
    Loc.snowfesta_kimi_chan.value, Loc.snowfesta_sae_chan.value, Loc.snowfesta_tassan.value,
    Loc.snowfesta_tomokun.value
]

MONKEYS_SNOWFESTA : Sequence[str] = [
    *MONKEYS_SNOWFESTA_A, *MONKEYS_SNOWFESTA_B, *MONKEYS_SNOWFESTA_C, *MONKEYS_SNOWFESTA_D, *MONKEYS_SNOWFESTA_E,
    *MONKEYS_SNOWFESTA_F, *MONKEYS_SNOWFESTA_G,
]

# Edotown
MONKEYS_EDOTOWN_A : Sequence[str] = [
    Loc.edotown_pipo_tobi.value, Loc.edotown_masan.value, Loc.edotown_mohachi.value
]

MONKEYS_EDOTOWN_B : Sequence[str] = [
    Loc.edotown_mon_ninpo.value, Loc.edotown_yosio.value, Loc.edotown_fatty_mcfats.value
]

MONKEYS_EDOTOWN_C : Sequence[str] = [
    Loc.edotown_tomoku_chan.value, Loc.edotown_uziko.value, Loc.edotown_gp.value
]

MONKEYS_EDOTOWN_C1 : Sequence[str] = [
    Loc.edotown_kikimaru.value
]

MONKEYS_EDOTOWN_D : Sequence[str] = [
    Loc.edotown_walter.value, Loc.edotown_monkibeth.value, Loc.edotown_babuzo.value, Loc.edotown_fishy_feet.value,
    Loc.edotown_pipo_torin.value
]

MONKEYS_EDOTOWN_E : Sequence[str] = [
    Loc.edotown_tomi.value, Loc.edotown_master_pan.value
]

MONKEYS_EDOTOWN_F : Sequence[str] = [
    Loc.edotown_monchin_chi.value, Loc.edotown_masachi.value, Loc.edotown_golota.value, Loc.edotown_kinsuke.value
]

MONKEYS_EDOTOWN : Sequence[str] = [
    *MONKEYS_EDOTOWN_A, *MONKEYS_EDOTOWN_B, *MONKEYS_EDOTOWN_C, *MONKEYS_EDOTOWN_C1, *MONKEYS_EDOTOWN_D,
    *MONKEYS_EDOTOWN_E, *MONKEYS_EDOTOWN_F,
]

# Boss3
MONKEYS_BOSS3 : Sequence[str] = [
    Loc.boss_monkey_yellow.value
]

# Heaven
MONKEYS_HEAVEN_A : Sequence[str] = [
    Loc.heaven_ukkichi.value, Loc.heaven_chomon.value, Loc.heaven_ukkido.value
]

MONKEYS_HEAVEN_B : Sequence[str] = [
    Loc.heaven_kyamio.value, Loc.heaven_talupon.value, Loc.heaven_bokitan.value, Loc.heaven_tami.value,
    Loc.heaven_micchino.value,
]

MONKEYS_HEAVEN_C : Sequence[str] = [
    Loc.heaven_talurin.value, Loc.heaven_occhimon.value, Loc.heaven_mikkurin.value, Loc.heaven_kicchino.value,
    Loc.heaven_kimurin.value, Loc.heaven_sakkano.value
]

MONKEYS_HEAVEN_D : Sequence[str] = [
    Loc.heaven_camino.value, Loc.heaven_valuccha.value
]

MONKEYS_HEAVEN_E : Sequence[str] = [
    Loc.heaven_pisuke.value, Loc.heaven_kansuke.value, Loc.heaven_pohta.value, Loc.heaven_keisuke.value
]

MONKEYS_HEAVEN : Sequence[str] = [
    *MONKEYS_HEAVEN_A, *MONKEYS_HEAVEN_B, *MONKEYS_HEAVEN_C, *MONKEYS_HEAVEN_D, *MONKEYS_HEAVEN_E
]

# Toyhouse
MONKEYS_TOYHOUSE_A : Sequence[str] = [
    Loc.toyhouse_pikkori.value, Loc.toyhouse_talukki.value, Loc.toyhouse_pinkino.value
]

MONKEYS_TOYHOUSE_B : Sequence[str] = [
    Loc.toyhouse_bon_mota.value, Loc.toyhouse_bon_verna.value, Loc.toyhouse_bon_papa.value, Loc.toyhouse_bon_mama.value,
    Loc.toyhouse_kalkin.value
]

MONKEYS_TOYHOUSE_C : Sequence[str] = [
    Loc.toyhouse_pakun.value, Loc.toyhouse_ukki_x.value, Loc.toyhouse_mon_gareji.value, Loc.toyhouse_shouji.value,
    Loc.toyhouse_woo_makka.value
]

MONKEYS_TOYHOUSE_D : Sequence[str] = [
    Loc.toyhouse_monto.value, Loc.toyhouse_mokitani.value, Loc.toyhouse_namigo.value, Loc.toyhouse_pipotron_red.value
]

MONKEYS_TOYHOUSE_E1 : Sequence[str] = [
    Loc.toyhouse_master_loafy.value
]

MONKEYS_TOYHOUSE_F : Sequence[str] = [
    Loc.toyhouse_golonero.value
]

MONKEYS_TOYHOUSE_G : Sequence[str] = [
    Loc.toyhouse_kocho.value
]

MONKEYS_TOYHOUSE_H : Sequence[str] = [
    Loc.toyhouse_tam_konta.value, Loc.toyhouse_tam_mimiko.value, Loc.toyhouse_tam_papa.value,
    Loc.toyhouse_tam_mama.value
]

MONKEYS_TOYHOUSE : Sequence[str] = [
    *MONKEYS_TOYHOUSE_A, *MONKEYS_TOYHOUSE_B, *MONKEYS_TOYHOUSE_C, *MONKEYS_TOYHOUSE_D, *MONKEYS_TOYHOUSE_E1,
    *MONKEYS_TOYHOUSE_F, *MONKEYS_TOYHOUSE_G, *MONKEYS_TOYHOUSE_H,
]

# Iceland
MONKEYS_ICELAND_A : Sequence[str] = [
    Loc.iceland_bikupuri.value, Loc.iceland_ukkisu.value, Loc.iceland_ukki_ami.value, Loc.iceland_balio.value
]

MONKEYS_ICELAND_B : Sequence[str] = [
    Loc.iceland_kimkon.value, Loc.iceland_ukkina.value, Loc.iceland_kushachin.value
]

MONKEYS_ICELAND_C : Sequence[str] = [
    Loc.iceland_malikko.value, Loc.iceland_bolikko.value
]

MONKEYS_ICELAND_D : Sequence[str] = [
    Loc.iceland_iceymon.value, Loc.iceland_mokkidon.value
]

MONKEYS_ICELAND_E : Sequence[str] = [
    Loc.iceland_jolly_mon.value, Loc.iceland_hikkori.value, Loc.iceland_rammy.value
]

MONKEYS_ICELAND_F : Sequence[str] = [
    Loc.iceland_monkino.value, Loc.iceland_kyam.value, Loc.iceland_kappino.value, Loc.iceland_kris_krimon.value
]

MONKEYS_ICELAND : Sequence[str] = [
    *MONKEYS_ICELAND_A, *MONKEYS_ICELAND_B, *MONKEYS_ICELAND_C, *MONKEYS_ICELAND_D, *MONKEYS_ICELAND_E,
    *MONKEYS_ICELAND_F
]

# Arabian
MONKEYS_ARABIAN_A : Sequence[str] = [
    Loc.arabian_scorpi_mon.value, Loc.arabian_minimon.value, Loc.arabian_moontero.value
]

MONKEYS_ARABIAN_B : Sequence[str] = [
    Loc.arabian_ukki_son.value, Loc.arabian_ukki_jeff.value, Loc.arabian_saru_maru.value, Loc.arabian_genghis_mon.value,
    Loc.arabian_cup_o_mon.value
]

MONKEYS_ARABIAN_C : Sequence[str] = [
    Loc.arabian_nijal.value, Loc.arabian_apey_jones.value, Loc.arabian_golden_mon.value
]

MONKEYS_ARABIAN_C1 : Sequence[str] = [
Loc.arabian_ukki_mamba.value, Loc.arabian_crazy_ol_mon.value
]

MONKEYS_ARABIAN_E : Sequence[str] = [
    Loc.arabian_shamila.value, Loc.arabian_tamiyanya.value, Loc.arabian_salteenz.value,
    Loc.arabian_dancing_mia.value, Loc.arabian_princess_judy.value
]

MONKEYS_ARABIAN_F : Sequence[str] = [
    Loc.arabian_miccho.value, Loc.arabian_kisha.value, Loc.arabian_gimuccho.value, Loc.arabian_wojin.value
]

MONKEYS_ARABIAN : Sequence[str] = [
    *MONKEYS_ARABIAN_A, *MONKEYS_ARABIAN_B, *MONKEYS_ARABIAN_C, *MONKEYS_ARABIAN_C1, *MONKEYS_ARABIAN_E,
    *MONKEYS_ARABIAN_F
]

# Boss4
MONKEYS_BOSS4 : Sequence[str] = [
    Loc.boss_monkey_pink.value
]

MONKEYS_BOSSES : Sequence[str] = [
    *MONKEYS_BOSS1, *MONKEYS_BOSS2, *MONKEYS_BOSS3, *MONKEYS_BOSS4
]

MONKEYS_MASTER : Sequence[str] = [
    *MONKEYS_ZERO, *MONKEYS_SEASIDE, *MONKEYS_WOODS, *MONKEYS_CASTLE, *MONKEYS_CISCOCITY, *MONKEYS_STUDIO,
    *MONKEYS_HALLOWEEN, *MONKEYS_WESTERN, *MONKEYS_ONSEN, *MONKEYS_SNOWFESTA, *MONKEYS_EDOTOWN, *MONKEYS_HEAVEN,
    *MONKEYS_TOYHOUSE, *MONKEYS_ICELAND, *MONKEYS_ARABIAN, *MONKEYS_BOSSES
]
MONKEYS_INDEX : dict[str, Sequence] = {
    # Zero
    Stage.zero.value            : MONKEYS_ZERO,

    # Seaside
    Stage.seaside_a.value       : MONKEYS_SEASIDE_A,
    Stage.seaside_b.value       : MONKEYS_SEASIDE_B,
    Stage.seaside_c.value       : MONKEYS_SEASIDE_C,

    # Woods
    Stage.woods_a.value         : MONKEYS_WOODS_A,
    Stage.woods_b.value         : MONKEYS_WOODS_B,
    Stage.woods_c.value         : MONKEYS_WOODS_C,
    Stage.woods_d.value         : MONKEYS_WOODS_D,

    # Castle
    Stage.castle_a.value        : MONKEYS_CASTLE_A,
    Stage.castle_b.value        : MONKEYS_CASTLE_B,
    Stage.castle_c.value        : MONKEYS_CASTLE_C,
    Stage.castle_d.value        : MONKEYS_CASTLE_D,
    Stage.castle_e.value        : MONKEYS_CASTLE_E,
    Stage.castle_f.value        : MONKEYS_CASTLE_F,

    # Boss1
    Stage.boss1.value           : MONKEYS_BOSS1,

    # Ciscocity
    Stage.ciscocity_a.value     : MONKEYS_CISCOCITY_A,
    Stage.ciscocity_b.value     : MONKEYS_CISCOCITY_B,
    Stage.ciscocity_c.value     : MONKEYS_CISCOCITY_C,
    Stage.ciscocity_d.value     : MONKEYS_CISCOCITY_D,
    Stage.ciscocity_e.value     : MONKEYS_CISCOCITY_E,

    # Studio
    Stage.studio_a.value        : MONKEYS_STUDIO_A,
    Stage.studio_b.value        : MONKEYS_STUDIO_B,
    Stage.studio_c.value        : MONKEYS_STUDIO_C,
    Stage.studio_d.value        : MONKEYS_STUDIO_D,
    Stage.studio_e.value        : MONKEYS_STUDIO_E,
    Stage.studio_f.value        : MONKEYS_STUDIO_F,
    Stage.studio_g.value        : MONKEYS_STUDIO_G,

    # Halloween
    Stage.halloween_a1.value    : MONKEYS_HALLOWEEN_A1,
    Stage.halloween_a.value     : MONKEYS_HALLOWEEN_A,
    Stage.halloween_b.value     : MONKEYS_HALLOWEEN_B,
    Stage.halloween_c.value     : MONKEYS_HALLOWEEN_C,
    Stage.halloween_d.value     : MONKEYS_HALLOWEEN_D,
    Stage.halloween_e.value     : MONKEYS_HALLOWEEN_E,
    Stage.halloween_f.value     : MONKEYS_HALLOWEEN_F,

    # Western
    Stage.western_a.value       : MONKEYS_WESTERN_A,
    Stage.western_b.value       : MONKEYS_WESTERN_B,
    Stage.western_c.value       : MONKEYS_WESTERN_C,
    Stage.western_d.value       : MONKEYS_WESTERN_D,
    Stage.western_e.value       : MONKEYS_WESTERN_E,
    Stage.western_f.value       : MONKEYS_WESTERN_F,

    # Boss2
    Stage.boss2.value           : MONKEYS_BOSS2,

    # Onsen
    Stage.onsen_a.value         : MONKEYS_ONSEN_A,
    Stage.onsen_a1.value        : MONKEYS_ONSEN_A1,
    Stage.onsen_a2.value        : MONKEYS_ONSEN_A2,
    Stage.onsen_b.value         : MONKEYS_ONSEN_B,
    Stage.onsen_c.value         : MONKEYS_ONSEN_C,
    Stage.onsen_d.value         : MONKEYS_ONSEN_D,
    Stage.onsen_d1.value        : MONKEYS_ONSEN_D1,
    Stage.onsen_e.value         : MONKEYS_ONSEN_E,

    # Snowfesta
    Stage.snowfesta_a.value     : MONKEYS_SNOWFESTA_A,
    Stage.snowfesta_b.value     : MONKEYS_SNOWFESTA_B,
    Stage.snowfesta_c.value     : MONKEYS_SNOWFESTA_C,
    Stage.snowfesta_d.value     : MONKEYS_SNOWFESTA_D,
    Stage.snowfesta_e.value     : MONKEYS_SNOWFESTA_E,
    Stage.snowfesta_f.value     : MONKEYS_SNOWFESTA_F,
    Stage.snowfesta_g.value     : MONKEYS_SNOWFESTA_G,

    # Edotown
    Stage.edotown_a.value       : MONKEYS_EDOTOWN_A,
    Stage.edotown_b.value       : MONKEYS_EDOTOWN_B,
    Stage.edotown_c.value       : MONKEYS_EDOTOWN_C,
    Stage.edotown_c1.value      : MONKEYS_EDOTOWN_C1,
    Stage.edotown_d.value       : MONKEYS_EDOTOWN_D,
    Stage.edotown_e.value       : MONKEYS_EDOTOWN_E,
    Stage.edotown_f.value       : MONKEYS_EDOTOWN_F,

    # Boss3
    Stage.boss3.value           : MONKEYS_BOSS3,

    # Heaven
    Stage.heaven_a.value        : MONKEYS_HEAVEN_A,
    Stage.heaven_b.value        : MONKEYS_HEAVEN_B,
    Stage.heaven_c.value        : MONKEYS_HEAVEN_C,
    Stage.heaven_d.value        : MONKEYS_HEAVEN_D,
    Stage.heaven_e.value        : MONKEYS_HEAVEN_E,

    # Toyhouse
    Stage.toyhouse_a.value      : MONKEYS_TOYHOUSE_A,
    Stage.toyhouse_b.value      : MONKEYS_TOYHOUSE_B,
    Stage.toyhouse_c.value      : MONKEYS_TOYHOUSE_C,
    Stage.toyhouse_d.value      : MONKEYS_TOYHOUSE_D,
    Stage.toyhouse_e1.value     : MONKEYS_TOYHOUSE_E1,
    Stage.toyhouse_f.value      : MONKEYS_TOYHOUSE_F,
    Stage.toyhouse_g.value      : MONKEYS_TOYHOUSE_G,
    Stage.toyhouse_h.value      : MONKEYS_TOYHOUSE_H,

    # Iceland
    Stage.iceland_a.value       : MONKEYS_ICELAND_A,
    Stage.iceland_b.value       : MONKEYS_ICELAND_B,
    Stage.iceland_c.value       : MONKEYS_ICELAND_C,
    Stage.iceland_d.value       : MONKEYS_ICELAND_D,
    Stage.iceland_e.value       : MONKEYS_ICELAND_E,
    Stage.iceland_f.value       : MONKEYS_ICELAND_F,

    # Arabian
    Stage.arabian_a.value       : MONKEYS_ARABIAN_A,
    Stage.arabian_b.value       : MONKEYS_ARABIAN_B,
    Stage.arabian_c.value       : MONKEYS_ARABIAN_C,
    Stage.arabian_c1.value      : MONKEYS_ARABIAN_C1,
    Stage.arabian_e.value       : MONKEYS_ARABIAN_E,
    Stage.arabian_f.value       : MONKEYS_ARABIAN_F,

    # Boss4
    Stage.boss4.value           : MONKEYS_BOSS4,
}

EVENTS_STUDIO_A1 : Sequence[EventMeta] = [
    EventMeta(Game.shortcut_studio_ad.value)
]

EVENTS_EDOTOWN_E : Sequence[EventMeta] = [
    EventMeta(Game.shortcut_edotown_eb.value)
]

EVENTS_ICELAND_E : Sequence[EventMeta] = [
    EventMeta(Game.trigger_iceland_e.value, AccessRule.SLING)
]

EVENTS_ARABIAN_C : Sequence[EventMeta] = [
    EventMeta(Game.trigger_arabian_c.value, AccessRule.CATCH)
]

EVENTS_ARABIAN_E1 : Sequence[EventMeta] = [
    EventMeta(Game.trigger_arabian_e1.value, AccessRule.GENIE)
]

EVENTS_INDEX : dict[str, Sequence[EventMeta]] = {
    Stage.iceland_e.value        : EVENTS_ICELAND_E,
    Stage.arabian_c.value        : EVENTS_ARABIAN_C,
    Stage.arabian_e1.value       : EVENTS_ARABIAN_E1,

    Stage.studio_a1.value        : EVENTS_STUDIO_A1,
    Stage.edotown_e.value        : EVENTS_EDOTOWN_E
}

def generate_name_to_id() -> dict[str, int]:
    return { name : MonkeyLocation(name).loc_id for name in MONKEYS_MASTER }