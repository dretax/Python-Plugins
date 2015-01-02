__author__ = 'DreTaX'
__version__ = '1.3'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re


class IllegalName:

    def On_PluginInit(self):
        Util.ConsoleLog("BannedPeople by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def getIllegal(self):
        if not Plugin.IniExists("IllegalNames"):
            IllegalNames = Plugin.CreateIni("IllegalNames")
            IllegalNames.AddSetting("IllegalNames", "Name1", "Suck")
            IllegalNames.AddSetting("IllegalNames", "Name2", "Fuck")
            IllegalNames.AddSetting("IllegalNames", "Name3", "SHITSERVER")
            IllegalNames.Save()
        return Plugin.GetIni("IllegalNames")


    def IllegalNameConfig(self):
        if not Plugin.IniExists("IllegalNameConfig"):
            loc = Plugin.CreateIni("IllegalNameConfig")
            loc.Save()
        return Plugin.GetIni("IllegalNameConfig")


    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None


    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        name = Player.Name
        n = len(name)
        ini = self.getIllegal()
        config = self.IllegalNameConfig()
        f = int(config.GetSetting("Settings", "Protection"))
        reason = config.GetSetting("Settings", "DisconnectReason")
        reason2 = config.GetSetting("Settings", "DisconnectReason2")
        space = int(config.GetSetting("Settings", "Spaces"))
        listnames = ini.EnumSection("IllegalNames")
        for checkn in listnames:
            get = ini.GetSetting("IllegalNames", checkn)
            lowername = name.lower()
            lowercheck = get.lower()
            if lowercheck in lowername:
                Player.Message(reason)
                Player.Disconnect()
                return
        if f == 1:
            if space == 0:
                a = re.match('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', name)
                if not a:
                    Player.Message(reason2)
                    Player.Message("Allowed Chars: a-z,0-9,!@#$%/\[]<>+=.-")
                    Player.Message("Spaces are not allowed")
                    Player.Disconnect()
            else:
                a = re.match('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', name)
                if not a or n <= 1:
                    Player.Message(reason2)
                    Player.Message("Allowed Chars: a-z,0-9,!@#$%/\[]<>+=.-")
                    Player.Disconnect()
        elif f == 2:
            if n <= 1:
                Player.Message(reason2)
                Player.Message("Allowed Chars: a-z,0-9,!@#$%/\[]<>+=.-")
                Player.Disconnect()
        elif f == 3:
            if space == 0:
                a = re.match('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', name)
                if not a or n <= 1:
                    Player.Message(reason2)
                    Player.Message("Allowed Chars: a-z,0-9,!@#$%/\[]<>+=.-")
                    Player.Message("Spaces are not allowed")
                    Player.Disconnect()
            else:
                a = re.match('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', name)
                if not a or n <= 1:
                    Player.Message(reason2)
                    Player.Message("Allowed Chars: a-z,0-9,!@#$%/\[]<>+=.-")
                    Player.Disconnect()
