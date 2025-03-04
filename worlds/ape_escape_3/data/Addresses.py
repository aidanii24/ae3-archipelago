from typing import Dict, List, Sequence
from enum import Enum, IntEnum

from .Strings import Itm, Loc, Game


### [< --- ADDRESSES --- >]
class Items(IntEnum):
    """
    Contains all relevant Memory Addresses associated with Items in the game.
    """
    # <!> Values are on/off between 0x01 and 0x02 respectively unless commented otherwise.

    # Gadgets
    Itm.gadget_club.value =         0x649950,
    Itm.gadget_net.value =          0x649954,
    Itm.gadget_radar.value =        0x649958,
    Itm.gadget_hoop.value =         0x64995c,
    Itm.gadget_sling.value =        0x649960,
    Itm.gadget_rcc.value =          0x649964,
    Itm.gadget_fly.value =          0x649968,
    Itm.gadget_swim.value =         0x649978,

    # Morphs
    Itm.morph_knight.value =        0x649930,
    Itm.morph_cowboy.value =        0x649934,
    Itm.morph_ninja.value =         0x649938,
    Itm.morph_magician.value =      0x64993c,
    Itm.morph_kungfu.value =        0x649940,
    Itm.morph_hero.value =          0x649944,
    Itm.morph_monkey.value =        0x649948,

    # Accessories
    Itm.chassis_twin.value =        0x649c98,   # boolean (0x00 - 0x01)
    Itm.chassis_black.value =       0x649c99,   # boolean (0x00 - 0x01)
    Itm.chassis_pudding.value =     0x649c9a,   # boolean (0x00 - 0x01)

    # Collectables
    Itm.nothing.value =             0x200000,   # Arbitrary Number

class Locations(IntEnum):
    """Contains all relevant Memory Addresses associated with Locations in the game."""
    # Monkeys
    # <!> Values are on/off between 0x00 and 0x01 respectively unless commented otherwise.

    ## TV Station/Zero
    Loc.zero_ukki_pan.value =           0x649b4e,

    ## Seaside Resort
    Loc.seaside_nessal.value =          0x6499dd,
    Loc.seaside_ukki_pia.value =        0x6499de,
    Loc.seaside_sarubo.value =          0x6499df,
    Loc.seaside_salurin.value =         0x6499e0,
    Loc.seaside_ukkitan.value =         0x649b4f,
    Loc.seaside_morella.value =         0x649b99,
    Loc.seaside_ukki_ben.value =        0x6499e1,
    Loc.seaside_kankichi.value =        0x649b5e,
    Loc.seaside_tomezo.value =          0x649b5f,
    Loc.seaside_kamayan.value =         0x649b60,
    Loc.seaside_taizo.value =           0x649b61

class GameStates(IntEnum):
    """Contains all relevant Memory Addresses associated with the general game."""
    # Status
    Game.state.value =                      0x8519e4,  # int32 (0x00 - 0x04)
    Game.character.value =                  0x649910,  # int32 (0x00 - 0x01)

    # Resources
    Game.jackets.value =                    0x649914,
    Game.cookies.value =                    0x649918,
    Game.chips.value =                      0x6499d4,
    Game.morph_gauge_active.value =         0x742014,
    Game.morph_gauge_recharge.value =       0x649924,
    Game.morph_stocks.value =               0x649928,  # float (0000C842 - 00808944)
    Game.ammo_boom.value =                  0x649998,  # int32
    Game.ammo_homing.value =                0x64999c,  # int32

    # Equipment
    Game.equip_circle.value =               0x64997c,
    Game.equip_cross.value =                0x649980,
    Game.equip_square.value =               0x649984,
    Game.equip_triangle.value =             0x649988,
    Game.equip_active.value =               0x64998c,
    Game.equip_pellet_active.value =        0x649990,
    Game.equip_chassis_active.value =       0x6499ac,
    Game.equip_quick_morph.value =          0x7954b0,
    Game.equip_morph_target.value =         0x692018,

### [< --- POINTER CHAINS --- >]
Pointers : Dict[int, Sequence[int]] = {
    GameStates[Game.morph_gauge_active.value].value     : [0x44, 0x24, 0x38, 0x18]
}

### [< --- ADDRESS GROUPS --- >]
GADGET_INDEX : Sequence[int] = [
    Items[Itm.gadget_swim.value].value, Items[Itm.gadget_net.value].value, Items[Itm.gadget_club.value].value,
    Items[Itm.gadget_radar.value].value, Items[Itm.gadget_hoop.value].value, Items[Itm.gadget_sling.value].value,
    Items[Itm.gadget_rcc.value].value, Items[Itm.gadget_fly.value].value
]

