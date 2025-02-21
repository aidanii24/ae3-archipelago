from typing import Optional, Dict, Set

from BaseClasses import ItemClassification, Item

from Addresses import address
from Strings import ae3_items

class ae3_item(Item):
    game : str = "Ape Escape 3"

item_group : Dict[str, Set[str]] = {}

item_table = {
    # Gadgets
    ae3_items.stun_club.value : address.items["stun_club"],
    ae3_items.monkey_net.value : address.items["monkey_net"],
    ae3_items.monkey_radar.value : address.items["monkey_radar"],
    ae3_items.super_hoop.value : address.items["super_hoop"],
    ae3_items.water_net.value : address.items["water_net"],
    ae3_items.slingback_shooter.value : address.items["slingback_shooter"],
    ae3_items.rc_car.value : address.items["rc_car"],
    ae3_items.sky_flyer.value : address.items["sky_flyer"],

    # Morphs
    ae3_items.morph_knight.value : address.items["morph_knight"],
    ae3_items.morph_cowboy.value : address.items["morph_cowboy"],
    ae3_items.morph_ninja.value : address.items["morph_ninja"],
    ae3_items.morph_magician.value : address.items["morph_magician"],
    ae3_items.morph_kungfu.value : address.items["morph_kungfu"],
    ae3_items.morph_hero.value : address.items["morph_hero"],
    ae3_items.morph_monkey.value : address.items["morph_monkey"],

    # Accessories
    ae3_items.acc_morph_stock.value : address.items["acc_morph_stock"],

    ae3_items.pellet_explosive.value : address.items["pellet_explosive"],
    ae3_items.pellet_guided.value : address.items["pellet_guided"],

    ae3_items.chassis_twin.value : address.items["chassis_twin"],
    ae3_items.chassis_black.value : address.items["chassis_black"],
    ae3_items.chassis_pudding.value : address.items["chassis_puding"]
}

def create_item_groups():
    keys : List[str] = list(item_table)

    # Gadgets
    for l in range(8):
        item_group.setdefault("Gadgets", []).append(keys[l])
    
    # Morphs
    for l in range(8, 14):
        item_group.setdefault("Morphs", []).append(keys[l])
    
    # Equipment
    item_group.setdefault("Equipment", []).append(item_group["Gadgets"])
    item_group.setdefault("Equipment", []).append(item_group["Morphs"])
    
    # Accessories
    for l in range (16, 17):
        item_group.setdefault("Pellets", []).append(keys[l])
    
    for l in range (18, 20):
        item_group.setdefault("Chassis", []).append(keys[l])

create_item_groups()