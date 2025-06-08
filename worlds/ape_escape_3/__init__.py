from typing import ClassVar, List, Optional, TextIO
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from BaseClasses import MultiWorld, Tutorial
import settings

from .data.Items import AE3Item, AE3ItemMeta, ITEMS_MASTER, Nothing, generate_collectables
from .data.Locations import Cellphone_Name_to_ID, MONKEYS_BOSSES, MONKEYS_MASTER_ORDERED, CAMERAS_MASTER_ORDERED, \
    CELLPHONES_MASTER_ORDERED, MONKEYS_PASSWORDS, MONKEYS_BREAK_ROOMS
from .data.Stages import STAGES_BREAK_ROOMS, LEVELS_BY_ORDER
from .data.Rules import GoalTarget, GoalTargetOptions, LogicPreference, LogicPreferenceOptions, PostGameCondition
from .data.Strings import Loc, Meta, APHelper, APConsole
from .data.Logic import is_goal_achieved, are_goals_achieved, Rulesets, ProgressionMode, ProgressionModeOptions
from .AE3_Options import AE3Options, create_option_groups, slot_data_options
from .Regions import create_regions
from .data import Items, Locations


# Identifier for Archipelago to recognize and run the client
def run_client(_url : Optional[str] = None):
    from .AE3_Client import launch
    launch_subprocess(launch, name="AE3Client")

components.append(
    Component(APConsole.Info.client_name.value, func = run_client, component_type = Type.CLIENT))

