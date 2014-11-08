__author__ = 'DreTaX'
__version__ = '1.4'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
from System import *

"""
    Class
"""


class AdminCommands:

    matrix = [
     ["foot:csirke", 2, 3, 4], ]

    def AdminCmdConfig(self):
        if not Plugin.IniExists("AdminCmdConfig"):
            loc = Plugin.CreateIni("AdminCmdConfig")
            loc.Save()
        return Plugin.GetIni("AdminCmdConfig")

    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None


    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        V3.1
    """
    def CheckV(self, Player, args):
        systemname = "AdminCommands"
        p = self.GetPlayerName(String.Join(" ", args))
        if p is not None:
            return p

        count = 0
        for pl in Server.ActivePlayers:
            for namePart in args:
                if namePart.lower() in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find " + String.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found " + str(count) + " player with similar name. Use more correct name!")
            return None

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "tpto":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                Player.GroundTeleport(pl.Location)
                Player.Teleport(pl.Location)
        elif cmd.cmd == "tphere":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.GroundTeleport(Player.Location)
                pl.Teleport(Player.Location)
        elif cmd.cmd == "god":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if DataStore.Get("godmode", Player.SteamID) == 1:
                DataStore.Remove("godmode", Player.SteamID)
                Player.Message("God mode off.")
                Player.basePlayer.metabolism.health.min = 0.0
            else:
                DataStore.Add("godmode", Player.SteamID, 1)
                Player.Message("God mode on.")
                Player.basePlayer.metabolism.health.min = 100.0