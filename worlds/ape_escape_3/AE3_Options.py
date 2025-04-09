from dataclasses import dataclass

from Options import OptionGroup, Toggle, DefaultOnToggle, Choice, PerGameCommonOptions, DeathLink
from worlds.ape_escape_3 import APHelper


class ProgressionMode(Choice):
    """
    Choose how the progression of the randomizer should be.
    Default: Boss

    > Singles - Each Stage will be unlocked one by one, as long as you find the Channel Key.
    > Boss - Alternate between unlocking groups of stages and the bosses in between.
    > Boss_Inclusive - Progression is similar to Boss, but the bosses are unlocked along with their preceding stages.
    """
    display_name : str = "Progression Mode"
    default = 1

    option_singles : int = 0
    option_boss : int = 1
    option_boss_inclusive : int = 2

class Monkeysanity(DefaultOnToggle):
    """
    Choose if Pipo Monkeys (and Dr. Tomoki) should count as Locations.
    Default: Enabled

    <!> WARNING <!>
    If this option is disabled, and other checks such as Camerasanity or Cellphonesanity are still also disabled,
    this option will be re-enabled.
    """
    visibility = False
    display_name : str = "Pipo Monkeysanity"

class Camerasanity(Choice):
    """
    Choose if Pipo Cameras should count as Locations.
    Default: Disabled

    > disabled : Pipo Cameras will not count as locations
    > enabled : Pipo Cameras will count as locations, and is counted when a Monkey Film is recorded.
    This means that the Pipo Monkey actors MUST BE PRESENT to acquire the item, or it will be missable until
    Free Play mode is unlocked for the channel upon clearing it.
    > no_actors : Pipo Cameras will count as locations, regardless if the Pipo Monkey Actors are present
    """
    display_name = "Pipo Camerasanity"
    default = 0

    option_disabled : int = 0
    option_enabled : int = 1
    option_no_actors : int = 2

class Cellphonesanity(Choice):
    """
    Choose if Cellphones should count as locations
    default: Disabled
    """
    display_name = "Cellphonesanity"

class StartingGadget(Choice):
    """
    Choose a Gadget to start the game with along with the Monkey Net. Choose None if you want to start with
    only the Monkey Net.
    Default: Stun Club (Vanilla)
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

class StartingMorph(Choice):
    """
    Choose a Morph to Start the game with.
    Default: None (Vanilla)
    """

    display_name : str = "Starting Morph"
    default = 0

    option_none : int = 0
    option_fantasy_knight : int = 1
    option_wild_west_kid : int = 2
    option_miracle_ninja : int = 3
    option_genie_dancer : int = 4
    option_dragon_kung_fu_fighter : int = 5
    option_cyber_ace : int = 6
    option_super_monkey : int = 7

class BaseMorphDuration(Choice):
    """
    Choose the base duration of morphs. This does not affect recharge durations.
    Default: 30s (Vanilla)
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
    Default: Disabled
    """
    visibility = False
    display_name : str = "Shuffle Monkey Net"

class ShuffleRCCarChassis(Toggle):
    """
    Choose if the various RC Car Chassis should also be included in the pool. Unlocking any chassis will
    automatically unlock the RC Car Gadget if it hasn't yet.
    Default: Disabled
    """
    display_name : str = "Shuffle RC Car Chassis"

class ShuffleMorphStocks(Toggle):
    """
    Choose if Morph Stocks should also be included in the pool.
    Default: Disabled
    """
    display_name : str = "Shuffle Morph Stocks"

class AddMorphExtensions(Toggle):
    """
    Choose if Morph Extensions should also be included in the pool. Each Morph Extension adds 2 seconds to your morph
    duration, up to a maximum of an additional 20 seconds added to your base morph duration.
    Default: Disabled
    """
    display_name : str = "Add Morph Extensions"

class EarlyFreePlay(Toggle):
    """
    Allows Free Play mode to be available without needing to fully clear a channel. Useful when wanting Camerasanity
    enabled without needing to worry about Pipo Monkey actors.
    default: Disabled.
    """
    display_name : str = "Early Free Play"

class EnableShoppingArea(DefaultOnToggle):
    """
    Choose if the Shopping Area should be able to sell (relevant) items.
    Default: Enabled
    """
    visibility = False
    display_name : str = "Enable Shopping Area"

# QoL/Bonus Options
class AutoEquipOnUnlock(Toggle):
    """
    Choose if Gadgets should be automatically equipped on unset buttons when unlocked.
    Default: Disabled
    """
    display_name : str = "Auto Equip Gadgets when obtained"

ae3_option_groups: dict[str, list[any]] = {
    "Randomizer Options"        : [ProgressionMode, Monkeysanity, Camerasanity, Cellphonesanity],
    "Item Options"              : [StartingGadget, StartingMorph, BaseMorphDuration, ShuffleMonkeyNet, ShuffleRCCarChassis,
                                    ShuffleMorphStocks, AddMorphExtensions],
    "Preferences"               : [EarlyFreePlay, EnableShoppingArea],
    "QoL Options"               : [AutoEquipOnUnlock],
    "Sync Options"              : [DeathLink]
}

@dataclass
class AE3Options(PerGameCommonOptions):
    progression_mode        : ProgressionMode
    monkeysanity            : Monkeysanity
    camerasanity            : Camerasanity
    cellphonesanity         : Cellphonesanity

    starting_gadget         : StartingGadget
    starting_morph          : StartingMorph
    base_morph_duration     : BaseMorphDuration

    shuffle_net             : ShuffleMonkeyNet
    shuffle_chassis         : ShuffleRCCarChassis
    shuffle_morph_stocks    : ShuffleMorphStocks
    add_morph_extensions    : AddMorphExtensions

    early_free_play         : EarlyFreePlay
    enable_shopping_area    : EnableShoppingArea

    auto_equip              : AutoEquipOnUnlock

    death_link              : DeathLink

def create_option_groups() -> list[OptionGroup]:
    groups : list[OptionGroup] = []
    for group, options in ae3_option_groups:
        groups.append(OptionGroup(group, options))

    return groups

def slot_data_options() -> list[str]:
    return [
        APHelper.progression_mode.value,
        APHelper.monkeysanity.value,
        APHelper.camerasanity.value,
        APHelper.cellphonesanity.value,

        APHelper.starting_gadget.value,
        APHelper.starting_morph.value,
        APHelper.base_morph_duration.value,

        APHelper.shuffle_net.value,
        APHelper.shuffle_chassis.value,
        APHelper.shuffle_morph_stocks.value,
        APHelper.add_morph_extensions.value,

        APHelper.early_free_play.value,
        APHelper.enable_shopping_area.value,

        APHelper.auto_equip.value,

        APHelper.death_link.value
    ]