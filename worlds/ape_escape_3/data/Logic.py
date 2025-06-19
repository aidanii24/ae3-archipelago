from copy import deepcopy
from typing import TYPE_CHECKING, Set, Sequence, Callable
import warnings

from BaseClasses import CollectionState, Item

from .Items import Channel_Key
from .Stages import AE3EntranceMeta, ENTRANCES_STAGE_SELECT, ENTRANCES_CHANNELS, LEVELS_BY_ORDER
from .Strings import Itm, Stage, APHelper

if TYPE_CHECKING:
    from .. import AE3World

### [< --- ACCESS RULES --- >]
## Check if Player can Catch Monkeys
def can_catch(state : CollectionState, player : int):
    return can_net(state, player) or can_morph_not_monkey(state, player)

def can_catch_long(state : CollectionState, player : int):
    return state.has_group(APHelper.catch_long.value, player)

def can_net(state : CollectionState, player : int):
    return state.has(Itm.gadget_net.value, player)

## Check if Player can Morph
def can_morph(state : CollectionState, player : int):
    return state.has_group(APHelper.morphs.value, player)

def can_morph_not_monkey(state : CollectionState, player : int):
    return state.has_group(APHelper.morphs_no_monkey.value, player)

# Gadget Checks
def has_radar(state : CollectionState, player : int):
    return state.has(Itm.gadget_radar.value, player)

def has_club(state : CollectionState, player : int):
    return state.has(Itm.gadget_club.value, player)

def has_hoop(state : CollectionState, player : int):
    return state.has(Itm.gadget_hoop.value, player)

def has_flyer(state : CollectionState, player : int):
    return state.has(Itm.gadget_fly.value, player)

## Check if Player can use the Slingback Shooter
def can_sling(state : CollectionState, player : int):
    return state.has(Itm.gadget_sling.value, player)

## Check if Player has Water Net
def can_swim(state : CollectionState, player : int):
    return state.has(Itm.gadget_swim.value, player)

## Check if Player can use the RC Car
def can_rcc(state : CollectionState, player : int):
    return state.has_group(APHelper.rc_cars.value, player)

# Morph Checks
def can_knight(state : CollectionState, player : int):
    return state.has(Itm.morph_knight.value, player)

def can_cowboy(state : CollectionState, player : int):
    return state.has(Itm.morph_cowboy.value, player)

def can_ninja(state : CollectionState, player : int):
    return state.has(Itm.morph_ninja.value, player)

def can_genie(state : CollectionState, player : int):
    return state.has(Itm.morph_magician.value, player)

def can_kungfu(state : CollectionState, player : int):
    return state.has(Itm.morph_kungfu.value, player)

def can_hero(state : CollectionState, player : int):
    return state.has(Itm.morph_hero.value, player)

def can_monkey(state : CollectionState, player : int):
    return state.has(Itm.morph_monkey.value, player)

# General Ability Checks
## Check if player can hit beyond basic hip drops
def can_attack(state : CollectionState, player : int):
    return state.has_group(APHelper.attack.value, player)

def can_hit(state : CollectionState, player : int):
    return state.has_group(APHelper.hit.value, player)

## Check if player has the ability to move fast
def can_dash(state : CollectionState, player : int):
    return state.has_group(APHelper.dash.value, player)

## Check if Player can use long-ranged attacks
def can_shoot(state : CollectionState, player : int):
    return state.has_group(APHelper.shoot.value, player)

def can_shoot_boom(state : CollectionState, player : int):
    return can_shoot(state, player) and state.has(Itm.ammo_boom.value, player)

## Check if Player can fly (can gain height)
def can_fly(state : CollectionState, player : int):
    return state.has_group(APHelper.fly.value, player)

## Check if the Player can glide
def can_glide(state : CollectionState, player : int):
    return state.has_group(APHelper.glide.value, player)

# Event Checks
def has_enough_keys(state : CollectionState, player : int, keys : int):
    return state.has(APHelper.channel_key.value, player, keys)

