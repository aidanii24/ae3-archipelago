from typing import TYPE_CHECKING, Set, Sequence, Callable

from BaseClasses import CollectionState, Item

from .Items import Channel_Key
from .Stages import AE3EntranceMeta, ENTRANCES_STAGE_SELECT, ENTRANCES_CHANNELS
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

from .Locations import MONKEYS_BOSSES
class ProgressionMode:
    name : str = "Generic Progression Mode"
    progression : list[int] = None
    order : list[int] = None
    level_select_entrances : list[AE3EntranceMeta] = None

    boss_indices : Sequence[int] = [ 3, 8, 12, 17, 21, 24, 26, 27 ]
    small_starting_channels : Sequence[int] = [ 6, 9, 11, 13, 15, 18, 20, 22, 23 ]

    def __init__(self):
        self.progression = self.progression
        self.order = [ _ for _ in range(28) ]
        self.level_select_entrances : list[AE3EntranceMeta] = [ *ENTRANCES_STAGE_SELECT ]

    def __str__(self):
        return self.name

    def shuffle(self, world : 'AE3World'):
        pass

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
            preserve_indices: list[int] = []

            if world.options.preserve_channel == 1:
                preserve_indices = [*self.boss_indices]
            elif world.options.preserve_channel == 2:
                preserve_indices = [*self.boss_indices[-2:]]
            elif world.options.preserve_channel == 3:
                preserve_indices = [self.boss_indices[-1]]

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
            special_post_game : bool = False
            if i == len(self.progression) - 1 and world.options.post_game_condition < 4:
                special_post_game = True
                required_keys -= 1

            # Get current channel index to be processed for access rules
            # by adding total from current and the range of the current set
            for channel in range(channel_set):
                channel_idx : int = total_from_current + channel
                access_rule : Rulesets = Rulesets(has_keys(required_keys))

                if special_post_game:
                    access_rule.critical.add(world.post_game_condition.verify)

                channel_rules.update({self.level_select_entrances[channel_idx].name : access_rule})

        return channel_rules

    def generate_keys(self, world : 'AE3World') -> list[Item]:
        # First Set of Level(s) will not cost keys, so subtract one from total length of progression
        amount: int = len(self.progression) - 1

        # Reduce Generated Keys for PostGameAccessRules other than "Channel Key"
        if world.options.post_game_condition < 4:
            amount -= 1
        # Reduce Generate Key for PostGameAccessRule "After End" and place it on the second to the last boss
        # (Which in Vanilla order, is always Specter 1
        elif world.options.post_game_condition == 5:
            amount -= 1

            bosses_in_order : list[int] = [ level for level in self.order if level in self.boss_indices ]
            penultimate : str = MONKEYS_BOSSES[self.boss_indices.index(bosses_in_order[-2])]

            world.get_location(penultimate).place_locked_item(Channel_Key.to_item(world.player))

        return Channel_Key.to_items(world.player, amount)

    def set_progression(self, progression : list[int] = None):
        if progression is None or not progression:
            return

        self.progression = progression

    def set_order(self, order : list[int] = None):
        if order is None or not order:
            return

        self.order = order

    def get_progress(self, keys : int):
        return sum(self.progression[:keys + 1])


class Singles(ProgressionMode):
    name : str = "Singles"
    progression : list[int] = [ 0, *[1 for _ in range(1, 28)]]

    def shuffle(self, world : 'AE3World'):
        new_order : list[int] = self.generate_new_order(world)

        base_destination_order : list[str] = [ entrance.destination for entrance in ENTRANCES_STAGE_SELECT]
        new_entrances : list[AE3EntranceMeta] = []

        # Update Entrance Destinations based on the Shuffle Result
        for slot, level in enumerate(new_order):
            entrance : AE3EntranceMeta = AE3EntranceMeta(ENTRANCES_CHANNELS[slot], Stage.travel_station_a.value,
                                                         base_destination_order[level])
            new_entrances.append(entrance)

        # Update with the new orders
        self.order = [*new_order]
        self.progression = [0, *[1 for _ in range(1, 28)]]
        self.level_select_entrances = [*new_entrances]


class Group(ProgressionMode):
    name : str = "Group"
    progression : list[int] = [ 2, 1, 4, 1, 3, 1, 4, 1, 3, 1, 2, 1, 1, 1, 1 ]   # 15 Sets

    def shuffle(self, world : 'AE3World'):
        new_order : list[int] = self.generate_new_order(world)

        base_destination_order : list[str] = [ entrance.destination for entrance in ENTRANCES_STAGE_SELECT]
        new_entrances : list[AE3EntranceMeta] = []

        # Update Entrance Destinations based on the Shuffle Result
        # and track channel being processed to create the new progression.
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

            entrance : AE3EntranceMeta = AE3EntranceMeta(ENTRANCES_CHANNELS[slot], Stage.travel_station_a.value,
                                                        base_destination_order[level])
            new_entrances.append(entrance)

            if not has_incremented:
                new_progression[sets] += 1

        # Update with the new orders
        self.progression = [*new_progression]
        self.order = [*new_order]
        self.level_select_entrances = [*new_entrances]


class World(ProgressionMode):
    name : str = "World"
    progression : list[int] = [ 3, 5, 4, 5, 4, 3, 1, 1, 1 ] # 9 Sets

    def shuffle(self, world : 'AE3World'):
        new_order : list[int] = self.generate_new_order(world)

        base_destination_order : list[str] = [ entrance.destination for entrance in ENTRANCES_STAGE_SELECT]
        new_entrances : list[AE3EntranceMeta] = []

        # Update Entrance Destinations based on the Shuffle Result
        # and track channel being processed to create the new progression.
        new_progression : list[int] = [-1]
        sets : int = 0
        for slot, level in enumerate(new_order):
            entrance: AE3EntranceMeta = AE3EntranceMeta(ENTRANCES_CHANNELS[slot], Stage.travel_station_a.value,
                                                        base_destination_order[level])
            new_entrances.append(entrance)
            new_progression[sets] += 1

            # Split the level group only after the level boss
            if level in self.boss_indices:
                sets += 1

                if len(new_progression) - sets <= 0 and level != new_order[-1]:
                    new_progression.append(0)

        # Update with the new orders
        self.progression = [*new_progression]
        self.order = [*new_order]
        self.level_select_entrances = [*new_entrances]

ProgressionModeOptions : Sequence[Callable] = [
    Singles, Group, World
]