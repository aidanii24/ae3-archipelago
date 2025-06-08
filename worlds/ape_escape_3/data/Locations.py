from typing import Sequence
from dataclasses import dataclass
from abc import ABC

from BaseClasses import Location, Region, ItemClassification

from .Strings import Loc, Stage, Events, Meta, APHelper
from .Addresses import NTSCU


### [< --- HELPERS --- >]
class AE3Location(Location):
    """
    Defines a Location in Ape Escape 3. This refers to points of interest for the randomizer, such as Monkeys,
    Cellphones, Cameras and Points of Interests in the Hub.

    Attributes:
        game : Name of the Game
    """

    game : str = Meta.game

@dataclass
class AE3LocationMeta(ABC):
    """Base Data Class for all Locations in Ape Escape 3."""

    name : str
    loc_id : int
    address : int

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

    def to_location(self, player : int, parent : Region) -> Location:
        return Location(player, self.name, self.loc_id, parent)

class CameraLocation(AE3LocationMeta):
    def __init__(self, name : str, offset : int = 0):
        self.name = name
        # Cameras will be id'd linearly, based on the starting id definied by Pipo Camera in addresses.py
        self.loc_id = NTSCU.Locations[Loc.pipo_camera.value] + offset
        self.address = self.loc_id

    def to_location(self, player : int, parent : Region) -> Location:
        return Location(player, self.name, self.loc_id, parent)

class CellphoneLocation(AE3LocationMeta):
    def __init__(self, text_id : str):
        self.name = Cellphone_Name_to_ID[text_id]
        # Locations can be assumed to always be in Addresses.Locations. NTSCU version will be used as basis for the ID.
        self.loc_id = NTSCU.Locations[text_id]
        self.address = self.loc_id

    def to_location(self, player : int, parent : Region) -> Location:
        return Location(player, self.name, self.loc_id, parent)

class EventMeta(AE3LocationMeta):
    """Base Class for all events."""
    def __init__(self, name : str):
        self.name = name
        self.loc_id = 0x0
        self.address = 0x0

    def to_event_location(self, player : int, parent : Region) -> Location:
        from .Items import AE3Item

        event : Location = Location(player, self.name, None, parent)
        item : AE3Item = AE3Item(self.name, ItemClassification.progression, None, player)

        event.place_locked_item(item)

        return event

### [< --- STAGE GROUPS --- >]

## Monkeys
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
MONKEYS_CASTLE_A1 : Sequence[str] = [
    Loc.castle_ukkido.value
]

MONKEYS_CASTLE_B : Sequence[str] = [
    Loc.castle_pipo_guard.value, Loc.castle_ukkinee.value
]

MONKEYS_CASTLE_B1 : Sequence[str] = [
    Loc.castle_monderella.value, Loc.castle_ukki_ichi.value
]

MONKEYS_CASTLE_C : Sequence[str] = [
    Loc.castle_saru_mon.value, Loc.castle_monga.value, Loc.castle_ukkiton.value, Loc.castle_king_leo.value
]

MONKEYS_CASTLE_D : Sequence[str] = [
    Loc.castle_ukkii.value
]

MONKEYS_CASTLE_D1 : Sequence[str] = [
    Loc.castle_saluto.value
]

MONKEYS_CASTLE_E : Sequence[str] = [
    Loc.castle_kings_double.value, Loc.castle_mattsun.value, Loc.castle_miya.value, Loc.castle_mon_san.value
]

MONKEYS_CASTLE_F : Sequence[str] = [
    Loc.castle_sal_1000.value
]

MONKEYS_CASTLE : Sequence[str] = [
    *MONKEYS_CASTLE_A1, *MONKEYS_CASTLE_B, *MONKEYS_CASTLE_B1, *MONKEYS_CASTLE_C, *MONKEYS_CASTLE_D,
    *MONKEYS_CASTLE_D1, *MONKEYS_CASTLE_E, *MONKEYS_CASTLE_F
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
    Loc.studio_bananamon.value
]

MONKEYS_STUDIO_D1 : Sequence[str] = [
    Loc.studio_mokinza.value
]

MONKEYS_STUDIO_E : Sequence[str] = [
    Loc.studio_ukki_lee_ukki.value, Loc.studio_ukkida_jiro.value, Loc.studio_sal_ukindo.value
]

MONKEYS_STUDIO_F1 : Sequence[str] = [
    Loc.studio_gimminey.value, Loc.studio_hant.value
]

MONKEYS_STUDIO_F : Sequence[str] = [
    Loc.studio_chippino.value
]

MONKEYS_STUDIO_G : Sequence[str] = [
    Loc.studio_ukki_paul.value, Loc.studio_sally_mon.value, Loc.studio_bonly.value, Loc.studio_monly.value
]

MONKEYS_STUDIO : Sequence[str] = [
    *MONKEYS_STUDIO_A, *MONKEYS_STUDIO_B, *MONKEYS_STUDIO_C, *MONKEYS_STUDIO_D, *MONKEYS_STUDIO_D1,
    *MONKEYS_STUDIO_E, *MONKEYS_STUDIO_F, *MONKEYS_STUDIO_F1, *MONKEYS_STUDIO_G,
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
    Loc.halloween_ukkisuke.value, Loc.halloween_chibi_sally.value
]

MONKEYS_HALLOWEEN_C2 : Sequence[str] = [
    Loc.halloween_ukkison.value
]

MONKEYS_HALLOWEEN_D : Sequence[str] = [
    Loc.halloween_saruhotep.value
]

MONKEYS_HALLOWEEN_D1 : Sequence[str] = [
    Loc.halloween_ukkito.value
]

MONKEYS_HALLOWEEN_D2 : Sequence[str] = [
    Loc.halloween_monzally.value, Loc.halloween_ukkiami.value
]

MONKEYS_HALLOWEEN_E : Sequence[str] = [
    Loc.halloween_monjan.value, Loc.halloween_nattchan.value, Loc.halloween_kabochin.value,
    Loc.halloween_ukki_mon.value
]

MONKEYS_HALLOWEEN_F : Sequence[str] = [
    Loc.halloween_mumpkin.value
]