def has_keys(keys : int):
    return lambda state, player : has_enough_keys(state, player, keys=keys)

def is_event_invoked(state : CollectionState, player : int, event_name : str):
    return state.has(event_name, player)

def is_event_not_invoked(state : CollectionState, player : int, event_name : str):
    return not state.has(event_name, player)

def event_invoked(event_name : str):
    return lambda state, player : is_event_invoked(state, player, event_name)

def event_not_invoked(event_name : str):
    return lambda state, player : is_event_not_invoked(state, player, event_name)

def is_goal_achieved(state : CollectionState, player : int, count : int = 1):
    return state.has(APHelper.victory.value, player, count)

def are_goals_achieved(goal_count : int):
    return lambda state, player : is_goal_achieved(state, player, goal_count)

### [< --- WRAPPER SHORTHAND --- >]
class AccessRule:
    """
        Defines required states for the player to achieve in order for an item to be considered "reachable".
    """

    # General
    CATCH = can_catch                           # Monkey Net unlocked or any Morph that can Catch Monkeys
    CATCH_LONG = can_catch_long                 # Has any morph with ranged capture
    MORPH = can_morph
    MORPH_NO_MONKEY = can_morph_not_monkey      # Unlocked any morph that is not Super Monkey
    ATTACK = can_attack                         # Can attack reasonably
    HIT = can_hit                               # Can hit at all
    DASH = can_dash                             # Unlocked Super Hoop or any fast moving Morph
    SHOOT = can_shoot                           # Slingback Shooter unlocked or has any morph with long range attacks
    SHOOT_BOOM = can_shoot_boom                      # Slingback Shooter unlocked or has any morph with long range attacks
    SWIM = can_swim
    FLY = can_fly                               # Sky Flyer unlocked or has any morph that can fly (gain height)
    GLIDE = can_glide                           # Sky Flyer unlocked or has any morph that can glide

    # Gadget
    NET = can_net                               # Monkey Net Unlocked
    CLUB = has_club                             # Unlocked Stun Club
    RADAR = has_radar                           # Unlocked Monkey Radar
    HOOP = has_hoop                             # Unlocked Dash Hoop
    FLYER = has_flyer                           # Unlocked Sky Flyer
    SLING = can_sling
    RCC = can_rcc

    # Morph
    KNIGHT = can_knight
    COWBOY = can_cowboy
    NINJA = can_ninja
    MAGICIAN = can_genie
    KUNGFU = can_kungfu
    HERO = can_hero
    MONKEY = can_monkey

    # NULL
    NULL = (lambda state, player : False)

    # Glitches
    GLITCH_FLY = 0
    GLITCH_FLOAT = 0

    # Victory
    GOAL = is_goal_achieved

### [< --- MANAGING CLASS --- >]
class Rulesets:
    """
    Helper for Storing and Managing Access Rules of Locations.

    Attributes:
        critical : Set of AccessRules that must always be true for a Location to be reachable.
        rules : Normal Sets of AccessRules. In addition to adhering to AccessRules set in Critical,
        at least one set of AccessRules must also be adhered to.
    """
    critical : Set[Callable] = None
    rules : list[list[Callable]] = None

    def __init__(self, *rules : Callable | list[Callable] | list[list[Callable]] | None,
                 critical : Set[Callable] = None):
        self.critical = set()
        self.rules = []

        if critical:
            self.critical = critical

        if rules:
            for rule in rules:
                if isinstance(rule, Callable):
                    self.rules.append([rule])
                elif isinstance(rule, list):
                    if all(isinstance(_, Callable) for _ in rule):
                        self.rules.append(rule)
                    elif all(isinstance(x, list) and all(isinstance(_, Callable) for _ in x) for x in rule):
                        self.rules.extend(rule)


    def __bool__(self):
        return bool(self.critical) or bool(self.rules)

    def update(self, rulesets : "Rulesets"):
        if not rulesets:
            return

        if rulesets.critical:
            self.critical.update(rulesets.critical)

        if rulesets.rules:
            for i, rule in enumerate(rulesets.rules):
                if rule in self.rules:
                    rulesets.rules.pop(i)

            self.rules.extend(rulesets.rules)

    def check(self, state : CollectionState, player : int) -> bool:
        # Any Critical Rules that return False should immediately mark the item as inaccessible with the current state
        if self.critical:
            for rule in self.critical:
                if not rule(state, player):
                    return False

        # At least one set of normal rules (if any) must return true to mark the item as reachable
        if not self.rules:
            return True

        reachable: bool = True

        for rulesets in self.rules:
            reachable = all(rule(state, player) for rule in rulesets)

            if reachable:
                break

        return reachable

    def condense(self, player) -> Callable[[CollectionState], bool]:
        return lambda state : self.check(state, player)