class AE3Settings(settings.Group):
    class GamePreferences(settings.Bool):
        """
        Preferences for game/client-enforcement behavior

        > auto-equip : Automatically assign received gadgets to a face button
        """


    class ClientPreferences(settings.Bool):
        """
        Preferences for client behavior, primarily when handling local session data saves.

        > delete_goaled : Delete session data if they have already goaled. Set this to `False` to disable.
        > delete_excess : Delete the oldest session data if the amount of saved session data exceeds a certain amount.
        Set this to `0` to disable it.
        > delete_old : Delete session data if they have not been saved into for a certain amount of days.
        Set this to `0` to disable.
        """


    auto_equip: GamePreferences | bool = False

    delete_goaled : ClientPreferences | bool = True
    delete_excess : int = 10
    delete_old : int = 30


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
    settings : AE3Settings
    web : ClassVar[WebWorld] = AE3Web()
    topology_present = True

    # Initialize Randomizer Options
    options_dataclass = AE3Options
    options : AE3Options

    # Define the Items and Locations to/for Archipelago
    item_name_to_id = Items.generate_name_to_id()
    location_name_to_id = Locations.generate_name_to_id()

    item_name_groups = Items.generate_item_groups()

    logic_preference : LogicPreference
    goal_target : GoalTarget = GoalTarget
    progression : ProgressionMode
    post_game_condition : PostGameCondition

    def __init__(self, multiworld : MultiWorld, player: int):
        self.item_pool : List[AE3Item] = []

        super(AE3World, self).__init__(multiworld, player)

    def generate_early(self):
        # Handle duplicate entries between Channel Options
        ## Remove Preserve Channels that exists in Push, Post and Blacklist Channel Options
        self.options.preserve_channel.value.difference_update(self.options.blacklist_channel)
        self.options.preserve_channel.value.difference_update(self.options.post_channel)
        self.options.preserve_channel.value.difference_update(self.options.push_channel)

        ## Remove Push Channels that exists in Post and Blacklist Channel Options
        additive : bool = "ADDITIVE" in self.options.push_channel.value
        self.options.push_channel.value.difference_update(self.options.blacklist_channel)
        self.options.push_channel.value.difference_update(self.options.post_channel)
        if additive and "ADDITIVE" not in self.options.push_channel.value:
            self.options.push_channel.value.add("ADDITIVE")

        ## Remove Post Channels that exists in Blacklist Channel Option
        self.options.post_channel.value.difference_update(self.options.blacklist_channel)

        # Get Logic Preference
        self.logic_preference = LogicPreferenceOptions[self.options.logic_preference]()

        # Get ProgressionMode
        self.progression = ProgressionModeOptions[self.options.progression_mode.value]()

        # Shuffle Channel if desired
        if self.options.shuffle_channel:
            self.progression.shuffle(self)
        # Directly Apply Channel Rules otherwise
        else:
            self.progression.reorder(-1, self.options.blacklist_channel.value)
            self.progression.reorder(-2, [*self.options.post_channel.value])
            self.progression.reorder(-3, [*self.options.push_channel.value])

        # Get Post Game Access Rule and exclude locations as necessary
        exclude_regions: list[str] = []
        exclude_locations: list[str] = []

        exclude_locations.extend(MONKEYS_PASSWORDS)

        # Exclude Blacklisted Channels
        # Exclude Channels in Post Game from being required for Post Game to be unlocked
        for channel in self.progression.order[-sum(self.progression.progression[-1:]):]:
            exclude_locations.extend(MONKEYS_MASTER_ORDERED[channel])
            exclude_locations.append(CAMERAS_MASTER_ORDERED[channel])

            excluded_phones_id: list[str] = CELLPHONES_MASTER_ORDERED[channel]
            exclude_locations.extend(Cellphone_Name_to_ID[cell_id] for cell_id in excluded_phones_id)

        # Check for Options that may override Monkeysanity Break Rooms Option
        # and exclude if not needed
        if not self.options.monkeysanity_break_rooms:
            exclude_regions.extend([*STAGES_BREAK_ROOMS])

        post_game_conditions: dict[str, int] = {}
        if self.options.post_game_condition_monkeys:
            amount: int = 434 if self.options.post_game_condition_monkeys < 0 \
                else self.options.post_game_condition_monkeys
            post_game_conditions[APHelper.monkey.value] = amount

            # Force Break Room Monkeys to be disabled on Vanilla Preset
            if self.options.post_game_condition_monkeys == -2:
                if not self.options.monkeysanity_break_rooms:
                    self.options.monkeysanity_break_rooms.value = 1
            # Respect Monkeysanity BreakRooms option otherwise
            elif not self.options.monkeysanity_break_rooms:
                exclude_regions.extend([*STAGES_BREAK_ROOMS])

        # Get Goal Target
        goal_target_index = self.options.goal_target
        self.goal_target = GoalTargetOptions[goal_target_index](self.options.goal_target_override,
                                                                [*exclude_regions], [*exclude_locations])

        if goal_target_index == 5 and not self.options.camerasanity:
            self.options.camerasanity.value = 1
        elif goal_target_index == 6 and not self.options.cellphonesanity:
            self.options.cellphonesanity.value = True
        elif goal_target_index == 7 and not self.options.shoppingsanity:
            self.options.shoppingsanity.value = 1

        # Exclude Channels in Post Game from being required for Post Game to be unlocked
        for channel in self.progression.order[-sum(self.progression.progression[-2:]):
                       -sum(self.progression.progression[-1:])]:
            exclude_locations.extend(MONKEYS_MASTER_ORDERED[channel])
            exclude_locations.append(CAMERAS_MASTER_ORDERED[channel])

            excluded_phones_id : list[str] = CELLPHONES_MASTER_ORDERED[channel]
            exclude_locations.extend(Cellphone_Name_to_ID[cell_id] for cell_id in excluded_phones_id)

        # Record remaining Post Game Condition options
        if self.options.post_game_condition_cameras:
            post_game_conditions[APHelper.camera.value] = self.options.post_game_condition_cameras.value

            # Force Camerasanity to enabled if disabled
            if not self.options.camerasanity.value:
                self.options.camerasanity.value = 1

        if self.options.post_game_condition_cellphones:
            post_game_conditions[APHelper.cellphone.value] = self.options.post_game_condition_cellphones.value

            # Force Cellphonesanity if disabled
            if not self.options.cellphonesanity:
                self.options.cellphonesanity.value = True

        if self.options.post_game_condition_shop:
            post_game_conditions[APHelper.shop.value] = self.options.post_game_condition_shop.value

            if not self.options.shoppingsanity:
                self.options.shoppingsanity.value = 1

        if self.options.post_game_condition_keys:
            post_game_conditions[APHelper.keys.value] = self.options.post_game_condition_keys.value

        self.post_game_condition = PostGameCondition(post_game_conditions, exclude_regions, exclude_locations)

        self.item_pool = []

    def create_regions(self):
        create_regions(self)

    def create_item(self, item : str) -> AE3Item:
        for itm in ITEMS_MASTER:
            if isinstance(itm, AE3ItemMeta):
                if itm.name == item:
                    return itm.to_item(self.player)

        return Nothing.to_item(self.player)

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

        equipment : List[AE3Item] = [stun_club, monkey_radar, super_hoop, slingback_shooter, water_net, rc_car,
                                  sky_flyer]

        # Push Starting Gadget as pre-collected
        if self.options.starting_gadget > 0:
            self.multiworld.push_precollected(equipment[self.options.starting_gadget - 1])
            del equipment[self.options.starting_gadget - 1]

        self.multiworld.push_precollected(monkey_net)

        # Remove any Gadgets specified in Starting Inventory
        equipment = [ gadget for gadget in equipment if gadget.name not in self.options.start_inventory]

        self.item_pool += [*equipment]

        equipment.clear()
        equipment = [knight, cowboy, ninja, magician, kungfu, hero, monkey]

        # Push Starting Morph as precollected
        if self.options.starting_morph > 0:
            self.multiworld.push_precollected(equipment[self.options.starting_morph - 1])
            del equipment[self.options.starting_morph - 1]

        # Remove any Morphs specified in Starting Inventory
        equipment = [ morph for morph in equipment if morph.name not in self.options.start_inventory]

        self.item_pool += [*equipment]

        if self.options.shuffle_chassis:
            if rc_car in self.item_pool:
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

        # Fill remaining locations with Collectables
        unfilled : int = len(self.multiworld.get_unfilled_locations(self.player)) - len(self.item_pool)
        self.item_pool += generate_collectables(self.random, self.player, unfilled)

        # Add Items to ItemPool
        self.multiworld.itempool += self.item_pool

        # Set Goal
        self.multiworld.completion_condition[self.player] = Rulesets(self.goal_target.enact()).condense(
             self.player)

    def fill_slot_data(self):
        slot_data : dict = self.options.as_dict(*slot_data_options())
        slot_data[APHelper.progression.value] = self.progression.progression
        slot_data[APHelper.channel_order.value] = self.progression.order

        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if not self.options.shuffle_channel:
            return

        spoiler_handle.write(
            f"\n\n[AE3] ============================================"
            f"\n Channel Order for {self.multiworld.get_player_name(self.player)} ({self.player})\n"
        )

        set_count = 0
        level_base = 0
        for i, channel in enumerate(self.progression.order):
            spoiler_handle.write(
                f"\n [{i + 1}]\t{LEVELS_BY_ORDER[channel]}"
            )

            if i - level_base == self.progression.progression[set_count] and i < len(self.progression.order) - 1:
                # Do not show Blacklisted Channels
                if set_count == len(self.progression.order) - 1:
                    return

                set_count += 1
                level_base = i

                if set_count < len(self.progression.progression) - 2:
                    spoiler_handle.write(f"\n- < {set_count} > ---------------------------------------")
                else:
                    tag : str = ""

                    if self.options.post_game_condition_keys:
                        tag += f"{self.options.post_game_condition_keys.value + set_count - 1}"
                    if any([bool(self.options.post_game_condition_monkeys),
                           bool(self.options.post_game_condition_cameras),
                           bool(self.options.post_game_condition_cellphones)]):
                        tag += "!"

                    spoiler_handle.write(f"\n- < {tag} > ---------------------------------------")

        spoiler_handle.write("\n")


    def generate_output(self, directory : str):
        datas = {
            "slot_data" : self.fill_slot_data()
        }