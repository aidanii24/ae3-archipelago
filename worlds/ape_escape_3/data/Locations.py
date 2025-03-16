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

MONKEYS_BOSSES : Sequence[str] = [
    *MONKEYS_BOSS1, *MONKEYS_BOSS2
]

MONKEYS_MASTER : Sequence[str] = [
    *MONKEYS_ZERO, *MONKEYS_SEASIDE, *MONKEYS_WOODS, *MONKEYS_CASTLE, *MONKEYS_CISCOCITY, *MONKEYS_STUDIO,
    *MONKEYS_BOSSES
]

EVENTS_STUDIO_A1 : Sequence[EventMeta] = [
    EventMeta(Game.shortcut_studio_ad.value)
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
}

EVENTS_INDEX : dict[str, Sequence[EventMeta]] = {
    Stage.studio_a1.value        : EVENTS_STUDIO_A1
}

# TODO - Rename this
def generate_name_to_id() -> dict[str, int]:
    return { name : MonkeyLocation(name).loc_id for name in MONKEYS_MASTER }