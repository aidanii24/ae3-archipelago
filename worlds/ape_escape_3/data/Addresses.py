from typing import Dict, Sequence
from abc import ABC

from .Strings import Itm, Loc, Game, Meta


### [< --- HELPERS --- >]
class VersionAddresses(ABC):
    """Base Class to access easily change target memory addresses depending on Game Version used"""
    Items : Dict[str, int]
    Locations : Dict[str, int]
    GameStates : Dict[str, int]
    Pointers : Dict[str, Sequence[int]]

    GADGETS : Sequence[int]
    MORPHS_B : Sequence[int]
    MORPHS_G : Sequence[int]
    BUTTONS_BY_INTERNAL : Sequence[int]
    BUTTONS_BY_INTUIT : Sequence[int]

    def __init__(self):
        self._do_init()

    def _do_init(self):
        if not self.Items and not self.GameStates:
            return

        gadgets: list[int] = []
        morphs_b : list[int] = []
        morphs_g : list[int] = []
        buttons_internal: list[int] = []
        buttons_intuit: list[int] = []

        # Create Sequence of Gadgets by ID in Quick Gadget Swap (Water Net is index 0 for convenience)
        for gadget in Itm.get_gadgets_ordered():
            if gadget in self.Items:
                gadgets.append(self.Items[gadget])
            else:
                gadgets.clear()
                break

        self.GADGETS = gadgets

        # Create Sequence of Morph Duration Addresses for Satoru/Kei
        for morph in Game.get_morph_duration():
            if morph in self.GameStates:
                morphs_b.append(self.GameStates[morph])
            else:
                morphs_b.clear()
                break

        self.MORPHS_B = morphs_b

        # Create Sequence of Morph Duration Addresses for Sayaka/Yumi
        for morph in Game.get_morph_duration(True):
            if morph in self.GameStates:
                morphs_g.append(self.GameStates[morph])
            else:
                morphs_g.clear()
                break

        self.MORPHS_G = morphs_g

        # Get Face Buttons in order of ID used by Gadget Selected (Circle, Cross, Square, Triangle)
        for button in Game.get_buttons_by_internal_index():
            if button in self.GameStates:
                buttons_internal.append(self.GameStates[button])
            else:
                buttons_internal.clear()
                break

        self.BUTTONS_BY_INTERNAL = buttons_internal

        # Get Face Buttons by order in which gadgets may intuitively be equipped (Triangle, Cross, Square, Circle)
        for button in Game.get_buttons_by_intuitive_index():
            if button in self.GameStates:
                buttons_intuit.append(self.GameStates[button])
            else:
                buttons_intuit.clear()
                break

        self.BUTTONS_BY_INTUIT = buttons_intuit

    def get_gadget_id(self, address: int):
        if not self.GADGETS:
            return -1

        if address not in self.GADGETS:
            return -1

        gadget_id: int = self.GADGETS.index(address)

        # Return immediately if Gadget is part of normal set (the first 7)
        if gadget_id <= 7:
            return gadget_id

        # Last 3 items are RC Car variants, so return the RC Car Address for them
        return self.GADGETS.index(self.Items[Itm.gadget_rcc.value])

    def get_morph_duration_addresses(self, character : int = 0):
        if character == 0:
            return self.MORPHS_B
        else:
            return self.MORPHS_G

