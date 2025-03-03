from typing import Set, Callable

from BaseClasses import CollectionState

from .Strings import Itm, APHelper

### [< --- ACCESS RULES --- >]
## Check if Player can Catch Monkeys
def can_catch(state : CollectionState, player : int):
    return can_net(state, player) or can_morph_not_monkey(state, player)

def can_net(state : CollectionState, player : int):
    return state.has(Itm.gadget_net.value, player)

## Check if Player can Morph (Any Morph)
def can_morph(state : CollectionState, player : int):
    return state.has(APHelper.morphs.value, player)

def can_morph_not_monkey(state : CollectionState, player : int):
    return state.has(APHelper.morphs_no_monkey.value, player)

## Check if Player can use long-ranged attacks
def can_shoot(state : CollectionState, player : int):
    return (state.has(Itm.gadget_sling.value, player) or

            state.has(Itm.morph_cowboy.value, player) or
            state.has(Itm.morph_hero.value, player))

## Check if Player can fly/glide
def can_fly(state : CollectionState, player : int):
    return (state.has(Itm.gadget_fly.value, player) or

            state.has(Itm.morph_ninja.value, player) or
            state.has(Itm.morph_hero.value, player))

# Gadget Checks
## Check if Player can use the Slingback Shooter
def can_sling(state : CollectionState, player : int):
    return state.has(Itm.gadget_sling.value, player)

## Check if Player can use the RC Car
def can_rcc(state : CollectionState, player : int):
    return state.has(Itm.gadget_rcc.value, player)

# Morph Checks
def can_genie(state : CollectionState, player : int):
    return state.has(Itm.morph_magician.value, player)

def can_monkey(state : CollectionState, player : int):
    return state.has(Itm.morph_monkey.value, player)

### [< --- WRAPPER SHORTHAND --- >]
class AccessRule:
    """
        Defines required states for the player to achieve in order for an item to be considered "reachable".
    """

    # General
    CATCH = can_catch                           # Monkey Net unlocked or any Morph that can Catch Monkeys
    MORPH = can_morph
    MORPH_NO_MONKEY = can_morph_not_monkey      # Unlocked any morph that is not Super Monkey
    SHOOT = can_shoot                           # Slingback Shooter unlocked or has any morph with long range attacks
    FLY = can_fly                               # Sky Flyer unlocked or has any morph that can fly/glide

    # Gadget
    SLING = can_sling
    RCC = can_rcc

    # Morph
    GENIE = can_genie
    MONKEY = can_monkey

    # Glitches
    GLITCH_FLY = 0
    GLITCH_FLOAT = 0

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
    Rules : Set[frozenset[Callable]] = None

    def __init__(self, critical : Set[Callable] = None, rules : Set[frozenset[Callable]] = None):
        if critical is not None:
            self.Critical = critical

        if rules is not None:
            self.Rules = rules