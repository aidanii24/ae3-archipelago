from copy import deepcopy
from typing import ClassVar, List, Optional, TextIO
import logging

from worlds.AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Tutorial, Location
from Options import OptionError
import settings

from .data.Items import AE3Item, AE3ItemMeta, ITEMS_MASTER, Nothing, generate_collectables
from .data.Locations import Cellphone_Name_to_ID, MONKEYS_BOSSES, MONKEYS_MASTER_ORDERED, CAMERAS_MASTER_ORDERED, \
    CELLPHONES_MASTER_ORDERED, MONKEYS_PASSWORDS, MONKEYS_BREAK_ROOMS, SHOP_PROGRESSION_75COMPLETION, \
    SHOP_EVENT_ACCESS_DIRECTORY, SHOP_HINT_BOOK, SHOP_COLLECTION_HINT_BOOK, SHOP_PERSISTENT_HINT_BOOK
from .data.Stages import STAGES_BREAK_ROOMS, LEVELS_BY_ORDER, STAGES_DIRECTORY_LABEL
from .data.Rules import GoalTarget, GoalTargetOptions, LogicPreference, LogicPreferenceOptions, PostGameCondition, \
    ShopItemRules
from .data.Strings import Loc, Meta, APHelper, APConsole, Itm
from .data.Logic import is_goal_achieved, are_goals_achieved, Rulesets, ProgressionMode, ProgressionModeOptions
from .AE3_Options import AE3Options, create_option_groups, slot_data_options
from .Regions import create_regions
from .data import Items, Locations


# Load Client component for Archipelago to recognize the Client
from . import components as components

