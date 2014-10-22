__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import *

"""
    Class
"""


class IdIdentifier:

    def Reports(self):
        if not Plugin.IniExists("Reports"):
            ini = Plugin.CreateIni("Reports")
            ini.Save()
        return Plugin.GetIni("Reports")

    # method by Illuminati
    def CheckV(self, Player, args):
        systemname = "[Report System]"
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
            Player.MessageFrom(systemname, "Couldn't find " + args + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found " + str(count) + " player with similar name. Use more correct name!")
            return None

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "report":
            ini = self.Reports()
            if len(args) == 0:
                Player.Message("Usage: /report username, Reason to report.")
                Player.Message("Comma after name is required.")
            elif len(args) == 1:
                if "," not in args:
                    Player.Message("Usage: /report username, Reason to report")
                    Player.Message("Comma after name is required.")
                    return
                args = args.split(",", 1)
                pl = self.CheckV(Player, args[0])
                if pl is None:
                    return
                dt = str(System.DateTime.Now)
                ini.AddSetting("Reports", pl.SteamID, "--" + dt + "--")
                ini.AddSetting("Reports", pl.SteamID, args[1] + " player's name: " + pl.Name + " Report By: " + Player.Name)
                ini.AddSetting("Reports", pl.SteamID, "--" + dt + "--")
                ini.Save()
                Player.Message("Report Submitted!")
                for admin in Server.ActivePlayers:
                    if admin.Admin:
                        admin.MessageFrom("[Report System]", "Complaint From Player: " + Player.Name + " of " + pl.Name)
                        admin.MessageFrom("[Report System]", "Reason: " + args[1])