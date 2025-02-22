from BaseClasses import Location

from .Strings import AE3Locations


class AE3Location(Location):
    """
        Defines a Location in Ape Escape 3. This refers to points of interest for the randomizer, such as Monkeys,
        Cellphones, Cameras and Points of Interests in the Hub.
    """

    game : str = "Ape Escape 3"

location_table = {
    # Monkeys

    ## TV Station/Zero
    AE3Locations.zero_ukki_pan.value : 0,

    ## Seaside Resort
    AE3Locations.seaside_nessal.value : 1,
    AE3Locations.seaside_ukki_pia.value : 2,
    AE3Locations.seaside_sarubo.value : 3,
    AE3Locations.seaside_salurin.value : 4,
    AE3Locations.seaside_ukkitan.value : 5,
    AE3Locations.seaside_morella.value : 6,
    AE3Locations.seaside_ukki_ben.value : 7,
    AE3Locations.seaside_break_kankichi.value : 8,
    AE3Locations.seaside_break_tomezo.value : 9,
    AE3Locations.seaside_break_kamayan.value : 10,
    AE3Locations.seaside_break_taizo.value : 11
}