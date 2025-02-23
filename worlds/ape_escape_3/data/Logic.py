from dataclasses import dataclass
from enum import Enum

from BaseClasses import CollectionState

from .Strings import AE3Items
from .. import AE3World

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


# Randomizer Logic Helper Classes
class Prerequisite(Enum):
    """
    Defines required states for the player to achieve in order for an item to be considered "reachable".
    """

    # General
    catch = 0                   # Net Unlocked (if Shuffled) or has any morph (If Gadget Association is disabled)
    morph = 1
    shoot = 2                   # Slingback Shooter unlocked or has any morph with long range attacks
    fly = 3                     # Sky Flyer unlocked or has any morph that can fly/glide

    # Gadget
    shoot_free = 10             # Slingback Shooter specifically unlocked
    rc_car = 11                 # RC Car Unlocked

    # Morph
    genie = 30                  # Genie Dancer is unlocked
    monkey = 31                 # Super Monkey is unlocked

    # Glitches
    glitch_fly = -1             # Has any combination of gadget/morph for flying/gliding
    glitch_float = -2           # Has any combination of gadget for floating