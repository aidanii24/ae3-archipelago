from typing import Dict, Sequence

from .Strings import Itm, Loc, Game


### [< --- ADDRESSES --- >]
Items : Dict[str, int] = {
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

        # Collectables
    Itm.nothing.value           : 0x200000,  # Arbitrary Number
}

Locations : Dict[str, int] = {
    # Monkeys
    # <!> Values are on/off between 0x00 and 0x01 respectively unless commented otherwise.

    ## TV Station/Zero
    Loc.zero_ukki_pan.value         : 0x649b4e,

    ## Seaside Resort
    Loc.seaside_nessal.value        : 0x6499dd,
    Loc.seaside_ukki_pia.value      : 0x6499de,
    Loc.seaside_sarubo.value        : 0x6499df,
    Loc.seaside_salurin.value       : 0x6499e0,
    Loc.seaside_ukkitan.value       : 0x649b4f,
    Loc.seaside_morella.value       : 0x649b99,
    Loc.seaside_ukki_ben.value      : 0x6499e1,
    Loc.seaside_kankichi.value      : 0x649b5e,
    Loc.seaside_tomezo.value        : 0x649b5f,
    Loc.seaside_kamayan.value       : 0x649b60,
    Loc.seaside_taizo.value         : 0x649b61
}

GameStates : Dict[str, int] = {
# Status
    Game.state.value                        : 0x8519e4,  # int32 (0x00 - 0x04)
    Game.character.value                    : 0x649910,  # int32 (0x00 - 0x01)

    # Resources
    Game.jackets.value                      : 0x649914,
    Game.cookies.value                      : 0x649918,
    Game.chips.value                        : 0x6499d4,
    Game.morph_gauge_active.value           : 0x742014,
    Game.morph_gauge_recharge.value         : 0x649924,
    Game.morph_stocks.value                 : 0x649928,  # float (0000C842 - 00808944)
    Game.ammo_boom.value                    : 0x649998,  # int32
    Game.ammo_homing.value                  : 0x64999c,  # int32

    # Equipment
    Game.equip_circle.value                 : 0x64997c,
    Game.equip_cross.value                  : 0x649980,
    Game.equip_square.value                 : 0x649984,
    Game.equip_triangle.value               : 0x649988,
    Game.equip_active.value                 : 0x64998c,
    Game.equip_pellet_active.value          : 0x649990,
    Game.equip_chassis_active.value         : 0x6499ac,
    Game.equip_quick_morph.value            : 0x7954b0,
    Game.equip_morph_target.value           : 0x692018,
}

### [< --- POINTER CHAINS --- >]
Pointers : Dict[int, Sequence[int]] = {
    GameStates[Game.morph_gauge_active.value]   : [0x44, 0x24, 0x38, 0x18]
}

### [< --- ADDRESS GROUPS --- >]
GADGET_INDEX : Sequence[int] = [
    Items[Itm.gadget_swim.value], Items[Itm.gadget_club.value], Items[Itm.gadget_net.value],
    Items[Itm.gadget_radar.value], Items[Itm.gadget_hoop.value], Items[Itm.gadget_sling.value],
    Items[Itm.gadget_rcc.value], Items[Itm.gadget_fly.value], Items[Itm.chassis_twin.value],
    Items[Itm.chassis_black.value], Items[Itm.chassis_pudding.value]
]

MORPH_INDEX : Sequence[int] = [
    Items[Itm.morph_knight.value], Items[Itm.morph_cowboy.value], Items[Itm.morph_ninja.value],
    Items[Itm.morph_magician.value], Items[Itm.morph_kungfu.value], Items[Itm.morph_hero.value],
    Items[Itm.morph_monkey.value]
]

BUTTON_INDEX : Sequence[int] = [
    GameStates[Game.equip_circle.value], GameStates[Game.equip_cross.value],
    GameStates[Game.equip_square.value], GameStates[Game.equip_triangle.value]
]

BUTTON_INTUIT_INDEX : Sequence[int] = [
    GameStates[Game.equip_triangle.value], GameStates[Game.equip_cross.value],
    GameStates[Game.equip_square.value], GameStates[Game.equip_circle.value]
]

### [< --- METHODS --- >]
def get_gadget_id(address : int):
    # Abort if Address is not in GADGET_INDEX
    if address not in GADGET_INDEX:
        return -1

    gadget_id : int = GADGET_INDEX.index(address)

    # Return immediately if Gadget is part of normal set (the first 7)
    if gadget_id <= 7:
        return gadget_id

    # Last 3 items are RC Car variants, so return thr RC Car Address for them
    return GADGET_INDEX.index(Items[Itm.gadget_rcc.value])