### [< --- ADDRESSES --- >]
class NTSCU(VersionAddresses):
    """Container for memory addresses in the NTSC-U (SCUS-97501) version of Ape Escape 3."""

    Items: Dict[str, int] = {
        # Gadgets
        Itm.gadget_club.value       : 0x649950,
        Itm.gadget_net.value        : 0x649954,
        Itm.gadget_radar.value      : 0x649958,
        Itm.gadget_hoop.value       : 0x64995c,
        Itm.gadget_sling.value      : 0x649960,
        Itm.gadget_rcc.value        : 0x649964,
        Itm.gadget_fly.value        : 0x649968,
        Itm.gadget_swim.value       : 0x649978,

        # Morphs
        Itm.morph_knight.value      : 0x649930,
        Itm.morph_cowboy.value      : 0x649934,
        Itm.morph_ninja.value       : 0x649938,
        Itm.morph_magician.value    : 0x64993c,
        Itm.morph_kungfu.value      : 0x649940,
        Itm.morph_hero.value        : 0x649944,
        Itm.morph_monkey.value      : 0x649948,

        # Accessories
        Itm.chassis_twin.value      : 0x6499A0,  # boolean (0x00 - 0x01)
        Itm.chassis_black.value     : 0x6499A1,  # boolean (0x00 - 0x01)
        Itm.chassis_pudding.value   : 0x6499A2,  # boolean (0x00 - 0x01)

        ## Functional Chassis Values
        Itm.real_chassis_twin.value     : 0x649c98,
        Itm.real_chassis_black.value    : 0x649c99,
        Itm.real_chassis_pudding.value  : 0x649c9a,
    }

    Locations: Dict[str, int] = {
        # Monkeys
        # <!> Values are on/off between 0x00 and 0x01 respectively unless commented otherwise.

        ## TV Station/Zero
        Loc.zero_ukki_pan.value                 : 0x649b4e,

        ## Seaside Resort
        Loc.seaside_nessal.value                : 0x6499dd,
        Loc.seaside_ukki_pia.value              : 0x6499de,
        Loc.seaside_sarubo.value                : 0x6499df,
        Loc.seaside_salurin.value               : 0x6499e0,
        Loc.seaside_ukkitan.value               : 0x649b4f,
        Loc.seaside_morella.value               : 0x649b99,
        Loc.seaside_ukki_ben.value              : 0x6499e1,
        Loc.seaside_kankichi.value              : 0x649b5e,
        Loc.seaside_tomezo.value                : 0x649b5f,
        Loc.seaside_kamayan.value               : 0x649b60,
        Loc.seaside_taizo.value                 : 0x649b61,

        ## Hide-n-Seek Forest
        Loc.woods_ukki_pon.value                : 0x6499e2,
        Loc.woods_ukkian.value                  : 0x6499e3,
        Loc.woods_ukki_red.value                : 0x6499e4,
        Loc.woods_rosalin.value                 : 0x649b4b,
        Loc.woods_salubon.value                 : 0x6499e5,
        Loc.woods_wolfmon.value                 : 0x6499e6,
        Loc.woods_ukiko.value                   : 0x649be8,
        Loc.woods_lambymon.value                : 0x6499e7,
        Loc.woods_kreemon.value                 : 0x6499e8,
        Loc.woods_ukkilei.value                 : 0x6499e9,
        Loc.woods_spork.value                   : 0x649be7,
        Loc.woods_king_goat.value               : 0x649b62,
        Loc.woods_marukichi.value               : 0x649b63,
        Loc.woods_kikimon.value                 : 0x649b64,
        Loc.woods_kominato.value                : 0x649b65,

        ## Saru-mon's Castle
        Loc.castle_ukkido.value                 : 0x6499ea,
        Loc.castle_pipo_guard.value             : 0x6499eb,
        Loc.castle_monderella.value             : 0x6499ec,
        Loc.castle_ukki_ichi.value              : 0x6499ed,
        Loc.castle_ukkinee.value                : 0x6499ee,
        Loc.castle_saru_mon.value               : 0x6499ef,
        Loc.castle_monga.value                  : 0x6499f0,
        Loc.castle_ukkiton.value                : 0x6499f1,
        Loc.castle_king_leo.value               : 0x6499f2,
        Loc.castle_ukkii.value                  : 0x6499f3,
        Loc.castle_saluto.value                 : 0x6499f4,
        Loc.castle_kings_double.value           : 0x649b68,
        Loc.castle_mattsun.value                : 0x649b69,
        Loc.castle_miya.value                   : 0x649b6a,
        Loc.castle_mon_san.value                : 0x649b6b,
        Loc.castle_sal_1000.value               : 0x649be4,

        ## Monkey White Battle!
        Loc.boss_monkey_white.value             : 0x649b40,

        ## The Big City
        Loc.ciscocity_ukima.value               : 0x6499f5,
        Loc.ciscocity_monbolo.value             : 0x6499f6,
        Loc.ciscocity_pipo_mondy.value          : 0x6499f7,
        Loc.ciscocity_ukki_mattan.value         : 0x6499f8,
        Loc.ciscocity_bemucho.value             : 0x6499f9,
        Loc.ciscocity_ukki_nader.value          : 0x649be5,
        Loc.ciscocity_sabu_sabu.value           : 0x649b5b,
        Loc.ciscocity_ginjiro.value             : 0x649b5c,
        Loc.ciscocity_kichiemon.value           : 0x649b5d,
        Loc.ciscocity_ukkilun.value             : 0x6499fb,
        Loc.ciscocity_bully_mon.value           : 0x6499fc,
        Loc.ciscocity_ukki_joe.value            : 0x6499fd,
        Loc.ciscocity_tamaki.value              : 0x6499fe,
        Loc.ciscocity_mickey_oou.value          : 0x6499ff,
        Loc.ciscocity_sally_kokoroe.value       : 0x649b6c,
        Loc.ciscocity_monkey_manager.value      : 0x649b6d,
        Loc.ciscocity_supervisor_chimp.value    : 0x649b6e,
        Loc.ciscocity_boss_ape.value            : 0x649b6f,

        ## Specter TV Studio
        Loc.studio_ukki_yan.value               : 0x649a00,
        Loc.studio_ukkipuss.value               : 0x649a01,
        Loc.studio_minoh.value                  : 0x649a02,
        Loc.studio_monta.value                  : 0x649a03,
        Loc.studio_pipopam.value                : 0x649a04,
        Loc.studio_monpii_ukkichi.value         : 0x649a05,
        Loc.studio_gabimon.value                : 0x649a06,
        Loc.studio_bananamon.value              : 0x649a07,
        Loc.studio_mokinza.value                : 0x649a08,
        Loc.studio_ukki_lee_ukki.value          : 0x649a09,
        Loc.studio_ukkida_jiro.value            : 0x649a0a,
        Loc.studio_sal_ukindo.value             : 0x649a0b,
        Loc.studio_gimminey.value               : 0x649a9e,
        Loc.studio_hant.value                   : 0x649aab,
        Loc.studio_chippino.value               : 0x649bd8,
        Loc.studio_ukki_paul.value              : 0x649b70,
        Loc.studio_sally_mon.value              : 0x649b71,
        Loc.studio_bonly.value                  : 0x649b72,
        Loc.studio_monly.value                  : 0x649b73,


        ## Bootown
        Loc.halloween_monkichiro.value          : 0x649a0c,
        Loc.halloween_leomon.value              : 0x649a0d,
        Loc.halloween_uikkun.value              : 0x649a0e,
        Loc.halloween_take_ukita.value          : 0x649a0f,
        Loc.halloween_bonbon.value              : 0x649a10,
        Loc.halloween_chichi.value              : 0x649a11,
        Loc.halloween_ukkisuke.value            : 0x649a13,
        Loc.halloween_chibi_sally.value         : 0x649a14,
        Loc.halloween_ukkison.value             : 0x649a15,
        Loc.halloween_saruhotep.value           : 0x649a16,
        Loc.halloween_ukkito.value              : 0x649a17,
        Loc.halloween_monzally.value            : 0x649a18,
        Loc.halloween_ukkiami.value             : 0x649a19,
        Loc.halloween_monjan.value              : 0x649b74,
        Loc.halloween_nattchan.value            : 0x649b75,
        Loc.halloween_kabochin.value            : 0x649b76,
        Loc.halloween_ukki_mon.value            : 0x649b77,
        Loc.halloween_mumpkin.value             : 0x649a12,

        ## Wild West Town
        Loc.western_morrey.value                : 0x649a1a,
        Loc.western_jomi.value                  : 0x649a1b,
        Loc.western_tammy.value                 : 0x649a1c,
        Loc.western_ukki_gigolo.value           : 0x649a1e,
        Loc.western_monboron.value              : 0x649a1f,
        Loc.western_west_ukki.value             : 0x649a28,
        Loc.western_lucky_woo.value             : 0x649b78,
        Loc.western_pamela.value                : 0x649b79,
        Loc.western_ukki_monber.value           : 0x649b7a,
        Loc.western_gaukichi.value              : 0x649b7b,
        Loc.western_shaluron.value              : 0x649a20,
        Loc.western_jay_mohn.value              : 0x649a21,
        Loc.western_munkee_joe.value            : 0x649a22,
        Loc.western_saru_chison.value           : 0x649a23,
        Loc.western_jaja_jamo.value             : 0x649a24,
        Loc.western_chammy_mo.value             : 0x649a25,
        Loc.western_golon_moe.value             : 0x649a26,
        Loc.western_golozo.value                : 0x649a27,
        Loc.western_ukkia_munbo.value           : 0x649a1d,
        Loc.western_mon_johny.value             : 0x649b1a,

        ## Monkey Blue Battle!
        Loc.boss_monkey_blue.value              : 0x649b41,

        ## The Hot Springs
        Loc.onsen_chabimon.value                : 0x649a29,
        Loc.onsen_saru_sam.value                : 0x649a2a,
        Loc.onsen_kiichiro.value                : 0x649a2b,
        Loc.onsen_tome_san.value                : 0x649a2c,
        Loc.onsen_michiyan.value                : 0x649a2d,
        Loc.onsen_ukki_ichiro.value             : 0x649a41,
        Loc.onsen_ukki_emon.value               : 0x649a2e,
        Loc.onsen_moki.value                    : 0x649a2f,
        Loc.onsen_ukimi.value                   : 0x649a30,
        Loc.onsen_domobeh.value                 : 0x649a31,
        Loc.onsen_sam_san.value                 : 0x649b81,
        Loc.onsen_donkichi.value                : 0x649b82,
        Loc.onsen_minokichi.value               : 0x649b83,
        Loc.onsen_tatabo.value                  : 0x649B84,
        Loc.onsen_kimi_san.value                : 0x649a34,
        Loc.onsen_michiro.value                 : 0x649a35,
        Loc.onsen_gen_san.value                 : 0x649bde,
        Loc.onsen_mujakin.value                 : 0x649a36,
        Loc.onsen_mihachin.value                : 0x649a37,
        Loc.onsen_fuji_chan.value               : 0x649a38,

        ## Winterville
        Loc.snowfesta_kimisuke.value            : 0x649a39,
        Loc.snowfesta_konzo.value               : 0x649a3a,
        Loc.snowfesta_saburota.value            : 0x649a3b,
        Loc.snowfesta_mitsuro.value             : 0x649a3c,
        Loc.snowfesta_takuo.value               : 0x649a94,
        Loc.snowfesta_konkichi.value            : 0x649aa6,
        Loc.snowfesta_fumikichi.value           : 0x649a3d,
        Loc.snowfesta_pipotron_yellow.value     : 0x649be3,
        Loc.snowfesta_tamubeh.value             : 0x649a3e,
        Loc.snowfesta_kimikichi.value           : 0x649a3f,
        Loc.snowfesta_gonbeh.value              : 0x649a40,
        Loc.snowfesta_shimmy.value              : 0x649be0,
        Loc.snowfesta_mako.value                : 0x649a43,
        Loc.snowfesta_miko.value                : 0x649a44,
        Loc.snowfesta_tamio.value               : 0x649a45,
        Loc.snowfesta_jeitan.value              : 0x649a46,
        Loc.snowfesta_ukki_jii.value            : 0x649a47,
        Loc.snowfesta_akki_bon.value            : 0x649bd7,
        Loc.snowfesta_kimi_chan.value           : 0x649b85,
        Loc.snowfesta_sae_chan.value            : 0x649b86,
        Loc.snowfesta_tassan.value              : 0x649b87,
        Loc.snowfesta_tomokun.value             : 0x649b88,

        ## The Emperor's Castle
        Loc.edotown_pipo_tobi.value             : 0x649a48,
        Loc.edotown_masan.value                 : 0x649a49,
        Loc.edotown_mohachi.value               : 0x649a4a,
        Loc.edotown_mon_ninpo.value             : 0x649a4c,
        Loc.edotown_yosio.value                 : 0x649a4d,
        Loc.edotown_fatty_mcfats.value          : 0x649a4e,
        Loc.edotown_kikimaru.value              : 0x649a4f,
        Loc.edotown_tomoku_chan.value           : 0x649a50,
        Loc.edotown_uziko.value                 : 0x649a51,
        Loc.edotown_gp.value                    : 0x649a52,
        Loc.edotown_walter.value                : 0x649a53,
        Loc.edotown_monkibeth.value             : 0x649a54,
        Loc.edotown_babuzo.value                : 0x649a55,
        Loc.edotown_fishy_feet.value            : 0x649a56,
        Loc.edotown_pipo_torin.value            : 0x649a57,
        Loc.edotown_tomi.value                  : 0x649a58,
        Loc.edotown_master_pan.value            : 0x649a59,
        Loc.edotown_monchin_chi.value           : 0x649b89,
        Loc.edotown_masachi.value               : 0x649b8a,
        Loc.edotown_golota.value                : 0x649b8b,
        Loc.edotown_kinsuke.value               : 0x649b8c,

        ## Monkey Blue Battle!
        Loc.boss_monkey_yellow.value            : 0x649b42,

        ## Mount Amazing
        Loc.heaven_ukkichi.value                : 0x649a5a,
        Loc.heaven_chomon.value                 : 0x649a5b,
        Loc.heaven_ukkido.value                 : 0x649a5c,
        Loc.heaven_kyamio.value                 : 0x649a5d,
        Loc.heaven_talupon.value                : 0x649a5e,
        Loc.heaven_bokitan.value                : 0x649a5f,
        Loc.heaven_tami.value                   : 0x649a66,
        Loc.heaven_micchino.value               : 0x649a67,
        Loc.heaven_talurin.value                : 0x649a60,
        Loc.heaven_occhimon.value               : 0x649a61,
        Loc.heaven_mikkurin.value               : 0x649a62,
        Loc.heaven_kicchino.value               : 0x649a63,
        Loc.heaven_kimurin.value                : 0x649a64,
        Loc.heaven_sakkano.value                : 0x649a65,
        Loc.heaven_camino.value                 : 0x649a68,
        Loc.heaven_valuccha.value               : 0x649a69,
        Loc.heaven_pisuke.value                 : 0x649b8d,
        Loc.heaven_kansuke.value                : 0x649b8e,
        Loc.heaven_pohta.value                  : 0x649b8f,
        Loc.heaven_keisuke.value                : 0x649b90,

        ## Toytown
        Loc.toyhouse_pikkori.value              : 0x649a6a,
        Loc.toyhouse_talukki.value              : 0x649a6b,
        Loc.toyhouse_pinkino.value              : 0x649a6c,
        Loc.toyhouse_bon_mota.value             : 0x649a6d,
        Loc.toyhouse_bon_verna.value            : 0x649a6e,
        Loc.toyhouse_bon_papa.value             : 0x649a6f,
        Loc.toyhouse_bon_mama.value             : 0x649a70,
        Loc.toyhouse_kalkin.value               : 0x649aa8,
        Loc.toyhouse_pakun.value                : 0x649a71,
        Loc.toyhouse_ukki_x.value               : 0x649a72,
        Loc.toyhouse_mon_gareji.value           : 0x649a73,
        Loc.toyhouse_shouji.value               : 0x649bdc,
        Loc.toyhouse_woo_makka.value            : 0x649bdd,
        Loc.toyhouse_monto.value                : 0x649a74,
        Loc.toyhouse_mokitani.value             : 0x649a75,
        Loc.toyhouse_namigo.value               : 0x649bda,
        Loc.toyhouse_pipotron_red.value         : 0x649be1,
        Loc.toyhouse_master_loafy.value         : 0x649a77,
        Loc.toyhouse_golonero.value             : 0x649a78,
        Loc.toyhouse_kocho.value                : 0x649bdb,
        Loc.toyhouse_tam_konta.value            : 0x649b91,
        Loc.toyhouse_tam_mimiko.value           : 0x649b92,
        Loc.toyhouse_tam_papa.value             : 0x649b93,
        Loc.toyhouse_tam_mama.value             : 0x649b94,

        ## Arctice Wonderland
        Loc.iceland_bikupuri.value              : 0x649a7b,
        Loc.iceland_ukkisu.value                : 0x649a7c,
        Loc.iceland_ukki_ami.value              : 0x649a7d,
        Loc.iceland_balio.value                 : 0x649a93,
        Loc.iceland_kimkon.value                : 0x649a79,
        Loc.iceland_ukkina.value                : 0x649a7a,
        Loc.iceland_kushachin.value             : 0x649a82,
        Loc.iceland_malikko.value               : 0x649a7e,
        Loc.iceland_bolikko.value               : 0x649a7f,
        Loc.iceland_iceymon.value               : 0x649a80,
        Loc.iceland_mokkidon.value              : 0x649a81,
        Loc.iceland_jolly_mon.value             : 0x649a83,
        Loc.iceland_hikkori.value               : 0x649a84,
        Loc.iceland_rammy.value                 : 0x649a85,
        Loc.iceland_monkino.value               : 0x649b95,
        Loc.iceland_kyam.value                  : 0x649b96,
        Loc.iceland_kappino.value               : 0x649b97,
        Loc.iceland_kris_krimon.value           : 0x649b98,

        ## Mirage Town
        Loc.arabian_scorpi_mon.value            : 0x649a86,
        Loc.arabian_minimon.value               : 0x649a87,
        Loc.arabian_moontero.value              : 0x649a88,
        Loc.arabian_ukki_son.value              : 0x649a89,
        Loc.arabian_ukki_jeff.value             : 0x649a8a,
        Loc.arabian_saru_maru.value             : 0x649a8b,
        Loc.arabian_genghis_mon.value           : 0x649a8c,
        Loc.arabian_cup_o_mon.value             : 0x649a8d,
        Loc.arabian_nijal.value                 : 0x649a8e,
        Loc.arabian_apey_jones.value            : 0x649a8f,
        Loc.arabian_ukki_mamba.value            : 0x649a90,
        Loc.arabian_golden_mon.value            : 0x649a91,
        Loc.arabian_crazy_ol_mon.value          : 0x649a92,
        Loc.arabian_shamila.value               : 0x649a95,
        Loc.arabian_tamiyanya.value             : 0x649a96,
        Loc.arabian_salteenz.value              : 0x649a98,
        Loc.arabian_dancing_mia.value           : 0x649a99,
        Loc.arabian_miccho.value                : 0x649bbb,
        Loc.arabian_kisha.value                 : 0x649bbc,
        Loc.arabian_gimuccho.value              : 0x649bbd,
        Loc.arabian_wojin.value                 : 0x649bbe,
        Loc.arabian_princess_judy.value         : 0x649a97,

        ## Monkey Pink Battle!
        Loc.boss_monkey_pink.value              : 0x649b43,

        ## Eversummer Island
        Loc.asia_ukki_mat.value                 : 0x649a9a,
        Loc.asia_salumani.value                 : 0x649a9b,
        Loc.asia_salulu.value                   : 0x649a9c,
        Loc.asia_baku.value                     : 0x649a9d,
        Loc.asia_salunch.value                  : 0x649aa7,
        Loc.asia_pincher_mon.value              : 0x649aaa,
        Loc.asia_mong_popo.value                : 0x649aa0,
        Loc.asia_mohcha.value                   : 0x649aa1,
        Loc.asia_kamcha.value                   : 0x649aa2,
        Loc.asia_bimocha.value                  : 0x649aa3,
        Loc.asia_gimchin.value                  : 0x649aa4,
        Loc.asia_kamaccha.value                 : 0x649aa5,
        Loc.asia_gyamu.value                    : 0x649aac,
        Loc.asia_takumon.value                  : 0x649aad,
        Loc.asia_ukki_ether.value               : 0x649aae,
        Loc.asia_tartan.value                   : 0x649aaf,
        Loc.asia_molzone.value                  : 0x649ab0,
        Loc.asia_chappio.value                  : 0x649ab1,
        Loc.asia_pomoah.value                   : 0x649ab2,
        Loc.asia_gucchai.value                  : 0x649bbf,
        Loc.asia_makaccho.value                 : 0x649bc0,
        Loc.asia_gamaran.value                  : 0x649bc1,
        Loc.asia_larry.value                    : 0x649bc2,

        ## Airplane Squadron
        Loc.plane_romo.value                    : 0x649ab3,
        Loc.plane_temko.value                   : 0x649ab4,
        Loc.plane_ukkigawa.value                : 0x649ab5,
        Loc.plane_mokkido.value                 : 0x649ab6,
        Loc.plane_pont.value                    : 0x649ab7,
        Loc.plane_gamish.value                  : 0x649ab8,
        Loc.plane_prince_bertus.value           : 0x649ab9,
        Loc.plane_takmon.value                  : 0x649aba,
        Loc.plane_chai_bunny.value              : 0x649abb,
        Loc.plane_mukita.value                  : 0x649be6,
        Loc.plane_tamrai.value                  : 0x649abc,
        Loc.plane_kemunpa.value                 : 0x649abd,
        Loc.plane_pipotron_blue.value           : 0x649be2,
        Loc.plane_mabaras.value                 : 0x649abe,
        Loc.plane_tamoos.value                  : 0x649abf,
        Loc.plane_kimoto.value                  : 0x649ac0,
        Loc.plane_octavian.value                : 0x649ac3,
        Loc.plane_samuel.value                  : 0x649bc3,
        Loc.plane_coril.value                   : 0x649bc4,
        Loc.plane_bont.value                    : 0x649bc5,
        Loc.plane_delly.value                   : 0x649bc6,
        Loc.plane_jeloh.value                   : 0x649ac1,
        Loc.plane_bongo.value                   : 0x649ac2,

        ## Kung-Fu Alley
        Loc.hong_dally.value                    : 0x649ac4,
        Loc.hong_nak_nayo.value                 : 0x649ac5,
        Loc.hong_donto_koi.value                : 0x649ac6,
        Loc.hong_po_kin_ki.value                : 0x649ac7,
        Loc.hong_ukki_chan.value                : 0x649ac8,
        Loc.hong_uki_uki.value                  : 0x649ac9,
        Loc.hong_muki_muki.value                : 0x649aca,
        Loc.hong_shinchi.value                  : 0x649acb,
        Loc.hong_doh_tsuitaro.value             : 0x649acd,
        Loc.hong_hi_uchi_ishi.value             : 0x649ace,
        Loc.hong_gala_waruo.value               : 0x649acf,
        Loc.hong_bassili_ukki.value             : 0x649ad0,
        Loc.hong_danchi.value                   : 0x649ad1,
        Loc.hong_pikon.value                    : 0x649ad2,
        Loc.hong_bankan.value                   : 0x649ad3,
        Loc.hong_sukei.value                    : 0x649ad4,
        Loc.hong_giyan.value                    : 0x649ad5,
        Loc.hong_muchaki.value                  : 0x649ada,
        Loc.hong_yoh_kitana.value               : 0x649adb,
        Loc.hong_goshi_andos.value              : 0x649adc,
        Loc.hong_pukuman.value                  : 0x649add,
        Loc.hong_block_master.value             : 0x649adf,
        Loc.hong_tompo.value                    : 0x649bc7,
        Loc.hong_wootan.value                   : 0x649bc8,
        Loc.hong_chechin.value                  : 0x649bc9,
        Loc.hong_hapcho.value                   : 0x649bca,
        Loc.hong_bonmos.value                   : 0x649ad7,
        Loc.hong_dark_master.value              : 0x649bdf,
        Loc.hong_teh_isu.value                  : 0x649ad8,
        Loc.hong_ponja.value                    : 0x649ad9,

        ## Monkey Red Battle!
        Loc.boss_monkey_red.value               : 0x649b44,

        Loc.bay_nadamon.value                   : 0x649ae0,
        Loc.bay_patoya.value                    : 0x649ae1,
        Loc.bay_gumbo.value                     : 0x649ae2,
        Loc.bay_pehyan.value                    : 0x649ae3,
        Loc.bay_mokito.value                    : 0x649ae4,
        Loc.bay_pipo_kate.value                 : 0x649ae5,
        Loc.bay_samtan.value                    : 0x649ae6,
        Loc.bay_pokkine.value                   : 0x649ae7,
        Loc.bay_daban.value                     : 0x649ae8,
        Loc.bay_shiny_pete.value                : 0x649aa9,
        Loc.bay_keiichi.value                   : 0x649ae9,
        Loc.bay_landon.value                    : 0x649aea,
        Loc.bay_mcbreezy.value                  : 0x649aeb,
        Loc.bay_ronson.value                    : 0x649aec,
        Loc.bay_gimo.value                      : 0x649aed,
        Loc.bay_hiroshi.value                   : 0x649aee,
        Loc.bay_nakabi.value                    : 0x649aef,
        Loc.bay_mibon.value                     : 0x649af0,
        Loc.bay_bololon.value                   : 0x649af1,
        Loc.bay_gimi_gimi.value                 : 0x649acc,
        Loc.bay_doemos.value                    : 0x649af2,
        Loc.bay_kazuo.value                     : 0x649af3,
        Loc.bay_pokkini.value                   : 0x649af4,
        Loc.bay_jimo.value                      : 0x649af5,
        Loc.bay_bokino.value                    : 0x649af6,
        Loc.bay_makidon.value                   : 0x649bcb,
        Loc.bay_dogy.value                      : 0x649bcc,
        Loc.bay_gibdon.value                    : 0x649bcd,
        Loc.bay_buligie.value                   : 0x649bce,

        Loc.tomo_kichibeh.value                 : 0x649af8,
        Loc.tomo_bonchicchi.value               : 0x649af9,
        Loc.tomo_mikibon.value                  : 0x649afa,
        Loc.tomo_dj_tamo.value                  : 0x649afb,
        Loc.tomo_ukkinaka.value                 : 0x649afc,
        Loc.tomo_ukkine.value                   : 0x649afd,
        Loc.tomo_pon_jiro.value                 : 0x649aff,
        Loc.tomo_chimpy.value                   : 0x649b00,
        Loc.tomo_kajitan.value                  : 0x649b01,
        Loc.tomo_uka_uka.value                  : 0x649b02,
        Loc.tomo_mil_mil.value                  : 0x649b03,
        Loc.tomo_taimon.value                   : 0x649b07,
        Loc.tomo_goro_san.value                 : 0x649b08,
        Loc.tomo_reiji.value                    : 0x649b09,
        Loc.tomo_ponta.value                    : 0x649b0a,
        Loc.tomo_tomio.value                    : 0x649b0b,
        Loc.tomo_gario.value                    : 0x649b0c,
        Loc.tomo_dj_pari.value                  : 0x649b0d,
        Loc.tomo_mitsuo.value                   : 0x649b0e,
        Loc.tomo_riley.value                    : 0x649b0f,
        Loc.tomo_pipo_ron.value                 : 0x649b10,
        Loc.tomo_mikita.value                   : 0x649b11,
        Loc.tomo_sal_13.value                   : 0x649b12,
        Loc.tomo_sal_12.value                   : 0x649b13,
        Loc.tomo_tomu.value                     : 0x649bcf,
        Loc.tomo_breadacus.value                : 0x649bd0,
        Loc.tomo_ukkigoro.value                 : 0x649bd1,
        Loc.tomo_ukiji.value                    : 0x649bd2,
        Loc.tomo_tomimon.value                  : 0x649af7,

        Loc.boss_tomoki.value                   : 0x647a58,

        Loc.space_poko.value                    : 0x649b14,
        Loc.space_gamuo.value                   : 0x649b15,
        Loc.space_mukikko.value                 : 0x649b3c,
        Loc.space_moto_ukki.value               : 0x649b16,
        Loc.space_jimi_jami.value               : 0x649b17,
        Loc.space_genbo.value                   : 0x649b18,
        Loc.space_twin_mitty.value              : 0x649b19,
        Loc.space_uttey.value                   : 0x649b1d,
        Loc.space_emma.value                    : 0x649b1e,
        Loc.space_dokicchi.value                : 0x649b1f,
        Loc.space_kamicchi.value                : 0x649b20,
        Loc.space_ukki_monda.value              : 0x649b21,
        Loc.space_porokko.value                 : 0x649b22,
        Loc.space_zonelin.value                 : 0x649b23,
        Loc.space_tamano.value                  : 0x649b24,
        Loc.space_nelson.value                  : 0x649b25,
        Loc.space_koloneh.value                 : 0x649b26,
        Loc.space_miluchy.value                 : 0x649b27,
        Loc.space_robert.value                  : 0x649b28,
        Loc.space_fronson.value                 : 0x649b29,
        Loc.space_demekin.value                 : 0x649b2a,
        Loc.space_kikuyoshi.value               : 0x649b2b,
        Loc.space_freet.value                   : 0x649b2c,
        Loc.space_chico.value                   : 0x649b2d,
        Loc.space_gamurin.value                 : 0x649b2e,
        Loc.space_pipo_mon.value                : 0x649b2f,
        Loc.space_gam_gam.value                 : 0x649b30,
        Loc.space_doronbo.value                 : 0x649b31,
        Loc.space_benja.value                   : 0x649b32,
        Loc.space_macchan.value                 : 0x649b33,
        Loc.space_rokkun.value                  : 0x649b34,
        Loc.space_ukki_love.value               : 0x649b35,
        Loc.space_momongo.value                 : 0x649b36,
        Loc.space_moepi.value                   : 0x649b37,
        Loc.space_pumon.value                   : 0x649b38,
        Loc.space_makiban.value                 : 0x649b39,
        Loc.space_upis.value                    : 0x649bd3,
        Loc.space_mondatta.value                : 0x649bd4,
        Loc.space_gicchom.value                 : 0x649bd5,
        Loc.space_barire.value                  : 0x649bd6,
        Loc.space_sal_10.value                  : 0x649b3d,
        Loc.space_sal_11.value                  : 0x649b3e,
        Loc.space_sal_3000.value                : 0x649beb,

        # Specter
        Loc.boss_specter.value                  : 0x649bec,
        Loc.boss_specter_final.value            : 0x649b46,

        # Permanent Boss Check Addresses
        ## These are used to store permanently store the status of these locations,
        ## as their real addresses affect and may even hinder game use and progression
        Loc.boss_alt_white.value                : 0x649b50,
        Loc.boss_alt_blue.value                 : 0x649b51,
        Loc.boss_alt_yellow.value               : 0x649b52,
        Loc.boss_alt_pink.value                 : 0x649b53,
        Loc.boss_alt_red.value                  : 0x649b54,
        Loc.boss_alt_tomoki.value               : 0x649b55,
        Loc.boss_alt_specter.value              : 0x649b56,
        Loc.boss_alt_specter_final.value        : 0x649b57,

        # Pipo Camera
        Loc.pipo_camera.value                   : 0x1F4,
        Loc.seaside_cam.value                   : 0x649B9A,
        Loc.woods_cam.value                     : 0x649B9B,
        Loc.castle_cam.value                    : 0x649B9C,
        Loc.ciscocity_cam.value                 : 0x649B9D,
        Loc.studio_cam.value                    : 0x649B9E,
        Loc.halloween_cam.value                 : 0x649B9F,
        Loc.western_cam.value                   : 0x649BA0,
        Loc.onsen_cam.value                     : 0x649BA1,
        Loc.snowfesta_cam.value                 : 0x649BA2,
        Loc.edotown_cam.value                   : 0x649BA3,
        Loc.heaven_cam.value                    : 0x649BA4,
        Loc.toyhouse_cam.value                  : 0x649BA5,
        Loc.iceland_cam.value                   : 0x649BA6,
        Loc.arabian_cam.value                   : 0x649BA7,
        Loc.asia_cam.value                      : 0x649BA8,
        Loc.plane_cam.value                     : 0x649BA9,
        Loc.hong_cam.value                      : 0x649BAA,
        Loc.bay_cam.value                       : 0x649BAB,
        Loc.tomo_cam.value                      : 0x649BAC,
        Loc.space_cam.value                     : 0x649BAD,

        # Cellphones
        Loc.tele_000.value                      : 0x649BB0,
        Loc.tele_001.value                      : 0x649BB1,
        Loc.tele_002.value                      : 0x649BB2,
        Loc.tele_003.value                      : 0x649BB3,
        Loc.tele_004ss.value                    : 0x649BB4,
        Loc.tele_004wo.value                    : 0x649BB5,
        Loc.tele_006.value                      : 0x649BB6,
        Loc.tele_007.value                      : 0x649BB7,
        Loc.tele_008.value                      : 0x649BB8,
        Loc.tele_009.value                      : 0x649BB9,
        Loc.tele_010.value                      : 0x649BBA,
        Loc.tele_011.value                      : 0x649BD9,
        Loc.tele_012cc.value                    : 0x649BED,
        Loc.tele_012tv.value                    : 0x649BEE,
        Loc.tele_013.value                      : 0x649BEF,
        Loc.tele_014.value                      : 0x649BF0,
        Loc.tele_015.value                      : 0x649BF1,
        Loc.tele_016.value                      : 0x649BF2,
        Loc.tele_017.value                      : 0x649BF3,
        Loc.tele_018.value                      : 0x649BF4,
        Loc.tele_019.value                      : 0x649BF5,
        Loc.tele_020.value                      : 0x649BF6,
        Loc.tele_021on.value                    : 0x649BF7,
        Loc.tele_021ic.value                    : 0x649BF8,
        Loc.tele_022sf.value                    : 0x649BF9,
        Loc.tele_022pl.value                    : 0x649BFA,
        Loc.tele_023.value                      : 0x649BFB,
        Loc.tele_024.value                      : 0x649BFC,
        Loc.tele_025.value                      : 0x649BFD,
        Loc.tele_026.value                      : 0x649BFE,
        Loc.tele_028.value                      : 0x649BFF,
        Loc.tele_029.value                      : 0x649C00,
        Loc.tele_030tv.value                    : 0x649C01,
        Loc.tele_030ty.value                    : 0x649C02,
        Loc.tele_031.value                      : 0x649C03,
        Loc.tele_032.value                      : 0x649C04,
        Loc.tele_033.value                      : 0x649C05,
        Loc.tele_034.value                      : 0x649C06,
        Loc.tele_035.value                      : 0x649C07,
        Loc.tele_037.value                      : 0x649C08,
        Loc.tele_039.value                      : 0x649C09,
        Loc.tele_040h_a.value                   : 0x649C0A,
        Loc.tele_040h_b.value                   : 0x649C0B,
        Loc.tele_042ar.value                    : 0x649C0C,
        Loc.tele_042ho.value                    : 0x649C0D,
        Loc.tele_044.value                      : 0x649C0E,
        Loc.tele_045.value                      : 0x649C0F,
        Loc.tele_047.value                      : 0x649C10,
        Loc.tele_048.value                      : 0x649C11,
        Loc.tele_051.value                      : 0x649C12,
        Loc.tele_052.value                      : 0x649C13,
        Loc.tele_062.value                      : 0x649C14,
        Loc.tele_063.value                      : 0x649C15,

        # Shopping Area
        ## Monkey Mart
        Loc.shop_morph_stock.value              : 0x100,

        ## Book Shop
        Loc.hint_book.value                     : 0x01,
        Loc.mon_fiction.value                   : 0x15,
        Loc.channel_guide.value                 : 0x29,

        Loc.hint_book_1.value                   : 0x649c84,
        Loc.hint_book_2.value                   : 0x649c85,
        Loc.hint_book_3.value                   : 0x649c86,
        Loc.hint_book_4.value                   : 0x649c87,
        Loc.hint_book_5.value                   : 0x649c88,
        Loc.hint_book_6.value                   : 0x649c89,
        Loc.hint_book_7.value                   : 0x649c8A,
        Loc.hint_book_8.value                   : 0x649c8B,
        Loc.hint_book_9.value                   : 0x649c8C,
        Loc.hint_book_10.value                  : 0x649c8D,
        Loc.hint_book_11.value                  : 0x649c8E,
        Loc.hint_book_12.value                  : 0x649c8F,
        Loc.hint_book_13.value                  : 0x649c90,
        Loc.hint_book_14.value                  : 0x649c91,
        Loc.hint_book_15.value                  : 0x649c92,
        Loc.hint_book_16.value                  : 0x649c93,
        Loc.hint_book_17.value                  : 0x649c94,
        Loc.hint_book_18.value                  : 0x649c95,
        Loc.hint_book_19.value                  : 0x649c96,
        Loc.hint_book_20.value                  : 0x649c97,

        Loc.mon_fiction_1.value                 : 0x649cb2,
        Loc.mon_fiction_2.value                 : 0x649cb3,
        Loc.mon_fiction_3.value                 : 0x649cb4,
        Loc.mon_fiction_4.value                 : 0x649cb5,
        Loc.mon_fiction_5.value                 : 0x649cb6,
        Loc.mon_fiction_6.value                 : 0x649cb7,
        Loc.mon_fiction_7.value                 : 0x649cb8,
        Loc.mon_fiction_8.value                 : 0x649cb9,
        Loc.mon_fiction_9.value                 : 0x649cba,
        Loc.mon_fiction_10.value                : 0x649cbb,
        Loc.mon_fiction_11.value                : 0x649cbc,
        Loc.mon_fiction_12.value                : 0x649cbd,
        Loc.mon_fiction_13.value                : 0x649cbe,
        Loc.mon_fiction_14.value                : 0x649cbf,
        Loc.mon_fiction_15.value                : 0x649cc0,
        Loc.mon_fiction_16.value                : 0x649cc1,
        Loc.mon_fiction_17.value                : 0x649cc2,
        Loc.mon_fiction_18.value                : 0x649cc3,
        Loc.mon_fiction_19.value                : 0x649cc4,
        Loc.mon_fiction_20.value                : 0x649cc5,

        Loc.channel_guide_1.value               : 0x649c9e,
        Loc.channel_guide_2.value               : 0x649c9f,
        Loc.channel_guide_3.value               : 0x649ca0,
        Loc.channel_guide_4.value               : 0x649ca1,
        Loc.channel_guide_5.value               : 0x649ca2,
        Loc.channel_guide_6.value               : 0x649ca3,
        Loc.channel_guide_7.value               : 0x649ca4,
        Loc.channel_guide_8.value               : 0x649ca5,
        Loc.channel_guide_9.value               : 0x649ca6,
        Loc.channel_guide_10.value              : 0x649ca7,
        Loc.channel_guide_11.value              : 0x649ca8,
        Loc.channel_guide_12.value              : 0x649ca9,
        Loc.channel_guide_13.value              : 0x649caa,
        Loc.channel_guide_14.value              : 0x649cab,
        Loc.channel_guide_15.value              : 0x649cac,
        Loc.channel_guide_16.value              : 0x649cad,
        Loc.channel_guide_17.value              : 0x649cae,
        Loc.channel_guide_18.value              : 0x649caf,
        Loc.channel_guide_19.value              : 0x649cb0,
        Loc.channel_guide_20.value              : 0x649cb1,

        ## Hobby Shop
        Loc.bonus_rc_cars.value                 : 0x3D,
        Loc.lucky_photo.value                   : 0x40,

        Loc.bonus_rc_cars_1.value               : 0x6499A3,
        Loc.bonus_rc_cars_2.value               : 0x6499A4,
        Loc.bonus_rc_cars_3.value               : 0x6499A5,

        Loc.shop_super_monkey_throw_stadium.value   : 0x649c9b,
        Loc.shop_ultim_ape_fighter.value            : 0x649c9c,
        Loc.shop_mesal_gear_solid.value             : 0x649c9d,

        Loc.weird_photos_1.value                : 0x649c52,
        Loc.weird_photos_2.value                : 0x649c53,
        Loc.weird_photos_3.value                : 0x649c54,
        Loc.weird_photos_4.value                : 0x649c55,
        Loc.weird_photos_5.value                : 0x649c56,
        Loc.weird_photos_6.value                : 0x649c57,
        Loc.weird_photos_7.value                : 0x649c58,
        Loc.weird_photos_8.value                : 0x649c59,
        Loc.weird_photos_9.value                : 0x649c5a,
        Loc.weird_photos_10.value               : 0x649c5b,
        Loc.weird_photos_11.value               : 0x649c5c,
        Loc.weird_photos_12.value               : 0x649c5d,
        Loc.weird_photos_13.value               : 0x649c5e,
        Loc.weird_photos_14.value               : 0x649c5f,
        Loc.weird_photos_15.value               : 0x649c60,
        Loc.weird_photos_16.value               : 0x649c61,
        Loc.weird_photos_17.value               : 0x649c62,
        Loc.weird_photos_18.value               : 0x649c63,
        Loc.weird_photos_19.value               : 0x649c64,
        Loc.weird_photos_20.value               : 0x649c65,

        Loc.secret_photos_1.value               : 0x649c66,
        Loc.secret_photos_2.value               : 0x649c67,
        Loc.secret_photos_3.value               : 0x649c68,
        Loc.secret_photos_4.value               : 0x649c69,
        Loc.secret_photos_5.value               : 0x649c6a,
        Loc.secret_photos_6.value               : 0x649c6b,
        Loc.secret_photos_7.value               : 0x649c6c,
        Loc.secret_photos_8.value               : 0x649c6d,
        Loc.secret_photos_9.value               : 0x649c6e,
        Loc.secret_photos_10.value              : 0x649c6f,
        Loc.secret_photos_11.value              : 0x649c70,
        Loc.secret_photos_12.value              : 0x649c71,
        Loc.secret_photos_13.value              : 0x649c72,
        Loc.secret_photos_14.value              : 0x649c73,
        Loc.secret_photos_15.value              : 0x649c74,
        Loc.secret_photos_16.value              : 0x649c75,
        Loc.secret_photos_17.value              : 0x649c76,
        Loc.secret_photos_18.value              : 0x649c77,
        Loc.secret_photos_19.value              : 0x649c78,
        Loc.secret_photos_20.value              : 0x649c79,
        Loc.secret_photos_21.value              : 0x649c7a,
        Loc.secret_photos_22.value              : 0x649c7b,
        Loc.secret_photos_23.value              : 0x649c7c,
        Loc.secret_photos_24.value              : 0x649c7d,
        Loc.secret_photos_25.value              : 0x649c7e,
        Loc.secret_photos_26.value              : 0x649c7f,
        Loc.secret_photos_27.value              : 0x649c80,
        Loc.secret_photos_28.value              : 0x649c81,
        Loc.secret_photos_29.value              : 0x649c82,
        Loc.secret_photos_30.value              : 0x649c83,

        Loc.concept_art_1.value                 : 0x649c34,
        Loc.concept_art_2.value                 : 0x649c35,
        Loc.concept_art_3.value                 : 0x649c36,
        Loc.concept_art_4.value                 : 0x649c37,
        Loc.concept_art_5.value                 : 0x649c38,
        Loc.concept_art_6.value                 : 0x649c39,
        Loc.concept_art_7.value                 : 0x649c3a,
        Loc.concept_art_8.value                 : 0x649c3b,
        Loc.concept_art_9.value                 : 0x649c3c,
        Loc.concept_art_10.value                : 0x649c3d,
        Loc.concept_art_11.value                : 0x649c3e,
        Loc.concept_art_12.value                : 0x649c3f,
        Loc.concept_art_13.value                : 0x649c40,
        Loc.concept_art_14.value                : 0x649c41,
        Loc.concept_art_15.value                : 0x649c42,
        Loc.concept_art_16.value                : 0x649c43,
        Loc.concept_art_17.value                : 0x649c44,
        Loc.concept_art_18.value                : 0x649c45,
        Loc.concept_art_19.value                : 0x649c46,
        Loc.concept_art_20.value                : 0x649c47,
        Loc.concept_art_21.value                : 0x649c48,
        Loc.concept_art_22.value                : 0x649c49,
        Loc.concept_art_23.value                : 0x649c4a,
        Loc.concept_art_24.value                : 0x649c4b,
        Loc.concept_art_25.value                : 0x649c4c,
        Loc.concept_art_26.value                : 0x649c4d,
        Loc.concept_art_27.value                : 0x649c4e,
        Loc.concept_art_28.value                : 0x649c4f,
        Loc.concept_art_29.value                : 0x649c50,
        Loc.concept_art_30.value                : 0x649c51,

        Loc.teleborg_cards_1.value              : 0x649c16,
        Loc.teleborg_cards_2.value              : 0x649c17,
        Loc.teleborg_cards_3.value              : 0x649c18,
        Loc.teleborg_cards_4.value              : 0x649c19,
        Loc.teleborg_cards_5.value              : 0x649c1a,
        Loc.teleborg_cards_6.value              : 0x649c1b,
        Loc.teleborg_cards_7.value              : 0x649c1c,
        Loc.teleborg_cards_8.value              : 0x649c1d,
        Loc.teleborg_cards_9.value              : 0x649c1e,
        Loc.teleborg_cards_10.value             : 0x649c1f,
        Loc.teleborg_cards_11.value             : 0x649c20,
        Loc.teleborg_cards_12.value             : 0x649c21,
        Loc.teleborg_cards_13.value             : 0x649c22,
        Loc.teleborg_cards_14.value             : 0x649c23,
        Loc.teleborg_cards_15.value             : 0x649c24,
        Loc.teleborg_cards_16.value             : 0x649c25,
        Loc.teleborg_cards_17.value             : 0x649c26,
        Loc.teleborg_cards_18.value             : 0x649c27,
        Loc.teleborg_cards_19.value             : 0x649c28,
        Loc.teleborg_cards_20.value             : 0x649c29,
        Loc.teleborg_cards_21.value             : 0x649c2a,
        Loc.teleborg_cards_22.value             : 0x649c2b,
        Loc.teleborg_cards_23.value             : 0x649c2c,
        Loc.teleborg_cards_24.value             : 0x649c2d,
        Loc.teleborg_cards_25.value             : 0x649c2e,
        Loc.teleborg_cards_26.value             : 0x649c2f,
        Loc.teleborg_cards_27.value             : 0x649c30,
        Loc.teleborg_cards_28.value             : 0x649c31,
        Loc.teleborg_cards_29.value             : 0x649c32,
        Loc.teleborg_cards_30.value             : 0x649c33,

        ## Music Shop
        Loc.movie_tape.value                    : 0xAE,
        Loc.music_disc.value                    : 0xCB,
        Loc.genie_dance_music.value             : 0xFD,

        Loc.movie_tape_1.value                  : 0x649cfb,
        Loc.movie_tape_2.value                  : 0x649cfc,
        Loc.movie_tape_3.value                  : 0x649cfd,
        Loc.movie_tape_4.value                  : 0x649cfe,
        Loc.movie_tape_5.value                  : 0x649cff,
        Loc.movie_tape_6.value                  : 0x649d00,
        Loc.movie_tape_7.value                  : 0x649d01,
        Loc.movie_tape_8.value                  : 0x649d02,
        Loc.movie_tape_9.value                  : 0x649d03,
        Loc.movie_tape_10.value                 : 0x649d04,
        Loc.movie_tape_11.value                 : 0x649d05,
        Loc.movie_tape_12.value                 : 0x649d06,
        Loc.movie_tape_13.value                 : 0x649d07,
        Loc.movie_tape_14.value                 : 0x649d08,
        Loc.movie_tape_15.value                 : 0x649d09,
        Loc.movie_tape_16.value                 : 0x649d0a,
        Loc.movie_tape_17.value                 : 0x649d0b,
        Loc.movie_tape_18.value                 : 0x649d0c,
        Loc.movie_tape_19.value                 : 0x649d0d,
        Loc.movie_tape_20.value                 : 0x649d0e,
        Loc.movie_tape_21.value                 : 0x649d0f,
        Loc.movie_tape_22.value                 : 0x649d10,
        Loc.movie_tape_23.value                 : 0x649d11,
        Loc.movie_tape_24.value                 : 0x649d12,
        Loc.movie_tape_25.value                 : 0x649d13,
        Loc.movie_tape_26.value                 : 0x649d14,
        Loc.movie_tape_27.value                 : 0x649d15,
        Loc.movie_tape_28.value                 : 0x649d16,
        Loc.movie_tape_29.value                 : 0x649d17,

        Loc.music_disc_1.value                  : 0x649cc6,
        Loc.music_disc_2.value                  : 0x649cc7,
        Loc.music_disc_3.value                  : 0x649cc8,
        Loc.music_disc_4.value                  : 0x649cc9,
        Loc.music_disc_5.value                  : 0x649cca,
        Loc.music_disc_6.value                  : 0x649ccb,
        Loc.music_disc_7.value                  : 0x649ccc,
        Loc.music_disc_8.value                  : 0x649ccd,
        Loc.music_disc_9.value                  : 0x649cce,
        Loc.music_disc_10.value                 : 0x649ccf,
        Loc.music_disc_11.value                 : 0x649cd0,
        Loc.music_disc_12.value                 : 0x649cd1,
        Loc.music_disc_13.value                 : 0x649cd2,
        Loc.music_disc_14.value                 : 0x649cd3,
        Loc.music_disc_15.value                 : 0x649cd4,
        Loc.music_disc_16.value                 : 0x649cd5,
        Loc.music_disc_17.value                 : 0x649cd6,
        Loc.music_disc_18.value                 : 0x649cd7,
        Loc.music_disc_19.value                 : 0x649cd8,
        Loc.music_disc_20.value                 : 0x649cd9,
        Loc.music_disc_21.value                 : 0x649cda,
        Loc.music_disc_22.value                 : 0x649cdb,
        Loc.music_disc_23.value                 : 0x649cdc,
        Loc.music_disc_24.value                 : 0x649cdd,
        Loc.music_disc_25.value                 : 0x649cde,
        Loc.music_disc_26.value                 : 0x649cdf,
        Loc.music_disc_27.value                 : 0x649ce0,
        Loc.music_disc_28.value                 : 0x649ce1,
        Loc.music_disc_29.value                 : 0x649ce2,
        Loc.music_disc_30.value                 : 0x649ce3,
        Loc.music_disc_31.value                 : 0x649ce4,
        Loc.music_disc_32.value                 : 0x649ce5,
        Loc.music_disc_33.value                 : 0x649ce6,
        Loc.music_disc_34.value                 : 0x649ce7,
        Loc.music_disc_35.value                 : 0x649ce8,
        Loc.music_disc_36.value                 : 0x649ce9,
        Loc.music_disc_37.value                 : 0x649cea,
        Loc.music_disc_38.value                 : 0x649ceb,
        Loc.music_disc_39.value                 : 0x649cec,
        Loc.music_disc_40.value                 : 0x649ced,
        Loc.music_disc_41.value                 : 0x649cee,
        Loc.music_disc_42.value                 : 0x649cef,
        Loc.music_disc_43.value                 : 0x649cf0,
        Loc.music_disc_44.value                 : 0x649cf1,
        Loc.music_disc_45.value                 : 0x649cf2,
        Loc.music_disc_46.value                 : 0x649cf3,
        Loc.music_disc_47.value                 : 0x649cf4,
        Loc.music_disc_48.value                 : 0x649cf5,
        Loc.music_disc_49.value                 : 0x649cf6,
        Loc.music_disc_50.value                 : 0x649cf7,

        Loc.genie_dance_music_blues.value       : 0x649cf8,
        Loc.genie_dance_music_slowdance.value   : 0x649cf9,
        Loc.genie_dance_music_waltz.value       : 0x649cfa,
    }

    GameStates: Dict[str, int] = {
        # Status
        Game.state.value                : 0x8519e4,     # int32 (0x00 - 0x04)
        Game.character.value            : 0x649910,     # int32 (0x00 - 0x01)
        Game.progress.value             : 0x73f810,     # Pointer Lead - End Value is 64bit
        Game.current_morph.value        : 0x64991c,
        Game.on_warp_gate.value         : 0x698298,     # boolean (0x00 - 0x01)
        Game.channels_unlocked.value    : 0x73ff2c,     # int32 (0x00 - 0x1B)
        Game.channel_selected.value     : 0x73ff28,     # int32 (0x00 - 0x1B)
        Game.channel_confirmed.value    : 0x73FF3c,     # boolean (0x00 - 0x01)
        Game.current_channel.value      : 0x8519f0,
        Game.current_stage.value        : 0x649548,     # String
        Game.current_room.value         : 0x6478f0,

        Game.screen_fade.value          : 0xce6024,     # 0x01 when not fading
        Game.screen_fade_count.value    : 0x851a50,     # 0x01 when not fading

        # HUD
        Game.gui_status.value           : 0x73a054,
        Game.hud_pointer.value          : 0x691fe8,

        # Controller
        Game.pressed.value              : 0x699D40,

        # Stats
        Game.morph_duration.value       : 0x0152cf10,
        Game.duration_knight_b.value    : 0x0152cf10,
        Game.duration_cowboy_b.value    : 0x0152d030,
        Game.duration_ninja_b.value     : 0x0152d150,
        Game.duration_genie_b.value     : 0x0152d270,
        Game.duration_kungfu_b.value    : 0x0152d390,
        Game.duration_hero_b.value      : 0x0152d4b0,
        Game.duration_ape_b.value       : 0x0152D5D0,

        Game.duration_knight_g.value    : 0x0152cf70,
        Game.duration_cowboy_g.value    : 0x0152d090,
        Game.duration_ninja_g.value     : 0x0152d1b0,
        Game.duration_genie_g.value     : 0x0152d2d0,
        Game.duration_kungfu_g.value    : 0x0152d3f0,
        Game.duration_hero_g.value      : 0x0152d510,
        Game.duration_ape_g.value       : 0x0152D610,

        # Resources
        Game.nothing.value              : 0x200000,  # Arbitrary Number

        Game.jackets.value              : 0x649914,
        Game.cookies.value              : 0x649918,
        Game.chips.value                : 0x6499d4,
        Game.morph_gauge_active.value   : 0x742014,  # Pointer Lead
        Game.morph_gauge_recharge.value : 0x649924,
        Game.morph_stocks.value         : 0x649928,  # float (0000C842 - 00808944)
        Game.ammo_boom.value            : 0x649998,  # int32
        Game.ammo_homing.value          : 0x64999c,  # int32

        # Equipment
        Game.equip_circle.value         : 0x64997c,
        Game.equip_cross.value          : 0x649980,
        Game.equip_square.value         : 0x649984,
        Game.equip_triangle.value       : 0x649988,
        Game.equip_active.value         : 0x64998c,
        Game.equip_current.value        : 0x647bd0,
        Game.equip_pellet_active.value  : 0x649990,
        Game.equip_chassis_active.value : 0x6499ac,
        Game.equip_quick_morph.value    : 0x7954b0,
        Game.equip_morph_target.value   : 0x692018,

        # Special States
        Game.in_pink_stage.value        : 0x8519e0,

        Game.interact_data.value        : 0x7720d4,
        Game.status_tracker.value       : 0x73f820,
        Game.data_desk.value            : 0x77,
        Game.pipo_camera.value          : -0x80,    # Offset from Interact Data Pointer
        Game.cellphone.value            : -0x355,   # Offset from Interact Data Pointer
        Game.cellphone2.value           : 0x1CB,   # Offset from Interact Data Pointer
        Game.game_mode.value            : 0x73FF38,
        Game.net_status.value           : 0x04,
        Game.club_status.value          : 0x08,

        # Commands
        Game.command.value              : 0x772030,
        Game.area_dest.value            : 0x772050,
        Game.spawn.value                : 0x772070,

        # Persistence
        Game.last_cookies.value         : 0x649994,
        Game.last_morph_energy.value    : 0x649995,
        Game.last_morph_stock.value     : 0x649996,
        Game.shop_morph_stock.value     : 0x649997,

        # Archipelago
        Game.last_item_index.value      : 0x6499C4
    }

    ### [< --- POINTER CHAINS --- >]
    Pointers: Dict[str, Sequence[int]] = {
        Game.progress.value             : [0x04, 0x1A0, 0x20, 0x0],
        Game.channel_next_choice.value  : [0x04, 0x1A0, 0xB0, 0x0],
        Game.morph_gauge_active.value   : [0x44, 0x24, 0x38, 0x18],
        Game.equip_current.value        : [0x58, 0x44, 0x24, 0x38, 0x10],

        Game.hud_pointer.value          : [0x0],

        Loc.boss_tomoki.value           : [0x2c, 0x1AC4],

        Game.interact_data.value        : [0x0],
        Game.game_mode.value            : [0x0, 0x78, 0x20, 0x0],
        Game.save.value                 : [0x77],
    }

def get_version_addresses(game_id : str) -> VersionAddresses | None:
    if game_id not in Meta.supported_versions:
        return None

    id_index : int = Meta.supported_versions.index(game_id)

    if id_index == 0:
        return NTSCU()

    return None