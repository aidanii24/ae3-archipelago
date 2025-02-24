from typing import Callable, List, TYPE_CHECKING

from BaseClasses import Region, Entrance, CollectionState

from .data import Logic
from .data.Strings import AE3Stages, AE3Locations
from .data.Locations import AE3Location, location_table
from .data.Addresses import Address

if TYPE_CHECKING:
    from . import AE3World


class AE3Stage:
    """
        Defines a Stage in Ape Escape 3. This refers to any area or room in the game, most commonly, the levels, or
        "channels", but also includes the title screen and hub world.
    """

    def __init__(self, name : str, entrance : Entrance, original_index : int):
        self.name : str = name
        self.name_as_bytes : List[bytes] = []

        self.entrance : Entrance = entrance
        self.keys: int = -1

        self.original_index : int = original_index
        self.index : int = -1

    def _compare_index(self, stage):
        return self.original_index < stage.original_index

def connect_regions(player : int, start : Region, dest : Region, rule = None):
    connection : Entrance = Entrance(player, start.name + " <> " + dest.name)

    if rule:
        connection.access_rule = rule

    start.exits.append(connection)
    connection.connect(dest)

def create_regions(world : "AE3World"):
    player = world.player
    multiworld = world.multiworld
    options = world.options

    # Generate AccessRules for Locations
    def generate_access_rules(loc : AE3Location) -> Callable[[CollectionState], bool]:
        def access_rule(state : CollectionState) -> bool:
            ## No rules mean there is no prerequisite for access; Return true
            if loc.rules.Critical is None and loc.rules.Rules is None:
                return True

            ## Any Critical Rules that return False should immediately mark the item as inaccessible with
            ## the current state
            if loc.rules.Critical:
                for rule in loc.rules.Critical:
                    if not rule(state, player):
                        return False

            ## At least one set of normal rules (if any) must return true to mark the item as reachable
            if not loc.rules.Rules:
                return None

            reachable: bool = False

            for ruleset in loc.rules.Rules:
                set_reachable: bool = False

                for rule in ruleset:
                    rule(state, player)

                reachable = reachable or set_reachable

            return reachable
        return access_rule

    #Create Regions
    ## Menu
    menu = Region(AE3Stages.title_screen.value, player, multiworld)
    tv_station = Region(AE3Stages.travel_station_a.value, player, multiworld)
    shopping_district = Region(AE3Stages.travel_station_b.value, player, multiworld)

    ## Channels
    zero = Region(AE3Stages.zero.value, player, multiworld)

    seaside_a = Region(AE3Stages.seaside_a.value, player, multiworld)
    seaside_b = Region(AE3Stages.seaside_b.value, player, multiworld)
    seaside_c = Region(AE3Stages.seaside_c.value, player, multiworld)

    ## Monkeys
    seaside_nessal = Region(AE3Locations.seaside_nessal.value, player, multiworld)
    seaside_ukki_pia = Region(AE3Locations.seaside_ukki_pia.value, player, multiworld)
    seaside_sarubo = Region(AE3Locations.seaside_sarubo.value, player, multiworld)
    seaside_salurin = Region(AE3Locations.seaside_salurin.value, player, multiworld)
    seaside_ukkitan = Region(AE3Locations.seaside_ukkitan.value, player, multiworld)
    seaside_morella = Region(AE3Locations.seaside_morella.value, player, multiworld)
    seaside_ukki_ben = Region(AE3Locations.seaside_ukki_ben.value, player, multiworld)

    seaside_break_kankichi = Region(AE3Locations.seaside_break_kankichi.value, player, multiworld)
    seaside_break_tomzeo = Region(AE3Locations.seaside_break_tomezo.value, player, multiworld)
    seaside_break_kamayan = Region(AE3Locations.seaside_break_kamayan.value, player, multiworld)
    seaside_break_taizo = Region(AE3Locations.seaside_break_taizo.value, player, multiworld)

    # Establish Specific Region Connections
    ## Menu
    menu.connect(tv_station)

    ## Hub
    connect_regions(player, tv_station, shopping_district)

    ## Seaside Resort
    connect_regions(player, tv_station, seaside_a)
    connect_regions(player, seaside_a, seaside_b)
    connect_regions(player, seaside_a, seaside_c, lambda state : Logic.can_use_monkey(state, player))

    connect_regions(player, seaside_a, seaside_nessal, lambda state : Logic.can_catch(state, player))
    connect_regions(player, seaside_a, seaside_ukki_pia, lambda state : Logic.can_catch(state, player))
    connect_regions(player, seaside_a, seaside_sarubo, lambda state : Logic.can_catch(state, player))
    connect_regions(player, seaside_a, seaside_salurin, lambda state : Logic.can_catch(state, player))
    connect_regions(player, seaside_a, seaside_ukkitan, lambda state : Logic.can_catch(state, player))
    connect_regions(player, seaside_a, seaside_morella, lambda state :
                                                        Logic.can_catch(state, player) and
                                                        Logic.can_shoot_free(state, player))
    connect_regions(player, seaside_b, seaside_ukki_ben, lambda state : Logic.can_catch(state, player))

    connect_regions(player, seaside_c, seaside_break_kankichi, lambda state :
                                                        Logic.can_catch(state, player) and
                                                        Logic.can_use_monkey(state, player))
    connect_regions(player, seaside_c, seaside_break_tomzeo, lambda state:
                                                        Logic.can_catch(state, player) and
                                                        Logic.can_use_monkey(state, player))
    connect_regions(player, seaside_c, seaside_break_kamayan, lambda state:
                                                        Logic.can_catch(state, player) and
                                                        Logic.can_use_monkey(state, player))
    connect_regions(player, seaside_c, seaside_break_taizo, lambda state:
                                                        Logic.can_catch(state, player) and
                                                        Logic.can_use_monkey(state, player))

    regions = [
        menu,
        tv_station, shopping_district,
    ]

    if not world.options.option_shuffle_net:
        zero_ukki_pan = Region(AE3Locations.zero_ukki_pan.value, player, multiworld)

        connect_regions(player, menu, zero_ukki_pan)
        connect_regions(player, zero_ukki_pan, tv_station)

        regions += [zero_ukki_pan]

    regions += [
        seaside_a, seaside_b, seaside_c,
        seaside_nessal, seaside_ukki_pia, seaside_sarubo, seaside_salurin, seaside_ukkitan, seaside_morella,
        seaside_ukki_ben,
        seaside_break_kankichi, seaside_break_tomzeo, seaside_break_kamayan, seaside_break_taizo
    ]

    # Check Regions
    region : Region
    for region in regions:
        ## Connect TV Station to all starting areas
        if "Outside" in region.name:
            region.connect(tv_station)

        ## Confirm Location
        if region.name in AE3Locations:
            location : AE3Location = AE3Location(player, region.name, Address.locations[region.name], region)

            ## Add Locations to their dedicated Region and confirm their AccessRules
            if region.name in location_table:
                if location.rules:
                    location.access_rule = generate_access_rules(location)
                region.locations.append(location)

    multiworld.regions.extend(regions)

    # Connection Diagrams
    from Utils import visualize_regions
    visualize_regions(multiworld.get_region("Menu", player), "_region_diagram.puml")

"""
# TODO
There should be a way to automate this rather than declare each region and location one by one.
"""