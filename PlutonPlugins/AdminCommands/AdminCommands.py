__author__ = 'DreTaX'
__version__ = '1.3a'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
from System import *

"""
    Class
"""


class AdminCommands:

    def AdminCmdConfig(self):
        if not Plugin.IniExists("AdminCmdConfig"):
            loc = Plugin.CreateIni("AdminCmdConfig")
            loc.Save()
        return Plugin.GetIni("AdminCmdConfig")

    # method by Illuminati
    def CheckV(self, Player, args):
        systemname = "Admin Commands"
        p = Server.FindPlayer(String.Join(" ", args))
        if p is not None:
            return p

        count = 0
        for pl in Server.ActivePlayers:
            for namePart in args:
                if namePart in pl.Name:
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, String.Format("Couldn't find {0}!", String.Join(" ", args)))
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, String.Format("Found {0} player with similar name. Use more correct name!"))
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
            else:
                DataStore.Add("godmode", Player.SteamID, 1)
                Player.Message("God mode on.")


    def On_PlayerAttacked(self, PlayerHurtEvent):
        get = DataStore.Get("godmode", PlayerHurtEvent.Victim.SteamID)
        if get is not None and get == 1:
             PlayerHurtEvent._info.damageAmount = 0

    def On_PlayerTakeDamage(self, PlayerTakeDmgEvent):
        get = DataStore.Get("godmode", PlayerTakeDmgEvent.Victim.SteamID)
        if get is not None and get == 1:
            PlayerTakeDmgEvent.Amount = 0

    def On_PlayerTakeRadiation(self, PlayerTakeRadsEvent):
        get = DataStore.Get("godmode", PlayerTakeRadsEvent.Victim.SteamID)
        if get is not None and get == 1:
            PlayerTakeRadsEvent.Amount = 0