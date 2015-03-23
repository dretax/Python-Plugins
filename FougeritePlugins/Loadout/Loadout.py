__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System

"""
    Class
"""


class Loadout:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("Loadout by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def On_Command(self, Player, cmd, args):
        if cmd == "inv":
            if Player.Admin or self.isMod(Player.SteamID):
                inventory = Player.Inventory
                inventory.AddItem("Invisible Helmet", 1)
                inventory.AddItem("Invisible Vest", 1)
                inventory.AddItem("Invisible Pants", 1)
                inventory.AddItem("Invisible Boots", 1)