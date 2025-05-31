from dataclasses import dataclass

from Options import OptionGroup, Toggle, DefaultOnToggle, Choice, PerGameCommonOptions, DeathLink, Visibility, \
    Range, OptionList
from .data.Strings import APHelper
from .data.Stages import LEVELS_BY_ORDER


class ProgressionMode(Choice):
    """
    Choose how the progression of the randomizer should be.
    Default: Group

    > Singles - Each Stage will be unlocked one by one, as long as you find the Channel Key.
    > Group - Alternate between unlocking groups of stages and the bosses in between.
    > World - Progression is similar to Boss, but the bosses are unlocked along with their preceding stages.
    > Quadruples - Each set of Levels will have 4 channels each!
    > Open* - All levels except the final two are immediately unlocked, but a certain number amount of keys is needed
    to access the next level. The default required is 10 Channel Keys.
    > Randomize* - How many levels are unlocked in a set is all up to chance!

    * These options can be customized with their respective options below.
    """
    display_name : str = "Progression Mode"
    default = 1

    option_singles : int = 0
    option_group : int = 1
    option_world : int = 2
    option_quadruples : int = 3
    option_open : int = 4
    option_randomize : int = 5

class OpenProgressionKeys(Range):
    """
    If the chosen Progression Mode is `open`, this option allows the amount of keys required to unlock the endgame
    channels to be customized. Use the same value for both Minimum and Maximum for an absolute value,
    or make them different to have generation randomly choose between them.
    """
    display_name : str = "Open Progression Mode Required Keys"
    default = 10

    range_start = 5
    range_end = 30

class RandomizeProgressionSetCount(Range):
    """
    If the chosen Progression mode is `randomize`, this option allows you to control the amount of channel sets
    that will be generated, and by extension, the minimum amount of keys to reach the end (but not post) game.
    Leave this at 0 to let generation decide for you, or specify a maximum or minimum value for more control.
    """
    display_name : str = "Randomize Progression Set Count"
    default = 0

    range_start = 0
    range_end = 28

class RandomizeProgressionChannelCount(OptionList):
    """
    If the chosen mode is `randomize`, this option allows you to control the amount of possible channels that can
    be included in a set. Leave this at default to let generation decide for you, or specify a maximum and minimum
    value for generation to use to randomize for each set.

    If a Set Count has been specified, it will be prioritized over this option,
    but generation will still attempt to respect this option as much as possible.

    Format: [min, max]
    Absolute Minimum : 1
    Absolute Maximum : 28
    """
    display_name : str = "Randomize Progression Channel Count"
    default = []

    def __init__(self, options: OptionList) -> None:
        super().__init__(options)

        if len(self.value) == 0:
            return

        if not any(isinstance(_, int) for _ in self.value):
            assert "AE3 > RandomizeProgressionChannelCount: One or more item(s) is not an integer."

        if len(self.value) < 1:
            assert "AE3 > RandomizeProgressionChannelCount: This option requires two integer items."

        # Treat as default if both values are 0
        if sum(self.value) == 0:
            self.value.clear()
            return

        # Truncate if needed
        if len(self.value) > 2:
            self.value = self.value[:2]

        self.value[0] = max(min(self.value[0], 28), 1)
        self.value[1] = 28 if self.value[1] == 0 else max(min(self.value[1], 28), self.value[0])

    def __bool__(self):
        return bool(self.value)

class LogicPreference(Choice):
    """
    Choose a certain logic preset that determines how difficult the game will be and how much expertise is asked from
    the player.
    Default: normal
    """
    display_name : str = "Logic Preference"
    default = 1

    option_casual : int = 0
    option_normal : int = 1
    option_hard : int = 2


class GoalTarget(Choice):
    """
    Choose what will count as winning the game.
    Default: specter

    > specter - Clear Specter's Battle (Vanilla End Game)
    > specter_final - Clear Specter's Final Battle (Vanilla Post Game)
    > triple_threat - Clear 3 Boss stages
    > play_spike - Capture 204 Monkeys
    > play_jimmy - Capture 300 Monkeys
    > directors_cut - Capture all 20 Monkey Films (This will FORCE set Camerasanity to 'enabled' if disabled)
    > phone_check - Activate all 53 Cellphones (this will FORCE enable Cellphonesanity)
    """
    display_name : str = "Goal Target"
    default = 0

    option_specter : int = 0
    option_specter_final : int = 1
    option_triple_threat : int = 2
    option_play_spike : int = 3
    option_play_jimmy : int = 4
    option_directors_cut : int = 5
    option_phone_check : int = 6
    # option_scavenger_hunt : int = 7