class ProgressionMode:
    name : str = "Generic Progression Mode"
    progression : list[int] = None
    order : list[int] = None
    level_select_entrances : list[AE3EntranceMeta] = None

    boss_indices : Sequence[int] = [ 3, 8, 12, 17, 21, 24, 26, 27 ]
    small_starting_channels : Sequence[int] = [ 6, 9, 11, 13, 15, 18, 20, 22, 23 ]

    def __init__(self, world : 'AE3World' = None):
        self.progression = []
        self.order = [ _ for _ in range(28) ]
        self.level_select_entrances : list[AE3EntranceMeta] = [ *ENTRANCES_STAGE_SELECT ]

    def __str__(self):
        return self.name

    def shuffle(self, world : 'AE3World'):
        new_order: list[int] = self.generate_new_order(world)

        # Update with the new orders
        self.order = [*new_order]

        # Apply Channel Rules
        self.reorder(-1, [*world.options.blacklist_channel.value])
        self.reorder(-2, [*world.options.post_channel.value])
        self.reorder(-3, [*world.options.push_channel.value])

        self.regenerate_level_select_entrances()

    def generate_new_order(self, world : 'AE3World') -> list[int]:
        new_order : list[int] = [_ for _ in range(28)]
        world.random.shuffle(new_order)

        self.small_starting_channels = world.logic_preference.small_starting_channels.copy()

        # Do not allow Bosses or problematic levels to be in the first few levels
        if (len(set(new_order[:5]).intersection(self.small_starting_channels)) > 0 or
               len(set(new_order[:3]).intersection([*self.boss_indices, *self.small_starting_channels])) > 0):
            blacklists : list[int] = [*self.small_starting_channels, *self.boss_indices]
            swap_indexes : list[int] = [ _ for _ in range(7, 26) if new_order[_] not in blacklists ]
            for idx, level in enumerate(new_order):
                if level not in blacklists:
                    continue

                if idx > 3 and len(blacklists) > len(self.small_starting_channels):
                    blacklists = [*self.small_starting_channels]

                swap : int = -1
                swap_idx : int = -1
                while swap < 0 or swap in blacklists:
                    if not swap_indexes:
                        break

                    swap_idx = world.random.choice(swap_indexes)
                    swap = new_order[swap_idx]

                new_order[idx], new_order[swap_idx] = new_order[swap_idx], new_order[idx]

                if swap_idx in swap_indexes:
                    swap_indexes.remove(swap_idx)

                if idx >= 5: break
        # Re-insert Channels specified to be preserved in their vanilla indices
        if world.options.preserve_channel:
            preserve_indices : list[int] = [
                LEVELS_BY_ORDER.index(channel) for channel in world.options.preserve_channel
            ]

            if preserve_indices:
                new_order = [_ for _ in new_order if _ not in preserve_indices]

                for index in preserve_indices:
                    new_order.insert(index, index)

        # Apply the chosen Shuffle Mode
        if world.options.shuffle_channel == 1:
            new_boss_order: list[int] = [_ for _ in new_order if _ in self.boss_indices]

            new_order = [_ for _ in new_order if _ not in self.boss_indices]

            for index in range(len(self.boss_indices)):
                new_order.insert(self.boss_indices[index], new_boss_order[index])

        return new_order

    def reorder(self, set_interest : int, channels : list[str]):
        temp_progression = deepcopy(self.progression)
        # In the presence of padding sets, remove them first
        # Any ProgressionModes that requires the padding will handle putting it back themselves
        if 0 in self.progression[1:-1]:
            temp_progression = [
                self.progression[0], *[_ for _ in self.progression[1:-1] if _ > 0], self.progression[-1]
            ]

        if set_interest < 0:
            set_interest = len(temp_progression) + set_interest

        targets : list[int] = [
            LEVELS_BY_ORDER.index(channel) for channel in channels
            if channel in LEVELS_BY_ORDER
        ].copy()

        if not targets:
            return

        self.progression = deepcopy(temp_progression)

        additive = APHelper.additive.value in channels

        # Group the Sets
        group_set : list[list[int]] = []
        count : int = 0
        for i, channel_set in enumerate(self.progression):
            offset : int = 0
            if i == 0:
                offset = 1

            target : int = count + channel_set + offset
            group_set.append([_ if _ not in targets else -1
                              for _ in self.order[count : target]])
            count = target

        if additive:
            group_set[set_interest].extend(targets)
        else:
            group_set.insert(set_interest + 1, targets)

            if set_interest <= 1:
                set_interest += 1

            # Create Temporary Values
            temp_order : list[int] = [channel for sets in group_set[:set_interest]
                                      for channel in sets if channel != -1]
            temp_progression : list[int] = [len(_) for _ in group_set[:set_interest]]
            temp_set : list[list[int]] = []

            # Regenerate Group Set with new order for all the interest set and all sets before it
            if temp_order:
                count : int = 0
                for i, channel_set in enumerate(temp_progression):
                    target : int = count + channel_set
                    temp_set.append([_ for _ in temp_order[count : target]])
                    count = target

                temp_set.extend(group_set[set_interest:])
                group_set = deepcopy(temp_set)

        # Clean Up
        for i, sets in enumerate(group_set):
            if -1 in sets:
                group_set[i] = [_ for _ in sets if _ != -1]

        new_order : list[int] = [channel for sets in group_set for channel in sets]
        new_progression : list[int] = []
        for i, sets in enumerate(group_set):
            amount : int = len(sets)

            if amount == 0 and i < len(group_set) - 1:
                continue

            if not new_progression:
                amount -= 1

            new_progression.append(amount)

        self.order = deepcopy(new_order)
        self.progression = deepcopy(new_progression)

    def generate_rules(self, world : 'AE3World') -> dict[str, Rulesets]:
        channel_rules : dict[str, Rulesets] = {}

        for i, channel_set in enumerate(self.progression):
            # The first set of levels should NOT have any access rules
            # Filler sets should also be ignored
            if i == 0 or channel_set == 0:
                continue

            # Get total channels up until this set's point (not counting levels in current set)
            total_from_current : int = sum(self.progression[:i]) + 1
            required_keys : int = i

            # Get current channel index to be processed for access rules
            # by adding total from current and the range of the current set
            for channel in range(channel_set):
                if i == len(self.progression) - 1:
                    break

                channel_idx : int = total_from_current + channel
                access_rule : Rulesets = Rulesets(has_keys(required_keys))

                if i == len(self.progression) - 2:
                    access_rule = Rulesets(world.post_game_condition.enact(required_keys - 1,
                                           world.options.monkeysanity_break_rooms.value))

                channel_rules.update({self.level_select_entrances[channel_idx].name : access_rule})

        return channel_rules

    def generate_keys(self, world : 'AE3World') -> list[Item]:
        # The first set of levels and blacklisted set of levels will not cost keys.
        # Keys required by post game is handled by its corresponding option
        amount: int = len(self.progression) - 3 + world.options.post_game_condition_keys + world.options.extra_keys
        return Channel_Key.to_items(world.player, amount)

    def regenerate_level_select_entrances(self):
        base_destination_order: list[str] = [entrance.destination for entrance in ENTRANCES_STAGE_SELECT]
        new_entrances : list[AE3EntranceMeta] = []

        for slot, channel in enumerate(self.order):
            entrance: AE3EntranceMeta = AE3EntranceMeta(ENTRANCES_CHANNELS[slot], Stage.travel_station_a.value,
                                                        base_destination_order[channel])
            new_entrances.append(entrance)

        self.level_select_entrances = [*new_entrances]

    def set_progression(self, progression : list[int] = None):
        if progression is None or not progression:
            return

        self.progression = progression

    def set_order(self, order : list[int] = None):
        if order is None or not order:
            return

        self.order = order

    def get_progress(self, keys : int, post_game_status : bool = False):
        # Offset key count if Channel Keys are not part of Post Game Condition
        if post_game_status and keys <= len(self.progression) - 2:
            keys += 1

        # Do not include Blacklist set when checking for progress
        # Only include Post Game set when checking Progress if Post Game Conditions have been met
        limit : int = -2 if not post_game_status else -1
        unlocked : int = sum(self.progression[:limit][:keys + 1])

        return unlocked