MONKEYS_HALLOWEEN : Sequence[str] = [
    *MONKEYS_HALLOWEEN_A1, *MONKEYS_HALLOWEEN_A, *MONKEYS_HALLOWEEN_B, *MONKEYS_HALLOWEEN_C, *MONKEYS_HALLOWEEN_C2,
    *MONKEYS_HALLOWEEN_D, *MONKEYS_HALLOWEEN_D1, *MONKEYS_HALLOWEEN_D2, *MONKEYS_HALLOWEEN_E,  *MONKEYS_HALLOWEEN_F
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

MONKEYS_WESTERN_D2 : Sequence[str] = [
    Loc.western_shaluron.value,
]

MONKEYS_WESTERN_D3 : Sequence[str] = [
    Loc.western_jay_mohn.value, Loc.western_munkee_joe.value, Loc.western_saru_chison.value, Loc.western_jaja_jamo.value
]

MONKEYS_WESTERN_E : Sequence[str] = [
    Loc.western_chammy_mo.value, Loc.western_golozo.value
]

MONKEYS_WESTERN_E1 : Sequence[str] = [
    Loc.western_golon_moe.value,
]

MONKEYS_WESTERN_F : Sequence[str] = [
    Loc.western_ukkia_munbo.value, Loc.western_mon_johny.value
]

MONKEYS_WESTERN : Sequence[str] = [
    *MONKEYS_WESTERN_A, *MONKEYS_WESTERN_B, *MONKEYS_WESTERN_C, *MONKEYS_WESTERN_D2, *MONKEYS_WESTERN_D3,
    *MONKEYS_WESTERN_E, *MONKEYS_WESTERN_E1, *MONKEYS_WESTERN_F,
]

# Boss2
MONKEYS_BOSS2 : Sequence[str] = [
    Loc.boss_monkey_blue.value
]

# Onsen
MONKEYS_ONSEN_A : Sequence[str] = [
    Loc.onsen_chabimon.value, Loc.onsen_ukki_ichiro.value
]

MONKEYS_ONSEN_A1M : Sequence[str] = [
    Loc.onsen_kiichiro.value, Loc.onsen_saru_sam.value
]

MONKEYS_ONSEN_A2M : Sequence[str] = [
    Loc.onsen_michiyan.value, Loc.onsen_tome_san.value
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
    *MONKEYS_ONSEN_A, *MONKEYS_ONSEN_A1M, *MONKEYS_ONSEN_A2M, *MONKEYS_ONSEN_B, *MONKEYS_ONSEN_C, *MONKEYS_ONSEN_D,
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
    Loc.edotown_tomoku_chan.value,
]

MONKEYS_EDOTOWN_C1 : Sequence[str] = [
    Loc.edotown_kikimaru.value
]

MONKEYS_EDOTOWN_C2 : Sequence[str] = [
    Loc.edotown_uziko.value, Loc.edotown_gp.value
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
    *MONKEYS_EDOTOWN_A, *MONKEYS_EDOTOWN_B, *MONKEYS_EDOTOWN_C, *MONKEYS_EDOTOWN_C1, *MONKEYS_EDOTOWN_C2,
    *MONKEYS_EDOTOWN_D, *MONKEYS_EDOTOWN_E, *MONKEYS_EDOTOWN_F
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
    Loc.heaven_micchino.value
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
    Loc.toyhouse_bon_mota.value, Loc.toyhouse_bon_verna.value, Loc.toyhouse_bon_papa.value, Loc.toyhouse_bon_mama.value
]

MONKEYS_TOYHOUSE_B1 : Sequence[str] = [
    Loc.toyhouse_kalkin.value
]

MONKEYS_TOYHOUSE_C : Sequence[str] = [
    Loc.toyhouse_pakun.value, Loc.toyhouse_ukki_x.value, Loc.toyhouse_mon_gareji.value, Loc.toyhouse_shouji.value,
    Loc.toyhouse_woo_makka.value
]

MONKEYS_TOYHOUSE_D : Sequence[str] = [
    Loc.toyhouse_monto.value, Loc.toyhouse_mokitani.value, Loc.toyhouse_namigo.value, Loc.toyhouse_pipotron_red.value
]

MONKEYS_TOYHOUSE_E : Sequence[str] = [
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
    *MONKEYS_TOYHOUSE_A, *MONKEYS_TOYHOUSE_B, *MONKEYS_TOYHOUSE_B1, *MONKEYS_TOYHOUSE_C, *MONKEYS_TOYHOUSE_D,
    *MONKEYS_TOYHOUSE_E, *MONKEYS_TOYHOUSE_F, *MONKEYS_TOYHOUSE_G, *MONKEYS_TOYHOUSE_H,
]

# Iceland
MONKEYS_ICELAND_A : Sequence[str] = [
    Loc.iceland_bikupuri.value, Loc.iceland_ukkisu.value
]

MONKEYS_ICELAND_A1 : Sequence[str] = [
    Loc.iceland_ukki_ami.value,
]

MONKEYS_ICELAND_A2 : Sequence[str] = [
    Loc.iceland_balio.value
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
    *MONKEYS_ICELAND_A, *MONKEYS_ICELAND_A1, *MONKEYS_ICELAND_A2, *MONKEYS_ICELAND_B, *MONKEYS_ICELAND_C,
    *MONKEYS_ICELAND_D, *MONKEYS_ICELAND_E, *MONKEYS_ICELAND_F
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
    Loc.arabian_dancing_mia.value
]

MONKEYS_ARABIAN_F : Sequence[str] = [
    Loc.arabian_miccho.value, Loc.arabian_kisha.value, Loc.arabian_gimuccho.value, Loc.arabian_wojin.value
]

MONKEYS_ARABIAN_G : Sequence[str] = [
    Loc.arabian_princess_judy.value
]

MONKEYS_ARABIAN : Sequence[str] = [
    *MONKEYS_ARABIAN_A, *MONKEYS_ARABIAN_B, *MONKEYS_ARABIAN_C, *MONKEYS_ARABIAN_C1, *MONKEYS_ARABIAN_E,
    *MONKEYS_ARABIAN_F, *MONKEYS_ARABIAN_G
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

MONKEYS_ASIA_A4 : Sequence[str] = [
    Loc.asia_baku.value
]

MONKEYS_ASIA_A6 : Sequence[str] = [
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

MONKEYS_ASIA_E : Sequence[str] = [
    Loc.asia_molzone.value
]

MONKEYS_ASIA_E2 : Sequence[str] = [
    Loc.asia_chappio.value, Loc.asia_pomoah.value
]

MONKEYS_ASIA_F : Sequence[str] = [
    Loc.asia_gucchai.value, Loc.asia_makaccho.value, Loc.asia_gamaran.value, Loc.asia_larry.value
]

MONKEYS_ASIA : Sequence[str] = [
    *MONKEYS_ASIA_A, *MONKEYS_ASIA_A1, *MONKEYS_ASIA_A4, *MONKEYS_ASIA_A6, *MONKEYS_ASIA_B, *MONKEYS_ASIA_B1,
    *MONKEYS_ASIA_B2, *MONKEYS_ASIA_D, *MONKEYS_ASIA_D2, *MONKEYS_ASIA_E, *MONKEYS_ASIA_E2, *MONKEYS_ASIA_F
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
    Loc.plane_pont.value
]

MONKEYS_PLANE_B2 : Sequence[str] = [
    Loc.plane_gamish.value
]

MONKEYS_PLANE_C : Sequence[str] = [
    Loc.plane_takmon.value, Loc.plane_mukita.value
]

MONKEYS_PLANE_C1 : Sequence[str] = [
    Loc.plane_prince_bertus.value, Loc.plane_chai_bunny.value
]

MONKEYS_PLANE_D : Sequence[str] = [
    Loc.plane_tamrai.value, Loc.plane_pipotron_blue.value
]

MONKEYS_PLANE_D1 : Sequence[str] = [
    Loc.plane_kemunpa.value
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
    *MONKEYS_PLANE_A, *MONKEYS_PLANE_A1, *MONKEYS_PLANE_B, *MONKEYS_PLANE_B1, *MONKEYS_PLANE_B2, *MONKEYS_PLANE_C,
    *MONKEYS_PLANE_C1, *MONKEYS_PLANE_D, *MONKEYS_PLANE_D1, *MONKEYS_PLANE_E, *MONKEYS_PLANE_F1, *MONKEYS_PLANE_G,
    *MONKEYS_PLANE_H
]

# Hong
MONKEYS_HONG_A : Sequence[str] = [
    Loc.hong_nak_nayo.value,
]

MONKEYS_HONG_A1 : Sequence[str] = [
    Loc.hong_donto_koi.value, Loc.hong_po_kin_ki.value
]

MONKEYS_HONG_A2 : Sequence[str] = [
    Loc.hong_dally.value,
]

MONKEYS_HONG_B : Sequence[str] = [
    Loc.hong_shinchi.value, Loc.hong_doh_tsuitaro.value
]

MONKEYS_HONG_B1 : Sequence[str] = [
    Loc.hong_ukki_chan.value, Loc.hong_uki_uki.value, Loc.hong_muki_muki.value, Loc.hong_hi_uchi_ishi.value
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
    *MONKEYS_HONG_A, *MONKEYS_HONG_A1, *MONKEYS_HONG_A2, *MONKEYS_HONG_B, *MONKEYS_HONG_B1, *MONKEYS_HONG_C,
    *MONKEYS_HONG_C1, *MONKEYS_HONG_C2, *MONKEYS_HONG_D, *MONKEYS_HONG_E, *MONKEYS_HONG_E1, *MONKEYS_HONG_F,
    *MONKEYS_HONG_G, *MONKEYS_HONG_H
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

MONKEYS_BAY_A6 : Sequence[str] = [
    Loc.bay_mokito.value
]

MONKEYS_BAY_B : Sequence[str] = [
    Loc.bay_pipo_kate.value, Loc.bay_samtan.value, Loc.bay_pokkine.value, Loc.bay_daban.value
]

MONKEYS_BAY_C : Sequence[str] = [
    Loc.bay_keiichi.value, Loc.bay_mcbreezy.value,
]

MONKEYS_BAY_C1 : Sequence[str] = [
    Loc.bay_shiny_pete.value, Loc.bay_landon.value, Loc.bay_ronson.value, Loc.bay_gimo.value
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
    Loc.bay_gimi_gimi.value, Loc.bay_pokkini.value, Loc.bay_bokino.value, Loc.bay_jimo.value
]

MONKEYS_BAY_F : Sequence[str] = [
    Loc.bay_makidon.value, Loc.bay_dogy.value, Loc.bay_gibdon.value, Loc.bay_buligie.value
]

MONKEYS_BAY : Sequence[str] = [
    *MONKEYS_BAY_A, *MONKEYS_BAY_A1, *MONKEYS_BAY_A6, *MONKEYS_BAY_B, *MONKEYS_BAY_C, *MONKEYS_BAY_C1,
    *MONKEYS_BAY_D, *MONKEYS_BAY_D1, *MONKEYS_BAY_E, *MONKEYS_BAY_E1, *MONKEYS_BAY_E2, *MONKEYS_BAY_F,
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
    Loc.tomo_taimon.value
]

MONKEYS_TOMO_E1 : Sequence[str] = [
    Loc.tomo_goro_san.value
]

MONKEYS_TOMO_E2 : Sequence[str] = [
    Loc.tomo_reiji.value
]

MONKEYS_TOMO_E3 : Sequence[str] = [
    Loc.tomo_ponta.value, Loc.tomo_tomio.value, Loc.tomo_gario.value
]

MONKEYS_TOMO_F2 : Sequence[str] = [
    Loc.tomo_dj_pari.value
]

MONKEYS_TOMO_F : Sequence[str] = [
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
    *MONKEYS_TOMO_E3, *MONKEYS_TOMO_F, *MONKEYS_TOMO_F2, *MONKEYS_TOMO_G, *MONKEYS_TOMO_G1, *MONKEYS_TOMO_H,
    *MONKEYS_TOMO_I, *MONKEYS_TOMO_J
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

MONKEYS_SPACE_G1 : Sequence[str] = [
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
    *MONKEYS_SPACE_F2, *MONKEYS_SPACE_G, *MONKEYS_SPACE_G1, *MONKEYS_SPACE_H, *MONKEYS_SPACE_I, *MONKEYS_SPACE_K
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

MONKEYS_PASSWORDS : Sequence[str] = [
    Loc.woods_spork.value, Loc.castle_sal_1000.value, Loc.snowfesta_shimmy.value, Loc.snowfesta_pipotron_yellow.value,
    Loc.toyhouse_pipotron_red.value, Loc.plane_pipotron_blue.value, Loc.hong_dark_master.value,
    Loc.space_sal_3000.value
]

MONKEYS_BREAK_ROOMS : Sequence[str] = [
    *MONKEYS_SEASIDE_C, *MONKEYS_WOODS_D, *MONKEYS_CASTLE_E, *MONKEYS_CISCOCITY_E, *MONKEYS_STUDIO_G,
    *MONKEYS_HALLOWEEN_E, *MONKEYS_WESTERN_C, *MONKEYS_ONSEN_C, *MONKEYS_SNOWFESTA_G, *MONKEYS_EDOTOWN_F,
    *MONKEYS_HEAVEN_E, *MONKEYS_TOYHOUSE_H, *MONKEYS_ICELAND_F, *MONKEYS_ARABIAN_F, *MONKEYS_ASIA_F, *MONKEYS_PLANE_G,
    *MONKEYS_HONG_F, *MONKEYS_BAY_F, *MONKEYS_TOMO_I, *MONKEYS_SPACE_H
]

MONKEYS_MASTER : Sequence[str] = [
    *MONKEYS_ZERO, *MONKEYS_SEASIDE, *MONKEYS_WOODS, *MONKEYS_CASTLE, *MONKEYS_CISCOCITY, *MONKEYS_STUDIO,
    *MONKEYS_HALLOWEEN, *MONKEYS_WESTERN, *MONKEYS_ONSEN, *MONKEYS_SNOWFESTA, *MONKEYS_EDOTOWN, *MONKEYS_HEAVEN,
    *MONKEYS_TOYHOUSE, *MONKEYS_ICELAND, *MONKEYS_ARABIAN, *MONKEYS_ASIA, *MONKEYS_PLANE, *MONKEYS_HONG,
    *MONKEYS_BAY, *MONKEYS_TOMO, *MONKEYS_SPACE, *MONKEYS_BOSSES
]

MONKEYS_MASTER_ORDERED : Sequence[list] = [
    MONKEYS_SEASIDE, MONKEYS_WOODS, MONKEYS_CASTLE, [Loc.boss_monkey_white.value], MONKEYS_CISCOCITY, MONKEYS_STUDIO,
    MONKEYS_HALLOWEEN, MONKEYS_WESTERN, [Loc.boss_monkey_blue.value], MONKEYS_ONSEN, MONKEYS_SNOWFESTA,
    MONKEYS_EDOTOWN, [Loc.boss_monkey_yellow.value], MONKEYS_HEAVEN, MONKEYS_TOYHOUSE, MONKEYS_ICELAND,
    MONKEYS_ARABIAN, [Loc.boss_monkey_pink.value], MONKEYS_ASIA, MONKEYS_PLANE, MONKEYS_HONG,
    [Loc.boss_monkey_red.value], MONKEYS_BAY, MONKEYS_TOMO, [Loc.boss_tomoki.value], MONKEYS_SPACE,
    [Loc.boss_specter.value], [Loc.boss_specter_final.value]
]

MONKEYS_INDEX : dict[str, Sequence] = {
    # Zero
    Stage.zero.value                    : MONKEYS_ZERO,

    # Seaside
    Stage.region_seaside_a.value        : MONKEYS_SEASIDE_A,
    Stage.region_seaside_b.value        : MONKEYS_SEASIDE_B,
    Stage.region_seaside_c.value        : MONKEYS_SEASIDE_C,

    # Woods
    Stage.region_woods_a.value          : MONKEYS_WOODS_A,
    Stage.region_woods_b.value          : MONKEYS_WOODS_B,
    Stage.region_woods_c.value          : MONKEYS_WOODS_C,
    Stage.region_woods_d.value          : MONKEYS_WOODS_D,

    # Castle
    Stage.region_castle_a1.value        : MONKEYS_CASTLE_A1,
    Stage.region_castle_b.value         : MONKEYS_CASTLE_B,
    Stage.region_castle_b1.value        : MONKEYS_CASTLE_B1,
    Stage.region_castle_c.value         : MONKEYS_CASTLE_C,
    Stage.region_castle_d.value         : MONKEYS_CASTLE_D,
    Stage.region_castle_d1.value        : MONKEYS_CASTLE_D1,
    Stage.region_castle_e.value         : MONKEYS_CASTLE_E,
    Stage.region_castle_f.value         : MONKEYS_CASTLE_F,

    # Boss1
    Stage.region_boss1.value            : MONKEYS_BOSS1,

    # Ciscocity
    Stage.region_ciscocity_a.value      : MONKEYS_CISCOCITY_A,
    Stage.region_ciscocity_b.value      : MONKEYS_CISCOCITY_B,
    Stage.region_ciscocity_c.value      : MONKEYS_CISCOCITY_C,
    Stage.region_ciscocity_d.value      : MONKEYS_CISCOCITY_D,
    Stage.region_ciscocity_e.value      : MONKEYS_CISCOCITY_E,

    # Studio
    Stage.region_studio_a.value         : MONKEYS_STUDIO_A,
    Stage.region_studio_b.value         : MONKEYS_STUDIO_B,
    Stage.region_studio_c.value         : MONKEYS_STUDIO_C,
    Stage.region_studio_d.value         : MONKEYS_STUDIO_D,
    Stage.region_studio_d1.value        : MONKEYS_STUDIO_D1,
    Stage.region_studio_e.value         : MONKEYS_STUDIO_E,
    Stage.region_studio_f.value         : MONKEYS_STUDIO_F,
    Stage.region_studio_f1.value        : MONKEYS_STUDIO_F1,
    Stage.region_studio_g.value         : MONKEYS_STUDIO_G,

    # Halloween
    Stage.region_halloween_a1.value     : MONKEYS_HALLOWEEN_A1,
    Stage.region_halloween_a.value      : MONKEYS_HALLOWEEN_A,
    Stage.region_halloween_b.value      : MONKEYS_HALLOWEEN_B,
    Stage.region_halloween_c.value      : MONKEYS_HALLOWEEN_C,
    Stage.region_halloween_c2.value     : MONKEYS_HALLOWEEN_C2,
    Stage.region_halloween_d.value      : MONKEYS_HALLOWEEN_D,
    Stage.region_halloween_d1.value     : MONKEYS_HALLOWEEN_D1,
    Stage.region_halloween_d2.value     : MONKEYS_HALLOWEEN_D2,
    Stage.region_halloween_e.value      : MONKEYS_HALLOWEEN_E,
    Stage.region_halloween_f.value      : MONKEYS_HALLOWEEN_F,

    # Western
    Stage.region_western_a.value        : MONKEYS_WESTERN_A,
    Stage.region_western_b.value        : MONKEYS_WESTERN_B,
    Stage.region_western_c.value        : MONKEYS_WESTERN_C,
    Stage.region_western_d2.value       : MONKEYS_WESTERN_D2,
    Stage.region_western_d3.value       : MONKEYS_WESTERN_D3,
    Stage.region_western_e.value        : MONKEYS_WESTERN_E,
    Stage.region_western_e1.value       : MONKEYS_WESTERN_E1,
    Stage.region_western_f.value        : MONKEYS_WESTERN_F,

    # Boss2
    Stage.region_boss2.value            : MONKEYS_BOSS2,

    # Onsen
    Stage.region_onsen_a.value          : MONKEYS_ONSEN_A,
    Stage.region_onsen_a1m.value        : MONKEYS_ONSEN_A1M,
    Stage.region_onsen_a2m.value        : MONKEYS_ONSEN_A2M,
    Stage.region_onsen_b.value          : MONKEYS_ONSEN_B,
    Stage.region_onsen_c.value          : MONKEYS_ONSEN_C,
    Stage.region_onsen_d.value          : MONKEYS_ONSEN_D,
    Stage.region_onsen_d1.value         : MONKEYS_ONSEN_D1,
    Stage.region_onsen_e.value          : MONKEYS_ONSEN_E,

    # Snowfesta
    Stage.region_snowfesta_a.value      : MONKEYS_SNOWFESTA_A,
    Stage.region_snowfesta_b.value      : MONKEYS_SNOWFESTA_B,
    Stage.region_snowfesta_c.value      : MONKEYS_SNOWFESTA_C,
    Stage.region_snowfesta_d.value      : MONKEYS_SNOWFESTA_D,
    Stage.region_snowfesta_e.value      : MONKEYS_SNOWFESTA_E,
    Stage.region_snowfesta_f.value      : MONKEYS_SNOWFESTA_F,
    Stage.region_snowfesta_g.value      : MONKEYS_SNOWFESTA_G,

    # Edotown
    Stage.region_edotown_a.value        : MONKEYS_EDOTOWN_A,
    Stage.region_edotown_b.value        : MONKEYS_EDOTOWN_B,
    Stage.region_edotown_c.value        : MONKEYS_EDOTOWN_C,
    Stage.region_edotown_c1.value       : MONKEYS_EDOTOWN_C1,
    Stage.region_edotown_c2.value       : MONKEYS_EDOTOWN_C2,
    Stage.region_edotown_d.value        : MONKEYS_EDOTOWN_D,
    Stage.region_edotown_e.value        : MONKEYS_EDOTOWN_E,
    Stage.region_edotown_f.value        : MONKEYS_EDOTOWN_F,

    # Boss3
    Stage.region_boss3.value            : MONKEYS_BOSS3,

    # Heaven
    Stage.region_heaven_a.value         : MONKEYS_HEAVEN_A,
    Stage.region_heaven_b.value         : MONKEYS_HEAVEN_B,
    Stage.region_heaven_c.value         : MONKEYS_HEAVEN_C,
    Stage.region_heaven_d.value         : MONKEYS_HEAVEN_D,
    Stage.region_heaven_e.value         : MONKEYS_HEAVEN_E,

    # Toyhouse
    Stage.region_toyhouse_a.value       : MONKEYS_TOYHOUSE_A,
    Stage.region_toyhouse_b.value       : MONKEYS_TOYHOUSE_B,
    Stage.region_toyhouse_b1.value      : MONKEYS_TOYHOUSE_B1,
    Stage.region_toyhouse_c.value       : MONKEYS_TOYHOUSE_C,
    Stage.region_toyhouse_d.value       : MONKEYS_TOYHOUSE_D,
    Stage.region_toyhouse_e.value       : MONKEYS_TOYHOUSE_E,
    Stage.region_toyhouse_f.value       : MONKEYS_TOYHOUSE_F,
    Stage.region_toyhouse_g.value       : MONKEYS_TOYHOUSE_G,
    Stage.region_toyhouse_h.value       : MONKEYS_TOYHOUSE_H,

    # Iceland
    Stage.region_iceland_a.value        : MONKEYS_ICELAND_A,
    Stage.region_iceland_a1.value       : MONKEYS_ICELAND_A1,
    Stage.region_iceland_a2.value       : MONKEYS_ICELAND_A2,
    Stage.region_iceland_b.value        : MONKEYS_ICELAND_B,
    Stage.region_iceland_c.value        : MONKEYS_ICELAND_C,
    Stage.region_iceland_d.value        : MONKEYS_ICELAND_D,
    Stage.region_iceland_e.value        : MONKEYS_ICELAND_E,
    Stage.region_iceland_f.value        : MONKEYS_ICELAND_F,

    # Arabian
    Stage.region_arabian_a.value        : MONKEYS_ARABIAN_A,
    Stage.region_arabian_b.value        : MONKEYS_ARABIAN_B,
    Stage.region_arabian_c.value        : MONKEYS_ARABIAN_C,
    Stage.region_arabian_c1.value       : MONKEYS_ARABIAN_C1,
    Stage.region_arabian_e.value        : MONKEYS_ARABIAN_E,
    Stage.region_arabian_f.value        : MONKEYS_ARABIAN_F,
    Stage.region_arabian_g.value        : MONKEYS_ARABIAN_G,

    # Boss4
    Stage.region_boss4.value            : MONKEYS_BOSS4,

    # Asia
    Stage.region_asia_a.value           : MONKEYS_ASIA_A,
    Stage.region_asia_a1.value          : MONKEYS_ASIA_A1,
    Stage.region_asia_a4.value          : MONKEYS_ASIA_A4,
    Stage.region_asia_a6.value          : MONKEYS_ASIA_A6,
    Stage.region_asia_b.value           : MONKEYS_ASIA_B,
    Stage.region_asia_b1.value          : MONKEYS_ASIA_B1,
    Stage.region_asia_b2.value          : MONKEYS_ASIA_B2,
    Stage.region_asia_d.value           : MONKEYS_ASIA_D,
    Stage.region_asia_d2.value          : MONKEYS_ASIA_D2,
    Stage.region_asia_e.value           : MONKEYS_ASIA_E,
    Stage.region_asia_e2.value          : MONKEYS_ASIA_E2,
    Stage.region_asia_f.value           : MONKEYS_ASIA_F,

    # Plane
    Stage.region_plane_a.value          : MONKEYS_PLANE_A,
    Stage.region_plane_a1.value         : MONKEYS_PLANE_A1,
    Stage.region_plane_b.value          : MONKEYS_PLANE_B,
    Stage.region_plane_b1.value         : MONKEYS_PLANE_B1,
    Stage.region_plane_b2.value         : MONKEYS_PLANE_B2,
    Stage.region_plane_c.value          : MONKEYS_PLANE_C,
    Stage.region_plane_c1.value         : MONKEYS_PLANE_C1,
    Stage.region_plane_d.value          : MONKEYS_PLANE_D,
    Stage.region_plane_d1.value         : MONKEYS_PLANE_D1,
    Stage.region_plane_e.value          : MONKEYS_PLANE_E,
    Stage.region_plane_f1.value         : MONKEYS_PLANE_F1,
    Stage.region_plane_g.value          : MONKEYS_PLANE_G,
    Stage.region_plane_h.value          : MONKEYS_PLANE_H,

    # Hong
    Stage.region_hong_a.value           : MONKEYS_HONG_A,
    Stage.region_hong_a1.value          : MONKEYS_HONG_A1,
    Stage.region_hong_a2.value          : MONKEYS_HONG_A2,
    Stage.region_hong_b.value           : MONKEYS_HONG_B,
    Stage.region_hong_b1.value          : MONKEYS_HONG_B1,
    Stage.region_hong_c.value           : MONKEYS_HONG_C,
    Stage.region_hong_c1.value          : MONKEYS_HONG_C1,
    Stage.region_hong_c2.value          : MONKEYS_HONG_C2,
    Stage.region_hong_d.value           : MONKEYS_HONG_D,
    Stage.region_hong_e.value           : MONKEYS_HONG_E,
    Stage.region_hong_e1.value          : MONKEYS_HONG_E1,
    Stage.region_hong_f.value           : MONKEYS_HONG_F,
    Stage.region_hong_g.value           : MONKEYS_HONG_G,
    Stage.region_hong_h.value           : MONKEYS_HONG_H,

    # boss5
    Stage.region_boss5.value            : MONKEYS_BOSS5,

    # bay
    Stage.region_bay_a.value            : MONKEYS_BAY_A,
    Stage.region_bay_a1.value           : MONKEYS_BAY_A1,
    Stage.region_bay_a6.value           : MONKEYS_BAY_A6,
    Stage.region_bay_b.value            : MONKEYS_BAY_B,
    Stage.region_bay_c.value            : MONKEYS_BAY_C,
    Stage.region_bay_c1.value           : MONKEYS_BAY_C1,
    Stage.region_bay_d.value            : MONKEYS_BAY_D,
    Stage.region_bay_d1.value           : MONKEYS_BAY_D1,
    Stage.region_bay_e.value            : MONKEYS_BAY_E,
    Stage.region_bay_e1.value           : MONKEYS_BAY_E1,
    Stage.region_bay_e2.value           : MONKEYS_BAY_E2,
    Stage.region_bay_f.value            : MONKEYS_BAY_F,

    # tomo
    Stage.region_tomo_a.value           : MONKEYS_TOMO_A,
    Stage.region_tomo_b.value           : MONKEYS_TOMO_B,
    Stage.region_tomo_c.value           : MONKEYS_TOMO_C,
    Stage.region_tomo_e.value           : MONKEYS_TOMO_E,
    Stage.region_tomo_e1.value          : MONKEYS_TOMO_E1,
    Stage.region_tomo_e2.value          : MONKEYS_TOMO_E2,
    Stage.region_tomo_e3.value          : MONKEYS_TOMO_E3,
    Stage.region_tomo_f.value           : MONKEYS_TOMO_F,
    Stage.region_tomo_f2.value          : MONKEYS_TOMO_F2,
    Stage.region_tomo_g.value           : MONKEYS_TOMO_G,
    Stage.region_tomo_g1.value          : MONKEYS_TOMO_G1,
    Stage.region_tomo_h.value           : MONKEYS_TOMO_H,
    Stage.region_tomo_i.value           : MONKEYS_TOMO_I,
    Stage.region_tomo_j.value           : MONKEYS_TOMO_J,

    # boss6
    Stage.region_boss6.value            : MONKEYS_BOSS6,

    # Space
    Stage.region_space_a.value          : MONKEYS_SPACE_A,
    Stage.region_space_b.value          : MONKEYS_SPACE_B,
    Stage.region_space_d.value          : MONKEYS_SPACE_D,
    Stage.region_space_e.value          : MONKEYS_SPACE_E,
    Stage.region_space_f.value          : MONKEYS_SPACE_F,
    Stage.region_space_f1.value         : MONKEYS_SPACE_F1,
    Stage.region_space_f2.value         : MONKEYS_SPACE_F2,
    Stage.region_space_g.value          : MONKEYS_SPACE_G,
    Stage.region_space_g1.value         : MONKEYS_SPACE_G1,
    Stage.region_space_h.value          : MONKEYS_SPACE_H,
    Stage.region_space_i.value          : MONKEYS_SPACE_I,
    Stage.region_space_k.value          : MONKEYS_SPACE_K,

    # Specter
    Stage.region_specter1.value         : MONKEYS_SPECTER,
    Stage.region_specter2.value         : MONKEYS_SPECTER_FINALE
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

## Cameras
CAMERAS_MASTER : Sequence[str] = [
    Loc.seaside_cam.value, Loc.woods_cam.value, Loc.castle_cam.value, Loc.ciscocity_cam.value, Loc.studio_cam.value,
    Loc.halloween_cam.value, Loc.western_cam.value, Loc.onsen_cam.value, Loc.snowfesta_cam.value, Loc.edotown_cam.value,
    Loc.heaven_cam.value, Loc.toyhouse_cam.value, Loc.iceland_cam.value, Loc.arabian_cam.value,
    Loc.asia_cam.value, Loc.plane_cam.value, Loc.hong_cam.value, Loc.bay_cam.value, Loc.tomo_cam.value,
    Loc.space_cam.value
]

CAMERAS_MASTER_ORDERED : Sequence[str] = [
    Loc.seaside_cam.value, Loc.woods_cam.value, Loc.castle_cam.value, "", Loc.ciscocity_cam.value, Loc.studio_cam.value,
    Loc.halloween_cam.value, Loc.western_cam.value, "", Loc.onsen_cam.value, Loc.snowfesta_cam.value,
    Loc.edotown_cam.value, "", Loc.heaven_cam.value, Loc.toyhouse_cam.value, Loc.iceland_cam.value,
    Loc.arabian_cam.value, "", Loc.asia_cam.value, Loc.plane_cam.value, Loc.hong_cam.value, "",
    Loc.bay_cam.value, Loc.tomo_cam.value, "", Loc.space_cam.value, "", ""
]

CAMERAS_INDEX : dict[str, str] = {
    Stage.region_seaside_b.value               : Loc.seaside_cam.value,
    Stage.region_woods_a.value                 : Loc.woods_cam.value,
    Stage.region_castle_c.value                : Loc.castle_cam.value,
    Stage.region_ciscocity_b.value             : Loc.ciscocity_cam.value,
    Stage.region_studio_e.value                : Loc.studio_cam.value,
    Stage.region_halloween_c.value             : Loc.halloween_cam.value,
    Stage.region_western_d2.value              : Loc.western_cam.value,
    Stage.region_onsen_a.value                 : Loc.onsen_cam.value,
    Stage.region_snowfesta_a.value             : Loc.snowfesta_cam.value,
    Stage.region_edotown_c.value               : Loc.edotown_cam.value,
    Stage.region_heaven_a.value                : Loc.heaven_cam.value,
    Stage.region_toyhouse_b.value              : Loc.toyhouse_cam.value,
    Stage.region_iceland_e.value               : Loc.iceland_cam.value,
    Stage.region_arabian_g.value               : Loc.arabian_cam.value,
    Stage.region_asia_a2.value                 : Loc.asia_cam.value,
    Stage.region_plane_c1.value                : Loc.plane_cam.value,
    Stage.region_hong_c.value                  : Loc.hong_cam.value,
    Stage.region_bay_c1.value                  : Loc.bay_cam.value,
    Stage.region_tomo_b.value                  : Loc.tomo_cam.value,
    Stage.region_space_e.value                : Loc.space_cam.value
}

CAMERAS_STAGE_INDEX : dict[str, str] = {
    Stage.seaside_b.value               : Loc.seaside_cam.value,
    Stage.woods_a.value                 : Loc.woods_cam.value,
    Stage.castle_c.value                : Loc.castle_cam.value,
    Stage.ciscocity_b.value             : Loc.ciscocity_cam.value,
    Stage.studio_e.value                : Loc.studio_cam.value,
    Stage.halloween_c.value             : Loc.halloween_cam.value,
    Stage.western_d.value               : Loc.western_cam.value,
    Stage.onsen_a.value                 : Loc.onsen_cam.value,
    Stage.snowfesta_a.value             : Loc.snowfesta_cam.value,
    Stage.edotown_c.value               : Loc.edotown_cam.value,
    Stage.heaven_a.value                : Loc.heaven_cam.value,
    Stage.toyhouse_b.value              : Loc.toyhouse_cam.value,
    Stage.iceland_e.value               : Loc.iceland_cam.value,
    Stage.arabian_g.value               : Loc.arabian_cam.value,
    Stage.asia_a.value                  : Loc.asia_cam.value,
    Stage.plane_c.value                 : Loc.plane_cam.value,
    Stage.hong_c.value                  : Loc.hong_cam.value,
    Stage.bay_c.value                   : Loc.bay_cam.value,
    Stage.tomo_b.value                  : Loc.tomo_cam.value,
    Stage.space_e.value                 : Loc.space_cam.value,
}

ACTORS_INDEX : dict[str, list[str]] = {
    Loc.seaside_cam.value               : [Loc.seaside_ukki_ben.value],
    Loc.woods_cam.value                 : [Loc.woods_ukki_red.value],
    Loc.castle_cam.value                : [Loc.castle_saru_mon.value],
    Loc.ciscocity_cam.value             : [Loc.ciscocity_ginjiro.value, Loc.ciscocity_kichiemon.value],
    Loc.studio_cam.value                : [Loc.studio_ukki_lee_ukki.value, Loc.studio_ukkida_jiro.value],
    Loc.halloween_cam.value             : [Loc.halloween_ukkison.value],
    Loc.western_cam.value               : [Loc.western_shaluron.value],
    Loc.onsen_cam.value                 : [Loc.onsen_ukki_ichiro.value],
    Loc.snowfesta_cam.value             : [Loc.snowfesta_konzo.value, Loc.snowfesta_takuo.value],
    Loc.edotown_cam.value               : [Loc.edotown_tomoku_chan.value],
    Loc.heaven_cam.value                : [Loc.heaven_ukkido.value],
    Loc.toyhouse_cam.value              : [Loc.toyhouse_bon_mota.value, Loc.toyhouse_bon_verna.value,
                                           Loc.toyhouse_bon_papa.value, Loc.toyhouse_bon_mama.value],
    Loc.iceland_cam.value               : [Loc.iceland_jolly_mon.value],
    Loc.arabian_cam.value               : [Loc.arabian_princess_judy.value],
    Loc.asia_cam.value                  : [Loc.asia_ukki_mat.value],
    Loc.plane_cam.value                 : [Loc.plane_prince_bertus.value, Loc.plane_chai_bunny.value],
    Loc.hong_cam.value                  : [Loc.hong_bassili_ukki.value],
    Loc.bay_cam.value                   : [Loc.bay_shiny_pete.value, Loc.bay_gimo.value],
    Loc.tomo_cam.value                  : [Loc.tomo_ukkinaka.value, Loc.tomo_ukkine.value],
    Loc.space_cam.value                 : [Loc.space_robert.value],
}

## Cellphones
# Seaside
CELLPHONES_SEASIDE_A : Sequence[str] = [
    Loc.tele_000.value, Loc.tele_002.value, Loc.tele_003.value
]

CELLPHONES_SEASIDE_B : Sequence[str] = [
    Loc.tele_004ss.value
]

CELLPHONES_SEASIDE : Sequence[str] = [
    *CELLPHONES_SEASIDE_A, *CELLPHONES_SEASIDE_B
]

# Woods
CELLPHONES_WOODS_A : Sequence[str] = [
    Loc.tele_001.value, Loc.tele_006.value, Loc.tele_007.value, Loc.tele_004wo.value
]

CELLPHONES_WOODS_B : Sequence[str] = [
    Loc.tele_008.value
]

CELLPHONES_WOODS : Sequence[str] = [
    *CELLPHONES_WOODS_A, *CELLPHONES_WOODS_B
]

# Castle
CELLPHONES_CASTLE_A : Sequence[str] = [
    Loc.tele_029.value
]

CELLPHONES_CASTLE_A1 : Sequence[str] = [
    Loc.tele_010.value, Loc.tele_009.value
]

CELLPHONES_CASTLE_A_ALL : Sequence[str] = [
    *CELLPHONES_CASTLE_A, *CELLPHONES_CASTLE_A1
]

CELLPHONES_CASTLE_D : Sequence[str] = [
    Loc.tele_011.value
]

CELLPHONES_CASTLE : Sequence[str] = [
    *CELLPHONES_CASTLE_A, *CELLPHONES_CASTLE_A1, *CELLPHONES_CASTLE_D
]

CELLPHONES_CISCOCITY_A : Sequence[str] = [
    Loc.tele_013.value, Loc.tele_012cc.value
]

CELLPHONES_CISCOCITY : Sequence[str] = [
    *CELLPHONES_CISCOCITY_A
]

CELLPHONES_STUDIO_A : Sequence[str] = [
    Loc.tele_062.value
]

CELLPHONES_STUDIO_B1 : Sequence[str] = [
    Loc.tele_014.value
]

CELLPHONES_STUDIO_F : Sequence[str] = [
    Loc.tele_030tv.value
]

CELLPHONES_STUDIO : Sequence[str] = [
    *CELLPHONES_STUDIO_A, *CELLPHONES_STUDIO_B1, *CELLPHONES_STUDIO_F
]

CELLPHONES_HALLOWEEN_A : Sequence[str] = [
    Loc.tele_052.value
]

CELLPHONES_HALLOWEEN_A1 : Sequence[str] = [
    Loc.tele_035.value
]

CELLPHONES_HALLOWEEN_C1 : Sequence[str] = [
    Loc.tele_016.value
]

CELLPHONES_HALLOWEEN_D : Sequence[str] = [
    Loc.tele_017.value
]

CELLPHONES_HALLOWEEN_A_ALL : Sequence[str] = [
    *CELLPHONES_HALLOWEEN_A, *CELLPHONES_HALLOWEEN_A1,
]

CELLPHONES_HALLOWEEN : Sequence[str] = [
    *CELLPHONES_HALLOWEEN_A, *CELLPHONES_HALLOWEEN_A1, *CELLPHONES_HALLOWEEN_C1, *CELLPHONES_HALLOWEEN_D
]

CELLPHONES_WESTERN_A : Sequence[str] = [
    Loc.tele_018.value
]

CELLPHONES_WESTERN_F : Sequence[str] = [
    Loc.tele_051.value
]

CELLPHONES_WESTERN_E : Sequence[str] = [
    Loc.tele_019.value
]

CELLPHONES_WESTERN : Sequence[str] = [
    *CELLPHONES_WESTERN_A, *CELLPHONES_WESTERN_F, *CELLPHONES_WESTERN_E
]

CELLPHONES_ONSEN_A : Sequence[str] = [
    Loc.tele_020.value, Loc.tele_063.value
]

CELLPHONES_ONSEN_D1 : Sequence[str] = [
    Loc.tele_021on.value
]

CELLPHONES_ONSEN : Sequence[str] = [
    *CELLPHONES_ONSEN_A, *CELLPHONES_ONSEN_D1
]

CELLPHONES_SNOWFESTA_F : Sequence[str] = [
    Loc.tele_022sf.value
]

CELLPHONES_SNOWFESTA : Sequence[str] = [
    *CELLPHONES_SNOWFESTA_F
]

CELLPHONES_EDOTOWN_A1 : Sequence[str] = [
    Loc.tele_023.value
]

CELLPHONES_EDOTOWN_B1 : Sequence[str] = [
    Loc.tele_025.value
]

CELLPHONES_EDOTOWN_C1 : Sequence[str] = [
    Loc.tele_024.value
]

CELLPHONES_EDOTOWN_C2 : Sequence[str] = [
    Loc.tele_026.value
]

CELLPHONES_EDOTOWN_C_ALL : Sequence[str] = [
    *CELLPHONES_EDOTOWN_C1, *CELLPHONES_EDOTOWN_C2
]

CELLPHONES_EDOTOWN : Sequence[str] = [
    *CELLPHONES_EDOTOWN_A1, *CELLPHONES_EDOTOWN_B1, *CELLPHONES_EDOTOWN_C1, *CELLPHONES_EDOTOWN_C2
]

CELLPHONES_HEAVEN_A1 : Sequence[str] = [
    Loc.tele_028.value
]

CELLPHONES_HEAVEN : Sequence[str] = [
    *CELLPHONES_HEAVEN_A1
]

CELLPHONES_TOYHOUSE_C : Sequence[str] = [
    Loc.tele_012tv.value
]

CELLPHONES_TOYHOUSE_G : Sequence[str] = [
    Loc.tele_030ty.value
]

CELLPHONES_TOYHOUSE : Sequence[str] = [
    *CELLPHONES_TOYHOUSE_C, *CELLPHONES_TOYHOUSE_G
]

CELLPHONES_ICELAND_A1 : Sequence[str] = [
    Loc.tele_031.value
]

CELLPHONES_ICELAND_D : Sequence[str] = [
    Loc.tele_021ic.value
]

CELLPHONES_ICELAND : Sequence[str] = [
    *CELLPHONES_ICELAND_A1, *CELLPHONES_ICELAND_D
]

CELLPHONES_ARABIAN_A : Sequence[str] = [
    Loc.tele_032.value, Loc.tele_033.value
]

CELLPHONES_ARABIAN_B : Sequence[str] = [
    Loc.tele_042ar.value
]

CELLPHONES_ARABIAN_E1 : Sequence[str] = [
    Loc.tele_034.value
]

CELLPHONES_ARABIAN : Sequence[str] = [
    *CELLPHONES_ARABIAN_A, *CELLPHONES_ARABIAN_B, *CELLPHONES_ARABIAN_E1
]

CELLPHONES_ASIA_B : Sequence[str] = [
    Loc.tele_037.value
]

CELLPHONES_ASIA_D1 : Sequence[str] = [
    Loc.tele_015.value
]

CELLPHONES_ASIA : Sequence[str] = [
    *CELLPHONES_ASIA_B, *CELLPHONES_ASIA_D1
]

CELLPHONES_PLANE_E : Sequence[str] = [
    Loc.tele_022pl.value
]

CELLPHONES_PLANE : Sequence[str] = [
    *CELLPHONES_PLANE_E
]

CELLPHONES_HONG_A : Sequence[str] = [
    Loc.tele_039.value, Loc.tele_040h_a.value
]

CELLPHONES_HONG_B1 : Sequence[str] = [
    Loc.tele_040h_b.value
]

CELLPHONES_HONG_D : Sequence[str] = [
    Loc.tele_042ho.value
]

CELLPHONES_HONG : Sequence[str] = [
    *CELLPHONES_HONG_A, *CELLPHONES_HONG_B1, *CELLPHONES_HONG_D
]

CELLPHONES_BAY_C : Sequence[str] = [
    Loc.tele_044.value
]

CELLPHONES_BAY : Sequence[str] = [
    *CELLPHONES_BAY_C
]

CELLPHONES_TOMO_A1 : Sequence[str] = [
    Loc.tele_045.value
]

CELLPHONES_TOMO : Sequence[str] = [
    *CELLPHONES_TOMO_A1
]

CELLPHONES_SPACE_A : Sequence[str] = [
    Loc.tele_047.value
]

CELLPHONES_SPACE_B : Sequence[str] = [
    Loc.tele_048.value
]

CELLPHONES_SPACE : Sequence[str] = [
    *CELLPHONES_SPACE_A, *CELLPHONES_SPACE_B
]

# Lists all first known instances of a duplicate phone call in vanilla progression
CELLPHONES_ID_DUPLICATES : Sequence[str] = [
    Loc.tele_004ss.value, Loc.tele_012cc.value, Loc.tele_021on.value, Loc.tele_022sf.value, Loc.tele_030tv.value,
    Loc.tele_040h_a.value, Loc.tele_042ar.value
]

CELLPHONES_STAGE_DUPLICATES : Sequence[str] = [
    Stage.woods_a.value, Stage.toyhouse_c.value, Stage.iceland_d.value, Stage.plane_e.value, Stage.toyhouse_g.value,
    Stage.hong_b.value, Stage.hong_d.value
]

CELLPHONES_MASTER : Sequence[str] = [
    *CELLPHONES_SEASIDE, *CELLPHONES_WOODS, *CELLPHONES_CASTLE, *CELLPHONES_CISCOCITY, *CELLPHONES_STUDIO,
    *CELLPHONES_HALLOWEEN, *CELLPHONES_WESTERN, *CELLPHONES_ONSEN, *CELLPHONES_SNOWFESTA, *CELLPHONES_EDOTOWN,
    *CELLPHONES_HEAVEN, *CELLPHONES_TOYHOUSE, *CELLPHONES_ICELAND, *CELLPHONES_ARABIAN, *CELLPHONES_ASIA,
    *CELLPHONES_PLANE, *CELLPHONES_HONG, *CELLPHONES_BAY, *CELLPHONES_TOMO, *CELLPHONES_SPACE
]

CELLPHONES_MASTER_ORDERED : Sequence[list] = [
    CELLPHONES_SEASIDE, CELLPHONES_WOODS, CELLPHONES_CASTLE, [], CELLPHONES_CISCOCITY, CELLPHONES_STUDIO,
    CELLPHONES_HALLOWEEN, CELLPHONES_WESTERN, [], CELLPHONES_ONSEN, CELLPHONES_SNOWFESTA, CELLPHONES_EDOTOWN, [],
    CELLPHONES_HEAVEN, CELLPHONES_TOYHOUSE, CELLPHONES_ICELAND, CELLPHONES_ARABIAN, [], CELLPHONES_ASIA,
    CELLPHONES_PLANE, CELLPHONES_HONG, [], CELLPHONES_BAY, CELLPHONES_TOMO, [], CELLPHONES_SPACE, [], []
]

CELLPHONES_INDEX : dict[str, Sequence[str]] = {
    Stage.region_seaside_a.value                : CELLPHONES_SEASIDE_A,
    Stage.region_seaside_b.value                : CELLPHONES_SEASIDE_B,

    Stage.region_woods_a.value                  : CELLPHONES_WOODS_A,
    Stage.region_woods_b.value                  : CELLPHONES_WOODS_B,

    Stage.region_castle_a.value                 : CELLPHONES_CASTLE_A,
    Stage.region_castle_a1.value                : CELLPHONES_CASTLE_A1,
    Stage.region_castle_d.value                 : CELLPHONES_CASTLE_D,

    Stage.region_ciscocity_a.value              : CELLPHONES_CISCOCITY_A,

    Stage.region_studio_a.value                 : CELLPHONES_STUDIO_A,
    Stage.region_studio_b1.value                : CELLPHONES_STUDIO_B1,
    Stage.region_studio_f.value                 : CELLPHONES_STUDIO_F,

    Stage.region_halloween_a.value              : CELLPHONES_HALLOWEEN_A,
    Stage.region_halloween_a1.value             : CELLPHONES_HALLOWEEN_A1,
    Stage.region_halloween_c1.value             : CELLPHONES_HALLOWEEN_C1,
    Stage.region_halloween_d.value              : CELLPHONES_HALLOWEEN_D,

    Stage.region_western_a.value                : CELLPHONES_WESTERN_A,
    Stage.region_western_f.value                : CELLPHONES_WESTERN_F,
    Stage.region_western_e.value                : CELLPHONES_WESTERN_E,

    Stage.region_onsen_a.value                  : CELLPHONES_ONSEN_A,
    Stage.region_onsen_d1.value                 : CELLPHONES_ONSEN_D1,

    Stage.region_snowfesta_f.value              : CELLPHONES_SNOWFESTA_F,

    Stage.region_edotown_a1.value               : CELLPHONES_EDOTOWN_A1,
    Stage.region_edotown_b1.value               : CELLPHONES_EDOTOWN_B1,
    Stage.region_edotown_c1.value               : CELLPHONES_EDOTOWN_C1,
    Stage.region_edotown_c2.value               : CELLPHONES_EDOTOWN_C2,

    Stage.region_heaven_a1.value                : CELLPHONES_HEAVEN_A1,

    Stage.region_toyhouse_c.value               : CELLPHONES_TOYHOUSE_C,
    Stage.region_toyhouse_g.value               : CELLPHONES_TOYHOUSE_G,

    Stage.region_iceland_a1.value               : CELLPHONES_ICELAND_A1,
    Stage.region_iceland_d.value                : CELLPHONES_ICELAND_D,

    Stage.region_arabian_a.value                : CELLPHONES_ARABIAN_A,
    Stage.region_arabian_b.value                : CELLPHONES_ARABIAN_B,
    Stage.region_arabian_e1.value               : CELLPHONES_ARABIAN_E1,

    Stage.region_asia_b.value                   : CELLPHONES_ASIA_B,
    Stage.region_asia_d1.value                  : CELLPHONES_ASIA_D1,

    Stage.region_plane_e.value                  : CELLPHONES_PLANE_E,

    Stage.region_hong_a.value                   : CELLPHONES_HONG_A,
    Stage.region_hong_b1.value                  : CELLPHONES_HONG_B1,
    Stage.region_hong_d.value                   : CELLPHONES_HONG_D,

    Stage.region_bay_c.value                    : CELLPHONES_BAY_C,

    Stage.region_tomo_a1.value                  : CELLPHONES_TOMO_A1,

    Stage.region_space_a.value                  : CELLPHONES_SPACE_A,
    Stage.region_space_b.value                  : CELLPHONES_SPACE_B,
}

CELLPHONES_STAGE_INDEX : dict[str, Sequence[str]] = {
    Stage.seaside_a.value               : CELLPHONES_SEASIDE_A,
    Stage.seaside_b.value               : CELLPHONES_SEASIDE_B,

    Stage.woods_a.value                 : CELLPHONES_WOODS_A,
    Stage.woods_b.value                 : CELLPHONES_WOODS_B,

    Stage.castle_a.value                : CELLPHONES_CASTLE_A_ALL,
    Stage.castle_d.value                : CELLPHONES_CASTLE_D,

    Stage.ciscocity_a.value             : CELLPHONES_CISCOCITY_A,

    Stage.studio_a.value                : CELLPHONES_STUDIO_A,
    Stage.studio_b.value                : CELLPHONES_STUDIO_B1,
    Stage.studio_f.value                : CELLPHONES_STUDIO_F,

    Stage.halloween_a.value             : CELLPHONES_HALLOWEEN_A_ALL,
    Stage.halloween_c.value             : CELLPHONES_HALLOWEEN_C1,
    Stage.halloween_d.value             : CELLPHONES_HALLOWEEN_D,

    Stage.western_a.value               : CELLPHONES_WESTERN_A,
    Stage.western_f.value               : CELLPHONES_WESTERN_F,
    Stage.western_e.value               : CELLPHONES_WESTERN_E,

    Stage.onsen_a.value                 : CELLPHONES_ONSEN_A,
    Stage.onsen_d.value                 : CELLPHONES_ONSEN_D1,

    Stage.snowfesta_f.value             : CELLPHONES_SNOWFESTA_F,

    Stage.edotown_a.value               : CELLPHONES_EDOTOWN_A1,
    Stage.edotown_b.value               : CELLPHONES_EDOTOWN_B1,
    Stage.edotown_c.value               : CELLPHONES_EDOTOWN_C_ALL,

    Stage.heaven_a.value                : CELLPHONES_HEAVEN_A1,

    Stage.toyhouse_c.value              : CELLPHONES_TOYHOUSE_C,
    Stage.toyhouse_g.value              : CELLPHONES_TOYHOUSE_G,

    Stage.iceland_a.value               : CELLPHONES_ICELAND_A1,
    Stage.iceland_d.value               : CELLPHONES_ICELAND_D,

    Stage.arabian_a.value               : CELLPHONES_ARABIAN_A,
    Stage.arabian_b.value               : CELLPHONES_ARABIAN_B,
    Stage.arabian_e.value               : CELLPHONES_ARABIAN_E1,

    Stage.asia_b.value                  : CELLPHONES_ASIA_B,
    Stage.asia_d.value                  : CELLPHONES_ASIA_D1,

    Stage.plane_e.value                 : CELLPHONES_PLANE_E,

    Stage.hong_a.value                  : CELLPHONES_HONG_A,
    Stage.hong_b.value                  : CELLPHONES_HONG_B1,
    Stage.hong_d.value                  : CELLPHONES_HONG_D,

    Stage.bay_c.value                   : CELLPHONES_BAY_C,

    Stage.tomo_a.value                  : CELLPHONES_TOMO_A1,

    Stage.space_a.value                 : CELLPHONES_SPACE_A,
    Stage.space_b.value                 : CELLPHONES_SPACE_B,
}

Cellphone_Name_to_ID : dict[str, str] = {
    Loc.tele_000.value              : Loc.cell_000.value,
    Loc.tele_001.value              : Loc.cell_001.value,
    Loc.tele_002.value              : Loc.cell_002.value,
    Loc.tele_003.value              : Loc.cell_003.value,
    Loc.tele_004ss.value            : Loc.cell_004ss.value,
    Loc.tele_004wo.value            : Loc.cell_004wo.value,
    Loc.tele_006.value              : Loc.cell_006.value,
    Loc.tele_007.value              : Loc.cell_007.value,
    Loc.tele_008.value              : Loc.cell_008.value,
    Loc.tele_009.value              : Loc.cell_009.value,
    Loc.tele_010.value              : Loc.cell_010.value,
    Loc.tele_011.value              : Loc.cell_011.value,
    Loc.tele_012cc.value            : Loc.cell_012cc.value,
    Loc.tele_012tv.value            : Loc.cell_012tv.value,
    Loc.tele_013.value              : Loc.cell_013.value,
    Loc.tele_014.value              : Loc.cell_014.value,
    Loc.tele_015.value              : Loc.cell_015.value,
    Loc.tele_016.value              : Loc.cell_016.value,
    Loc.tele_017.value              : Loc.cell_017.value,
    Loc.tele_018.value              : Loc.cell_018.value,
    Loc.tele_019.value              : Loc.cell_019.value,
    Loc.tele_020.value              : Loc.cell_020.value,
    Loc.tele_021on.value            : Loc.cell_021on.value,
    Loc.tele_021ic.value            : Loc.cell_021ic.value,
    Loc.tele_022sf.value            : Loc.cell_022sf.value,
    Loc.tele_022pl.value            : Loc.cell_022pl.value,
    Loc.tele_023.value              : Loc.cell_023.value,
    Loc.tele_024.value              : Loc.cell_024.value,
    Loc.tele_025.value              : Loc.cell_025.value,
    Loc.tele_026.value              : Loc.cell_026.value,
    Loc.tele_028.value              : Loc.cell_028.value,
    Loc.tele_029.value              : Loc.cell_029.value,
    Loc.tele_030tv.value            : Loc.cell_030tv.value,
    Loc.tele_030ty.value            : Loc.cell_030ty.value,
    Loc.tele_031.value              : Loc.cell_031.value,
    Loc.tele_032.value              : Loc.cell_032.value,
    Loc.tele_033.value              : Loc.cell_033.value,
    Loc.tele_034.value              : Loc.cell_034.value,
    Loc.tele_035.value              : Loc.cell_035.value,
    Loc.tele_037.value              : Loc.cell_037.value,
    Loc.tele_039.value              : Loc.cell_039.value,
    Loc.tele_040h_a.value           : Loc.cell_040h_a.value,
    Loc.tele_040h_b.value           : Loc.cell_040h_b.value,
    Loc.tele_042ar.value            : Loc.cell_042ar.value,
    Loc.tele_042ho.value            : Loc.cell_042ho.value,
    Loc.tele_044.value              : Loc.cell_044.value,
    Loc.tele_045.value              : Loc.cell_045.value,
    Loc.tele_047.value              : Loc.cell_047.value,
    Loc.tele_048.value              : Loc.cell_048.value,
    Loc.tele_051.value              : Loc.cell_051.value,
    Loc.tele_052.value              : Loc.cell_052.value,
    Loc.tele_062.value              : Loc.cell_062.value,
    Loc.tele_063.value              : Loc.cell_063.value,
}

### [< --- EVENT GROUPS --- >]
EVENTS_CASTLE_B : Sequence[str] = [
    Events.castle_b_clapper.value
]

EVENTS_CASTLE_A2 : Sequence[str] = [
    Events.castle_a2_button.value
]

EVENTS_CISCOCITY_D : Sequence[str] = [
    Events.ciscocity_d_exit.value
]

EVENTS_CISCOCITY_C : Sequence[str] = [
    Events.ciscocity_c_button.value
]

EVENTS_STUDIO_A1 : Sequence[str] = [
    Events.studio_a1_button.value
]

EVENTS_STUDIO_A2 : Sequence[str] = [
    Events.studio_a2_button.value
]

EVENTS_STUDIO_B1 : Sequence[str] = [
    Events.studio_b1_button.value
]

EVENTS_STUDIO_F : Sequence[str] = [
    Events.studio_f_tele_robo.value
]

EVENTS_HALLOWEEN_B : Sequence[str] = [
    Events.halloween_b_jumbo_robo.value
]

EVENTS_HALLOWEEN_B1 : Sequence[str] = [
    Events.halloween_b1_jumbo_robo_shoot.value
]

EVENTS_ONSEN_A : Sequence[str] = [
    Events.onsen_a_button.value
]

EVENTS_SNOWFESTA_E : Sequence[str] = [
    Events.snowfesta_e_bell.value
]

EVENTS_EDOTOWN_B1 : Sequence[str] = [
    Events.edotown_b1_button.value
]

EVENTS_EDOTOWN_E : Sequence[str] = [
    Events.edotown_e_scroll.value
]

EVENTS_ICELAND_C : Sequence[str] = [
    Events.iceland_c_jumbo_robo.value
]

EVENTS_ICELAND_E : Sequence[str] = [
    Events.iceland_e_button.value
]

EVENTS_ARABIAN_C : Sequence[str] = [
    Events.arabian_c_golden_mon.value
]

EVENTS_ARABIAN_C1 : Sequence[str] = [
    Events.arabian_c1_exit.value
]

EVENTS_ARABIAN_G : Sequence[str] = [
    Events.arabian_g_exit.value
]

EVENTS_ASIA_A : Sequence[str] = [
    Events.asia_a_block.value
]

EVENTS_ASIA_A1 : Sequence[str] = [
    Events.asia_a1_block.value
]

EVENTS_ASIA_A2 : Sequence[str] = [
    Events.asia_a2_block.value
]

EVENTS_ASIA_B2 : Sequence[str] = [
    Events.asia_b2_button.value
]

EVENTS_ASIA_E1 : Sequence[str] = [
    Events.asia_e1_button.value
]

EVENTS_PLANE_D1 : Sequence[str] = [
    Events.plane_d1_clapper.value
]

EVENTS_HONG_B : Sequence[str] = [
    Events.hong_b_kungfu.value
]

EVENTS_HONG_B2 : Sequence[str] = [
    Events.hong_b2_button.value
]

EVENTS_BAY_A7 : Sequence[str] = [
    Events.bay_a7_button.value
]

EVENTS_BAY_A5 : Sequence[str] = [
    Events.bay_a5_button.value
]

EVENTS_BAY_E1 : Sequence[str] = [
    Events.bay_e1_button.value
]

EVENTS_TOMO_E2 : Sequence[str] = [
    Events.tomo_e2_kungfu.value
]

EVENTS_TOMO_G : Sequence[str] = [
    Events.tomo_g_button.value
]

EVENTS_TOMO_H : Sequence[str] = [
    Events.tomo_h_button.value
]

EVENTS_SPACE_E : Sequence[str] = [
    Events.space_e_button.value
]

EVENTS_SPACE_G : Sequence[str] = [
    Events.space_g_button.value
]

EVENTS_SPACE_G1 : Sequence[str] = [
    Events.space_g1_button.value
]

EVENTS_SPACE_F1 : Sequence[str] = [
    Events.space_f1_kungfu.value
]

EVENTS_SPACE_F2 : Sequence[str] = [
    Events.space_f2_button.value
]

EVENTS_SPACE_D : Sequence[str] = [
    Events.space_d_button.value
]

EVENTS_INDEX : dict[str, Sequence[str]] = {
    Stage.region_castle_b.value         : EVENTS_CASTLE_B,
    Stage.region_castle_a2.value        : EVENTS_CASTLE_A2,
    Stage.region_ciscocity_d.value      : EVENTS_CISCOCITY_D,
    Stage.region_ciscocity_c1.value     : EVENTS_CISCOCITY_C,
    Stage.region_studio_a1.value        : EVENTS_STUDIO_A1,
    Stage.region_studio_a2.value        : EVENTS_STUDIO_A2,
    Stage.region_studio_b1.value        : EVENTS_STUDIO_B1,
    Stage.region_studio_f.value         : EVENTS_STUDIO_F,
    Stage.region_halloween_b.value      : EVENTS_HALLOWEEN_B,
    Stage.region_halloween_b1.value     : EVENTS_HALLOWEEN_B1,
    Stage.region_onsen_a.value          : EVENTS_ONSEN_A,
    Stage.region_snowfesta_e.value      : EVENTS_SNOWFESTA_E,
    Stage.region_edotown_b1.value       : EVENTS_EDOTOWN_B1,
    Stage.region_edotown_e.value        : EVENTS_EDOTOWN_E,
    Stage.region_iceland_c.value        : EVENTS_ICELAND_C,
    Stage.region_iceland_e.value        : EVENTS_ICELAND_E,
    Stage.region_arabian_c.value        : EVENTS_ARABIAN_C,
    Stage.region_arabian_c1.value       : EVENTS_ARABIAN_C1,
    Stage.region_arabian_g.value        : EVENTS_ARABIAN_G,
    Stage.region_asia_a.value           : EVENTS_ASIA_A,
    Stage.region_asia_a1.value          : EVENTS_ASIA_A1,
    Stage.region_asia_a2.value          : EVENTS_ASIA_A2,
    Stage.region_asia_b2.value          : EVENTS_ASIA_B2,
    Stage.region_asia_e1.value          : EVENTS_ASIA_E1,
    Stage.region_plane_d1.value         : EVENTS_PLANE_D1,
    Stage.region_hong_b.value           : EVENTS_HONG_B,
    Stage.region_hong_b2.value          : EVENTS_HONG_B2,
    Stage.region_bay_a7.value           : EVENTS_BAY_A7,
    Stage.region_bay_a5.value           : EVENTS_BAY_A5,
    Stage.region_bay_e1.value           : EVENTS_BAY_E1,
    Stage.region_tomo_e2.value          : EVENTS_TOMO_E2,
    Stage.region_tomo_g.value           : EVENTS_TOMO_G,
    Stage.region_tomo_h.value           : EVENTS_TOMO_H,
    Stage.region_space_e.value          : EVENTS_SPACE_E,
    Stage.region_space_g.value          : EVENTS_SPACE_G,
    Stage.region_space_g1.value         : EVENTS_SPACE_G1,
    Stage.region_space_f1.value         : EVENTS_SPACE_F1,
    Stage.region_space_f2.value         : EVENTS_SPACE_F2,
    Stage.region_space_d.value          : EVENTS_SPACE_D,
}

LOCATIONS_INDEX : dict[str, Sequence[str]] = {
    key : [*MONKEYS_INDEX.get(key, []), *CAMERAS_INDEX.get(key, []), *CELLPHONES_INDEX.get(key, [])]
    for key in [*{*MONKEYS_INDEX.keys(), *CAMERAS_INDEX.keys(), *CELLPHONES_INDEX.keys()}]
}

LOCATIONS_DIRECTORY : dict[str, Sequence[str]] = {
    APHelper.monkey.value : MONKEYS_MASTER,
    APHelper.camera.value : CAMERAS_MASTER,
    APHelper.cellphone.value : CELLPHONES_MASTER,
}

def generate_name_to_id() -> dict[str, int]:
    # Monkeys
    name_to_id : dict[str, int] = { name : MonkeyLocation(name).loc_id for name in MONKEYS_MASTER }

    # Cameras
    name_to_id.update({name : CameraLocation(name, i).loc_id for i, name in enumerate(CAMERAS_MASTER)})

    # Cellphones
    name_to_id.update(
        {cell.name : cell.loc_id for cell in [CellphoneLocation(name) for name in CELLPHONES_MASTER]}
    )

    return name_to_id