class AE3Settings(settings.Group):
    class SessionPreferences(settings.Bool):
        """
        Preferences for game session management.

        > save_state_on_room_transition: Automatically create a save state when transitioning between rooms.
        > save_state_on_item_received: Automatically create a save state when receiving a new progressive item.
        > save_state_on_location_check: Automatically create a save state when checking a new location.
        > load_state_on_connect: Load a state automatically after connecting to the multiworld if the client
        is already connected to the game and that the last save is from a save state and not a normal game save.
        """

    class SessionsPreferences(settings.Bool):
        """"""

    class GamePreferences(settings.Bool):
        """
        Preferences for game/client-enforcement behavior

        > auto-equip : Automatically assign received gadgets to a face button
        """

    class GenerationPreferences(settings.Bool):
        """
        Preferences for game generation. Only relevant for world generation and not the setup of or during play.

        > whitelist_pgc_bypass: Allow Ape Escape 3 players to enable "PGC Bypass" as a possible outcome for
        Lucky Ticket Consolation Prize.
        > whitelist_instant_goal: Allow Ape Escape 3 players to enable "Instant Goal" as a possible outcome for
        Lucky Ticket Consolation Prize.
        """

        def __len__(self):
            return len(self)

        def __getitem__(self, index):
            return self[index]

    class GenerationPreference(settings.Bool):
        """"""

        def __len__(self):
            return len(self)

        def __getitem__(self, index):
            return self[index]


    save_state_on_room_transition : SessionPreferences | bool = False
    save_state_on_item_received : SessionsPreferences | bool = True
    save_state_on_location_check : SessionsPreferences | bool = False
    load_state_on_connect : SessionsPreferences | bool = False

    auto_equip : GamePreferences | bool = True

    whitelist_pgc_bypass: GenerationPreferences | bool = False
    whitelist_instant_goal: GenerationPreference | bool = False


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
    location_name_groups = Locations.generate_location_groups()

    logic_preference : LogicPreference
    goal_target : GoalTarget = GoalTarget
    progression : ProgressionMode
    post_game_condition : PostGameCondition
    shop_rules : ShopItemRules

    exclude_locations: list

    logger: logging.Logger = logging.getLogger()

    def __init__(self, multiworld : MultiWorld, player: int):
        self.item_pool : List[AE3Item] = []

        super(AE3World, self).__init__(multiworld, player)

    def generate_early(self):
        ut_initialized: bool = self.prepare_ut()
        if ut_initialized: return

        # Limit Post/Blacklist Channels to 8 items
        if len(self.options.post_channel.value) > 8:
            additive: bool = APHelper.additive.value in self.options.post_channel
            new_post: list[str] = [*self.options.post_channel.value][:8]
            if additive:
                new_post.append(APHelper.additive.value)

            self.options.post_channel.value = {*deepcopy(new_post)}

        if len(self.options.blacklist_channel.value) > 8:
            self.options.blacklist_channel.value = self.options.blacklist_channel.value[:8]

        # Handle duplicate entries between Channel Options
        ## Remove Preserve Channels that exists in Push, Post and Blacklist Channel Options
        if self.options.preserve_channel:
            self.options.preserve_channel.value.difference_update(self.options.blacklist_channel)
            self.options.preserve_channel.value.difference_update(self.options.post_channel)
            self.options.preserve_channel.value.difference_update(self.options.push_channel)

        ## Remove Push Channels that exists in Post and Blacklist Channel Options
        if self.options.push_channel:
            additive : bool = APHelper.additive.value in self.options.push_channel.value
            self.options.push_channel.value.difference_update(self.options.blacklist_channel)
            self.options.push_channel.value.difference_update(self.options.post_channel)
            if additive and APHelper.additive.value not in self.options.push_channel.value:
                self.options.push_channel.value.add(APHelper.additive.value)

        ## Remove Post Channels that exists in Blacklist Channel Option
        if self.options.post_channel:
            self.options.post_channel.value.difference_update(self.options.blacklist_channel)

        # Get Logic Preference
        self.logic_preference = LogicPreferenceOptions[self.options.logic_preference]()
        self.logic_preference.apply_unlimited_gadget_float_rules(
            bool(self.options.hip_drop_storage_logic.value),
            bool(self.options.prolonged_quad_jump_logic.value),
        )

        if self.options.base_morph_duration.value >= 30 or self.options.add_morph_extensions.value:
            self.logic_preference.apply_timed_kung_fu_rule(
                self.options.base_morph_duration.value,
                bool(self.options.add_morph_extensions.value)
            )
            self.logic_preference.apply_timed_morph_float(
                self.options.base_morph_duration.value,
                bool(self.options.add_morph_extensions.value)
            )

        # Get ProgressionMode
        self.progression = ProgressionModeOptions[self.options.progression_mode.value](self)

        # Shuffle Channel if desired
        if self.options.shuffle_channel:
            self.progression.shuffle(self)
        # Directly Apply Channel Rules otherwise
        else:
            self.progression.reorder(-1, [*self.options.blacklist_channel.value])
            self.progression.reorder(-2, [*self.options.post_channel.value])
            self.progression.reorder(-3, [*self.options.push_channel.value])
            self.progression.regenerate_level_select_entrances()

        # Get Post Game Access Rule and exclude locations as necessary
        exclude_regions: list[str] = []
        exclude_locations: list[str] = []

        exclude_locations.extend(MONKEYS_PASSWORDS)

        # Exclude Blacklisted Channels
        # Exclude Channels in Post Game from being required for Post Game to be unlocked
        if self.progression.progression[-1]:
            for channel in self.progression.order[-self.progression.progression[-1]:]:
                exclude_locations.extend(MONKEYS_MASTER_ORDERED[channel])
                exclude_locations.append(CAMERAS_MASTER_ORDERED[channel])

                excluded_phones_id: list[str] = CELLPHONES_MASTER_ORDERED[channel]
                exclude_locations.extend(Cellphone_Name_to_ID[cell_id] for cell_id in excluded_phones_id)

        # Force-enable shoppingsanity early if required by goal target or post-game condition
        goal_target_index = self.options.goal_target.value
        if goal_target_index == 7 or self.options.post_game_condition_shop:
            if not self.options.shoppingsanity:
                self.options.shoppingsanity.value = 1

        # Exclude Shop Items based on Shoppingsanity Type and Blacklisted Channels
        if self.options.blacklist_channel.value and self.options.shoppingsanity.value > 0:
            ## Always exclude Ultim-ape Fighter Minigame if anything is blacklisted
            exclude_locations.extend(SHOP_PROGRESSION_75COMPLETION)

            ## Exclude Event/Condition-sensitive Items based on excluded levels
            blacklisted_stages = {stage for channel in self.options.blacklist_channel.value
                                  for stage in STAGES_DIRECTORY_LABEL[channel]}
            for region, item in SHOP_EVENT_ACCESS_DIRECTORY.items():
                if region in blacklisted_stages:
                    exclude_locations.extend(item)

        # Check for Options that may override Monkeysanity Break Rooms Option
        # and exclude if not needed
        if not self.options.monkeysanity_break_rooms:
            exclude_regions.extend([*STAGES_BREAK_ROOMS])

        post_game_conditions: dict[str, int] = {}
        if self.options.post_game_condition_monkeys:
            amount: int = 441 if self.options.post_game_condition_monkeys < 0 \
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
        self.goal_target = GoalTargetOptions[goal_target_index](self.options.goal_target_override,
                                                                [*exclude_regions], [*exclude_locations],
                                                                self.options.shoppingsanity.value)

        if goal_target_index == 5 and not self.options.camerasanity:
            self.options.camerasanity.value = 1
        elif goal_target_index == 6 and not self.options.cellphonesanity:
            self.options.cellphonesanity.value = True

        # Exclude Channels in Post Game from being required for Post Game to be unlocked
        post_game_start_index = sum(self.progression.progression[:-2]) + 1
        for channel in (self.progression.order[post_game_start_index :
        post_game_start_index + self.progression.progression[-2]]):
            exclude_locations.extend(MONKEYS_MASTER_ORDERED[channel])
            exclude_locations.append(CAMERAS_MASTER_ORDERED[channel])

            excluded_phones_id : list[str] = CELLPHONES_MASTER_ORDERED[channel]
            exclude_locations.extend(Cellphone_Name_to_ID[cell_id] for cell_id in excluded_phones_id)

            for region, item in SHOP_EVENT_ACCESS_DIRECTORY.items():
                if region in [*STAGES_DIRECTORY_LABEL.values()][channel]:
                    exclude_locations.extend(item)

        # Exclude Ultim-ape Fighter from being a PGC requirement, as it requires as many monkeys as possible
        exclude_locations.extend(SHOP_PROGRESSION_75COMPLETION)

        # Record remaining Post Game Condition options
        if self.options.post_game_condition_bosses:
            post_game_conditions[APHelper.bosses.value] = self.options.post_game_condition_bosses.value

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

        if self.options.post_game_condition_keys:
            post_game_conditions[APHelper.keys.value] = self.options.post_game_condition_keys.value

        self.shop_rules: ShopItemRules = ShopItemRules(self)
        if self.shop_rules.post_game_items:
            exclude_locations.extend(self.shop_rules.post_game_items)

        self.post_game_condition = PostGameCondition(post_game_conditions, exclude_regions, exclude_locations,
                                                     self.options.shoppingsanity.value)

        self.shop_rules.set_pgc_rules(self)
        self.item_pool = []

        if self.options.lucky_ticket_consolation_effects:
            current: set[str] = set(self.options.consolation_effects_whitelist)
            exclude: set[str] = set()

            if not self.settings.whitelist_pgc_bypass:
                exclude.add(APHelper.bypass_pgc.value)

            if not self.settings.whitelist_instant_goal:
                exclude.add(APHelper.instant_goal.value)

            current.difference_update(exclude)
            current.add(APHelper.nothing.value)

            self.options.consolation_effects_whitelist.value = [*current]

        self.exclude_locations = exclude_locations

        # self.log_debug()

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

        if self.options.shoppingsanity.value == 4:
            amount = self.options.restock_progression.value + self.options.extra_shop_stocks.value - 1

            self.item_pool.extend([self.create_item(APHelper.shop_stock.value)
                                   for _ in range(amount)])

        # Fill remaining locations with Collectables
        unfilled : int = len(self.multiworld.get_unfilled_locations(self.player)) - len(self.item_pool)
        if self.options.shoppingsanity.value and self.options.hints_from_hintbooks.value:
            if self.options.shoppingsanity.value == 2:
                hint_books = set([*SHOP_PERSISTENT_HINT_BOOK, *SHOP_COLLECTION_HINT_BOOK])
            else:
                hint_books = set(SHOP_HINT_BOOK)
            unfilled -= len(hint_books.difference(self.exclude_locations))

        if unfilled < 0:
            raise OptionError(
                f"AE3: Too many progression items for available locations (overflow: {-unfilled}). "
                f"Reduce extra_keys, extra_shop_stocks, or blacklisted channels.")

        self.item_pool += generate_collectables(self.random, self.player, unfilled)

        # Add Items to ItemPool
        self.multiworld.itempool += self.item_pool

        # Set Goal
        self.multiworld.completion_condition[self.player] = Rulesets(self.goal_target.enact()).condense(
             self.player)

    def pre_fill(self) -> None:
        if self.options.shoppingsanity.value and self.options.hints_from_hintbooks.value:
            if self.options.shoppingsanity.value == 2:
                hint_books = [*SHOP_PERSISTENT_HINT_BOOK, *SHOP_COLLECTION_HINT_BOOK]
            else:
                hint_books = [*SHOP_HINT_BOOK]

            for hint_book in hint_books:
                if hint_book in self.exclude_locations:
                    continue

                self.multiworld.get_location(hint_book, self.player).place_locked_item(
                    self.create_item(APHelper.hint_book.value))

    def generate_hints(self):
        hints: dict[int, dict[str, int] | list[dict[str, int]]] = {}
        progressive_scouts: list[dict[str, int]] = []
        book_scouts: list[Location] = []
        excluded_items: list[str] = [Itm.gadget_net.value, APHelper.hint_book.value]
        items: list[str] = [*self.item_name_groups[APHelper.equipment.value],
                            *self.item_name_groups[APHelper.archipelago.value]]

        if self.options.starting_gadget:
            gadgets: list[str] = [Itm.gadget_club.value,
                                  Itm.gadget_radar.value,
                                  Itm.gadget_hoop.value,
                                  Itm.gadget_sling.value,
                                  Itm.gadget_swim.value,
                                  Itm.gadget_rcc.value,
                                  Itm.gadget_fly.value]

            excluded_items.append(gadgets[self.options.starting_gadget - 1])

        if self.options.starting_morph:
            excluded_items.append(Itm.get_morphs_ordered()[self.options.starting_morph - 1])

        if self.options.shuffle_chassis:
            items.extend(Itm.get_chassis_by_id(no_default=True))

        if self.options.shuffle_morph_stocks:
            items.append(Itm.acc_morph_stock.value)

        if self.options.add_morph_extensions:
            items.append(Itm.acc_morph_ext.value)

        items = [item for item in items if item not in excluded_items]

        for item in items:
            book_scouts.extend([loc for loc in self.multiworld.find_item_locations(item, self.player)])

        # Use fillers when not enough Progressive Item Locations are scouted
        if self.options.hints_from_hintbooks and len(book_scouts) < 20:
            if self.options.lucky_ticket_consolation_effects:
                for scout in book_scouts:
                    progressive_scouts.append({"name": scout.name, "id": scout.address, "player": scout.player})

            fillers: list[str] = [Itm.jacket.value, Itm.energy_mega.value, Itm.cookie_giant.value, Itm.chip_10x.value]
            for i, filler in enumerate(fillers):
                book_scouts.extend([loc for loc in self.multiworld.find_item_locations(filler, self.player)])
                if len(book_scouts) >= 20: break

        if self.options.lucky_ticket_consolation_effects:
            if not progressive_scouts:
                for scout in book_scouts:
                    progressive_scouts.append({"name": scout.name, "id": scout.address, "player": scout.player})

            hints[0] = progressive_scouts

        if self.options.hints_from_hintbooks:
            book_scouts = self.random.sample(book_scouts, 20)

            if self.options.shoppingsanity == 2:
                hint_books = [self.location_name_to_id[book] for book in [*SHOP_COLLECTION_HINT_BOOK,
                                                                          *SHOP_PERSISTENT_HINT_BOOK]]
            else:
                hint_books = [self.location_name_to_id[book] for book in SHOP_HINT_BOOK]

            for i, loc in enumerate(book_scouts):
                hints[hint_books[i]] = {
                    "id"      : loc.address,
                    "player"  : loc.player
                }

        return hints

    def fill_slot_data(self):
        slot_data : dict = self.options.as_dict(*slot_data_options())
        slot_data[APHelper.progression.value] = self.progression.progression
        slot_data[APHelper.channel_order.value] = self.progression.order
        slot_data[APHelper.shop_progression.value] = self.shop_rules.sets

        if (self.options.shoppingsanity.value and self.options.hints_from_hintbooks.value or
                self.options.lucky_ticket_consolation_effects):
            slot_data[APHelper.hints.value] = self.generate_hints()

        slot_data[APHelper.version.value] = APConsole.Info.world_ver.value

        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(
            f"\n\n[AE3] ============================================"
            f"\n Channel Order for {self.multiworld.get_player_name(self.player)} ({self.player})\n"
        )

        group_set: list[list[int]] = []
        count: int = 0
        for i, channel_set in enumerate(self.progression.progression):
            offset: int = 0
            if i == 0:
                offset = 1

            target: int = count + channel_set + offset
            group_set.append([_ for _ in self.progression.order[count: target]])
            count = target

        count: int = 0
        for i, sets in enumerate(group_set):
            if not sets:
                continue

            if i and i < len(group_set) - 2:
                spoiler_handle.write(f"\n- < {i} > ---------------------------------------")
            elif i and i == len(group_set) - 1:
                spoiler_handle.write(f"\n- < X > ---------------------------------------")
            elif i:
                tag: str = ""

                if self.options.post_game_condition_keys:
                    tag += f"{self.options.post_game_condition_keys.value + i - 1}"
                if any([bool(self.options.post_game_condition_monkeys),
                        bool(self.options.post_game_condition_bosses),
                        bool(self.options.post_game_condition_cameras),
                        bool(self.options.post_game_condition_cellphones)]):
                    tag += "!"

                spoiler_handle.write(f"\n- < {tag} > ---------------------------------------")

            for channels in sets:
                spoiler_handle.write(f"\n [{count + 1}]\t{LEVELS_BY_ORDER[channels]}")
                count += 1

        spoiler_handle.write("\n")

    def log_debug(self):
        print("====================")
        print("Channel Order:")
        count = 0
        for lset in self.progression.progression:
            print(f"- < {count} > ---------------------")
            current = lset if count > 0 else lset + 1
            for channel in range(current):
                print(LEVELS_BY_ORDER[self.progression.order[count]])
                count += 1

        print("\nPost Game Condition:")
        for condition, amount in self.post_game_condition.amounts.items():
            print(f"\t{condition}: {amount}")

        print("\nGoal Target:")
        print(f"\t{self.goal_target.amount} / {len(self.goal_target.locations)}")
        for target in self.goal_target.locations:
            print(target)

    def generate_output(self, directory : str):
        datas = {
            "slot_data" : self.fill_slot_data()
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict) -> dict:
        return slot_data

    def prepare_ut(self) -> bool:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        is_in_ut: bool = re_gen_passthrough and self.game in re_gen_passthrough
        if is_in_ut:
            slot_data = re_gen_passthrough[self.game]
            # Re-instate important YAML Options
            self.options.blacklist_channel.value = slot_data[APHelper.blacklist_channel.value]

            self.options.monkeysanity_break_rooms.value = slot_data[APHelper.monkeysanitybr.value]
            self.options.monkeysanity_passwords.value = slot_data[APHelper.monkeysanitypw.value]
            self.options.camerasanity.value = slot_data[APHelper.camerasanity.value]
            self.options.cellphonesanity.value = slot_data[APHelper.cellphonesanity.value]
            self.options.shoppingsanity.value = slot_data[APHelper.shoppingsanity.value]

            self.options.restock_progression.value = slot_data[APHelper.restock_progression.value]
            self.options.cheap_items_minimum_requirement.value = slot_data[APHelper.cheap_items_min.value]
            self.options.cheap_items_early_amount.value = slot_data[APHelper.cheap_items_early_amount.value]
            self.options.farm_logic_sneaky_borgs.value = slot_data[APHelper.farm_logic_sneaky_borgs.value]

            self.options.early_free_play.value = slot_data[APHelper.early_free_play.value]

            # Regenerate Logic Preference
            self.logic_preference = LogicPreferenceOptions[slot_data[APHelper.logic_preference.value]]()
            self.logic_preference.apply_unlimited_gadget_float_rules(
                bool(slot_data[APHelper.hds_logic.value]),
                bool(slot_data[APHelper.pqj_logic.value]),
            )

            if self.options.base_morph_duration.value >= 30 or self.options.add_morph_extensions.value:
                self.logic_preference.apply_timed_kung_fu_rule(
                    self.options.base_morph_duration.value,
                    bool(self.options.add_morph_extensions.value)
                )
                self.logic_preference.apply_timed_morph_float(
                    self.options.base_morph_duration.value,
                    bool(self.options.add_morph_extensions.value)
                )

            if slot_data[APHelper.base_morph_duration.value] >= 30 or slot_data[APHelper.add_morph_extensions.value]:
                self.logic_preference.apply_timed_kung_fu_rule(
                    slot_data[APHelper.base_morph_duration.value],
                    bool(slot_data[APHelper.add_morph_extensions.value])
                )
                self.logic_preference.apply_timed_morph_float(
                    slot_data[APHelper.base_morph_duration.value],
                    bool(slot_data[APHelper.add_morph_extensions.value])
                )

            # Regenerate Progression, Goal Target, PGC and Rules
            ## Progression Mode
            if APHelper.progression_mode.value in slot_data:
                self.progression = ProgressionModeOptions[slot_data[APHelper.progression_mode.value]]()

                ## Progression
                if APHelper.progression.value in slot_data and self.progression:
                    self.progression.set_progression(slot_data[APHelper.progression.value])

                ## Channel Order
                if APHelper.channel_order.value in slot_data and self.progression:
                    self.progression.set_order(slot_data[APHelper.channel_order.value])

                self.progression.regenerate_level_select_entrances()


            # Get initial exclusions for Goal Target
            excluded_stages: list[str] = []
            excluded_locations: list[str] = [*MONKEYS_PASSWORDS]

            # Exclude Shop Items based on Shoppingsanity Type and Blacklisted Channels
            if slot_data[APHelper.blacklist_channel.value] and slot_data[APHelper.shoppingsanity.value] > 0:
                ## Always exclude Ultim-ape Fighter Minigame if anything is blacklisted
                excluded_locations.extend(SHOP_PROGRESSION_75COMPLETION)

                ## Exclude Event/Condition-sensitive Items based on excluded levels
                for region, item in SHOP_EVENT_ACCESS_DIRECTORY.items():
                    if region in slot_data[APHelper.blacklist_channel.value]:
                        excluded_locations.extend(item)

            if not self.options.monkeysanity_break_rooms:
                excluded_stages.extend([*STAGES_BREAK_ROOMS])

            ### Exclude Blacklisted Channels from Goal Target and Post Game Condition
            if self.progression.progression[-1]:
                for channel in self.progression.order[-self.progression.progression[-1]:]:
                    excluded_locations.extend(MONKEYS_MASTER_ORDERED[channel])
                    excluded_locations.append(CAMERAS_MASTER_ORDERED[channel])

                    excluded_phones_id: list[str] = CELLPHONES_MASTER_ORDERED[channel]
                    excluded_locations.extend(Cellphone_Name_to_ID[cell_id] for cell_id in excluded_phones_id)

            # Exclude Ultim-ape Fighter if any blacklisted channels exist
            if self.progression.progression[-1]:
                excluded_locations.extend(SHOP_PROGRESSION_75COMPLETION)

            goal_amount: int = 0
            if APHelper.goal_target_ovr.value in slot_data:
                goal_amount: int = slot_data[APHelper.goal_target_ovr.value]

            # Goal Target
            if APHelper.goal_target.value in slot_data:
                goal_target = slot_data[APHelper.goal_target.value]
                self.goal_target = GoalTargetOptions[goal_target](goal_amount,
                                                                  excluded_stages,
                                                                  excluded_locations,
                                                                  self.options.shoppingsanity.value)

                ## Get Post Game Conditions
                amounts: dict[str, int] = {}

                if APHelper.pgc_monkeys.value in slot_data and slot_data[APHelper.pgc_monkeys.value]:
                    amount: int = 434 if slot_data[APHelper.pgc_monkeys.value] < 0 \
                        else slot_data[APHelper.pgc_monkeys.value]
                    amounts[APHelper.monkey.value] = amount

                if APHelper.pgc_bosses.value in slot_data and slot_data[APHelper.pgc_bosses.value]:
                    amounts[APHelper.bosses.value] = slot_data[APHelper.pgc_bosses.value]

                if APHelper.pgc_cameras.value in slot_data and slot_data[APHelper.pgc_cameras.value]:
                    amounts[APHelper.camera.value] = slot_data[APHelper.pgc_cameras.value]

                if APHelper.pgc_cellphones.value in slot_data and slot_data[APHelper.pgc_cellphones.value]:
                    amounts[APHelper.cellphone.value] = slot_data[APHelper.pgc_cellphones.value]

                if APHelper.pgc_shop.value in slot_data and slot_data[APHelper.pgc_shop.value]:
                    amounts[APHelper.shop.value] = slot_data[APHelper.pgc_shop.value]

                if APHelper.pgc_keys.value in slot_data and slot_data[APHelper.pgc_keys.value]:
                    amounts[APHelper.keys.value] = slot_data[APHelper.pgc_keys.value]

                # Exclude Channels in Post Game from being required for Post Game to be unlocked
                post_game_start_index = sum(self.progression.progression[:-2]) + 1
                for channel in (self.progression.order[post_game_start_index:
                post_game_start_index + self.progression.progression[-2]]):
                    excluded_locations.extend(MONKEYS_MASTER_ORDERED[channel])
                    excluded_locations.append(CAMERAS_MASTER_ORDERED[channel])

                    excluded_phones_id: list[str] = CELLPHONES_MASTER_ORDERED[channel]
                    excluded_locations.extend(Cellphone_Name_to_ID[cell_id] for cell_id in excluded_phones_id)

                # Exclude Ultim-ape Fighter from being a PGC requirement, as it requires as many monkeys as possible
                excluded_locations.extend(SHOP_PROGRESSION_75COMPLETION)

                ## Post Game Access Rule Initialization
                self.post_game_condition = PostGameCondition(amounts, excluded_stages, excluded_locations)

                ## Set up Shop Rules
                self.shop_rules: ShopItemRules = ShopItemRules(self)
                if self.shop_rules.post_game_items:
                    excluded_locations.extend(self.shop_rules.post_game_items)

                self.post_game_condition = PostGameCondition(amounts, excluded_stages, excluded_locations,
                                                             self.options.shoppingsanity.value)

                # Set Shop Rules PGC
                self.shop_rules.set_pgc_rules(self)

                # Store excluded locations
                self.exclude_locations = excluded_locations

        return is_in_ut