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

    ## Castle
    castle_ukkido               = "Ukkido"
    castle_pipo_guard           = "Pipo Guard"
    castle_monderella           = "Monderella"
    castle_ukki_ichi            = "Ukki-ichi"
    castle_ukkinee              = "Ukkinee"
    castle_saru_mon             = "Saru-mon"
    castle_monga                = "Monga"
    castle_ukkiton              = "Ukkiton"
    castle_king_leo             = "King Leo"
    castle_ukkii                = "Ukkii"
    castle_saluto               = "Saluto"
    castle_kings_double         = "King's Double"
    castle_mattsun              = "Mattsun"
    castle_miya                 = "Miya"
    castle_mon_san              = "Mon San"
    castle_sal_1000             = "SAL-1000"

    ## Monkey White Battle!
    boss_monkey_white           = "Monkey White"

    ## The Big City
    ciscocity_ukima             = "Ukima"
    ciscocity_monbolo           = "Monbolo"
    ciscocity_pipo_mondy        = "Pipo Mondy"
    ciscocity_ukki_mattan       = "Ukki Mattan"
    ciscocity_bemucho           = "Bemucho"
    ciscocity_ukki_nader        = "Ukki Nader"
    ciscocity_sabu_sabu         = "Sabu-Sabu"
    ciscocity_ginjiro           = "Ginjiro"
    ciscocity_kichiemon         = "Kichiemon"
    ciscocity_ukkilun           = "Ukkilun"
    ciscocity_bully_mon         = "Bully-mon"
    ciscocity_ukki_joe          = "Ukki Joe"
    ciscocity_tamaki            = "Tamaki"
    ciscocity_mickey_oou        = "Mickey Oou"
    ciscocity_sally_kokoroe     = "Sally Kokoroe"
    ciscocity_monkey_manager    = "Monkey Manager"
    ciscocity_supervisor_chimp  = "Supervisor Chimp"
    ciscocity_boss_ape          = "Boss Ape"

    ## Specter TV Studio
    studio_ukki_yan             = "Ukki Yan"
    studio_ukkipuss             = "Ukkipuss"
    studio_minoh                = "Minoh"
    studio_monta                = "Monta"
    studio_pipopam              = "Pipopam"
    studio_monpii_ukkichi       = "Monpii Ukkichi"
    studio_gabimon              = "Gabimon"
    studio_bananamon            = "Bananamon"
    studio_mokinza              = "Mokinza"
    studio_ukki_lee_ukki        = "Ukki Lee Ukki"
    studio_ukkida_jiro          = "Ukkida Jiro"
    studio_sal_ukindo           = "Sal Ukindo"
    studio_gimminey             = "Gimminey"
    studio_hant                 = "Hant"
    studio_chippino             = "Chippino"
    studio_ukki_paul            = "Ukki Paul"
    studio_sally_mon            = "Sally Mon"
    studio_bonly                = "Bonly"
    studio_monly                = "Monly"

    ## Bootown
    halloween_monkichiro        = "Monkichiro"
    halloween_leomon            = "Leomon"
    halloween_uikkun            = "Uikkun"
    halloween_take_ukita        = "Take Ukita"
    halloween_bonbon            = "Bonbon"
    halloween_chichi            = "ChiChi"
    halloween_ukkisuke          = "Ukkisuke"
    halloween_chibi_sally       = "Chibi Sally"
    halloween_ukkison           = "Ukkison"
    halloween_saruhotep         = "Saruhotep"
    halloween_ukkito            = "Ukkito"
    halloween_monzally          = "Monzally"
    halloween_ukkiami           = "Ukkiami"
    halloween_monjan            = "Monjan"
    halloween_nattchan          = "Nattchan"
    halloween_kabochin          = "Kabochin"
    halloween_ukki_mon          = "Ukki Mon"
    halloween_mumpkin           = "Mumpkin"

    ## Wild West Town
    western_morrey              = "Morrey"
    western_jomi                = "Jomi"
    western_tammy               = "Tammy"
    western_ukki_gigolo         = "Ukki Gigolo"
    western_monboron            = "Monboron"
    western_west_ukki           = "West Ukki"
    western_lucky_woo           = "Lucky Woo"
    western_pamela              = "Pamela"
    western_ukki_monber         = "Ukki Monber"
    western_gaukichi             = "Gaukichi"
    western_shaluron            = "Shaluron"
    western_jay_mohn            = "Jay Mohn"
    western_munkee_joe          = "Monkee Joe"
    western_saru_chison         = "Saru Chison"
    western_jaja_jamo           = "Jaja Jamo"
    western_chammy_mo           = "Chammy Mo"
    western_golon_moe           = "Golon Moe"
    western_golozo              = "Golozo"
    western_ukkia_munbo         = "Ukkia Munbo"
    western_mon_johny           = "Mon Johny"

    boss_monkey_blue            = "Monkey Blue"

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

    castle =                    "Saru-mon's Castle"
    castle_a =                  "Saru-mon's Castle - Gates"
    castle_b =                  "Saru-mon's Castle - Courtyard"
    castle_c =                  "Saru-mon's Castle - Ballroom"
    castle_d =                  "Saru-mon's Castle - Dungeon"
    castle_e =                  "Saru-mon's Castle - Break Room"
    castle_f =                  "Saru-mon's Castle - Arena"

    boss1 =                     "Monkey White Battle!"

    ciscocity =                 "The Big City"
    ciscocity_a =               "The Big City - City"
    ciscocity_b =               "The Big City - Bank"
    ciscocity_c =               "The Big City - Theater"
    ciscocity_d =               "The Big City - Football Stadium"
    ciscocity_e =               "The Big City - Break Room"

    studio =                    "Specter TV Studio"
    studio_a =                  "Specter TV Studio - Reception"
    studio_a1 =                 "Specter TV Studio - Reception - Door to Buildings Set"
    studio_b =                  "Specter TV Studio - General Sets"
    studio_c =                  "Specter TV Studio - Moon Set"
    studio_d =                  "Specter TV Studio - Buildings Set"
    studio_e =                  "Specter TV Studio - Shopping Set"
    studio_f =                  "Specter TV Studio - Robot Set"
    studio_g =                  "Specter TV Studio - Break Room"

    halloween =                 "Bootown"
    halloween_a =               "Bootown - Carnival"
    halloween_a1 =              "Bootown - Carnival Canal"
    halloween_b =               "Bootown - Circus Tent"
    halloween_c1 =              "Bootown - Lake Pier"
    halloween_c =               "Bootown - Lake"
    halloween_d =               "Bootown - Mausoleum"
    halloween_e =               "Bootown - Break Room"
    halloween_f =               "Bootown - Park"

    western =                   "Wild West Town"
    western_a =                 "Wild West Town - Town"
    western_b =                 "Wild West Town - Tavern"
    western_c =                 "Wild West Town - Break Room"
    western_d =                 "Wild West Town - Train"
    western_e =                 "Wild West Town - Canyon"
    western_f =                 "Wild West Town - Train Station"

    boss2 =                     "Monkey Blue Battle!"

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

    # Environment
    shortcut_studio_ad =    "Shortcut to Specter TV Studio - Buildings Set"

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
        client_ver =    " Client v0.3a"
        world_ver =     " World v0.3b"

        p_check =       " [|?|] Confirming PCSX2 Status..."
        p_init =        " [...] Starting PINE Interface. Connecting to PCSX2..."
        p_init_g =      " [...] Confirming Running Game..."
        p_init_s =      " [...] Connecting to an Archipelago Server..."
        p_init_sre =    " [...] Waiting for player to reconnect to server..."

        init =          " [-/-] Successfully connected to PCSX2"
        init_game =     " [-/-] Connected to Ape Escape 3!"
        exit =          " [-/-] Disconnected from PCSX2."

    class Err(BaseEnum):
        sym =           " [!!!]"

        sock_no =       " [!!!] Failed to find PCSX2. Make sure it is running and that PINE is enabled."
        sock_fail =     " [!!!] Failed to connect to PCSX2."
        sock_disc =     " [!!!] Lost connection to PCSX2."
        sock_re =       " Retrying to connect to PCSX2..."

        game_no =       " [!!!] PCSX2 is not running a game. Please run a supported version of Ape Escape 3"
        game_wrong =    " [!!!] PCSX2 is running, but the loaded game is different or is an unsupported version."
        conf_game =     " [!!!] Please load a supported version of Ape Escape 3."

