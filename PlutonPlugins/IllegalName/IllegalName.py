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
        name = string.encode('UTF-8')
        name = name.decode('UTF-8', 'strict')
        name = re.sub(r'[^\x00-\x7F]+','', name)
        return name

    def On_ClientAuth(self, AuthEvent):
        Player = AuthEvent.con
        name = str(AuthEvent.Name)
        n = len(name)
        ini = self.IllegalNameConfig()
        asciie = int(ini.GetSetting("options", "CheckForNonAscii"))
        regex = int(ini.GetSetting("options", "CheckWithRegEx"))
        illini = self.getIllegal()
        reason = ini.GetSetting("options", "DisconnectReason")
        reason2 = ini.GetSetting("options", "DisconnectReason2")
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
        if regex == 1:
            starts = name.startswith(' ')
            ends = name.endswith(' ')
            if starts is True:
                name.replace(name[0], '')
            if ends is True:
                name.replace(name[n], '')
            a = re.match('^[a-zA-Z0-9_!+?%éáűőúöüó()<>/\@#,.\\s\[\]-]+$', name)
            if not a or n <= 1:
                Player.Kick(reason2)
                return
            name = re.sub(' +',' ', name)
        if asciie == 1:
            newname = self.CutName(name)
            name = newname
        AuthEvent.con.username = name