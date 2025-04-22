from typing import TYPE_CHECKING, Set, Callable
from enum import Enum

from BaseClasses import CollectionState

from .Items import AE3Item, Channel_Key
from .Strings import Itm, APHelper

if TYPE_CHECKING:
    from .. import AE3World

### [< --- ACCESS RULES --- >]
## Check if Player can Catch Monkeys
def can_catch(state : CollectionState, player : int):
    return can_net(state, player) or can_morph_not_monkey(state, player)

def can_catch_long(state : CollectionState, player : int):
    return state.has(APHelper.catch_long.value, player)

def can_net(state : CollectionState, player : int):
    return state.has(Itm.gadget_net.value, player)

## Check if Player can Morph
def can_morph(state : CollectionState, player : int):
    return state.has(APHelper.morphs.value, player)

def can_morph_not_monkey(state : CollectionState, player : int):
    return state.has(APHelper.morphs_no_monkey.value, player)

# Gadget Checks
def has_club(state : CollectionState, player : int):
    return state.has(Itm.gadget_club.value, player)

## Check if Player can use the Slingback Shooter
def can_sling(state : CollectionState, player : int):
    return state.has(Itm.gadget_sling.value, player)

## Check if Player has Water Net
def can_swim(state : CollectionState, player : int):
    return state.has(Itm.gadget_swim.value, player)

## Check if Player can use the RC Car
def can_rcc(state : CollectionState, player : int):
    return state.has(APHelper.rc_cars.value, player)

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
    return state.has(APHelper.attack.value, player)

def can_hit(state : CollectionState, player : int):
    return state.has(APHelper.hit.value, player)

## Check if player has the ability to move fast
def can_dash(state : CollectionState, player : int):
    return state.has(APHelper.dash.value, player)

## Check if Player can use long-ranged attacks
def can_shoot(state : CollectionState, player : int):
    return state.has(APHelper.shoot.value, player)

## Check if Player can fly (can gain height)
def can_fly(state : CollectionState, player : int):
    return state.has(APHelper.fly.value, player)

## Check if the Player can glide
def can_glide(state : CollectionState, player : int):
    return state.has(APHelper.glide.value, player)

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
    NET = can_net                               # Monkey Net Unlocked
    MORPH = can_morph
    MORPH_NO_MONKEY = can_morph_not_monkey      # Unlocked any morph that is not Super Monkey
    ATTACK = can_attack                    # Can attack reasonably
    CLUB = has_club                             # Unlocked Stun Club
    DASH = can_dash                             # Unlocked Super Hoop or any fast moving Morph
    SHOOT = can_shoot                           # Slingback Shooter unlocked or has any morph with long range attacks
    SWIM = can_swim
    FLY = can_fly                               # Sky Flyer unlocked or has any morph that can fly (gain height)
    GLIDE = can_glide                           # Sky Flyer unlocked or has any morph that can glide

    # Gadget
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
        Critical : Set of AccessRules that must always be true for a Location to be reachable.
        Rules : Normal Sets of AccessRules. In addition to adhering to AccessRules set in Critical,
        at least one set of AccessRules must also be adhered to.
    """
    Critical : Set[Callable] = None
    Rules : Set[Set[Callable]] = None

    def __init__(self, critical : Set[Callable] = None, rules : Set[Set[Callable]] = None):
        if critical is not None:
            self.Critical = critical
        else:
            self.Critical = set()

        if rules is not None:
            self.Rules = rules
        else:
            self.Rules = set()

    def __bool__(self):
        return bool(self.Critical) or bool(self.Rules)

    def check(self, state : CollectionState, player : int) -> bool:
        # Any Critical Rules that return False should immediately mark the item as inaccessible with the current state
        if self.Critical:
            for rule in self.Critical:
                if not rule(state, player):
                    return False

        # At least one set of normal rules (if any) must return true to mark the item as reachable
        if not self.Rules:
            return True

        reachable: bool = False

        for rulesets in self.Rules:
            for rule in rulesets:
                if not rule(state, player):
                    continue

                reachable = True
                break

        return reachable

    def condense(self, player) -> Callable[[CollectionState], bool]:
        return lambda state : self.check(state, player)

from .Locations import MONKEYS_BOSSES
class ProgressionMode(Enum):
    """
    Defines how the game should progress and the goal to achieve
    """

    # Seaside Resort is unlocked at value 0, so starting unlocked levels are 1 less than actually represented.
    SINGLES =       [1 for _ in range(27)]
    BOSS =          [2, 1, 4, 1, 3, 1, 4, 1, 3, 1, 2, 1, 1, 1, 1]
    BOSS_INCL =     [3, 5, 4, 5, 4, 3, 1, 1, 1]

    def generate_keys(self, world : "AE3World") -> list[AE3Item]:
        amt : int = len(self.value)
        auto_set : bool = False

        if self == self.BOSS:
            auto_set = True

        # Automatically assign to bosses (except both Specter bosses) if autoset_bosses is True
        if auto_set:
            bosses : int = len(MONKEYS_BOSSES) - 2
            for _ in range(0, bosses):
                world.get_location(MONKEYS_BOSSES[_]).place_locked_item(Channel_Key.to_item(world.player))

            amt -= bosses

        return Channel_Key.to_items(world.player, amt)

    def get_current_progress(self, keys : int) -> int:
        unlocks : int = 0
        for i, unlocked in enumerate(self.value):
            unlocks += unlocked

            if i >= keys:
                break

        return unlocks

    @classmethod
    def get_progression_mode(cls, index : int):
        return [*cls][index]