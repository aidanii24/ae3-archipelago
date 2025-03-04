from collections.abc import Sequence
from dataclasses import dataclass
from typing import List
from abc import ABC

from BaseClasses import Item, ItemClassification

from .Strings import Itm, Game, Meta, APHelper
from .Addresses import Items, GameStates, Pointers

### [< --- HELPERS --- >]
class AE3Item(Item):
    """
    Defines an Item in Ape Escape 3. These include but are not limited to the Gadgets, Morphs and select buyable items
    in the Shopping District.
    """

    game : str = Meta.game.value

@dataclass
class AE3ItemMeta(ABC):
    """Base Data Class for all Items in Ape Escape 3."""
    name : str
    item_id : int
    address : int

    def to_item(self, player : int, classification : ItemClassification = None) -> AE3Item:
        cls = classification

        if cls is None:
            cls = ItemClassification.filler

        return AE3Item(self.name, cls, self.item_id, player)

@dataclass
class EquipmentItem(AE3ItemMeta):
    """
    Base Data Class for any Item that the player can only have one of. They can only be either locked or unlocked.

    Parameters:
        name : Name of Item from Strings.py
    """

    def __init__(self, name : str):
        self.name = name
        self.item_id = Items[name]    # Equipment can be assumed to always be in Addresses.Items.
        self.address = self.item_id

    def to_item(self, player : int, classification : ItemClassification = None) -> AE3Item:
        cls = classification

        if cls is None:
            cls = ItemClassification.progression

        return AE3Item(self.name, cls, self.item_id, player)

@dataclass
class CollectableItem(AE3ItemMeta):
    """
    Base Data Class for any Item that the player can obtain multiples of continuously regardless of whether the player
    is allowed to collect more.

    Parameters:
        name : Name of Item from Strings.py
        address : Memory Address of Item from Addresses.py
        amount : Amount of the Item to give
        capacity : Maximum amount of the item the player can hold
        weight : How often to be chosen to fill a location
        id_offset : (default : 0) Added Offset to ID for Items that target the same Memory Address
    """

    amount : int | float
    capacity : int
    weight : float

    pointers: Sequence[int] = None

    def __init__(self, name : str, address : int, amount : int | float,
                 capacity : int, weight : float, id_offset : int = 0):
        self.name = name
        self.item_id = address + id_offset
        self.address = address

        self.amount = amount
        self.capacity = capacity
        self.weight = weight

        if address in Pointers:
            self.pointers = Pointers[address]

class UpgradeableItem(AE3ItemMeta):
    """
    Base class for any item the player can obtain multiples of but only exists in specific amounts.

    Parameters:
        name : Name of Item from Strings.py
        address : Memory Address of Item from Addresses.py
        limit : Maximum amount of the item that is expected to exist in the game
        id_offset : (default : 0) Added Offset to ID for Items that target the same Memory Address
    """

    limit : int

    def __init__(self, name : str, address : int, limit : int, id_offset : int = 0):
        self.name = name
        self.item_id = address + id_offset
        self.address = address

        self.limit = limit

### [< --- ITEMS --- >]
# Gadgets
Gadget_Club = EquipmentItem(Itm.gadget_club.value)
Gadget_Net = EquipmentItem(Itm.gadget_net.value)
Gadget_Radar = EquipmentItem(Itm.gadget_radar.value)
Gadget_Hoop = EquipmentItem(Itm.gadget_hoop.value)
Gadget_Sling = EquipmentItem(Itm.gadget_sling.value)
Gadget_Swim = EquipmentItem(Itm.gadget_swim.value)
Gadget_RCC = EquipmentItem(Itm.gadget_rcc.value)
Gadget_Fly = EquipmentItem(Itm.gadget_fly.value)

# Morphs
Morph_Knight = EquipmentItem(Itm.morph_knight.value)
Morph_Cowboy = EquipmentItem(Itm.morph_cowboy.value)
Morph_Ninja = EquipmentItem(Itm.morph_ninja.value)
Morph_Magician = EquipmentItem(Itm.morph_magician.value)
Morph_Kungfu = EquipmentItem(Itm.morph_kungfu.value)
Morph_Hero = EquipmentItem(Itm.morph_hero.value)
Morph_Monkey = EquipmentItem(Itm.morph_monkey.value)

# Accessories
Chassis_Twin = EquipmentItem(Itm.chassis_twin.value)
Chassis_Black = EquipmentItem(Itm.chassis_black.value)
Chassis_Pudding = EquipmentItem(Itm.chassis_pudding.value)

# Upgradeables
Acc_Morph_Stock = UpgradeableItem(Game.morph_stocks.value, GameStates[Game.morph_stocks.value], 10)