class PostGameAccessRule(Choice):
    """
    Choose how the final level post-game level should be unlocked. This is only relevant if the Goal Target requires
    this level.
    Default: vanilla

    > vanilla - Capture all base and break room monkeys (This will FORCE set Monkeysanity - Break Rooms to 'enabled',
    regardless of it the Goal ends up requiring access to Post Game or not)
    > active_monkeys - Capture all monkeys marked as locations
    > all_cameras - Capture all Monkey Films (This will FORCE set Camerasanity to 'enabled' if disabled)
    > all_cellphones - Activate all Cellphones (This will FORCE enable Cellhponesanity)
    > channel_key - Provide an extra channel key to unlock this level
    > after_end - The extra channel key will be placed on the penultimate boss (Specter in Vanilla Channel Order)
    """
    display_name : str = "Post-Game Condition"
    default = 0

    option_vanilla : int = 0
    option_active_monkeys : int = 1
    option_all_cameras : int = 2
    option_all_cellphones : int = 3
    option_channel_key : int = 4
    option_after_end : int = 5


class ShuffleChannel(Choice):
    """
    Choose if Channel Order should be randomized.
    Default: disabled

    > disabled - Channel Order will not be shuffled
    > type_shuffle - Normal channels will only be shuffled with other normal levels, same for boss channels.
    This preserves the slots of the bosses, but the order of the bosses themselves will still be shuffled.
    > full_shuffle - All channels will be shuffled regardless
    """
    display_name : str = "Shuffle Channels"
    default = 0

    option_disabled : int = 0
    option_type_shuffle : int = 1
    option_full_shuffle : int = 2


class PreserveChannel(Choice):
    """
    If Channel Order is not disabled, choose which channel should preserve their number.
    Default: none

    > none - No channel will be exempted from the Channel Shuffle
    > bosses - Bosses will not be shuffled
    > specters - Specter and Specter Final will not be shuffled
    > specter_final - Specter Final will not be shuffled
    """
    display_name : str = "Channel Shuffle Preserve"
    default = 0

    option_none : int = 0
    option_bosses : int = 1
    option_specters : int = 2
    option_specter_final : int = 3

class PushChannel(OptionList):
    """
    Specify which channels should be pushed to the End Game (Penultimate set of channels).

    By default, this will replace and swap the specified channels with the channels already present in the End Game,
    but this can be changed to add without swapping by specifying "ADDITIVE" anywhere into the list.

    Format: ["item_a", "item_b", "item_c", ..., (optional)"ADDITIVE"]
    """
    display_name : str = "Push Channel"
    default = []

    valid_keys = [*LEVELS_BY_ORDER]

class PostChannel(OptionList):
    """
    Specify which channels should be placed to the Post Game
    (Ultimate set of channels locked behind Post Game Condition).

    By default, this will replace and swap the specified channels with the channels already present in the Post Game,
    but this can be changed to add without swapping by specifying "ADDITIVE" anywhere into the list.

    Format: ["item_a", "item_b", "item_c", ..., (optional)"ADDITIVE"]
    """
    display_name : str = "Post Channel"
    default = []

    valid_keys = [*LEVELS_BY_ORDER]

class BlacklistChannel(OptionList):
    """
    Specify which channels whose locations should be excluded from generation, and then placed at the end of the
    channel order.

    Format: ["item_a", "item_b", "item_c", ...]
    """
    display_name : str = "Blacklist Channel"
    default = []

    valid_keys = [*LEVELS_BY_ORDER]


class Monkeysanity(DefaultOnToggle):
    """
    Choose if Pipo Monkeys (and Dr. Tomoki) should count as Locations.
    Default: Enabled

    <!> WARNING <!>
    If this option is disabled, and other checks such as Camerasanity or Cellphonesanity are still also disabled,
    this option will be re-enabled.
    """
    visibility = Visibility.none
    display_name : str = "Pipo Monkeysanity"


class MonkeysanityBreakRooms(Choice):
    """
    Choose if Break Room monkeys should count as locations, and if so, if the Super Monkey morph must first be
    obtained before the game allows them to spawn.
    Default: disabled

    > disabled - Break Room monkeys will not spawn
    > enabled - Break Room monkeys will spawn, but only when the Super Monkey morph is obtained
    > early - Break Room monkeys will spawn, regardless of if the player has obtained the Super Monkey morph
    """
    display_name : str = "Pipo Monkeysanity - Break Rooms"
    default = 0

    option_disabled : int = 0
    option_enabled : int = 1
    option_early : int = 2


