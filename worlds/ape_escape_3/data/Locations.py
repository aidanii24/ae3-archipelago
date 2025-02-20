from typing import Optional, Dict, Set

from BaseClasses import Location

from .Strings import ae3_locations

class ae3_location(Location):
    game : str = "Ape Escape 3"

location_table = {
    # Monkeys

    ## TV Station/Zero
    ae3_locations.zero_ukki_pan : 0,

    ## Seaside Resort
    ae3_locations.seaside_nessal.value : 1,
    ae3_locations.seaside_ukki_pia.value : 2,
    ae3_locations.seaside_sarubo.value : 3,
    ae3_locations.seaside_salurin.value : 4,
    ae3_locations.seaside_ukkitan.value : 5,
    ae3_locations.seaside_morella.value : 6,
    ae3_locations.seaside_ukki_ben.value : 7,
    ae3_locations.seaside_break_kankichi.value : 8,
    ae3_locations.seaside_break_tomezo.value : 9,
    ae3_locations.seaside_break_kamayan.value : 10,
    ae3_locations.seaside_break_taizo.value : 11
}