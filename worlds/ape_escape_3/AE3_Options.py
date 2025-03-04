from dataclasses import dataclass

from Options import Toggle, Choice, PerGameCommonOptions

# Item Options
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
    StartingGadget : StartingGadget
    ShuffleNet : ShuffleMonkeyNet
    ShuffleChassis : ShuffleRCCarChassis

    AutoEquip : AutoEquipOnUnlock