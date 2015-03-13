# coding=utf-8
__author__ = 'DreTaX'
__version__ = '1.4'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import re
import sys
path = Util.GetPublicFolder()
Lib = True
try:
    sys.path.append(path + "\\Python\\Lib\\")
    import random
except ImportError:
    Lib = False
"""
    Class
"""

RandNames = []
Names = []
class IllegalName:

    Words = {}
    asciie = None
    regex = None
    samename = None

    def On_PluginInit(self):
        ini = self.IllegalNameConfig()
        replace = ini.EnumSection("ReplaceCharactersTo")
        for wr in replace:
            s = str(ini.GetSetting("ReplaceCharactersTo", wr))
            self.Words.update({wr:s})
        self.asciie = int(ini.GetSetting("Settings", "CheckForNonAscii"))
        self.regex = int(ini.GetSetting("Settings", "CheckWithRegEx"))
        self.samename = int(ini.GetSetting("Settings", "SameName"))

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
        illini = self.getIllegal()
        listnames = illini.EnumSection("IllegalNames")
        compile = re.compile(r'\b(' + '|'.join(self.Words.keys()) + r')\b')
        name = compile.sub(lambda x: self.Words[x.group()], name)
        if self.asciie == 1:
            newname = self.CutName(name)
            name = newname
        if self.regex == 1:
            name = re.sub(' +',' ', name)
            name = re.sub('[\t]+','', name)
            starts = name.startswith(' ')
            ends = name.endswith(' ')
            if starts is True:
                name.replace(name[0], '')
            if ends is True:
                n = len(name)
                name.replace(name[n-1], '')
            a = re.match('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', name)
            if not a:
                name = re.sub('^[a-zA-Z0-9_!+?%()<>/\@#,.\\s\[\]-]+$', "", name)
        n = len(name)
        for checkn in listnames:
            get = illini.GetSetting("IllegalNames", checkn)
            if get.lower() in name.lower():
                n = 1
        if self.samename == 1:
            if name in Names:
                n = 1
        if n <= 1:
            name = "Stranger"
            if Lib:
                rand = self.GetNum()
                name = name + str(rand)
        Names.append(name)
        AuthEvent.Connection.username = str(name)

    def On_PlayerDisconnected(self, Player):
        name = Player.Name
        if "Stranger" in name:
            ssw = [int(s) for s in name if s.isdigit()]
            ssw = int(''.join(str(e) for e in ssw))
            if ssw in RandNames:
                RandNames.remove(ssw)
            if name in Names:
                Names.remove(name)