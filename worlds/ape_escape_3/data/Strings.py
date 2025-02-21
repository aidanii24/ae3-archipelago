from enum import Enum

class ae3_items(Enum):
    # Gadgets
    stun_club : "Stun Club"
    monkey_net : "Monkey Net"
    monkey_radar : "Monkey_Radar"
    super_hoop : "Super Hoop"
    slingback_shooter : "Slingback Shooter"
    water_net : "Water Net"
    rc_car : "RC Car"
    sky_flyer : "Sky Flyer"

    # Morphs
    morph_knight : "Fantasy Knight"
    morph_cowboy : "Wild West Kid"
    morph_ninja : "Miracle Ninja"
    morph_magician : "Genie Dancer"
    morph_kungfu : "Dragon Kung Fu Fighter"
    morph_hero : "Cyber Ace"
    morph_monkey : "Super Monkey"

    # Accessories
    acc_morph_stock : "Morph Stock"

    pellet_explosive : "Explosive Pellet"
    pellet_guided : "Guided Pellet"

    chassis_twin : "Twin's Chassis"
    chassis_black : "Black Chassis"
    chassis_pudding : "Pudding Chassis"

class ae3_locations(Enum):
    # Monkeys

    ## TV Station/Zero
    zero_ukki_pan : "Ukki Pan - TV Station"

    ## Seaside Resort
    seaside_nessal : "Nessal - Seaside Resort"
    seaside_ukki_pia : "Ukki Pia - Seaside Resort"
    seaside_sarubo : "Sarubo - Seaside Resort"
    seaside_salurin : "Salurin - Seaside Resort"
    seaside_ukkitan : "Ukkitan - Seaside Resort"
    seaside_morella : "Morella - Seaside Resort"
    seaside_ukki_ben : "Ukki Ben - Seaside Resort"
    seaside_break_kankichi : "Kankichi - Seaside Resort"
    seaside_break_tomezo : "Tomezo - Seaside Resort"
    seaside_break_kamayan : "Kamayan - Seaside Resort"
    seaside_break_taizo : "Taizo - Seaside Resort"

class ae3_stages(Enum):
    # Menu/Hub
    title_screen : "Menu"
    char_select : "Character Select"
    travel_station_a : "TV Station"
    travel_station_b : "Shopping District"

    # Channels
    zero : "TV Station (Stage)"
    seaside : "Seaside Resort"