class Singles(ProgressionMode):
    def __init__(self, world : 'AE3World' = None):
        super().__init__(world)

        self.name = "Singles"
        self.progression = [0, *[1 for _ in range(1, 28)], 0]

class Group(ProgressionMode):
    def __init__(self, world : 'AE3World' = None):
        super().__init__(world)

        self.name = "Group"
        self.progression = [2, 1, 4, 1, 3, 1, 4, 1, 3, 1, 2, 1, 1, 1, 1, 0]  # 15 Sets


    def shuffle(self, world : 'AE3World'):
        new_order : list[int] = self.generate_new_order(world)

        ## Pre-emptively remove Blacklisted Channels
        blacklist : list[int] = [LEVELS_BY_ORDER.index(channel) for channel in world.options.blacklist_channel
                                 if channel in LEVELS_BY_ORDER]
        new_order : list[int] = [_ for _ in new_order if _ not in blacklist]

        # Track channel being processed to create the new progression.
        new_progression : list[int] = [-1]
        is_last_index_boss : bool = False
        sets : int = 0

        for slot, level in enumerate(new_order):
            has_incremented : bool = False

            # Split the level group before and after boss
            if level in self.boss_indices:
                is_last_index_boss = True

                # If the current set has no levels counted yet, increment it first before incrementing the set number
                if (not sets and new_progression[sets] < 0) or (sets and new_progression[sets] < 1):
                    new_progression[sets] += 1
                    has_incremented = True

                if not new_progression[sets] < 0:
                    sets += 1

                if len(new_progression) - sets <= 0:
                    new_progression.insert(sets, 0)

            elif is_last_index_boss:
                # Do not increment set when coming from the first set that only has a boss level

                if sets == 1 and new_progression[1] > 0:
                    sets += 1
                elif sets > 1 and new_progression[sets] > 0:
                    sets += 1

                is_last_index_boss = False

                if len(new_progression) - sets <= 0:
                    new_progression.insert(sets, 0)

            if not has_incremented:
                new_progression[sets] += 1

        # Add Blacklisted Channels at end
        new_progression.append(len(blacklist))
        new_order.extend(blacklist)

        # Update with the new orders
        self.progression = [*new_progression]
        self.order = [*new_order]

        # Apply Channel Rules
        self.reorder(-2, [*world.options.post_channel.value])
        self.reorder(-3, [*world.options.push_channel.value])

        # Update new Channel Destinations
        self.regenerate_level_select_entrances()


