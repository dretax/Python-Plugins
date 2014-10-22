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

    # method by Illuminati
    def CheckV(self, Player, args):
        systemname = "IdIdentifier"
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
            Player.MessageFrom(systemname, "Couldn't find " + str(args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found " + str(count) + " player with similar name. Use more correct name!")
            return None

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
        if cmd.cmd == "offban":
            ini = self.ManualBan()
            if len(args) == 0:
                Player.Message("Specify an ID")
            elif len(args) == 1:
                if Player.Admin:
                    id = str(args[0])
                    ini.AddSetting("Banned", id, "1")
                    ini.Save()
                    Player.Message("Id of Player (" + id + ") was banned.")
        elif cmd.cmd == "uid":
            if len(args) == 0:
                Player.Message("User name required!")
            elif len(args) > 0:
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                Player.Message("UID of " + playerr.Name + " is:" + playerr.SteamID)
        elif cmd.cmd == "playerlist":
            all = ""
            i = 0
            Player.Message("Online Players: " + str(Server.ActivePlayers.Count))
            for pl in Server.ActivePlayers:
                i += 1
                if i <= 30:
                    all = all + str(pl.Name) + ", "
                else:
                    Player.Message(all)
                    all = all.replace(all, "")
                    all = all + str(pl.Name + ", ")
                    i = 1
            Player.Message(all)