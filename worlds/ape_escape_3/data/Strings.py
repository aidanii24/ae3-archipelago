from enum import Enum, EnumMeta
from typing import Sequence


### [< --- HELPERS --- >]
class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False

        return True

class BaseEnum(Enum, metaclass=MetaEnum):
    pass

### [< --- STRING TABLES--- >]
class Itm(BaseEnum):
    """
    Strings for all the Items of Ape Escape 3. This includes Gadgets, Morphs and select items
    from the Shopping district
    """

    # Gadgets
    gadget_club =       "Stun Club"
    gadget_net =        "Monkey Net"
    gadget_radar =      "Monkey Radar"
    gadget_hoop =       "Super Hoop"
    gadget_sling =      "Slingback Shooter"
    gadget_swim =       "Water Net"
    gadget_rcc =        "RC Car"
    gadget_fly =        "Sky Flyer"

    # Morphs
    morph_knight =      "Fantasy Knight"
    morph_cowboy =      "Wild West Kid"
    morph_ninja =       "Miracle Ninja"
    morph_magician =    "Genie Dancer"
    morph_kungfu =      "Dragon Kung Fu Fighter"
    morph_hero =        "Cyber Ace"
    morph_monkey =      "Super Monkey"

    # Accessories
    chassis_twin =      "Twin's Chassis"
    chassis_black =     "Black Chassis"
    chassis_pudding =   "Pudding Chassis"

    # Collectables
    nothing =           "Nothing"
    jacket =            "Jacket"
    cookie =            "Cookies"
    cookie_giant =      "Giant Cookie"
    chip_1x =           "1 Coin"
    chip_5x =           "5 Coins"
    chip_10x =          "10 Coins"
    energy =            "Energy"
    energy_mega =       "Mega Energy"
    acc_morph_stock =   "Morph Stock"
    ammo_boom =         "Explosive Pellet"
    ammo_homing =       "Guided Pellet"

    @classmethod
    def get_gadgets_ordered(cls) -> Sequence[str]:
        return [cls.gadget_swim.value, cls.gadget_club.value, cls.gadget_net.value, cls.gadget_radar.value,
                cls.gadget_hoop.value, cls.gadget_sling.value, cls.gadget_rcc.value, cls.gadget_fly.value]

class Loc(BaseEnum):
    """
    Strings for all the Locations of Ape Escape 3. This includes Monkeys, Cellphones, Cameras, and Points of Interest.
    """

    # Monkeys
    ## TV Station/Zero
    zero_ukki_pan               = "Ukki Pan"

    ## Seaside Resort
    seaside_nessal              = "Nessal"
    seaside_ukki_pia            = "Ukki Pia"
    seaside_sarubo              = "Sarubo"
    seaside_salurin             = "Salurin"
    seaside_ukkitan             = "Ukkitan"
    seaside_morella             = "Morella"
    seaside_ukki_ben            = "Ukki Ben"
    seaside_kankichi            = "Kankichi"
    seaside_tomezo              = "Tomezo"
    seaside_kamayan             = "Kamayan"
    seaside_taizo               = "Taizo"

    ## Hide-n-Seek Forest
    woods_ukki_pon              = "Ukki Pon"
    woods_ukkian                = "Ukkian"
    woods_ukki_red               = "Ukki Red"
    woods_rosalin               = "Rosalin"
    woods_salubon               = "Salubon"
    woods_wolfmon               = "Wolfmon"
    woods_ukiko                 = "Ukiko"
    woods_lambymon              = "Lambymon"
    woods_kreemon               = "Kreemon"
    woods_ukkilei               = "Ukkilei"
    woods_spork                 = "Spork"
    woods_king_goat             = "King Goat"
    woods_marukichi             = "Marukichi"
    woods_kikimon               = "Kikimon"
    woods_kominato              = "Kominato"

class Stage(BaseEnum):
    """Strings for the various stages of Ape Escape 3. This refers to the names of all the rooms in the game."""

    # Menu/Hub
    title_screen =              "Menu"
    char_select =               "Character Select"
    travel_station_a =          "TV Station"
    travel_station_b =          "Shopping District"

    # Channels
    zero =                      "TV Station (Stage)"

    seaside =                   "Seaside Resort"
    seaside_a =                 "Seaside Resort - Outside"
    seaside_b =                 "Seaside Resort - Chapel"
    seaside_c =                 "Seaside Resort - Break Room"

    woods =                     "Hide-n-Seek Forest"
    woods_a =                   "Hide-n-Seek Forest - Forest"
    woods_b =                   "Hide-n-Seek Forest - Hills"
    woods_c =                   "Hide-n-Seek Forest - Cabin"
    woods_d =                   "Hide-n-Seek Forest - Break Room"

