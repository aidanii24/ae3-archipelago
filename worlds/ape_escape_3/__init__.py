import os
import typing

from BaseClasses import Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld

from .Options import ae3_options
from .Region import create_regions, ae3_stage
from .data.Strings import ae3_item, ae3_items, ae3_locations
from .data.Items import item_table, item_group

class ae3_web(WebWorld):
    theme = "ocean"

    tutorials = [Tutorial(
        "Multiworld Guide Setup",
        " - A guide to setting up Ape Escape 3 for Archipelago",
        "English",
        "setup.md",
        "setup/en",
        ["aidanii"]
    )]

class ae3_runtime_options(self):
    auto_equip : bool = False

class ae3_world(World):
    """
    Ape Escape 3 is a 3D platformer published and developed by Sony Computer Entertainment, released 
    in 2005 for the Sony Playstation 2. Specter for the third time has escaped again, and this time,
    he and his Pipo Monkey army has taken over Television and programs anyone who watches into a 
    mindless couch potato. Even our previous heroes have fallen for the trap, and now its up to Kei
    and Yumi to save the world from the control of Specter.
    """

    game : str = "Ape Escape"
    web : ClassVar[WebWorld] = ae3_web()
    topology_present = True

    options_dataclass = ae3_options
    options = ae3_options

    def generate_early(self):
        self.auto_equip = self.options.option_auto_equip

        self.itempool = []
    
    def create_regions(self):
        create_regions(self)
    
    # Classify Items for the Randomizer. 
    # Mark Important accordingly using the enums available in *Item Classification*
    def create_item(self, name : str):
        item_id = item_table["name"]
        classification = ItemClassification.progression

        if name in item_group["Equipment"]:
            classification = ItemClassification.filler
        
        item = ae3_item(name, classification, item_id, self.player)
        return item

    def create_items():
        reserved_locations : int = 0

        # Could automate this in a loop; the variable name most likely isn't important...?

        stun_club = create_item(ae3_items.stun_club)
        monkey_net = create_item(ae3_items.monkey_net)
        monkey_radar = create_item(ae3_items.monkey_radar)
        super_hoop = create_item(ae3_items.super_hoop)
        rc_car = create_item(ae3_items.rc_car)
        sky_flyer = create_item(ae3_item.sky_flyer)

        knight = create_item(ae3_items.morph_knight)
        cowboy = create_item(ae3_item.morph_cowboy)
        ninja = create_item(ae3_item.morph_ninja)
        magician = create_item(ae3_item.morph_magician)
        kungfu = create_item(ae3_item.morph_kungfu)
        hero = create_item(ae3_item.morph_hero)
        monkey = create_item(ae3_item.morph_monkey)

        gadgets : List[ae3_item] = [monkey_net, stun_club, monkey_radar, super_hoop, rc_car, sky_flyer]
        
        if self.option.option_starting_gadget > 0:
            del gadgets[self.option.option_starting_gadget]
        
        if self.option.shuffle_monkey_net:
            del gadgets[0]

        starting_gadget : int = self.option.option_starting_gadget

        self.itempool += gadgets
        self.itempool += [knight, cowboy, ninja, magician, kungfu, hero, monkey]
        
        if self.option.option_shuffle_chassis:
            chassis_twin = create_item(ae3_item.chassis_twin)
            chassis_black = create_item(ae3_item.chassis_black)
            chassis_pudding = create_item(ae3_item.chassis_pudding)

            self.itempool += [chassis_twin, chassis_pudding, chassis_black]

        # <!> Add Items to ItemPool
        self.multiworld.itempool = self.itempool
    
    def fill_slot_data(self):
        return {
            "Starting Gadget" : self.option.option_starting_gadget.value,
            "Shuffle Net" : self.option.option_shuffle_net.value,
            "Include RC Car Chassis in Randomizer" : self.option.option_shuffle_chassis,
            "Auto-equip Gadgets when obtained" : self.option.option_auto_equip
        }
    
    def generate_output(self, dir : str):
        data = {
            "slot_data" : self.fill_slot_data()
        }