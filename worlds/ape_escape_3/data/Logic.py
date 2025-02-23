from typing import Set, Callable

from BaseClasses import CollectionState

from .Strings import AE3Items

# General Checks
## Check if Player can Catch Monkeys
def can_catch(state : CollectionState, player : int):
    return state.has(AE3Items.monkey_net.value, player)

## Check if Player can Morph (Any Morph)
def can_morph(state : CollectionState, player : int):
    return state.has("Morphs", player)

## Check if Player can use long-ranged attacks
def can_shoot(state : CollectionState, player : int):
    return (state.has(AE3Items.slingback_shooter.value, player) or

            state.has(AE3Items.morph_cowboy.value, player) or
            state.has(AE3Items.morph_hero.value, player))

## Check if Player can fly/glide
def can_fly(state : CollectionState, player : int):
    return (state.has(AE3Items.sky_flyer.value, player) or

            state.has(AE3Items.morph_ninja.value, player) or
            state.has(AE3Items.morph_hero.value, player))

# Gadget Checks
## Check if Player can use long-ranged attacks freely and can aim it manually (e.g. has the Slingback Shooter)
def can_shoot_free(state : CollectionState, player : int):
    return state.has(AE3Items.slingback_shooter.value, player)

## Check if Player can use the RC Car
def can_use_rc_car(state : CollectionState, player : int):
    return state.has(AE3Items.rc_car.value, player)

# Morph Checks
def can_use_genie(state : CollectionState, player : int):
    return state.has(AE3Items.morph_magician.value, player)

def can_use_monkey(state : CollectionState, player : int):
    return state.has(AE3Items.morph_monkey.value, player)

class AccessRules:
    """
        Defines required states for the player to achieve in order for an item to be considered "reachable".
    """

    # General
    CATCH = can_catch               # Net Unlocked (if Shuffled) or has any morph (If Gadget Association is disabled)
    MORPH = can_morph
    SHOOT = can_shoot               # Slingback Shooter unlocked or has any morph with long range attacks
    FLY = can_fly                   # Sky Flyer unlocked or has any morph that can fly/glide

    # Gadget
    SHOOT_FREE = can_shoot_free     # Slingback Shooter specifically unlocked
    RC_CAR = can_use_rc_car

    # Morph
    GENIE = can_use_genie
    MONKEY = can_use_monkey

    # Glitches
    GLITCH_FLY = 0
    GLITCH_FLOAT = 0

class LocationRules:
    """
    Helper for Storing and Managing Access Rules of Locations.

    Attributes:
        Critical : Set of AccessRules that must always be true for a Location to be reachable.
        Rules : Normal Sets of AccessRules. In addition to adhering to AccessRules set in Critical,
        at least one set of AccessRules must also be adhered to.
    """
    Critical : Set[Callable] = None
    Rules : Set[frozenset[Callable]] = None

    def __init__(self, critical : Set[Callable] = None, rules : Set[frozenset[Callable]] = None):
        if critical is not None:
            self.Critical = critical

        if rules is not None:
            self.Rules = rules