from dataclasses import dataclass

from Options import Toggle, Choice, PerGameCommonOptions

# Item Options
class ProgressionType(Choice):
    """
    Choose how the progression of the randomizer should be.

    > Singles - Each Stage will be unlocked one by one, as long as you find the Channel Key. (Not Implemented)
    > Boss - Stages between bosses are all unlocked together. Finding a Channel Key in them will lead to their
    following boss stage being unlocked. After beating the boss, the next set of stages are unlocked.
    > Boss_Inclusive - Progression is similar to Boss, but the bosses are unlocked along with their preceding stages.
    Finding a Channel Key will simply unlock the next set of Stages. (Not Implemented)
    """
    display_name : str = "Progression Type"
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
    option_water_net = 5
    option_rc_car = 6
    option_sky_flyer = 7

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
    display_name : str = "Include RC Car Chassis in Randomizer"

# QoL/Bonus Options
class AutoEquipOnUnlock(Toggle):
    """
    Choose if Gadgets should be automatically equipped on unset buttons when unlocked.
    """
    display_name : str = "Auto Equip Gadgets when obtained"

@dataclass
class AE3Options(PerGameCommonOptions):
    progression_type : ProgressionType

    starting_gadget : StartingGadget
    shuffle_chassis : ShuffleRCCarChassis

    auto_equip : AutoEquipOnUnlock