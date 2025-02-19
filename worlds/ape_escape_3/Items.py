from typing import Optional, Dict, Set

from BaseClasses import ItemClassification, Item

from .Addresses import address
from .Strings import ae3_items

class ape_escape_3_item(Item):
    game : str = "Ape Escape 3"

item_group : Dict[str, Set[str]] = {}

item_table = {
    # Gadgets
    ae3_items.stun_club.value : address.items["stun_club"],
    ae3_items.monkey_net.value : address.items["monkey_net"],
    ae3_items.monkey_radar.value : address.items["monkey_radar"],
    ae3_items.super_hoop.value : address.items["super_hoop"],
    ae3_items.rc_car.value : address.items["rc_car"],
    ae3_items.sky_flyer.value : address.items["sky_flyer"],
    ae3_items.water_net.value : address.items["water_net"],

    # Morphs
    ae3_items.knight.value : address.items["knight"],
    ae3_items.cowboy.value : address.items["cowboy"],
    ae3_items.ninja.value : address.items["ninja"],
    ae3_items.magician.value : address.items["magician"],
    ae3_items.kungfu.value : address.items["kungfu"],
    ae3_items.hero.value : address.items["hero"],
    ae3_items.monkey.value : address.items["monkey"],

    # Accessories
    ae3_items.morph_stock.value : address.items["morph_stock"],

    ae3_items.chassis_twin.value : address.items["chassis_twin"],
    ae3_items.chassis_black.value : address.items["chassis_black"],
    ae3_items.chassis_pudding.value : address.items["chassis_puding"]
}

def create_item_groups():
    # Gadgets
    for l in range(7):
        item_group.setdefault("Gadgets", []).append(item_table[l])
    
    # Morphs
    for l in range(7, 13):
        item_group.setdefault("Morphs", []).append(item_table[l])
    
    # Accessories/Chassis
    for l in range (15, 17):
        item_group.setdefault("Chassis", []).append(item_table[l])

create_item_groups()