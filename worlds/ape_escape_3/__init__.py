from typing import ClassVar, List

from BaseClasses import MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld

from .Options import AE3Options
from .Region import create_regions, AE3Stage
from .data.Items import AE3Item, item_table, item_group
from .data.Strings import AE3Items, AE3Locations

class AE3Web(WebWorld):
    theme = "ocean"

    tutorials = [Tutorial(
        "Multiworld Guide Setup",
        " - A guide to setting up Ape Escape 3 for Archipelago",
        "English",
        "setup.md",
        "setup/en",
        ["aidanii"]
    )]

class AE3RuntimeOptions():
    auto_equip : bool = False

class AE3World(World):
    """
    Ape Escape 3 is a 3D platformer published and developed by Sony Computer Entertainment, released 
    in 2005 for the Sony Playstation 2. Specter for the third time has escaped again, and this time,
    he and his Pipo Monkey army has taken over Television and programs anyone who watches into a 
    mindless couch potato. Even our previous heroes have fallen for the trap, and now its up to Kei
    and Yumi to save the world from the control of Specter.
    """

    game : str = "Ape Escape"
    web : ClassVar[WebWorld] = AE3Web()
    topology_present = True

    options_dataclass = AE3Options
    options = AE3Options

    def __init__(self, multiworld : MultiWorld, player : int):
        self.auto_equip : bool = False

        self.item_pool : List[AE3Item] = []

        super(AE3World, self).__init__(multiworld, player)

    def generate_early(self):
        self.auto_equip = self.options.option_auto_equip

        self.item_pool = []
    
    def create_regions(self):
        create_regions(self)
    
    # Classify Items for the Randomizer. 
    # Mark Important accordingly using the enums available in *Item Classification*
    def create_item(self, name : str) -> AE3Item:
        item_id = item_table["name"]
        classification = ItemClassification.progression

        if name in item_group["Equipment"]:
            classification = ItemClassification.filler
        
        item = AE3Item(name, classification, item_id, self.player)
        return item

    def create_items(self):
        reserved_locations : int = 0

        # Could automate this in a loop; the variable name most likely isn't important...?

        stun_club = self.create_item(AE3Items.stun_club.value)
        monkey_net = self.create_item(AE3Items.monkey_net.value)
        monkey_radar = self.create_item(AE3Items.monkey_radar.value)
        super_hoop = self.create_item(AE3Items.super_hoop.value)
        slingback_shooter = self.create_item(AE3Items.slingback_shooter.value)
        water_net = self.create_item(AE3Items.water_net.value)
        rc_car = self.create_item(AE3Items.rc_car.value)
        sky_flyer = self.create_item(AE3Items.sky_flyer.value)

        knight = self.create_item(AE3Items.morph_knight.value)
        cowboy = self.create_item(AE3Items.morph_cowboy.value)
        ninja = self.create_item(AE3Items.morph_ninja.value)
        magician = self.create_item(AE3Items.morph_magician.value)
        kungfu = self.create_item(AE3Items.morph_kungfu.value)
        hero = self.create_item(AE3Items.morph_hero.value)
        monkey = self.create_item(AE3Items.morph_monkey.value)

        gadgets : List[AE3Item] = [stun_club, monkey_radar, super_hoop, slingback_shooter, water_net, rc_car,
                                   sky_flyer]

        if self.options.option_starting_gadget > 0:
            del gadgets[self.option.option_starting_gadget - 1]
        
        if not self.option.shuffle_monkey_net:
            gadgets.append(monkey_net)

        self.item_pool += gadgets
        self.item_pool += [knight, cowboy, ninja, magician, kungfu, hero, monkey]
        
        if self.option.option_shuffle_chassis:
            chassis_twin = self.create_item(AE3Items.chassis_twin.value)
            chassis_black = self.create_item(AE3Items.chassis_black.value)
            chassis_pudding = self.create_item(AE3Items.chassis_pudding.value)

            self.item_pool += [chassis_twin, chassis_pudding, chassis_black]

        # <!> Add Items to ItemPool
        self.multiworld.itempool = self.item_pool
    
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