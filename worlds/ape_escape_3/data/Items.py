from typing import Dict, Set, List

from BaseClasses import ItemClassification, Item

from Addresses import Address
from Strings import AE3Items

class AE3Item(Item):
    """
    Defines an Item in Ape Escape 3. These include but are not limited to the Gadgets, Morphs and select buyable items
    in the Shopping District.
    """

    game : str = "Ape Escape 3"

item_group : Dict[str, Set[str]] = {}

item_table = {
    # Gadgets
    AE3Items.stun_club.value : Address.items["stun_club"],
    AE3Items.monkey_net.value : Address.items["monkey_net"],
    AE3Items.monkey_radar.value : Address.items["monkey_radar"],
    AE3Items.super_hoop.value : Address.items["super_hoop"],
    AE3Items.water_net.value : Address.items["water_net"],
    AE3Items.slingback_shooter.value : Address.items["slingback_shooter"],
    AE3Items.rc_car.value : Address.items["rc_car"],
    AE3Items.sky_flyer.value : Address.items["sky_flyer"],

    # Morphs
    AE3Items.morph_knight.value : Address.items["morph_knight"],
    AE3Items.morph_cowboy.value : Address.items["morph_cowboy"],
    AE3Items.morph_ninja.value : Address.items["morph_ninja"],
    AE3Items.morph_magician.value : Address.items["morph_magician"],
    AE3Items.morph_kungfu.value : Address.items["morph_kungfu"],
    AE3Items.morph_hero.value : Address.items["morph_hero"],
    AE3Items.morph_monkey.value : Address.items["morph_monkey"],

    # Accessories
    AE3Items.acc_morph_stock.value : Address.items["acc_morph_stock"],

    AE3Items.pellet_explosive.value : Address.items["pellet_explosive"],
    AE3Items.pellet_guided.value : Address.items["pellet_guided"],

    AE3Items.chassis_twin.value : Address.items["chassis_twin"],
    AE3Items.chassis_black.value : Address.items["chassis_black"],
    AE3Items.chassis_pudding.value : Address.items["chassis_puding"]
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