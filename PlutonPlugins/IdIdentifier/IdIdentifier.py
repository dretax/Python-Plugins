__author__ = 'DreTaX'
__version__ = '1.4'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
from time import gmtime, strftime

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

    """
        CheckV Assistants
    """

    def GetPlayerName(self, name, Mode=1):
        if Mode == 1 or Mode == 3:
            for pl in Server.ActivePlayers:
                if pl.Name.lower() == name:
                    return pl
        if Mode == 2 or Mode == 3:
            for pl in Server.OfflinePlayers.Values:
                if pl.Name.lower() == name:
                    return pl
        return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        Mode: Search mode (Default: 1)
            1 = Search Online Players
            2 = Search Offline Players
            3 = Both
        V6.0
    """

    def CheckV(self, Player, args, Mode=1):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.Join(" ", args).lower(), Mode)
            if p is not None:
                return p
            if Mode == 1 or Mode == 3:
                for pl in Server.ActivePlayers:
                    for namePart in args:
                        if namePart.lower() in pl.Name.lower():
                            p = pl
                            count += 1
            if Mode == 2 or Mode == 3:
                for offlineplayer in Server.OfflinePlayers.Values:
                    for namePart in args:
                        if namePart.lower() in offlineplayer.Name.lower():
                            p = offlineplayer
                            count += 1
        else:
            ag = str(args).lower()  # just incase
            p = self.GetPlayerName(ag, Mode)
            if p is not None:
                return p
            if Mode == 1 or Mode == 3:
                for pl in Server.ActivePlayers:
                    if ag in pl.Name.lower():
                        p = pl
                        count += 1
            if Mode == 2 or Mode == 3:
                for offlineplayer in Server.OfflinePlayers.Values:
                    if ag in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
        if count == 0:
            Player.MessageFrom("IdIdentifier", "Couldn't Find " + str.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom("IdIdentifier", "Found " + str(count) +
                               " player with similar name. Use more correct name!")
            return None

    def On_PlayerConnected(self, Player):
        sid = Player.SteamID
        banini = self.ManualBan()
        isbanned = banini.GetSetting("Banned", sid)
        if str(isbanned) == "1":
            Player.Kick("You are banned.")
            return
        name = Player.Name
        ip = Player.IP
        location = str(Player.Location)
        ini = self.PlayersIni()
        if ini.GetSetting("Track", sid) is not None:
            ini.SetSetting("Track", sid, name)
        else:
            ini.AddSetting("Track", sid, name)
        ini.Save()
        Plugin.Log("LastJoin", name + "|" + sid + "|" + ip + "|" + location)

    def On_PlayerDisconnected(self, Player):
        name = Player.Name
        id = Player.SteamID
        ip = Player.IP
        location = str(Player.Location)
        Plugin.Log("LastQuit", name + "|" + id + "|" + ip + "|" + location)

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