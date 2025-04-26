from collections.abc import Sequence
from dataclasses import dataclass
from abc import ABC
import random

from BaseClasses import Item, ItemClassification
from .Strings import Itm, Loc, Game, Meta, APHelper
from .Addresses import NTSCU

### [< --- HELPERS --- >]
class AE3Item(Item):
    """
    Defines an Item in Ape Escape 3. These include but are not limited to the Gadgets, Morphs and select buyable items
    in the Shopping District.
    """

    game : str = Meta.game

@dataclass
class AE3ItemMeta(ABC):
    """Base Data Class for all Items in Ape Escape 3."""
    name : str
    item_id : int
    address : int

    def to_item(self, player : int) -> AE3Item:
        return AE3Item(self.name, ItemClassification.filler, self.item_id, player)

@dataclass
class EquipmentItem(AE3ItemMeta):
    """
    Base Data Class for any Item that the player can only have one of. They can only be either locked or unlocked.

    Parameters:
        name : Name of Item from Strings.py
    """

    def __init__(self, name : str):
        self.name = name
        # Equipment can be assumed to always be in Addresses.Items. NTSCU version will be used as basis for the ID.
        self.item_id = NTSCU.Items[name]
        self.address = self.item_id

    def to_item(self, player : int, classification : ItemClassification = ItemClassification.progression) -> AE3Item:
        return AE3Item(self.name, classification, self.item_id, player)

@dataclass
class CollectableItem(AE3ItemMeta):
    """
    Base Data Class for any Item that the player can obtain multiples of continuously regardless of whether the player
    is allowed to collect more.

    Parameters:
        name : Name of Item from Strings.py
        resource : Name of resource affected by Item from Strings.py
        amount : Amount of the Item to give
        weight : How often to be chosen to fill a location
        id_offset : (default : 0) Added Offset to ID for Items that target the same Memory Address
    """

    resource : str
    amount : int | float
    capacity : int
    weight : int

    def __init__(self, name : str, resource : str, amount : int | float, weight : int, id_offset : int = 0):
        self.name = name
        # Collectables can be assumed to always be in Addresses.Items. NTSCU version will be used as basis for the ID.
        self.address = NTSCU.GameStates[resource]
        self.item_id = self.address + id_offset
        self.resource = resource

        self.amount = amount
        self.capacity = Capacities[resource]
        self.weight = weight

class UpgradeableItem(AE3ItemMeta):
    """
    Base class for any item the player can obtain multiples of but only exists in specific amounts.

    Parameters:
        name : Name of Item from Strings.py
        resource : Name of resource affected by Item from Strings.py
        limit : Maximum amount of the item that is expected to exist in the game
        id_offset : (default : 0) Added Offset to ID for Items that target the same Memory Address
    """

    resource : str
    amount : int | float
    limit : int

    def __init__(self, name : str, resource : str, amount : int | float, limit : int, id_offset : int = 0):
        self.name = name
        # Upgradeables can be assumed to always be in Addresses.Items. NTSCU version will be used as basis for the ID.
        self.address = NTSCU.GameStates[resource]
        self.item_id = self.address + id_offset
        self.resource = resource

        self.amount = amount
        self.limit = limit

    def to_item(self, player : int, classification : ItemClassification = ItemClassification.useful) -> AE3Item:
        return AE3Item(self.name, classification, self.item_id, player)

    def to_items(self, player : int, classification : ItemClassification = ItemClassification.useful) -> list[AE3Item]:
        return [self.to_item(player, classification) for _ in range(self.limit)]

class ArchipelagoItem(AE3ItemMeta):
    """Base class for any non in-game item"""
    def __init__(self, name : str):
        self.name = name
        self.item_id = AP[name]

    def to_item(self, player : int) -> AE3Item:
        return AE3Item(self.name, ItemClassification.progression, self.item_id, player)

    def to_items(self, player : int, amount : int):
        return [self.to_item(player) for _ in range(amount)]

### [< --- DATA --->]
Capacities : dict[str, int | float] = {
    Game.morph_duration.value       : 30.0,
    Game.nothing.value              : 0x0,
    Game.cookies.value              : 100.0,
    Game.jackets.value              : 0x63,
    Game.chips.value                : 0x270F,
    Game.morph_gauge_active.value   : 30.0,
    Game.morph_stocks.value         : 1100.0,
    Game.ammo_boom.value            : 0x9,
    Game.ammo_homing.value          : 0x9,
}

AP : dict[str, int] = {
    APHelper.channel_key.value      : 0x3E8,
    APHelper.victory.value          : 0x3E9
}

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
Acc_Morph_Stock = UpgradeableItem(Itm.acc_morph_stock.value, Game.morph_stocks.value, 100.0, 10)
Acc_Morph_Ext = UpgradeableItem(Itm.acc_morph_ext.value, Game.morph_duration.value, 2.0, 10)

# Collectables
Nothing = CollectableItem(Itm.nothing.value, Game.nothing.value,0, 1)

