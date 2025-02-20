import os
import typing

from BaseClasses import Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld

from .Options import *

class ae3_web(WebWorld):
    theme = "ocean"

    tutorials = [Tutorial(
        "Multiworld Guide Setup",
        " - A guide to setting up Ape Escape 3 for Archipelago",
        "English",
        "setup.md",
        "setup/en",
        ["aidanii"]
    )]

class ae3_runtime_options(self):
    auto_equip : bool = False

class ae3_world(World):
    """
    Ape Escape 3 is a 3D platformer published and developed by Sony Computer Entertainment, released 
    in 2005 for the Sony Playstation 2. Specter for the third time has escaped again, and this time,
    he and his Pipo Monkey army has taken over Television and programs anyone who watches into a 
    mindless couch potato. Even our previous heroes have fallen for the trap, and now its up to Kei
    and Yumi to save the world from the control of Specter.
    """

    game : str = "Ape Escape"
    web : ClassVar[WebWorld] = ae3_web()
    topology_present = True

    options_dataclass = ae3_options
    options = ae3_options

    def initialize(self):
        ae3_runtime_options.auto_equip = self.Options.auto_equip_on_unlock