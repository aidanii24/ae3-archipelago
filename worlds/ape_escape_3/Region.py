from typing import List

from BaseClasses import Region, Entrance

from .data.Strings import AE3Stages, AE3Locations
from .data.Locations import AE3Location
from .data.Addresses import Address
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

def create_regions(world : AE3World):
    player = world.player
    multiworld = world.multiworld
    options = world.options

    # Menu
    menu = Region(AE3Stages.title_screen.value, player, multiworld)
    tv_station = Region(AE3Stages.travel_station_a.value, player, multiworld)
    shopping_district = Region(AE3Stages.travel_station_b.value, player, multiworld)

    # Channels
    zero = Region(AE3Stages.zero.value, player, multiworld)
    seaside = Region(AE3Stages.seaside.value, player, multiworld)

    # Monkeys
    zero_ukki_pan = Region(AE3Locations.zero_ukki_pan.value, player, multiworld)

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

    # Establish Basic Region Connections
    ## Connect Regions that will always be fixed (The Tutorial level and Hub World rooms)
    tv_station.connect(shopping_district)
    zero.add_exits(tv_station.name)

    regions = [
        menu, tv_station, shopping_district,
        zero, 
        zero_ukki_pan,
        seaside,
        seaside_nessal, seaside_ukki_pia, seaside_sarubo, seaside_salurin, seaside_ukkitan, seaside_morella,
        seaside_ukki_ben, seaside_salurin,
        seaside_break_kankichi, seaside_break_tomzeo, seaside_break_kamayan, seaside_break_taizo
    ]

    # Add Locations to the Regions
    region : Region
    for region in regions:
        if region.name in AE3Locations:
            region.locations.append(AE3Location(player, region.name, Address.locations[region.name], region))

    multiworld.regions.extend(regions)

"""
# TODO
There should be a way to automate this rather than declare each region and location one by one.
"""