class World(ProgressionMode):
    def __init__(self, world : 'AE3World' = None):
        super().__init__(world)

        self.name = "World"
        self.progression = [ 3, 5, 4, 5, 4, 3, 1, 1, 1, 0 ]

    def shuffle(self, world : 'AE3World'):
        new_order : list[int] = self.generate_new_order(world)

        # Pre-emptively remove Blacklisted Channels
        blacklist : list[int] = [LEVELS_BY_ORDER.index(channel) for channel in world.options.blacklist_channel
                                 if channel in LEVELS_BY_ORDER]
        if blacklist:
            new_order = [_ for _ in new_order if _ not in blacklist]

        # Track channel being processed to create the new progression.
        new_progression : list[int] = [-1]
        sets : int = 0
        for slot, level in enumerate(new_order):
            new_progression[sets] += 1

            # Split the level group only after the level boss
            if level in self.boss_indices:
                sets += 1

                if len(new_progression) - sets <= 0 and level != new_order[-1]:
                    new_progression.append(0)

        # Add Blacklisted Channels at end
        new_progression.append(len(blacklist))
        new_order.extend(blacklist)

        # Update with the new orders
        self.progression = [*new_progression]
        self.order = [*new_order]

        # Apply Channel Rules
        self.reorder(-2, [*world.options.post_channel.value])
        self.reorder(-3, [*world.options.push_channel.value])

        # Update new Channel Destinations
        self.regenerate_level_select_entrances()