class Groups:
    STAGES_TITLE : Sequence[str] = [
        Stage.title_screen.value
    ]

    STAGES_SEASIDE : Sequence[str] = [
        Stage.seaside_a.value, Stage.seaside_b, Stage.seaside_c
    ]

    STAGES_WOODS : Sequence[str] = [
        Stage.woods_a.value, Stage.woods_b.value, Stage.woods_c.value, Stage.woods_d.value
    ]

    STAGES_CASTLE : Sequence[str] = [
        Stage.castle_a.value, Stage.castle_b.value, Stage.castle_c.value, Stage.castle_d.value, Stage.castle_e.value,
        Stage.castle_f.value
    ]

    STAGES_CISCOCITY : Sequence[str] = []
    STAGES_STUDIO : Sequence[str] = []
    STAGES_HALLOWEEN : Sequence[str] = []
    STAGES_WESTERN : Sequence[str] = []
    STAGES_BOSSES: Sequence[str] = []

    STAGES_MASTER : Sequence[str] = [
        *STAGES_SEASIDE, *STAGES_WOODS, *STAGES_CASTLE##, *STAGES_CISCOCITY, *STAGES_STUDIO,
        ##*STAGES_HALLOWEEN, *STAGES_WESTERN, *STAGES_BOSSES
    ]

    STAGES_INDEX : Sequence[Sequence[str]] = [
        STAGES_MASTER, STAGES_SEASIDE, STAGES_WOODS, STAGES_CASTLE##, STAGES_CISCOCITY, STAGES_STUDIO,
        ##STAGES_HALLOWEEN, STAGES_WESTERN, STAGES_BOSSES
    ]

