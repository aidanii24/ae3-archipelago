from dataclasses import dataclass

from Options import Toggle, Choice, PerGameCommonOptions, DeathLink

# Item Options
class GameMode(Choice):
    """
    Choose how the progression of the randomizer should be.

    > Singles - Each Stage will be unlocked one by one, as long as you find the Channel Key.
    > Boss - Alternate between unlocking groups of stages and the bosses in between.
    > Boss_Inclusive - Progression is similar to Boss, but the bosses are unlocked along with their preceding stages.
    """
    display_name : str = "Game Mode"
    default = 1

    option_singles : int = 0
    option_boss : int = 1
    option_boss_inclusive : int = 2

class StartingGadget(Choice):
    """
    Choose a Gadget to start the game with along with the Monkey Net. Choose None if you want to start with
    only the Monkey Net.
    """
    display_name : str = "Starting Gadget"
    default = 1

    option_none : int = 0
    option_stun_club : int = 1
    option_monkey_radar : int = 2
    option_super_hoop : int = 3
    option_slingback_shooter : int = 4
    option_water_net : int = 5
    option_rc_car : int = 6
    option_sky_flyer : int = 7

class BaseMorphDuration(Choice):
    """
    Choose the base duration of morphs. This does not affect recharge durations.
    """
    display_name : str = "Base Morph Duration"
    default = 30

    option_10s : int = 10
    option_15s : int = 15
    option_30s : int = 30
    option_40s : int = 40
    option_60s : int = 60

class ShuffleMonkeyNet(Toggle):
    """
    Choose if the Monkey Net should also be shuffled. This will skip the tutorial level immediately.
    """
    display_name : str = "Shuffle Monkey Net"

class ShuffleRCCarChassis(Toggle):
    """
    Choose if the various RC Car Chassis should also be included in the pool. Unlocking any chassis will
    automatically unlock the RC Car Gadget if it hasn't yet.
    """
    display_name : str = "Shuffle RC Car Chassis"

class ShuffleMorphStocks(Toggle):
    """
    Choose if Morph Stocks should also be included in the pool.
    """
    display_name : str = "Shuffle Morph Stocks"

class AddMorphExtensions(Toggle):
    """
    Choose if Morph Extensions should also be included in the pool. Each Morph Extension adds 2 seconds to your morph
    duration, up to a maximum of an additional 20 seconds added to your base morph duration.
    """
    display_name : str = "Add Morph Extensions"

class EnableShoppingArea(Toggle):
    """
    Choose if the Shopping Area should be able to sell (relevant) items.
    """
    display_name : str = "Enable Shopping Area"

# QoL/Bonus Options
class AutoEquipOnUnlock(Toggle):
    """
    Choose if Gadgets should be automatically equipped on unset buttons when unlocked.
    """
    display_name : str = "Auto Equip Gadgets when obtained"

@dataclass
class AE3Options(PerGameCommonOptions):
    game_mode               : GameMode

    starting_gadget         : StartingGadget
    base_morph_duration     : BaseMorphDuration
    shuffle_chassis         : ShuffleRCCarChassis
    shuffle_morph_stocks    : ShuffleMorphStocks
    add_morph_extensions    : AddMorphExtensions

    auto_equip              : AutoEquipOnUnlock

    death_link              : DeathLink