Setup
=====
This guide will get your through the steps required to be able to use Ape Escape 3 Archipelago.

Prerequisite
------------
Ape Escape 3 Archipelago is simply an implementation of Ape Escape 3 into Archipelago. Please first install these required software before being able to use it.

- Archipelago (0.6.1 or higher) [[Install](https://github.com/ArchipelagoMW/Archipelago)] [[Guide](https://archipelago.gg/tutorial/Archipelago/setup/en)]
- PCSX2 Emulator (1.7 or higher) [[Install](https://pcsx2.net/downloads)] [[Guide](https://pcsx2.net/docs/category/setup)]
- Ape Escape 3 [Please acquire and dump your own copy.]
    - NTSC-U `SCUS-97501`

After installing these applications, please see our [Releases](https://github.com/aidanii24/ae3-archipelago/releases) to download the APWorld file.

Installation
------------
For most systems, simply double-click the APWorld, and Archipelago will automatically install it.

If your system does not automatically associate `.apworld` files with Archipelago, you can also install it by dragging the file into an open window of Archipelago.

To manually install an `.apworld` file, open the Archipelago install directory and create a folder named `custom_worlds` if it does not exist already. Simply place the file inside that folder and then open Archipelago.


Settings
--------
### PCSX2
This implementation interfaces with PCSX2 via its PINE connection to apply and enforce randomization and logic rules.

By default, PINE features are disabled in PCSX2. Please follow these steps to enable it:
1. Under `Tools`, check `Show Advanced Settings`.
2. Under `System`. open `Settings`
3. In the `Advanced Tab`, under the `PINE Settings` section, check `Enabled`

#### Slot
Under PINE Settings is also another field "Slot". By default, this is set to 28011. This is the default port number 
the client will search for. This can be changed if a different port number is desired.

### Client
Certain client behaviour, such as Gadget Auto-Equip and PINE Connect Offline persists between game sessions rather than 
dependent on the world's `options.yaml`. These can be configured under `host.yaml` inside the Archipelago directory.

#### PINE Connections (Advanced)
**Slot**

By default, the client will search for PCSX2 with the port number 28011. This should also be the number set in the 
PCSX2 settings under `Settings` > `Advanced` > `PINE Settings` > `Slot`. If it is desired to connect to a PCSX2 instance 
set with a different port number, the client can be directed to look for a different port number by running the 
client command `/pine_slot <slot>`, where `<slot>` is the new port number to search for. If the client is already 
connected to a different instance of PCSX2 when changing port numbers, the command `/pine_connect` must also be run 
afterward, where the client will disconnect with its current connection, and connect to the new port.

If it is known ahead of time that the client should connect to a PCSX2 instance with a different Slot number, players 
can set the `emulator_windows_preferred_port` option in their YAML options file, so that the client will automatically 
use that port once the client connects to an Archipelago Room.

**Platform (Linux)**

Under Linux, the client will search for PCSX2 connections in the XDG_RUNTIME_DIR directory. The slot number is only ever 
used in Windows, and because of this, different instances of PCSX2 will always create the same socket with the same 
filename in the same path. That is, except for the Flatpak version, which due to the containerization, will create 
another socket in a deeper directory. By default, The client will look for both, first at the base of the 
runtime directory, then the flatpak runtime directory, and will connect to the first one it finds a valid socket for. 
However, if it is desired to only connect to a specific kind of instance of PCSX2, the client command 
`/pine_platform <platform>` can be run, where `<platform>` can be either `auto`, `standard` (appimage, or other 
non-containerized installations), and `flatpak`. When set to any option other than auto, the client 
will ignore any other sockets if it is not from that platform, even if it is available.

If it is known ahead of time that the client should only connect to a specific instance of PCSX2, players can set the 
`emulator_linux_preferred_platform` option in their YAML options file, so that the client will automatically know which 
instance is preferred to be connected to upon connection to an Archipelago room

Game
----
Archipelago works with **YAML** files for user settings and options. Ape Escape 3 Archipelago also uses this to check for player preferences and to generate a game based on those preferences.

### Generation
A template YAML file is provided along the APWorld in the releases page. To create a template YAML locally, click on `Generate Template Options` in Archipelago. This will open a folder where it has generated YAML files for all the games installed.

When generating the game, the host must acquire the YAML files of all participating players and then generate a game with the APWorlds of all relevant games installed in their Archipelago. Ape Escape 3 Archipelago is not an officially supported implementation, and so any games including it must be generated locally. To generate locally, gather all the YAML files under the `players` folder in the Archipelago folder, then click `Generate`.

### Configuration
Ape Escape 3 Archipelago is very customizable in the player experience it aims to provide. For a general overview of configuring the YAML file, please refer to this [guide](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en). 

The options for configuring the game are inside the YAML files, and they are all accompanied by detailed descriptions in how they will change the game. For persistent, cross-session options, please refer to your `host.yaml` file and look under the Ape Escape 3 options. This file can be accessed by clicking the `host.yaml` button in Archipelago, or in the root of the Archipelago directory.

### Hosting
After the host has successfully generated a game, a server zip will appear in the `outputs` folder of the Archipelago directory. Once found, follow these [steps](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) from the official guides of Archipelago for hosting a game.

### Connecting
Once the host has a room ready, players must open the Archipelago Clients for their respective games and connect to the room. For Ape Escape 3 Archipelago, click the `Ape Escape 3 Archipelgo` button in Archipelago. Once the client opens, provide the URL of the room at the top of the screen and press `Connect`.

### Starting
After connecting to Archipelago, the client will begin looking for PCSX2. If PCSX2 is already open, it would have connected already. 

When starting a new game, please connect to a room before confirming a new game. You can confirm that the randomizations have taken place if you are given your starting items at the tutorial, and Aki does not introduce you to the TV Station, and instead hints on a new minigame.

Troubleshooting
---------------
### Archipelago
During installation, generation, or launching of the client, please refer to the `logs` folder in the Archipelago folder to see what errors have occurred. We always recommend using the _most recent_ version of both Archipelago and Ape Escape 3 Archipelago for the best experience.

### PCSX2
When the client cannot find PCSX2, please make sure that PINE is enabled in the advanced settings of the application.

Generally, ensure that the slot number the client is searching for (which can be checked with `/status` when 
connected to an Archipelago Room) is the same as the slot number specified in the PCSX2 Settings under `Advanced` > 
`PINE Settings` > `Slot`. If the slot the client is looking for and the slot in the PCSX2 settings, either change 
the PCSX2 Settings to use the slot the client is looking for, or direct the client to search for the slot number PCSX2 
is currently set to using the command `/pine_slot <slot>`. If the slot number under PCSX2 settings is changed during an 
active game, the game must be relaunched, either by shutting down the game, or restarting the emulator.

Under Linux, ensure that the platform the client is searching for is the version of PCSX2 being used. The platform the 
client is currently searching for can be checked by using `/status` when connected to an Archipelago room. For example, 
if the client PINE platform is set to `flatpak`, the client will only look for available connections of the flatpak 
version of PCSX2, and will ignore available connections from the appimage version of PCSX2. If the client is set to 
look for the wrong platform, this can be changed using the client command `/pine_platform`.

Reference
-----------------
For a list of available Location Groups, please refer to [this file](./location_groups.txt).

### Support
For any questions or problems regarding Ape Escape 3 Archipelago that neither official Archipelago Guides, PCSX2 Guides nor this guide can answer, please contact the developers in the Archipelago Discord Server. The Ape Escape 3 thread can be found under the future-game-design forums of the server, or simply follow this [link](https://discord.com/channels/731205301247803413/1336332485788831825).