class Quadruples(ProgressionMode):
    def __init__(self, world : 'AE3World' = None):
        super().__init__(world)

        self.name = "Quadruples"
        self.progression = [3, *[4 for _ in range(6)], 0]

class Open(ProgressionMode):
    required_keys : int = 0

    def __init__(self, world : 'AE3World' = None):
        super().__init__(world)

        self.name = "Open"
        self.progression = [25, 1, 1, 0]

        # Insert filler slots to simulate r
        if world is not None:
            self.required_keys = world.options.open_progression_keys.value - 1
            required_keys : list[int] = [0 for _ in range(self.required_keys)]
            self.progression[1:1] = required_keys

    def reorder(self, set_interest : int, channels : list[str]):
        super().reorder(set_interest, channels)
        if self.progression[1] != 0 and self.required_keys:
            self.progression[1:1] = [0 for _ in range(self.required_keys)]

class Randomize(ProgressionMode):
    def __init__(self, world : 'AE3World' = None):
        super().__init__(world)

        self.name = "Randomize"
        self.progression = []

        if world is None:
            return

        set_minimum : int = 1
        set_maximum : int = 16
        sets : int = world.options.randomize_progression_set_count.value
        if world.options.randomize_progression_channel_range.value:
            set_minimum = world.options.randomize_progression_channel_range.value[0]
            set_maximum = world.options.randomize_progression_channel_range.value[1]

        if sets:
            set_maximum = int(28 / sets)

        minimum : int = set_minimum
        maximum : int = set_maximum

        attempts : int = 0
        while sum(self.progression) < 27:
            # Enforce Set Count
            if sets and len(self.progression) + 1 == sets:
                self.progression.append(27 - sum(self.progression))
                break

            sets_amount : int = (world.random.randint(minimum, maximum))

            # Adjust sets amount if it will lead to progression tracking more channels than exists
            if sum(self.progression) + sets_amount > 27:
                sets_amount = 28 - sum(self.progression)

            # Subtract by an offset of 1 if this is the first set
            if not self.progression:
                sets_amount -= 1

            self.progression.append(sets_amount)

            # Recalibrate Maximum and Minimum as necessary
            if maximum > 27 - sum(self.progression):
                maximum = 27 - sum(self.progression)

            if minimum > maximum:
                minimum = maximum

            # Reset and try again when channel count exceeds expected when minimum gets pushed to 0
            if minimum <= 0 and sum(self.progression) != 27:
                minimum = set_minimum
                maximum = set_maximum
                self.progression.clear()

                attempts += 1
            elif sum(self.progression) == 27:
                break

            # If there are too many attempts, fall back to Quadruples
            if attempts > 5:
                self.progression = [3, *[4 for _ in range(6)], 0]
                warnings.warn("AE3 > Randomize: Generation failed to generate a valid Channel Set. "
                              "Falling back to Quadruples Progression...")
                break

        if sum(self.progression) != 27:
            raise AssertionError("AE3 > Randomize: Generation failed to generate a valid Channel Set. ")

        self.progression.append(0)


ProgressionModeOptions : Sequence[Callable] = [
    Singles, Group, World, Quadruples, Open, Randomize
]