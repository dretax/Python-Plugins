__author__ = 'DreTaX'
__version__ = '1.3'

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

    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None


    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.0
    """
    def CheckV(self, Player, args):
        systemname = "IdIdentifier"
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(String.Join(" ", args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            p = self.GetPlayerName(str(args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                if str(args).lower() in pl.Name.lower():
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
        ini.AddSetting("Track", sid, name)
        ini.AddSetting("LastJoin", name, "|" + sid + "|" + ip + "|" + dt + "|" + location)
        ini.Save()

    def On_PlayerDisconnected(self, Player):
        name = Player.Name
        id = Player.SteamID
        location = str(Player.Location)
        ini = self.PlayersIni()
        dt = str(System.DateTime.Now)
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