# Collectables
Nothing = CollectableItem(Itm.nothing.value, Items[Itm.nothing.value], 0,0, 0.0)

Cookie = CollectableItem(Itm.cookie.value, GameStates[Game.cookies.value], 20.0, 100, 0.4)
Cookie_Giant = CollectableItem(Itm.cookie_giant.value, GameStates[Game.cookies.value], 100.0, 100,
                               0.15,0x01)
Jacket = CollectableItem(Itm.jacket.value, GameStates[Game.jackets.value], 1.0, 0x63, 0.1)
Chip_1x = CollectableItem(Itm.chip_1x.value, GameStates[Game.chips.value], 1, 0x270F, 0.5)
Chip_5x = CollectableItem(Itm.chip_5x.value, GameStates[Game.chips.value], 5, 0x270F, 0.45,
                          0x01)
Chip_10x = CollectableItem(Itm.chip_10x.value, GameStates[Game.chips.value], 10, 0x270F, 0.4,
                            0x02)
Energy = CollectableItem(Itm.energy.value, GameStates[Game.morph_gauge_active.value], 3.0, 30,
                         0.35, 0x0)
Energy_Mega = CollectableItem(Itm.energy_mega.value, GameStates[Game.morph_gauge_active.value], 30.0,
                              30, 0.25, 0x01)

Ammo_Boom = CollectableItem(Itm.ammo_boom.value, GameStates[Game.ammo_boom.value], 1, 0x9,
                            0.3)
Ammo_Homing = CollectableItem(Itm.ammo_homing.value, GameStates[Game.ammo_homing.value], 1, 0x9,
                              0.3)

### [< --- ITEM GROUPS --- >]
GADGETS : Sequence[EquipmentItem] = [
    Gadget_Swim, Gadget_Club, Gadget_Net, Gadget_Radar, Gadget_Hoop, Gadget_Sling, Gadget_RCC, Gadget_Fly
]

MORPHS : Sequence[EquipmentItem] = [
    Morph_Knight, Morph_Cowboy, Morph_Ninja, Morph_Magician, Morph_Kungfu, Morph_Hero, Morph_Monkey
]

EQUIPMENT : Sequence[EquipmentItem] = [
    *GADGETS, *MORPHS
]

ACCESSORIES : Sequence[EquipmentItem] = [
    Chassis_Twin, Chassis_Black, Chassis_Pudding
]

UPGRADEABLES : Sequence[UpgradeableItem] = [
    Acc_Morph_Stock
]

COLLECTABLES : Sequence[CollectableItem] = [
    Nothing, Cookie, Cookie_Giant, Jacket, Chip_1x, Chip_5x, Chip_10x, Energy, Energy_Mega, Ammo_Boom, Ammo_Homing
]

MASTER : Sequence[AE3ItemMeta] = [
    *GADGETS, *MORPHS, *ACCESSORIES, *UPGRADEABLES, *COLLECTABLES
]

INDEX : Sequence[Sequence] = [
    MASTER, GADGETS, MORPHS, EQUIPMENT, ACCESSORIES, UPGRADEABLES, COLLECTABLES
]

### [< --- METHODS --- >]
def from_id(item_id = int, category : int = 0):
    """Get Item by its ID"""
    ref : Sequence = INDEX[category]

    i : AE3ItemMeta = next((i for i in ref if i.item_id == item_id), None)
    return i

def from_name(name = str, category : int = 0):
    """Get Item by its Name"""
    ref : Sequence = INDEX[category]

    i : AE3ItemMeta = next((i for i in ref if i.name == name), None)
    return i

def generate_name_to_id() -> dict[str : int]:
    """Get a Dictionary of all Items in Name-ID pairs"""
    i : AE3ItemMeta
    return {i.name : i.item_id for i in MASTER}

def generate_id_to_name() -> dict[int : str]:
    """Get a Dictionary of all Items in ID-Name pairs"""
    i : AE3ItemMeta
    return {i.item_id : i.name for i in MASTER}

def generate_item_groups() -> dict[str : set[str]]:
    """Get a Dictionary of Item Groups"""
    groups : dict[str : set[str]] = {}

    i : AE3ItemMeta
    for i in GADGETS:
        groups.setdefault(APHelper.gadgets.value, set()).add(i.name)

    for i in MORPHS:
        groups.setdefault(APHelper.morphs.value, set()).add(i.name)

        if i.name is not Itm.morph_monkey.value:
            groups.setdefault(APHelper.morphs_no_monkey.value, set()).add(i.name)

    groups.setdefault(APHelper.equipment.value, set()).update(groups[APHelper.gadgets.value])
    groups.setdefault(APHelper.equipment.value, set()).update(groups[APHelper.morphs.value])

    return groups