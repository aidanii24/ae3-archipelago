from typing import Callable, Set, Sequence, TYPE_CHECKING
from dataclasses import dataclass
from abc import ABC

from BaseClasses import Location, Region, ItemClassification

from .Strings import Loc, Stage, Game, Meta, APHelper
from .Logic import AccessRule, Rulesets
from .Addresses import NTSCU


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
        Only parameters of type RuleSet can set Critical Rules.
    """

    def __init__(self, name : str):
        self.name = name
        # Locations can be assumed to always be in Addresses.Locations. NTSCU version will be used as basis for the ID.
        self.loc_id = NTSCU.Locations[name]
        self.address = self.loc_id
        self.rules = Rulesets()

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
        from .Items import AE3Item

        event : Location = Location(player, self.name, None, parent)
        item : AE3Item = AE3Item(self.name, ItemClassification.progression, None, player)

        event.place_locked_item(item)

        return event

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

# Asia
MONKEYS_ASIA_A : Sequence[str] = [
    Loc.asia_pincher_mon.value
]

MONKEYS_ASIA_A1 : Sequence[str] = [
    Loc.asia_salumani.value, Loc.asia_salulu.value
]

MONKEYS_ASIA_A3 : Sequence[str] = [
    Loc.asia_baku.value
]

MONKEYS_ASIA_A4 : Sequence[str] = [
    Loc.asia_ukki_mat.value, Loc.asia_salunch.value
]

MONKEYS_ASIA_B : Sequence[str] = [
    Loc.asia_mong_popo.value, Loc.asia_mohcha.value, Loc.asia_kamcha.value
]

MONKEYS_ASIA_B1 : Sequence[str] = [
    Loc.asia_bimocha.value, Loc.asia_gimchin.value
]

MONKEYS_ASIA_B2 : Sequence[str] = [
    Loc.asia_kamaccha.value
]

MONKEYS_ASIA_D : Sequence[str] = [
    Loc.asia_gyamu.value, Loc.asia_tartan.value
]

MONKEYS_ASIA_D2 : Sequence[str] = [
    Loc.asia_takumon.value, Loc.asia_ukki_ether.value
]

MONKEYS_ASIA_E1 : Sequence[str] = [
    Loc.asia_molzone.value
]

MONKEYS_ASIA_E2 : Sequence[str] = [
    Loc.asia_chappio.value, Loc.asia_pomoah.value
]

MONKEYS_ASIA_F : Sequence[str] = [
    Loc.asia_gucchai.value, Loc.asia_makaccho.value, Loc.asia_gamaran.value, Loc.asia_larry.value
]

MONKEYS_ASIA : Sequence[str] = [
    *MONKEYS_ASIA_A, *MONKEYS_ASIA_A1, *MONKEYS_ASIA_A3, *MONKEYS_ASIA_A4, *MONKEYS_ASIA_B, *MONKEYS_ASIA_B1,
    *MONKEYS_ASIA_B1, *MONKEYS_ASIA_B2, *MONKEYS_ASIA_D, *MONKEYS_ASIA_D2, *MONKEYS_ASIA_E1, *MONKEYS_ASIA_E2,
    *MONKEYS_ASIA_F
]

# Plane
MONKEYS_PLANE_A : Sequence[str] = [
    Loc.plane_romo.value, Loc.plane_temko.value
]

MONKEYS_PLANE_A1 : Sequence[str] = [
    Loc.plane_ukkigawa.value
]

MONKEYS_PLANE_B : Sequence[str] = [
    Loc.plane_mokkido.value
]

MONKEYS_PLANE_B1 : Sequence[str] = [
    Loc.plane_pont.value, Loc.plane_gamish.value,
]

MONKEYS_PLANE_C : Sequence[str] = [
    Loc.plane_takmon.value, Loc.plane_mukita.value
]

MONKEYS_PLANE_C1 : Sequence[str] = [
    Loc.plane_prince_bertus.value, Loc.plane_chai_bunny.value
]

MONKEYS_PLANE_D : Sequence[str] = [
    Loc.plane_tamrai.value, Loc.plane_kemunpa.value, Loc.plane_pipotron_blue.value
]

MONKEYS_PLANE_E : Sequence[str] = [
    Loc.plane_mabaras.value, Loc.plane_tamoos.value, Loc.plane_kimoto.value
]

MONKEYS_PLANE_F1 : Sequence[str] = [
    Loc.plane_octavian.value
]

MONKEYS_PLANE_G : Sequence[str] = [
    Loc.plane_samuel.value, Loc.plane_coril.value, Loc.plane_bont.value, Loc.plane_delly.value
]

MONKEYS_PLANE_H : Sequence[str] = [
    Loc.plane_jeloh.value, Loc.plane_bongo.value
]

MONKEYS_PLANE : Sequence[str] = [
    *MONKEYS_PLANE_A, *MONKEYS_PLANE_A1, *MONKEYS_PLANE_B, *MONKEYS_PLANE_B1, *MONKEYS_PLANE_C, *MONKEYS_PLANE_C1,
    *MONKEYS_PLANE_D, *MONKEYS_PLANE_E, *MONKEYS_PLANE_F1, *MONKEYS_PLANE_G, *MONKEYS_PLANE_H
]

# Hong
MONKEYS_HONG_A : Sequence[str] = [
    Loc.hong_dally.value, Loc.hong_nak_nayo.value,
]

MONKEYS_HONG_A1 : Sequence[str] = [
    Loc.hong_donto_koi.value, Loc.hong_po_kin_ki.value
]

MONKEYS_HONG_A2 : Sequence[str] = [
    Loc.hong_dally.value,
]

MONKEYS_HONG_B : Sequence[str] = [
    Loc.hong_ukki_chan.value, Loc.hong_uki_uki.value, Loc.hong_muki_muki.value, Loc.hong_hi_uchi_ishi.value
]

MONKEYS_HONG_B1 : Sequence[str] = [
    Loc.hong_shinchi.value, Loc.hong_doh_tsuitaro.value
]

MONKEYS_HONG_C : Sequence[str] = [
    Loc.hong_bassili_ukki.value, Loc.hong_pikon.value, Loc.hong_bankan.value, Loc.hong_sukei.value,
    Loc.hong_giyan.value
]

MONKEYS_HONG_C1 : Sequence[str] = [
    Loc.hong_danchi.value
]

MONKEYS_HONG_C2 : Sequence[str] = [
    Loc.hong_gala_waruo.value
]

MONKEYS_HONG_D : Sequence[str] = [
    Loc.hong_muchaki.value
]

MONKEYS_HONG_E : Sequence[str] = [
    Loc.hong_yoh_kitana.value, Loc.hong_goshi_andos.value, Loc.hong_pukuman.value
]

MONKEYS_HONG_E1 : Sequence[str] = [
    Loc.hong_block_master.value
]

MONKEYS_HONG_F : Sequence[str] = [
    Loc.hong_tompo.value, Loc.hong_wootan.value, Loc.hong_chechin.value, Loc.hong_hapcho.value
]

MONKEYS_HONG_G : Sequence[str] = [
    Loc.hong_bonmos.value, Loc.hong_dark_master.value
]

MONKEYS_HONG_H : Sequence[str] = [
    Loc.hong_teh_isu.value, Loc.hong_ponja.value
]

MONKEYS_HONG : Sequence[str] = [
    *MONKEYS_HONG_A, *MONKEYS_HONG_A1, *MONKEYS_HONG_B, *MONKEYS_HONG_B1, *MONKEYS_HONG_C, *MONKEYS_HONG_C1,
    *MONKEYS_HONG_D, *MONKEYS_HONG_E, *MONKEYS_HONG_E1, *MONKEYS_HONG_F, *MONKEYS_HONG_G, *MONKEYS_HONG_H
]

# boss5
MONKEYS_BOSS5 : Sequence[str] = [
    Loc.boss_monkey_red.value
]

# Bay
MONKEYS_BAY_A : Sequence[str] = [
    Loc.bay_nadamon.value, Loc.bay_patoya.value
]

MONKEYS_BAY_A1 : Sequence[str] = [
    Loc.bay_gumbo.value, Loc.bay_pehyan.value
]

MONKEYS_BAY_A5 : Sequence[str] = [
    Loc.bay_mokito.value
]

MONKEYS_BAY_B : Sequence[str] = [
    Loc.bay_pipo_kate.value, Loc.bay_samtan.value, Loc.bay_pokkine.value, Loc.bay_daban.value
]

MONKEYS_BAY_C : Sequence[str] = [
    Loc.bay_shiny_pete.value, Loc.bay_keiichi.value, Loc.bay_landon.value, Loc.bay_mcbreezy.value,
    Loc.bay_ronson.value, Loc.bay_gimo.value
]

MONKEYS_BAY_D : Sequence[str] = [
    Loc.bay_hiroshi.value, Loc.bay_mibon.value, Loc.bay_bololon.value
]

MONKEYS_BAY_D1 : Sequence[str] = [
    Loc.bay_nakabi.value
]

MONKEYS_BAY_E : Sequence[str] = [
    Loc.bay_doemos.value
]

MONKEYS_BAY_E1 : Sequence[str] = [
    Loc.bay_kazuo.value
]

MONKEYS_BAY_E2 : Sequence[str] = [
    Loc.bay_gimi_gimi.value, Loc.bay_pokkini.value, Loc.bay_bokino.value
]

MONKEYS_BAY_E3 : Sequence[str] = [
    Loc.bay_jimo.value
]

MONKEYS_BAY_F : Sequence[str] = [
    Loc.bay_makidon.value, Loc.bay_dogy.value, Loc.bay_gibdon.value, Loc.bay_buligie.value
]

MONKEYS_BAY : Sequence[str] = [
    *MONKEYS_BAY_A, *MONKEYS_BAY_A1, *MONKEYS_BAY_A5, *MONKEYS_BAY_B, *MONKEYS_BAY_C, *MONKEYS_BAY_D, *MONKEYS_BAY_D1,
    *MONKEYS_BAY_E, *MONKEYS_BAY_E1, *MONKEYS_BAY_E2, *MONKEYS_BAY_E3, *MONKEYS_BAY_F,
]

# Tomo
MONKEYS_TOMO_A : Sequence[str] = [
    Loc.tomo_kichibeh.value, Loc.tomo_bonchicchi.value, Loc.tomo_mikibon.value
]

MONKEYS_TOMO_B : Sequence[str] = [
    Loc.tomo_dj_tamo.value, Loc.tomo_ukkinaka.value, Loc.tomo_ukkine.value, Loc.tomo_pon_jiro.value
]

MONKEYS_TOMO_C : Sequence[str] = [
    Loc.tomo_chimpy.value, Loc.tomo_kajitan.value, Loc.tomo_uka_uka.value, Loc.tomo_mil_mil.value
]

MONKEYS_TOMO_E : Sequence[str] = [
    Loc.tomo_taimon.value, Loc.tomo_goro_san.value
]

MONKEYS_TOMO_E1 : Sequence[str] = [
    Loc.tomo_reiji.value
]

MONKEYS_TOMO_E2 : Sequence[str] = [
    Loc.tomo_ponta.value, Loc.tomo_tomio.value, Loc.tomo_gario.value
]

MONKEYS_TOMO_F1 : Sequence[str] = [
    Loc.tomo_dj_pari.value
]

MONKEYS_TOMO_F2 : Sequence[str] = [
    Loc.tomo_mitsuo.value
]

MONKEYS_TOMO_G : Sequence[str] = [
    Loc.tomo_pipo_ron.value, Loc.tomo_mikita.value,
]

MONKEYS_TOMO_G1 : Sequence[str] = [
    Loc.tomo_riley.value,
]

MONKEYS_TOMO_H : Sequence[str] = [
    Loc.tomo_sal_13.value, Loc.tomo_sal_12.value
]

MONKEYS_TOMO_I : Sequence[str] = [
    Loc.tomo_tomu.value, Loc.tomo_breadacus.value, Loc.tomo_ukkigoro.value, Loc.tomo_ukiji.value
]

MONKEYS_TOMO_J : Sequence[str] = [
    Loc.tomo_tomimon.value
]

MONKEYS_TOMO : Sequence[str] = [
    *MONKEYS_TOMO_A,*MONKEYS_TOMO_B, *MONKEYS_TOMO_C, *MONKEYS_TOMO_E, *MONKEYS_TOMO_E1, *MONKEYS_TOMO_E2,
    *MONKEYS_TOMO_F1, *MONKEYS_TOMO_F2, *MONKEYS_TOMO_G, *MONKEYS_TOMO_G1, *MONKEYS_TOMO_H, *MONKEYS_TOMO_J
]

# boss6
MONKEYS_BOSS6 : Sequence[str] = [
    Loc.boss_tomoki.value
]

# Space
MONKEYS_SPACE_A : Sequence[str] = [
    Loc.space_poko.value, Loc.space_gamuo.value, Loc.space_mukikko.value
]

MONKEYS_SPACE_B : Sequence[str] = [
    Loc.space_moto_ukki.value, Loc.space_jimi_jami.value, Loc.space_genbo.value, Loc.space_twin_mitty.value
]

MONKEYS_SPACE_D : Sequence[str] = [
    Loc.space_uttey.value, Loc.space_emma.value, Loc.space_dokicchi.value, Loc.space_kamicchi.value,
    Loc.space_ukki_monda.value, Loc.space_porokko.value, Loc.space_zonelin.value
]
MONKEYS_SPACE_E : Sequence[str] = [
    Loc.space_tamano.value, Loc.space_nelson.value, Loc.space_koloneh.value, Loc.space_miluchy.value,
    Loc.space_robert.value, Loc.space_fronson.value, Loc.space_demekin.value
]

MONKEYS_SPACE_F : Sequence[str] = [
    Loc.space_kikuyoshi.value, Loc.space_freet.value, Loc.space_chico.value
]

MONKEYS_SPACE_F1 : Sequence[str] = [
    Loc.space_gamurin.value
]

MONKEYS_SPACE_F2 : Sequence[str] = [
    Loc.space_pipo_mon.value, Loc.space_gam_gam.value, Loc.space_doronbo.value, Loc.space_benja.value
]
MONKEYS_SPACE_G : Sequence[str] = [
    Loc.space_macchan.value, Loc.space_rokkun.value
]

MONKEYS_SPACE_G2 : Sequence[str] = [
    Loc.space_ukki_love.value, Loc.space_momongo.value, Loc.space_moepi.value, Loc.space_pumon.value,
    Loc.space_makiban.value
]

MONKEYS_SPACE_H : Sequence[str] = [
    Loc.space_upis.value, Loc.space_mondatta.value, Loc.space_gicchom.value, Loc.space_barire.value
]

MONKEYS_SPACE_I : Sequence[str] = [
    Loc.space_sal_10.value, Loc.space_sal_11.value
]
MONKEYS_SPACE_K : Sequence[str] = [
    Loc.space_sal_3000.value
]

MONKEYS_SPACE : Sequence[str] = [
    *MONKEYS_SPACE_A, *MONKEYS_SPACE_B, *MONKEYS_SPACE_D, *MONKEYS_SPACE_E, *MONKEYS_SPACE_F, *MONKEYS_SPACE_F1,
    *MONKEYS_SPACE_F2, *MONKEYS_SPACE_G, *MONKEYS_SPACE_G2, *MONKEYS_SPACE_H, *MONKEYS_SPACE_I, *MONKEYS_SPACE_K
]

MONKEYS_SPECTER : Sequence[str] = [
    Loc.boss_specter.value
]

MONKEYS_SPECTER_FINALE : Sequence[str] = [
    Loc.boss_specter_final.value
]

MONKEYS_BOSSES : Sequence[str] = [
    *MONKEYS_BOSS1, *MONKEYS_BOSS2, *MONKEYS_BOSS3, *MONKEYS_BOSS4, *MONKEYS_BOSS5, *MONKEYS_BOSS6, *MONKEYS_SPECTER,
    *MONKEYS_SPECTER_FINALE
]

MONKEYS_MASTER : Sequence[str] = [
    *MONKEYS_ZERO, *MONKEYS_SEASIDE, *MONKEYS_WOODS, *MONKEYS_CASTLE, *MONKEYS_CISCOCITY, *MONKEYS_STUDIO,
    *MONKEYS_HALLOWEEN, *MONKEYS_WESTERN, *MONKEYS_ONSEN, *MONKEYS_SNOWFESTA, *MONKEYS_EDOTOWN, *MONKEYS_HEAVEN,
    *MONKEYS_TOYHOUSE, *MONKEYS_ICELAND, *MONKEYS_ARABIAN, *MONKEYS_ASIA, *MONKEYS_PLANE, *MONKEYS_HONG,
    *MONKEYS_BAY, *MONKEYS_TOMO, *MONKEYS_SPACE, *MONKEYS_BOSSES
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

    # Asia
    Stage.asia_a.value          : MONKEYS_ASIA_A,
    Stage.asia_a1.value         : MONKEYS_ASIA_A1,
    Stage.asia_a3.value         : MONKEYS_ASIA_A3,
    Stage.asia_a4.value         : MONKEYS_ASIA_A4,
    Stage.asia_b.value          : MONKEYS_ASIA_B,
    Stage.asia_b1.value         : MONKEYS_ASIA_B1,
    Stage.asia_b2.value         : MONKEYS_ASIA_B2,
    Stage.asia_d.value          : MONKEYS_ASIA_D,
    Stage.asia_d2.value         : MONKEYS_ASIA_D2,
    Stage.asia_e1.value         : MONKEYS_ASIA_E1,
    Stage.asia_e2.value         : MONKEYS_ASIA_E2,
    Stage.asia_f.value          : MONKEYS_ASIA_F,

    # Plane
    Stage.plane_a.value         : MONKEYS_PLANE_A,
    Stage.plane_a1.value        : MONKEYS_PLANE_A1,
    Stage.plane_b.value         : MONKEYS_PLANE_B,
    Stage.plane_b1.value        : MONKEYS_PLANE_B1,
    Stage.plane_c.value         : MONKEYS_PLANE_C,
    Stage.plane_c1.value        : MONKEYS_PLANE_C1,
    Stage.plane_d.value         : MONKEYS_PLANE_D,
    Stage.plane_e.value         : MONKEYS_PLANE_E,
    Stage.plane_f1.value        : MONKEYS_PLANE_F1,
    Stage.plane_g.value         : MONKEYS_PLANE_G,
    Stage.plane_h.value         : MONKEYS_PLANE_H,

    # Hong
    Stage.hong_a.value          : MONKEYS_HONG_A,
    Stage.hong_b.value          : MONKEYS_HONG_B,
    Stage.hong_b1.value         : MONKEYS_HONG_B1,
    Stage.hong_c.value          : MONKEYS_HONG_C,
    Stage.hong_c1.value         : MONKEYS_HONG_C1,
    Stage.hong_c2.value         : MONKEYS_HONG_C2,
    Stage.hong_d.value          : MONKEYS_HONG_D,
    Stage.hong_e.value          : MONKEYS_HONG_E,
    Stage.hong_e1.value         : MONKEYS_HONG_E1,
    Stage.hong_f.value          : MONKEYS_HONG_F,
    Stage.hong_g.value          : MONKEYS_HONG_G,
    Stage.hong_h.value          : MONKEYS_HONG_H,

    # boss5
    Stage.boss5.value           : MONKEYS_BOSS5,

    # bay
    Stage.bay_a.value           : MONKEYS_BAY_A,
    Stage.bay_a1.value          : MONKEYS_BAY_A1,
    Stage.bay_a5.value          : MONKEYS_BAY_A5,
    Stage.bay_b.value           : MONKEYS_BAY_B,
    Stage.bay_c.value           : MONKEYS_BAY_C,
    Stage.bay_d.value           : MONKEYS_BAY_D,
    Stage.bay_d1.value          : MONKEYS_BAY_D1,
    Stage.bay_e.value           : MONKEYS_BAY_E,
    Stage.bay_e1.value          : MONKEYS_BAY_E1,
    Stage.bay_e2.value          : MONKEYS_BAY_E2,
    Stage.bay_e3.value          : MONKEYS_BAY_E3,
    Stage.bay_f.value           : MONKEYS_BAY_F,

    # tomo
    Stage.tomo_a.value          : MONKEYS_TOMO_A,
    Stage.tomo_b.value          : MONKEYS_TOMO_B,
    Stage.tomo_c.value          : MONKEYS_TOMO_C,
    Stage.tomo_e.value          : MONKEYS_TOMO_E,
    Stage.tomo_e1.value         : MONKEYS_TOMO_E1,
    Stage.tomo_e2.value         : MONKEYS_TOMO_E2,
    Stage.tomo_f1.value         : MONKEYS_TOMO_F1,
    Stage.tomo_f2.value         : MONKEYS_TOMO_F2,
    Stage.tomo_g.value          : MONKEYS_TOMO_G,
    Stage.tomo_g1.value         : MONKEYS_TOMO_G1,
    Stage.tomo_h.value          : MONKEYS_TOMO_H,
    Stage.tomo_i.value          : MONKEYS_TOMO_I,
    Stage.tomo_j.value          : MONKEYS_TOMO_J,

    # boss6
    Stage.boss6.value           : MONKEYS_BOSS6,

    # Space
    Stage.space_a.value         : MONKEYS_SPACE_A,
    Stage.space_b.value         : MONKEYS_SPACE_B,
    Stage.space_d.value         : MONKEYS_SPACE_D,
    Stage.space_e.value         : MONKEYS_SPACE_E,
    Stage.space_f.value         : MONKEYS_SPACE_F,
    Stage.space_f1.value        : MONKEYS_SPACE_F1,
    Stage.space_f2.value        : MONKEYS_SPACE_F2,
    Stage.space_g.value         : MONKEYS_SPACE_G,
    Stage.space_g2.value        : MONKEYS_SPACE_G2,
    Stage.space_h.value         : MONKEYS_SPACE_H,
    Stage.space_i.value         : MONKEYS_SPACE_I,
    Stage.space_k.value         : MONKEYS_SPACE_K,

    # Specter
    Stage.specter1.value        : MONKEYS_SPECTER,
    Stage.specter2.value        : MONKEYS_SPECTER_FINALE
}

MONKEYS_DIRECTORY : dict[str, Sequence[str]] = {
    APHelper.zero.value                 : MONKEYS_ZERO,
    APHelper.seaside.value              : MONKEYS_SEASIDE,
    APHelper.woods.value                : MONKEYS_WOODS,
    APHelper.castle.value               : MONKEYS_CASTLE,
    APHelper.castle_2.value             : MONKEYS_CASTLE,
    APHelper.ciscocity.value            : MONKEYS_CISCOCITY,
    APHelper.studio.value               : MONKEYS_STUDIO,
    APHelper.studio_2.value             : MONKEYS_STUDIO,
    APHelper.halloween.value            : MONKEYS_HALLOWEEN,
    APHelper.halloween_2.value          : MONKEYS_HALLOWEEN,
    APHelper.western.value              : MONKEYS_WESTERN,
    APHelper.western_2.value            : MONKEYS_WESTERN,
    APHelper.onsen.value                : MONKEYS_ONSEN,
    APHelper.onsen_2.value              : MONKEYS_ONSEN,
    APHelper.snowfesta.value            : MONKEYS_SNOWFESTA,
    APHelper.snowfesta_2.value          : MONKEYS_SNOWFESTA,
    APHelper.edotown.value              : MONKEYS_EDOTOWN,
    APHelper.edotown_2.value            : MONKEYS_EDOTOWN,
    APHelper.heaven.value               : MONKEYS_HEAVEN,
    APHelper.heaven_2.value             : MONKEYS_HEAVEN,
    APHelper.toyhouse.value             : MONKEYS_TOYHOUSE,
    APHelper.toyhouse_2.value           : MONKEYS_TOYHOUSE,
    APHelper.iceland.value              : MONKEYS_ICELAND,
    APHelper.iceland_2.value            : MONKEYS_ICELAND,
    APHelper.arabian.value              : MONKEYS_ARABIAN,
    APHelper.asia.value                 : MONKEYS_ASIA,
    APHelper.asia_2.value               : MONKEYS_ASIA,
    APHelper.plane.value                : MONKEYS_PLANE,
    APHelper.hong.value                 : MONKEYS_HONG,
    APHelper.hong_2.value               : MONKEYS_HONG,
    APHelper.bay.value                  : MONKEYS_BAY,
    APHelper.tomo.value                 : MONKEYS_TOMO,
    APHelper.tomo_2.value               : MONKEYS_TOMO,
    APHelper.boss6.value                : MONKEYS_BOSS6,
    APHelper.space.value                : MONKEYS_SPACE,
    APHelper.space_2.value              : MONKEYS_SPACE,
    APHelper.specter1.value             : MONKEYS_BOSSES,
    APHelper.specter2.value             : MONKEYS_BOSSES,
}

### [< --- EVENT GROUPS --- >]
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

EVENTS_ASIA_A1 : Sequence[EventMeta] = [
    EventMeta(Game.trigger_asia_a1.value)
]

EVENTS_ASIA_A2 : Sequence[EventMeta] = [
    EventMeta(Game.trigger_asia_a2.value)
]

EVENTS_ASIA_B2 : Sequence[EventMeta] = [
    EventMeta(Game.shortcut_asia_b2b.value)
]

EVENTS_ASIA_E : Sequence[EventMeta] = [
    EventMeta(Game.trigger_asia_e.value)
]

EVENTS_BAY_A4 : Sequence[EventMeta] = [
    EventMeta(Game.trigger_bay_a4.value)
]

EVENTS_BAY_E1 : Sequence[EventMeta] = [
    EventMeta(Game.trigger_bay_e1.value, AccessRule.SLING)
]

EVENTS_SPACE_E : Sequence[EventMeta] = [
    EventMeta(Game.trigger_space_e.value)
]

EVENTS_SPACE_F2 : Sequence[EventMeta] = [
    EventMeta(Game.trigger_space_f2.value)
]

EVENTS_SPACE_G1 : Sequence[EventMeta] = [
    EventMeta(Game.trigger_space_g1.value)
]

EVENTS_SPACE_G2 : Sequence[EventMeta] = [
    EventMeta(Game.trigger_space_g2.value)
]

EVENTS_INDEX : dict[str, Sequence[EventMeta]] = {
    # Triggers
    Stage.iceland_e.value       : EVENTS_ICELAND_E,
    Stage.arabian_c.value       : EVENTS_ARABIAN_C,
    Stage.asia_a1.value         : EVENTS_ASIA_A1,
    Stage.asia_a2.value         : EVENTS_ASIA_A2,
    Stage.asia_e.value          : EVENTS_ASIA_E,
    Stage.bay_a4.value          : EVENTS_BAY_A4,
    Stage.bay_e1.value          : EVENTS_BAY_E1,
    Stage.space_e.value         : EVENTS_SPACE_E,
    Stage.space_f2.value        : EVENTS_SPACE_F2,
    Stage.space_g1.value        : EVENTS_SPACE_G1,
    Stage.space_g2.value        : EVENTS_SPACE_G2,

    # Shortcuts
    Stage.studio_a1.value       : EVENTS_STUDIO_A1,
    Stage.edotown_e.value       : EVENTS_EDOTOWN_E,
    Stage.asia_b2.value         : EVENTS_ASIA_B2
}

def generate_name_to_id() -> dict[str, int]:
    return { name : MonkeyLocation(name).loc_id for name in MONKEYS_MASTER }