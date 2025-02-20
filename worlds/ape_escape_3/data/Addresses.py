class address:
    items = {
        # <!> Values are on/off between 0x01 and 0x02 respectively unless commented otherwise.

        # Gadgets
        "stun_club" : 0x649950,
        "monkey_net" : 0x649954,
        "monkey_radar" : 0x649958,
        "super_hoop" : 0x649960,
        "rc_car" : 0x649964,
        "sky_flyer" : 0x649968,
        "water_net" : 0x649978,

        # Morphs
        "morph_knight" : 0x649930,
        "morph_cowboy" : 0x649934,
        "morph_ninja" : 0x649938,
        "morph_magician" : 0x64993c,
        "morph_kungfu" : 0x649940,
        "morph_hero" : 0x649944,
        "morph_monkey" : 0x649948,

        # Accessories
        "acc_morph_stock" : 0x649928,   # float (0000C842 - 00808944)

        "pellet_explosive" : 0x649998,  # int32
        "pellet_guided" : 0x64999c,     # int32

        "chassis_twin" : 0x649c98,      # boolean (0x00 - 0x01)
        "chassis_black" : 0x649c99,     # boolean (0x00 - 0x01)
        "chassis_pudding" : 0x649c9a,   # boolean (0x00 - 0x01)
    }

    locations = {
        # Monkeys
        # <!> Values are on/off between 0x00 and 0x01 respectively unless commented otherwise.

        ## TV Station/Zero
        "zero_ukki_pan" : 0x649b4e,

        ## Seaside Resort
        "seaside_nessal" : 0x6499dd,
        "seaside_ukki_pia" : 0x6499de,
        "seaside_sarubo" : 0x6499df,
        "seaside_salurin" : 0x6499e0,
        "seaside_ukkitan" : 0x649b4f,
        "seaside_morella" : 0x649b99,
        "seaside_ukki_ben" : 0x6499e1,
        "seaside_break_kankichi" : 0x649b5e,
        "seaside_break_tomezo" : 0x649b5f,
        "seaside_break_kamayan" : 0x649b60,
        "seaside_break_taizo" : 0x649b61
    }

    player = {
        # Status
        "state" : 0x8519e4,             # int32 (0x00 - 0x04)
        "character" : 0x649910,         # int32 (0x00 - 0x01)
        "lives" : 0x649914,
        "cookies" : 0x649918,
        "status_morph_recharge" : 0x649924,

        # Equipment
        "equip_circle" : 0x64997c,
        "equip_cross" : 0x649980,
        "equip_square" : 0x649984,
        "equip_triangle" : 0x649988,
        "equip_active" : 0x64998c,
        "equip_pellet_active" : 0x649990,
        "equip_chassis_active" : 0x6499ac,
        "equip_morph_quick" : 0x7954b0,
        "equip_morph_target" : 0x692018,
    }