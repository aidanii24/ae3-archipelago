from typing import Dict, Sequence
from abc import ABC

from .Strings import Itm, Loc, Game, Meta, APHelper


### [< --- HELPERS --- >]
class VersionAddresses(ABC):
    """Base Class to access easily change target memory addresses depending on Game Version used"""
    Items : Dict[str, int]
    Locations : Dict[str, int]
    GameStates : Dict[str, int]
    Pointers : Dict[int, Sequence[int]]

    GADGETS : Sequence[int]
    BUTTONS_BY_INTERNAL : Sequence[int]
    BUTTONS_BY_INTUIT : Sequence[int]

    def __init__(self):
        self._do_init()

    def _do_init(self):
        if not self.Items and not self.GameStates:
            return

        gadgets: list[int] = []
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

        # Last 3 items are RC Car variants, so return thr RC Car Address for them
        return self.GADGETS.index(self.Items[Itm.gadget_rcc.value])

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
        Itm.chassis_twin.value      : 0x649c98,  # boolean (0x00 - 0x01)
        Itm.chassis_black.value     : 0x649c99,  # boolean (0x00 - 0x01)
        Itm.chassis_pudding.value   : 0x649c9a,  # boolean (0x00 - 0x01)
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
        Loc.boss_monkey_white.value         : 0x649b40,

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
        Loc.western_gaukichi.value               : 0x649b7b,
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
    }

    GameStates: Dict[str, int] = {
        # Status
        Game.state.value                : 0x8519e4,  # int32 (0x00 - 0x04)
        Game.character.value            : 0x649910,  # int32 (0x00 - 0x01)
        Game.progress.value             : 0x73f810,  # Pointer Lead - End Value is 64bit
        Game.on_warp_gate.value         : 0x698298,  # boolean (0x00 - 0x01)
        Game.levels_unlocked.value      : 0x73ff2c,
        Game.level_confirmed.value      : 0x73FF3C,  # boolean (0x00 - 0x01)
        Game.current_stage.value        : 0x8519f0,

        # Resources
        Game.nothing.value               : 0x200000,  # Arbitrary Number

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
        Game.equip_pellet_active.value  : 0x649990,
        Game.equip_chassis_active.value : 0x6499ac,
        Game.equip_quick_morph.value    : 0x7954b0,
        Game.equip_morph_target.value   : 0x692018,
    }

    ### [< --- POINTER CHAINS --- >]
    Pointers: Dict[int, Sequence[int]] = {
        GameStates[Game.progress.value]             : [0x04, 0x1A0, 0x20, 0x0],
        GameStates[Game.morph_gauge_active.value]   : [0x44, 0x24, 0x38, 0x18]
    }

AP : dict[str, int] = {
    APHelper.channel_key.value      : 0x100,
    APHelper.victory.value          : 0x500
}

def get_version_addresses(game_id : str) -> VersionAddresses | None:
    if game_id not in Meta.supported_versions:
        return None

    id_index : int = Meta.supported_versions.index(game_id)

    if id_index == 0:
        return NTSCU()



