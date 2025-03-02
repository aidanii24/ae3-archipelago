from collections.abc import Sequence
from dataclasses import dataclass
from abc import ABC

from BaseClasses import Item

from .Addresses import Items, GameStates
from .Strings import Itm, Game, Meta

### [< --- HELPERS --- >]
class AE3Item(Item):
    """
    Defines an Item in Ape Escape 3. These include but are not limited to the Gadgets, Morphs and select buyable items
    in the Shopping District.
    """

    game : str = Meta.game.value

@dataclass
class AE3ItemMeta(ABC):
    """
    Base Class for all Items in Ape Escape 3. Used to manage objects Clientside and should not be used Serverside.
    """
    name : str
    item_id : int
    address : int

@dataclass
class EquipmentItem(AE3ItemMeta):
    """
    Base Class for any Item that the player can only have one of. They can only be either locked or unlocked.
    """

    def __init__(self, name : str):
        self.name = name
        self.item_id = Items[name].value    # Equipment can be assumed to always be in Addresses.Items.
        self.address = self.item_id

@dataclass
class CollectableItem(AE3ItemMeta):
    """
    Base Class for any Item that the player can obtain multiples of continuously regardless of whether the player is
    allowed to collect more.

    Attributes:
        capacity : Maximum amount of the item the player can hold
        weight : How often to be chosen to fill a location
    """

    capacity : int
    weight : float

    def __init__(self, name : str, address : int, capacity : int, weight : float, id_offset : int = 0):
        self.name = name
        self.item_id = address + id_offset
        self.address = address

        self.capacity = capacity
        self.weight = weight

class UpgradeableItem(AE3ItemMeta):
    """
    Base class for any item the player can obtain multiples of but only exists in specific amounts.

    Attributes:
        limit : Maximum amount of the item that is expected to exist in the game
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
Acc_Morph_Stock = UpgradeableItem(Itm.acc_morph_stock.value, Items[Game.morph_stocks.value].value, 10)

# Collectables
Nothing = CollectableItem(Itm.nothing.value, Items[Itm.nothing.value].value, 0, 0.0)

Cookie = CollectableItem(Itm.cookie.value, GameStates[Game.cookies.value].value, 5, 0.4)
Cookie_Giant = CollectableItem(Itm.cookie_giant.value, GameStates[Game.cookies.value].value, 5, 0.15,
                               0x01)
Jacket = CollectableItem(Itm.jacket.value, GameStates[Game.jackets.value].value, 99, 0.1)
Chip_1x = CollectableItem(Itm.chip_1x.value, GameStates[Game.chips.value].value, 9999, 0.5)
Chip_5x = CollectableItem(Itm.chip_5x.value, GameStates[Game.chips.value].value, 9999, 0.45,
                          0x01)
Chip_10x = CollectableItem(Itm.chip_10x.value, GameStates[Game.chips.value].value, 9999, 0.4,
                            0x02)
Energy = CollectableItem(Itm.energy.value, GameStates[Game.morph_gauge_active.value].value, 30, 0.35,)
Energy_Mega = CollectableItem(Itm.energy_mega.value, GameStates[Game.morph_gauge_recharge.value].value, 3,
                            0.25)

Ammo_Boom = CollectableItem(Itm.ammo_boom.value, Items[Game.ammo_boom.value].value, 9, 0.3)
Ammo_Homing = CollectableItem(Itm.ammo_homing.value, Items[Game.ammo_homing.value].value, 9, 0.3)

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
def from_id(item_id = int, category : int = 0) -> AE3ItemMeta:
    """Get Item by its ID"""
    ref : Sequence = INDEX[category]

    i : AE3ItemMeta = next((i for i in ref if i.item_id == item_id), None)
    return i

def from_name(name = str, category : int = 0) -> AE3ItemMeta:
    """Get Item by its Name"""
    ref : Sequence = INDEX[category]

    i : AE3ItemMeta = next((i for i in ref if i.name == name), None)
    return i