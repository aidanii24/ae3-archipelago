from typing import ClassVar, List, Optional

from BaseClasses import MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type

from .data.Items import AE3Item, Chassis_Pudding, Nothing, Channel_Key, Victory, generate_collectables
from .data.Strings import Loc, Meta, APHelper, APConsole
from .data.Logic import is_goal_achieved, are_goals_achieved, ProgressionMode
from .AE3_Options import AE3Options, create_option_groups, slot_data_options
from .Regions import create_regions
from .data import Items, Locations


# Identifier for Archipelago to recognize and run the client
def run_client(_url : Optional[str] = None):
    from .AE3_Client import launch
    launch_subprocess(launch, name="AE3Client")

components.append(
    Component(APConsole.Info.client_name.value, func = run_client, component_type = Type.CLIENT))

class AE3Web(WebWorld):
    theme = "ocean"
    option_groups = create_option_groups()

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
    game = Meta.game
    web : ClassVar[WebWorld] = AE3Web()
    topology_present = True

    # Initialize Randomizer Options
    options_dataclass = AE3Options
    options : AE3Options

    # Define the Items and Locations to/for Archipelago
    item_name_to_id = Items.generate_name_to_id()
    location_name_to_id = Locations.generate_name_to_id()

    item_name_groups = Items.generate_item_groups()

    progression : ProgressionMode

    def __init__(self, multiworld : MultiWorld, player: int):
        self.auto_equip : bool = False

        self.item_pool : List[AE3Item] = []

        super(AE3World, self).__init__(multiworld, player)

    def generate_early(self):
        self.auto_equip = self.options.auto_equip
        self.progression = ProgressionMode.get_progression_mode(self.options.progression_mode.value)

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

        # <!> Push important items early for easy testing
        self.multiworld.push_precollected(ninja)
        #
        # self.multiworld.push_precollected(Channel_Key.to_item(self.player))
        # self.get_location(Loc.zero_ukki_pan.value).place_locked_item(Channel_Key.to_item(self.player))
        # self.get_location(Loc.seaside_ukkitan.value).place_locked_item(Channel_Key.to_item(self.player))
        # self.get_location(Loc.seaside_ukki_pia.value).place_locked_item(Channel_Key.to_item(self.player))
        # self.get_location(Loc.seaside_nessal.value).place_locked_item(Channel_Key.to_item(self.player))
        # self.get_location(Loc.seaside_salurin.value).place_locked_item(Channel_Key.to_item(self.player))
        # self.get_location(Loc.seaside_sarubo.value).place_locked_item(Channel_Key.to_item(self.player))
        # self.get_location(Loc.seaside_morella.value).place_locked_item(Channel_Key.to_item(self.player))
        # self.get_location(Loc.seaside_ukki_ben.value).place_locked_item(Channel_Key.to_item(self.player))

        self.get_location(Loc.seaside_ukkitan.value).place_locked_item(Chassis_Pudding.to_item(self.player))

        equipment : List[AE3Item] = [stun_club, monkey_radar, super_hoop, slingback_shooter, water_net, rc_car,
                                  sky_flyer]

        # Push Starting Gadget as pre-collected
        if self.options.starting_gadget > 0:
            self.multiworld.push_precollected(equipment[self.options.starting_gadget - 1])
            del equipment[self.options.starting_gadget - 1]

        self.multiworld.push_precollected(monkey_net)

        self.item_pool += [*equipment]

        equipment.clear()
        equipment = [knight, cowboy, ninja, magician, kungfu, hero, monkey]

        # Push Starting Morph as precollected
        if self.options.starting_morph > 0:
            self.multiworld.push_precollected(equipment[self.options.starting_morph - 1])
            del equipment[self.options.starting_morph - 1]

        self.item_pool += [*equipment]

        if self.options.shuffle_chassis:
            self.item_pool.remove(rc_car)

            chassis_twin = Items.Chassis_Twin.to_item(self.player)
            chassis_black = Items.Chassis_Black.to_item(self.player)
            chassis_pudding = Items.Chassis_Pudding.to_item(self.player)

            self.item_pool += [chassis_twin, chassis_pudding, chassis_black]

        # Add Upgradeables
        if self.options.shuffle_morph_stocks:
            self.item_pool += Items.Acc_Morph_Stock.to_items(self.player)

        if self.options.add_morph_extensions:
            self.item_pool += Items.Acc_Morph_Ext.to_items(self.player)

        # Add Archipelago Items
        self.item_pool += self.progression.generate_keys(self)

        # Manually Set Items
        self.get_location(Loc.boss_specter.value).place_locked_item(Victory.to_item(self.player))

        # <!> DEBUG - Temporarily preset Password Monkeys with Nothing Items for now
        self.get_location(Loc.castle_sal_1000.value).place_locked_item(Nothing.to_item(self.player))
        self.get_location(Loc.woods_spork.value).place_locked_item(Nothing.to_item(self.player))
        self.get_location(Loc.snowfesta_pipotron_yellow.value).place_locked_item(Nothing.to_item(self.player))
        self.get_location(Loc.toyhouse_pipotron_red.value).place_locked_item(Nothing.to_item(self.player))
        self.get_location(Loc.hong_dark_master.value).place_locked_item(Nothing.to_item(self.player))
        self.get_location(Loc.space_sal_3000.value).place_locked_item(Nothing.to_item(self.player))

        # Fill remaining locations with Collectables
        unfilled : int = len(self.multiworld.get_unfilled_locations()) - len(self.item_pool)
        self.item_pool += generate_collectables(self.player, unfilled)

        # Set Win Condition
        self.multiworld.completion_condition[self.player] = lambda state : is_goal_achieved(state, self.player)

        # Add Items to ItemPool
        self.multiworld.itempool = self.item_pool

    def fill_slot_data(self):
        return self.options.as_dict(*slot_data_options())

    def generate_output(self, directory : str):
        datas = {
            "slot_data" : self.fill_slot_data()
        }