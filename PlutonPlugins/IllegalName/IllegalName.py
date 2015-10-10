# coding=utf-8
__author__ = 'DreTaX'
__version__ = '1.4.1'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import re
import sys
path = Util.GetPublicFolder()
try:
    sys.path.append(path + "\\Python\\Lib\\")
    import random
except ImportError:
    raise ImportError("IllegalName: Download the Python Extra libs from the website!")

"""
    Class
"""

RandNames = []
Names = []
Restricted = []


class IllegalName:

    Words = {}
    asciie = None
    regex = None
    samename = None
    maxl = None

    def On_PluginInit(self):
        ini = self.IllegalNameConfig()
        replace = ini.EnumSection("ReplaceCharactersTo")
        for wr in replace:
            s = str(ini.GetSetting("ReplaceCharactersTo", wr))
            self.Words.update({wr:s})
        self.asciie = int(ini.GetSetting("Settings", "CheckForNonAscii"))
        self.regex = int(ini.GetSetting("Settings", "CheckWithRegEx"))
        self.samename = int(ini.GetSetting("Settings", "SameName"))
        self.maxl = int(ini.GetSetting("Settings", "NameLength"))
        illini = self.getIllegal()
        enum = illini.EnumSection("IllegalNames")
        for checkn in enum:
            get = illini.GetSetting("IllegalNames", checkn).lower()
            Restricted.append(get)

    def GetNum(self):
        for x in xrange(0, 1000):
            if x in RandNames:
                continue
            RandNames.append(x)
            return x

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
        name = re.sub(r'[^\x00-\x7F]+', '', string)
        return name

    def Replace(self, Old, To, Text):
        return re.sub('(?i)'+re.escape(Old), lambda m: To, Text)

    def On_ClientAuth(self, AuthEvent):
        name = AuthEvent.Name
        compile = re.compile(r'\b(' + '|'.join(self.Words.keys()) + r')\b')
        name = compile.sub(lambda x: self.Words[x.group()], name)
        name = self.CutName(name)
        name = re.sub(' +', ' ', name)
        name = re.sub('[\t]+', '', name)
        starts = name.startswith(' ')
        ends = name.endswith(' ')
        if starts:
            name = name.replace(name[0], '')
        if ends:
            n = len(name)
            if n > 1:
                name = name.replace(name[n - 1], '')
        a = re.match('^[a-zA-Z0-9_!+?()<>/@#,. \[\]\\-]+$', name)
        if not a:
            name = re.sub('^[a-zA-Z0-9_!+?()<>/@#,. \[\]\\-]+$', "", name)
        n = len(name)
        if n > self.maxl:
            n = 1
        if name.lower() in str(Restricted):
            n = 1
        if name.lower() in str(Names).lower() and "stranger" not in name.lower():
            n = 1
        if n <= 1:
            name = "Stranger"
            rand = self.GetNum()
            name = name + str(rand)
        Names.append(name)
        AuthEvent.Connection.username = name

    def On_PlayerDisconnected(self, Player):
        name = Player.Name
        if "Stranger" in name:
            ssw = [int(s) for s in name if s.isdigit()]
            ssw = int(''.join(str(e) for e in ssw))
            if ssw in RandNames:
                RandNames.remove(ssw)
            if name in Names:
                Names.remove(name)