Cookie = CollectableItem(Itm.cookie.value, Game.cookies.value, 20.0, 20)
Cookie_Giant = CollectableItem(Itm.cookie_giant.value, Game.cookies.value, 100.0, 10, 0x01)
Jacket = CollectableItem(Itm.jacket.value, Game.jackets.value, 1, 5)
Chip_1x = CollectableItem(Itm.chip_1x.value, Game.chips.value, 1, 40)
Chip_5x = CollectableItem(Itm.chip_5x.value, Game.chips.value, 5, 35, 0x01)
Chip_10x = CollectableItem(Itm.chip_10x.value, Game.chips.value, 10, 30, 0x02)
Energy = CollectableItem(Itm.energy.value, Game.morph_gauge_active.value, 3.0, 40,25)
Energy_Mega = CollectableItem(Itm.energy_mega.value, Game.morph_gauge_active.value, 30.0, 10,
                              0x01)

Ammo_Boom = CollectableItem(Itm.ammo_boom.value, Game.ammo_boom.value, 1, 25)
Ammo_Homing = CollectableItem(Itm.ammo_homing.value, Game.ammo_homing.value, 1, 25)

# Archipelago
Channel_Key = ArchipelagoItem(APHelper.channel_key.value)
Victory = ArchipelagoItem(APHelper.victory.value)

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
    Acc_Morph_Stock, Acc_Morph_Ext
]

COLLECTABLES : Sequence[CollectableItem] = [
    Nothing, Cookie, Cookie_Giant, Jacket, Chip_1x, Chip_5x, Chip_10x, Energy, Energy_Mega, Ammo_Boom, Ammo_Homing
]

ARCHIPELAGO : Sequence[ArchipelagoItem] = [
    Channel_Key, Victory
]

MASTER : Sequence[AE3ItemMeta] = [
    *GADGETS, *MORPHS, *ACCESSORIES, *UPGRADEABLES, *COLLECTABLES, *ARCHIPELAGO
]

INDEX : Sequence[Sequence] = [
    MASTER, GADGETS, MORPHS, EQUIPMENT, ACCESSORIES, UPGRADEABLES, COLLECTABLES, ARCHIPELAGO
]

### [< --- METHODS --- >]
def from_id(item_id = int, category : int = 0):
    """Get Item by its ID"""
    ref : Sequence = INDEX[category]

    i : AE3ItemMeta = next((i for i in ref if i.item_id == item_id), None)
    return i

def generate_name_to_id() -> dict[str : int]:
    """Get a Dictionary of all Items in Name-ID pairs"""
    i : AE3ItemMeta
    return {i.name : i.item_id for i in MASTER}

def generate_item_groups() -> dict[str : set[str]]:
    """Get a Dictionary of Item Groups"""
    groups : dict[str : set[str]] = {}

    i : AE3ItemMeta
    # Gadgets
    for i in GADGETS:
        groups.setdefault(APHelper.gadgets.value, set()).add(i.name)

    # Morphs
    for i in MORPHS:
        groups.setdefault(APHelper.morphs.value, set()).add(i.name)

    # Equipment
    groups.setdefault(APHelper.equipment.value, set()).update(groups[APHelper.gadgets.value])
    groups.setdefault(APHelper.equipment.value, set()).update(groups[APHelper.morphs.value])

    # Morphs (without Super Monkey)
    groups.setdefault(APHelper.morphs_no_monkey.value, groups[APHelper.morphs.value]).remove(Itm.morph_monkey.value)

    # RC Cars
    groups.setdefault(APHelper.rc_cars.value, set()).update([
        Itm.gadget_rcc.value, Itm.chassis_twin.value, Itm.chassis_black.value, Itm.chassis_pudding.value
    ])

    # Catch (Long)
    groups.setdefault(APHelper.catch_long.value, set()).update([
        Itm.morph_cowboy.value, Itm.morph_ninja.value, Itm.morph_magician.value, Itm.morph_hero.value
    ])

    # Attack
    groups.setdefault(APHelper.attack.value, set()).update([
        Itm.gadget_club.value, Itm.gadget_sling.value, *groups[APHelper.morphs_no_monkey.value]
    ])

    # Hit
    groups.setdefault(APHelper.hit.value, set()).update([
        Itm.gadget_hoop.value, Itm.morph_monkey.value, Itm.gadget_fly.value, *groups[APHelper.rc_cars.value],
        *groups[APHelper.attack.value]
    ])

    # Dash
    groups.setdefault(APHelper.dash.value, set()).update([
        Itm.gadget_hoop.value, Itm.morph_ninja.value, Itm.morph_hero.value
    ])

    # Shoot
    groups.setdefault(APHelper.shoot.value, set()).update([
        Itm.gadget_sling.value, Itm.morph_cowboy.value, Itm.morph_hero.value
    ])

    # Fly
    groups.setdefault(APHelper.fly.value, set()).update([
        Itm.gadget_fly.value, Itm.morph_ninja.value
    ])

    # Glide
    groups.setdefault(APHelper.glide.value, set()).update([
        Itm.morph_hero.value, *groups[APHelper.fly.value]
    ])

    return groups

def generate_collectables(player : int, amt : int) -> list[AE3Item]:
    """Get a list of Items of the specified Archipelago"""
    weights : list[int] = [w.weight for w in COLLECTABLES]

    result : list[CollectableItem] = random.choices([*COLLECTABLES], [*weights], k = amt)
    items : list[AE3Item] = [c.to_item(player) for c in result]
    return items