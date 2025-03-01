from .Strings import AE3Locations

class Address:
    """
    Container for all the relevant memory addresses in Ape Escape 3.

    Attributes:
        items : Item Strings of the Game
        locations : Location Strings of the Game
        player : Strings related to status and resources of the player
    """
    items = {
        # <!> Values are on/off between 0x01 and 0x02 respectively unless commented otherwise.

        # Gadgets
        "stun_club"                 : 0x649950,
        "monkey_net"                : 0x649954,
        "monkey_radar"              : 0x649958,
        "super_hoop"                : 0x64995c,
        "slingback_shooter"         : 0x649960,
        "water_net"                 : 0x649978,
        "rc_car"                    : 0x649964,
        "sky_flyer"                 : 0x649968,

        # Morphs
        "morph_knight"              : 0x649930,
        "morph_cowboy"              : 0x649934,
        "morph_ninja"               : 0x649938,
        "morph_magician"            : 0x64993c,
        "morph_kungfu"              : 0x649940,
        "morph_hero"                : 0x649944,
        "morph_monkey"              : 0x649948,

        # Accessories
        "acc_morph_stock"           : 0x649928,     # float (0000C842 - 00808944)

        "pellet_explosive"          : 0x649998,     # int32
        "pellet_guided"             : 0x64999c,     # int32

        "chassis_twin"              : 0x649c98,     # boolean (0x00 - 0x01)
        "chassis_black"             : 0x649c99,     # boolean (0x00 - 0x01)
        "chassis_pudding"           : 0x649c9a,     # boolean (0x00 - 0x01)
    }

    locations = {
        # Monkeys
        # <!> Values are on/off between 0x00 and 0x01 respectively unless commented otherwise.

        ## TV Station/Zero
        AE3Locations.zero_ukki_pan.value                    : 0x649b4e,

        ## Seaside Resort
        AE3Locations.seaside_nessal.value                   : 0x6499dd,
        AE3Locations.seaside_ukki_pia.value                 : 0x6499de,
        AE3Locations.seaside_sarubo.value                   : 0x6499df,
        AE3Locations.seaside_salurin.value                  : 0x6499e0,
        AE3Locations.seaside_ukkitan.value                  : 0x649b4f,
        AE3Locations.seaside_morella.value                  : 0x649b99,
        AE3Locations.seaside_ukki_ben.value                 : 0x6499e1,

        AE3Locations.seaside_break_kankichi.value           : 0x649b5e,
        AE3Locations.seaside_break_tomezo.value             : 0x649b5f,
        AE3Locations.seaside_break_kamayan.value            : 0x649b60,
        AE3Locations.seaside_break_taizo.value              : 0x649b61
    }

    player = {
        # Status
        "state"                     : 0x8519e4,             # int32 (0x00 - 0x04)
        "character"                 : 0x649910,             # int32 (0x00 - 0x01)
        "lives"                     : 0x649914,
        "cookies"                   : 0x649918,
        "status_morph_recharge"     : 0x649924,

        # Equipment
        "equip_circle"              : 0x64997c,
        "equip_cross"               : 0x649980,
        "equip_square"              : 0x649984,
        "equip_triangle"            : 0x649988,
        "equip_active"              : 0x64998c,
        "equip_pellet_active"       : 0x649990,
        "equip_chassis_active"      : 0x6499ac,
        "equip_morph_quick"         : 0x7954b0,
        "equip_morph_target"        : 0x692018,
    }