class MonkeysanityPasswords(Choice):
    """
    Choose if Password monkeys should count as locations, and if so, how they should be unlocked.
    Default: disabled

    > disabled - Password monkeys will not spawn
    > enabled - Password monkeys will be unlocked from the start and spawn in their rooms.
    > hunt - Password monkeys will be unlocked when certain conditions are met, and only then will they spawn.
    """
    visibility = Visibility.none
    display_name: str = "Pipo Monkeysanity - Passwords"
    default = 0

    option_disabled: int = 0
    option_enabled: int = 1
    option_hunt: int = 2


class Camerasanity(Choice):
    """
    Choose if Pipo Cameras should count as Locations.
    Default: Disabled

    > disabled - Pipo Cameras will not count as locations
    > enabled - Pipo Cameras will count as locations, and is counted when a Monkey Film is recorded.
    This means that the Pipo Monkey actors MUST BE PRESENT to acquire the item, or it will be missable until
    Free Play mode is unlocked for the channel upon clearing it.
    > no_actors - Pipo Cameras will count as locations, regardless if the Pipo Monkey Actors are present
    """
    display_name = "Pipo Camerasanity"
    default = 0

    option_disabled : int = 0
    option_enabled : int = 1
    option_no_actors : int = 2


class Cellphonesanity(Toggle):
    """
    Choose if Cellphones should count as locations
    default: Disabled
    """
    display_name = "Cellphonesanity"

class Shoppingsanity(Choice):
    """
    Choose if items from the Book Shop, Hobby Shop, and Music Shop, and the Morph Stocks from Monkey Mart
    should count as locations.
    Default: Disabled

    > disabled - Shop Items will not count as locations
    > enabled - Shop Items will count as locations
    > collection - Shop Items will count as locations by the amount of that type of item that is owned
    > progressive - Shop Items will become available as you unlock more channels
    > restock - Shop Items will become available as you find more Shop Stocks
    """
    display_name = "Shoppingsanity"
    default = 0

    option_disabled : int = 0
    option_enabled : int = 1
    option_collection : int = 2
    option_progressive : int = 3
    option_restock : int = 4


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
    visibility = Visibility.none
    display_name : str = "Shuffle Monkey Net"


class ShuffleRCCarChassis(Toggle):
    """
    Choose if the various RC Car Chassis should also be included in the pool. Unlocking any chassis will
    automatically unlock the RC Car Gadget if it hasn't yet. This does not automatically equip the chassis.
    Default: Disabled
    """
    display_name : str = "Shuffle RC Car Chassis"


