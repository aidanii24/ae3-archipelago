from typing import TYPE_CHECKING

from BaseClasses import Region, Entrance

from .data.Locations import Location, ae3_location
from .data.Strings import ae3_stages, ae3_locations

class ae3_stage:
    def __init__(self, name : str, original_index : int):
        self.name : str = name
        self.name_as_bytes : List[bytes] = []

        self.keys : int = -1
        self.original_index : int = original_index
        self.index = -1

    def _compare_index(self, stage):
        return self.original_index < index.original_index

def create_regions(world : "Ape_Escape_3_World"):
    player = world.player
    multiworld = world.multiworld
    options = world.options

    # Menu
    menu = Region(ae3_stages.title_screen, player, multiworld)
    tv_station = Region(ae3_stages.travel_station_a, player, multiworld)
    shopping_district = Region(ae3_stages.travel_station_b, player, multiworld)

    # Channels
    zero = Region(ae3_stages.zero, player, multiworld)
    seaside = Region(ae3_stages.seaside, player, multiworld)

    # Monkeys
    ukki_pan = Region(ae3_locations.zero_ukki_pan, player, multiworld)

    nessal = Region(ae3_loqcations.seaside_nessal, player, multiworld)
    ukki_pia = Region(ae3_locations.seaside_ukki_pia, player, multiworld)
    sarubo = Region(ae3_locations.seaside_sarubo, player, multiworld)
    salurin = Region(ae3_locations.seaside_salurin, player, multiworld)
    ukkitan = Region(ae3_locations.seaside_ukkitan, player, multiworld)
    morella = Region(ae3_locations.seaside_morella, player, multiworld)
    ukki_ben = Region(ae3_locations.seaside_ukki_ben, player, multiworld)
    salurin = Region(ae3_locations.seaside_salurin, player, multiworld)

    kankichi = Region(ae3_locations.seaside_break_kankichi, player, multiworld)
    tomzeo = Region(ae3_locations.seaside_break_tomezo, player, multiworld)
    kamayan = Region(ae3_locations.seaside_break_kamayan, player, multiworld)
    taizo = Region(ae3_locations.seaside_break_taizo, player, multiworld)

    regions = [
        menu, tv_station, shopping_district,
        zero, 
        ukki_pan,
        seaside,
        nessal, ukki_pia, sarubo, salurin, ukkitan, morella, ukki_ben, salurin,
        kankichi, tomzeo, kamayan, taizo
    ]

    multiworld.regions.extend(regions)

"""
# TODO
There should be a way to automate this rather than declare each region and location one by one.
"""