class Game(BaseEnum):
    # Player
    state =                 "Player State"
    character =             "Character"
    progress =              "Progress"
    levels_unlocked =       "Levels Unlocked"
    on_warp_gate =          "On Warp Gate"
    level_confirmed =       "Level Confirmed"
    current_stage =         "Current Stage"

    # Resources
    jackets =               "Jackets"
    cookies =               "Cookies"
    chips =                 "Coins"
    morph_energy =          "Morph Energy"
    morph_gauge_active =    "Morph Gauge (Active)"
    morph_gauge_recharge =  "Morph Gauge (Recharge)"
    morph_stocks =          "Morph Stocks"
    ammo_boom =             "Explosive Pellets"
    ammo_homing =           "Guided Pellets"

    nothing =               "Nothing"

    # Equipment
    equip_circle =          "Gadget on Circle Button"
    equip_cross =           "Gadget on Cross Button"
    equip_square =          "Gadget on Square Button"
    equip_triangle =        "Gadget on Triangle Button"
    equip_active =          "Gadget in Current Use"
    equip_pellet_active =   "Pellet Selected"
    equip_chassis_active =  "RC Car Chassis Selected"
    equip_quick_morph =     "Quick Morph Selected"
    equip_morph_target =    "Selected Morph"

    @classmethod
    def get_buttons_by_internal_index(cls) -> Sequence[str]:
        return [cls.equip_circle.value, cls.equip_cross.value, cls.equip_square.value, cls.equip_triangle.value]

    @classmethod
    def get_buttons_by_intuitive_index(cls) -> Sequence[str]:
        return [cls.equip_triangle.value, cls.equip_cross.value, cls.equip_square.value, cls.equip_circle.value]

class Meta:
    game : str =                            "Ape Escape 3"
    platform : str =                        "PS2"
    supported_versions : Sequence[str] =    ["SCUS-97501"]  # NTSC-U, PAL, NTSC-J

class APHelper(BaseEnum):
    """
    Strings for all the Items created to assist with logic and progression for Archipelago with Ape Escape 3.
    """

    # Progression
    channel_key =           "Channel Key"
    victory =               "Victory"

    # Special
    hlp_morph_ext =         "Morph Gauge Extension"

    # Item Groups
    gadgets =               "Gadgets"
    morphs =                "Morphs"
    morphs_no_monkey =      "Morphs (Not Super Monkey)"
    equipment =             "Equipment"

    # Game Groups
    travel_station =        "o_1"

    round2 =                "round2"

    # AP Options
    progression_type =      "progression_type"

    starting_gadget =       "starting_gadget"
    shuffle_net =           "shuffle_net"
    shuffle_chassis =       "shuffle_chassis"

    auto_equip =            "auto_equip"

class APConsole:
    """
    Strings for all text to be used in the Archipelago Game Client
    """

    class Info(BaseEnum):
        sym_wait =      " [...]"
        sym_conf =      " [-/-]"
        decor =         "||==========================================||"
        greet =         " Welcome to Ape Escape 3 Archipelago!"
        game_name =     " Ape Escape 3 Archipelago"
        client_name =   " Ape Escape 3 Client"
        client_ver =    " Client v0.2a"
        world_ver =     " World v0.2a"

        p_init =        " [...] Starting PINE Interface. Connecting to PCSX2..."
        p_init_g =      " [...] Confirming Running Game..."
        p_init_s =      " [...] Connecting to an Archipelago Server..."
        p_init_sre =    " [...] Waiting for player to reconnect to server..."

        init =          " [-/-] Successfully connected to PCSX2"
        init_game =     " [-/-] Connected to Ape Escape 3!"

    class Err(BaseEnum):
        sym =           " [!!!]"

        sock_no =       " [!!!] Failed to find PCSX2. Make sure it is running and that PINE is enabled."
        sock_fail =     " [!!!] Failed to connect to PCSX2."
        sock_disc =     " [!!!] Lost connection to PCSX2."
        sock_re =       " Retrying to connect to PCSX2..."

        game_no =       " [!!!] PCSX2 is not running a game. Please run a supported version of Ape Escape 3"
        game_wrong =    " [!!!] PCSX2 is running, but the loaded game is different or is an unsupported version."
        conf_game =     " [!!!] Please load a supported version of Ape Escape 3."