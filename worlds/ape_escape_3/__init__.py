from typing import ClassVar, List, Optional

from BaseClasses import MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type

from .AE3_Options import AE3Options
from .Regions import create_regions
from .data import Items, Locations
from .data.Items import AE3Item
from .data.Locations import location_table
from .data.Strings import Meta, APConsole

# Identifier for Archipelago to recognize and run the client
def run_client(_url : Optional[str] = None):
    from .AE3_Client import launch
    launch_subprocess(launch, name="AE3Client")

components.append(
    Component(APConsole.Info.client_name.value, func = run_client, component_type = Type.CLIENT))

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


class AE3World(World):
    """
    Ape Escape 3 is a 3D platformer published and developed by Sony Computer Entertainment, released 
    in 2005 for the Sony Playstation 2. Specter for the third time has escaped again, and this time,
    he and his Pipo Monkey army has taken over Television and programs anyone who watches into a 
    mindless couch potato. Even our previous heroes have fallen for the trap, and now its up to Kei
    and Yumi to save the world from the control of Specter.
    """

    # Define Basic Game Parameters
    game = Meta.game.value
    web : ClassVar[WebWorld] = AE3Web()
    topology_present = True

    # Initialize Randomizer Options
    options_dataclass = AE3Options
    options = AE3Options  # Purely for Type Hints; not logically significant

    # Define the Items and Locations to/for Archipelago
    item_name_to_id = Items.generate_name_to_id()
    location_name_to_id = Locations.generate_name_to_id()

    item_name_groups = Items.generate_item_groups()

    def __init__(self, multiworld : MultiWorld, player: int):
        self.auto_equip : bool = False

        self.item_pool : List[AE3Item] = []

        super(AE3World, self).__init__(multiworld, player)

    def generate_early(self):
        self.auto_equip = self.options.AutoEquip

        self.item_pool = []

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        # Define Items
        stun_club = Items.Gadget_Club.to_item(self.player)
        monkey_net = Items.Gadget_Net.to_item(self.player)
        monkey_radar = Items.Gadget_Radar.to_item(self.player)
        super_hoop = Items.Gadget_Hoop.to_item(self.player)
        slingback_shooter = Items.Gadget_Sling.to_item(self.player)
        water_net = Items.Gadget_Swim.to_item(self.player)
        rc_car = Items.Gadget_RCC.to_item(self.player)
        sky_flyer = Items.Gadget_Fly.to_item(self.player)

        knight = Items.Morph_Knight.to_item(self.player)
        cowboy = Items.Morph_Cowboy.to_item(self.player)
        ninja = Items.Morph_Ninja.to_item(self.player)
        magician = Items.Morph_Magician.to_item(self.player)
        kungfu = Items.Morph_Kungfu.to_item(self.player)
        hero = Items.Morph_Hero.to_item(self.player)
        monkey = Items.Morph_Monkey.to_item(self.player)

        gadgets : List[AE3Item] = [stun_club, monkey_radar, super_hoop, slingback_shooter, water_net, rc_car,
                                  sky_flyer]

        # Push Starting Gadget as pre-collected
        if self.options.StartingGadget > 0:
            self.multiworld.push_precollected(gadgets[self.options.StartingGadget - 1])
            del gadgets[self.options.StartingGadget - 1]

        self.multiworld.push_precollected(monkey_net)

        self.item_pool += gadgets
        self.item_pool += [cowboy, ninja, magician, kungfu, hero, monkey]

        if self.options.ShuffleChassis:
            chassis_twin = Items.Chassis_Twin.to_item(self.player)
            chassis_black = Items.Chassis_Black.to_item(self.player)
            chassis_pudding = Items.Chassis_Pudding.to_item(self.player)

            self.item_pool += [chassis_twin, chassis_pudding, chassis_black]

        # Add Items to ItemPool
        self.multiworld.itempool = self.item_pool

    def fill_slot_data(self):
        return {
            "Starting Gadget" : self.options.StartingGadget.value,
            "Include RC Car Chassis in Randomizer" : self.options.ShuffleChassis.value,
            "Auto-equip Gadgets when obtained" : self.options.AutoEquip.value
        }

    def generate_output(self, dir : str):
        data = {
            "slot_data" : self.fill_slot_data()
        }