class ShuffleMorphStocks(Toggle):
    """
    Choose if Morph Stocks should also be included in the pool. This does not affect the Monkey Mart.
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

class ExtraKeys(Range):
    """
    Determine if extra channel keys should be generated in addition to the minimum required to unlock all the channels.
    """
    display_name : str = "Extra Channel Keys"
    default = 0

    range_start = 0
    range_end = 15


class EarlyFreePlay(Toggle):
    """
    Allows Free Play mode to be available without needing to fully clear a channel. Useful when wanting Camerasanity
    enabled without needing to worry about Pipo Monkey actors.
    default: Disabled.
    """
    display_name : str = "Early Free Play"


class EnableMonkeyMart(DefaultOnToggle):
    """
    Choose if Monkey Mart should be able to sell cookies, energy and pellets. Morph Stock and Lucky Ticket will
    remain available

    Default: Enabled
    """
    display_name : str = "Enable Monkey Mart"

class LuckyTicketConsolationEffects(Toggle):
    """
    Choose if Lucky Ticket Consolation Effects should be enabled. When you get a consolation prize, get a chance to
    activate a special effect that can affect the Archipelago experience.
    """

class ConsolationEffectsBlacklist(OptionList):
    """
    When `Lucky Ticket Consolation` is enabled, this option allows you to disable certain effects from being chosen.

    Highly destructive effects have override values in host.yaml that will lead to options here being ignored.
    If you wish to enable these effects, please refer to the settings in your host.yaml, or contact your game host
    in charge of generating the game.
    """
    display_name : str = "Lucky Ticket Consolation Effects Blacklist"
    default = ["Bypass Post-Game Condition", "Instant Goal"]


ae3_option_groups : dict[str, list] = {
    "Randomizer Options"        : [ProgressionMode, OpenProgressionKeys, RandomizeProgressionSetCount,
                                   RandomizeProgressionChannelCount, LogicPreference, GoalTarget, PostGameAccessRule,
                                   ShuffleChannel, PreserveChannel, PushChannel, PostChannel, BlacklistChannel,
                                   Monkeysanity,MonkeysanityBreakRooms, MonkeysanityPasswords, Camerasanity,
                                   Cellphonesanity, Shoppingsanity],
    "Item Options"              : [StartingGadget, StartingMorph, BaseMorphDuration, ShuffleMonkeyNet,
                                   ShuffleRCCarChassis, ShuffleMorphStocks, AddMorphExtensions, ExtraKeys],
    "Preferences"               : [EarlyFreePlay, EnableMonkeyMart, LuckyTicketConsolationEffects,
                                   ConsolationEffectsBlacklist],
    "Sync Options"              : [DeathLink]
}

@dataclass
class AE3Options(PerGameCommonOptions):
    Progression_Mode                        : ProgressionMode
    Open_Progression_Keys                   : OpenProgressionKeys
    Randomize_Progression_Set_Count         : RandomizeProgressionSetCount
    Randomize_Progression_Channel_Count     : RandomizeProgressionChannelCount
    Logic_Preference                        : LogicPreference
    Goal_Target                             : GoalTarget
    Post_Game_Condition                     : PostGameAccessRule
    Shuffle_Channel                         : ShuffleChannel
    Preserve_Channel                        : PreserveChannel
    Push_Channel                            : PushChannel
    Post_Channel                            : PostChannel
    Blacklist_Channel                       : BlacklistChannel
    Monkeysanity                            : Monkeysanity
    Monkeysanity_BreakRooms                 : MonkeysanityBreakRooms
    Monkeysanity_Passwords                  : MonkeysanityPasswords
    Camerasanity                            : Camerasanity
    Cellphonesanity                         : Cellphonesanity
    Shoppingsanity                          : Shoppingsanity

    Starting_Gadget                         : StartingGadget
    Starting_Morph                          : StartingMorph
    Base_Morph_Duration                     : BaseMorphDuration

    Shuffle_Net                             : ShuffleMonkeyNet
    Shuffle_Chassis                         : ShuffleRCCarChassis
    Shuffle_Morph_Stocks                    : ShuffleMorphStocks
    Add_Morph_Extensions                    : AddMorphExtensions
    Extra_Keys                              : ExtraKeys

    Early_Free_Play                         : EarlyFreePlay
    Enable_Monkey_Mart                      : EnableMonkeyMart
    Lucky_Ticket_Consolation_Effects        : LuckyTicketConsolationEffects
    Consolation_Effects_Blacklist           : ConsolationEffectsBlacklist

    death_link                              : DeathLink

def create_option_groups() -> list[OptionGroup]:
    groups : list[OptionGroup] = []
    for group, options in ae3_option_groups.items():
        groups.append(OptionGroup(group, options))

    return groups

def slot_data_options() -> list[str]:
    return [
        APHelper.progression_mode.value,
        APHelper.open_required.value,
        APHelper.randomize_set_count.value,
        APHelper.randomize_channel_count.value,
        APHelper.logic_preference.value,
        APHelper.goal_target.value,
        APHelper.post_game_access_rule.value,
        APHelper.shuffle_channel.value,
        APHelper.preserve_channel.value,
        APHelper.push_channel.value,
        APHelper.post_channel.value,
        APHelper.blacklist_channel.value,
        APHelper.monkeysanity.value,
        APHelper.monkeysanitybr.value,
        APHelper.monkeysanitypw.value,
        APHelper.camerasanity.value,
        APHelper.cellphonesanity.value,
        APHelper.shoppingsanity.value,

        APHelper.starting_gadget.value,
        APHelper.starting_morph.value,
        APHelper.base_morph_duration.value,

        APHelper.shuffle_net.value,
        APHelper.shuffle_chassis.value,
        APHelper.shuffle_morph_stocks.value,
        APHelper.add_morph_extensions.value,
        APHelper.extra_keys.value,

        APHelper.early_free_play.value,
        APHelper.enable_monkey_mart.value,
        APHelper.ticket_consolation.value,
        APHelper.consolation_blacklist.value,

        APHelper.death_link.value
    ]