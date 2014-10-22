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

    def PlayersIni(self):
        if not Plugin.IniExists("Players"):
            ini = Plugin.CreateIni("Players")
            ini.Save()
        return Plugin.GetIni("Players")

    def ManualBan(self):
        if not Plugin.IniExists("ManualBan"):
            ini = Plugin.CreateIni("ManualBan")
            ini.Save()
        return Plugin.GetIni("ManualBan")

    def On_PlayerConnected(self, Player):
        sid = Player.SteamID
        banini = self.ManualBan()
        isbanned = banini.GetSetting("Banned", sid)
        if str(isbanned) == "1":
            Player.Kick("You are banned.")
            return
        name = Player.Name
        ip = str(Player.IP)
        location = str(Player.Location)
        dt = str(System.DateTime.Now)
        ini = self.PlayersIni()
        if (ini.GetSetting("Track", sid) is not None and ini.GetSetting("LastJoin", name) is not None):
            ini.SetSetting("Track", sid, name)
            ini.SetSetting("LastJoin", name, "|" + sid + "|" + ip + "|" + dt + "|" + location)
            ini.Save()
        else:
            ini.AddSetting("Track", sid, name)
            ini.AddSetting("LastJoin", name, "|" + sid + "|" + ip + "|" + dt + "|" + location)
            ini.Save()

    def On_PlayerDisconnected(self, Player):
        name = Player.Name
        id = Player.SteamID
        location = str(Player.Location)
        ini = self.PlayersIni()
        dt = str(System.DateTime.Now)
        if ini.GetSetting("Track", name) is not None:
            ini.SetSetting("LastQuit", name, "|" + id + "|" + dt + "|" + location)
        else:
            ini.AddSetting("LastQuit", name, "|" + id + "|" + dt + "|" + location)
        ini.Save()

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd == "offban":
            ini = self.ManualBan()
            if len(args) == 0:
                Player.Message("Specify an ID")
            elif len(args) == 1:
                if Player.Admin:
                    id = str(args[0])
                    ini.AddSetting("Banned", id, "1")
                    ini.Save()
                    Player.Message("Id of Player (" + id + ") was banned.")
        elif cmd == "playerlist":
            all = ""
            for pl in Server.ActivePlayers:
                all = all + str(pl.Name) + ", "
            Player.Message(all)