MORPH_INDEX : Sequence[int] = [
    Items[Itm.morph_knight.value].value, Items[Itm.morph_cowboy.value].value, Items[Itm.morph_ninja.value].value,
    Items[Itm.morph_magician.value].value, Items[Itm.morph_kungfu.value].value, Items[Itm.morph_hero.value].value,
    Items[Itm.morph_monkey.value].value
]

BUTTON_INDEX : Sequence[int] = [
    GameStates[Game.equip_circle.value].value, GameStates[Game.equip_cross.value].value,
    GameStates[Game.equip_square.value].value, GameStates[Game.equip_triangle.value].value,
]

@DeprecationWarning
class Address:
    """
    Container for all the relevant memory addresses in Ape Escape 3.

    Attributes:
        itm : Item Strings of the Game
        loc : Location Strings of the Game
        game : Strings related to the overall game
    """
    itm : Dict[str : int | List[int] ]= {
        # <!> Values are on/off between 0x01 and 0x02 respectively unless commented otherwise.

        # Gadgets
        Itm.gadget_club.name            : 0x649950,
        Itm.gadget_net.name             : 0x649954,
        Itm.gadget_radar.name           : 0x649958,
        Itm.gadget_hoop.name            : 0x64995c,
        Itm.gadget_sling.name           : 0x649960,
        Itm.gadget_swim.name            : 0x649978,
        Itm.gadget_rcc.name             : 0x649964,
        Itm.gadget_fly.name             : 0x649968,

        # Morphs
        Itm.morph_knight.name           : 0x649930,
        Itm.morph_cowboy.name           : 0x649934,
        Itm.morph_ninja.name            : 0x649938,
        Itm.morph_magician.name         : 0x64993c,
        Itm.morph_kungfu.name           : 0x649940,
        Itm.morph_hero.name             : 0x649944,
        Itm.morph_monkey.name           : 0x649948,

        # Accessories
        Itm.chassis_twin.name           : 0x649c98, # boolean (0x00 - 0x01)
        Itm.chassis_black.name          : 0x649c99, # boolean (0x00 - 0x01)
        Itm.chassis_pudding.name        : 0x649c9a, # boolean (0x00 - 0x01)
    }

    loc = {
        # Monkeys
        # <!> Values are on/off between 0x00 and 0x01 respectively unless commented otherwise.

        ## TV Station/Zero
        Loc.zero_ukki_pan.name          : 0x649b4e,

        ## Seaside Resort
        Loc.seaside_nessal.name         : 0x6499dd,
        Loc.seaside_ukki_pia.name       : 0x6499de,
        Loc.seaside_sarubo.name         : 0x6499df,
        Loc.seaside_salurin.name        : 0x6499e0,
        Loc.seaside_ukkitan.name        : 0x649b4f,
        Loc.seaside_morella.name        : 0x649b99,
        Loc.seaside_ukki_ben.name       : 0x6499e1,
        Loc.seaside_kankichi.name       : 0x649b5e,
        Loc.seaside_tomezo.name         : 0x649b5f,
        Loc.seaside_kamayan.name        : 0x649b60,
        Loc.seaside_taizo.name          : 0x649b61
    }

    game = {
        # Status
        Game.state.name                     : 0x8519e4, # int32 (0x00 - 0x04)
        Game.character.name                 : 0x649910, # int32 (0x00 - 0x01)

        # Resources
        Game.jackets.name                   : 0x649914,
        Game.cookies.name                   : 0x649918,
        Game.morph_gauge_active.name        : 0x649920,
        Game.morph_gauge_recharge.name      : 0x649924,
        Itm.acc_morph_stock.name            : 0x649928,  # float (0000C842 - 00808944)
        Itm.ammo_boom.name                  : 0x649998,  # int32
        Itm.ammo_homing.name                : 0x64999c,  # int32

        # Equipment
        Game.equip_circle.name              : 0x64997c,
        Game.equip_cross.name               : 0x649980,
        Game.equip_square.name              : 0x649984,
        Game.equip_triangle.name            : 0x649988,
        Game.equip_active.name              : 0x64998c,
        Game.equip_pellet_active            : 0x649990,
        Game.equip_chassis_active           : 0x6499ac,
        Game.equip_quick_morph              : 0x7954b0,
        Game.equip_morph_target             : 0x692018,
    }