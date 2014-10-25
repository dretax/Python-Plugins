__author__ = 'DreTaX'
__version__ = '1.2'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import re

"""
    Class
"""


class IllegalName:

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

    def CutName(self, string):
        try:
            name = string.encode('UTF-8')
            name = name.decode('UTF-8', 'strict')
            name = re.sub(r'[^\x00-\x7F]+','', name)
            return name
        except:
            return False

    def On_ClientAuth(self, AuthEvent):
        Player = AuthEvent.con
        name = str(AuthEvent.Name)
        n = len(name)
        ini = self.IllegalNameConfig()
        asciie = int(ini.GetSetting("options", "CheckForAscii"))
        illini = self.getIllegal()
        f = int(ini.GetSetting("options", "protection1"))
        reason = ini.GetSetting("options", "DisconnectReason")
        reason2 = ini.GetSetting("options", "DisconnectReason2")
        reason3 = ini.GetSetting("options", "DisconnectReason3")
        space = ini.GetSetting("options", "Spaces")
        listnames = illini.EnumSection("IllegalNames")
        counted = len(listnames)
        i = 0
        if counted > 0:
            for checkn in listnames:
                get = illini.GetSetting("IllegalNames", checkn)
                i += 1
                lowername = name.lower()
                lowercheck = get.lower()
                if counted >= i:
                    if lowercheck in lowername:
                        Player.Kick(reason)
                        return
        if f == 1:
            if space == 0:
                a = re.match('^[a-zA-Z0-9_!+?%éáűőúöüó()<>/\@#,.\[\]-]+$', name)
                if not a:
                    Player.Kick(reason3)
                    return
            else:
                a = re.match('^[a-zA-Z0-9_!+?%éáűőúöüó()<>/\@#,.\\s\[\]-]+$', name)
                if not a or n <= 1:
                    Player.Kick(reason2)
                    return
                AuthEvent.con.username = re.sub(' +',' ', name)
                name = re.sub(' +',' ', name)
        elif f == 2:
            if n <= 1:
                Player.Kick(reason2)
        elif f == 3:
            if space == 0:
                a = re.match('^[a-zA-Z0-9_!+?%éáűőúöüó()<>/\@#,.\[\]-]+$', name)
                if not a or n <= 1:
                    Player.Kick(reason3)
                    return
            else:
                a = re.match('^[a-zA-Z0-9_!+?%éáűőúöüó()<>/\@#,.\\s\[\]-]+$', name)
                if not a or n <= 1:
                    Player.Kick(reason2)
                    return
                AuthEvent.con.username = re.sub(' +',' ', name)
                name = re.sub(' +',' ', name)
        if asciie == 1:
            asciireason = ini.GetSetting("options", "AsciiReason")
            newname = self.CutName(name)
            if newname is False:
                Player.Kick(asciireason)
                return
            AuthEvent.con.username = newname