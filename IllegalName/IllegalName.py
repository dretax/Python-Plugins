__author__ = 'DreTaX'
__version__ = '1.0a'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

class IllegalName:

    def On_PluginInit(self):
        Util.ConsoleLog("IllegalName by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def getIllegal(self):
        if not Plugin.IniExists("IllegalNames"):
            IllegalNames = Plugin.CreateIni("IllegalNames")
            IllegalNames.AddSetting("IllegalNames", "Name1", "Suck")
            IllegalNames.AddSetting("IllegalNames", "Name2", "Fuck")
            IllegalNames.AddSetting("IllegalNames", "Name3", "SHITSERVER")
            IllegalNames.Save()
        return Plugin.GetIni("IllegalNames")

    def TrytoGrabName(self, Player):
        try:
            name = Player.Name
            return name
        except:
            Plugin.Log("IllegalNErr", "Error caught at TrytoGrabName method.")
            return None

    def IllegalNameConfig(self):
        if not Plugin.IniExists("IllegalNameConfig"):
            loc = Plugin.CreateIni("IllegalNameConfig")
            loc.Save()
        return Plugin.GetIni("IllegalNameConfig")

    def On_PlayerConnected(self, Player):
        name = self.TrytoGrabName(Player)
        if name == None:
            return
        n = len(name)
        ini = self.IllegalNameConfig()
        illini = self.getIllegal()
        f = int(ini.GetSetting("options", "protection1"))
        reason = ini.GetSetting("options", "DisconnectReason")
        reason2 = ini.GetSetting("options", "DisconnectReason2")
        space = ini.GetSetting("options", "Spaces")
        listnames = illini.EnumSection("IllegalNames")
        counted = len(listnames)
        i = 0
        if counted > 0:
            for checkn in listnames:
                get = illini.GetSetting("IllegalNames", checkn)
                i += 1
                lowername = Data.ToLower(name)
                lowercheck = Data.ToLower(get)
                if counted >= i:
                    if lowercheck in lowername:
                        Player.Message(reason)
                        Player.Disconnect()
                        return
        if f == 1:
            if space == 0:
                a = re.match('^[a-zA-Z0-9_!+?%éáűőúöüó()<>/\@#,.\[\]-]+$', name)
                if not a:
                    Player.Message(reason2)
                    Player.Message("Allowed Chars: a-z,0-9,!@#$%/\[]<>+=.-")
                    Player.Message("Spaces are not allowed")
                    Player.Disconnect()
            else:
                a = re.match('^[a-zA-Z0-9_ !+?%éáűőúöüó()<>/\@#,.\[\]-]+$', name)
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
            if (space == 0):
                a = re.match('^[a-zA-Z0-9_!+?%éáűőúöüó()<>/\@#,.\[\]-]+$', name)
                if not a or n <= 1:
                    Player.Message(reason2)
                    Player.Message("Allowed Chars: a-z,0-9,!@#$%/\[]<>+=.-")
                    Player.Message("Spaces are not allowed")
                    Player.Disconnect()
            else:
                a = re.match('^[a-zA-Z0-9_ !+?%éáűőúöüó()<>/\@#,.\[\]-]+$', name)
                if not a or n <= 1:
                    Player.Message(reason2)
                    Player.Message("Allowed Chars: a-z,0-9,!@#$%/\[]<>+=.-")
                    Player.Disconnect()