# coding=utf-8
__author__ = 'DreTaX'
__version__ = '1.6.5'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

RandNames = []
Names = []
Restricted = []
red = "[color #FF0000]"


class AAscii:

    a = None
    m = None
    maxl = None
    DeleteIllegalCharsMods = None
    DeleteIllegalCharsAdmins = None
    KickInsteadOfRenaming = None

    def On_PluginInit(self):
        ini = self.ANA()
        self.a = int(ini.GetSetting("Settings", "DontRenameAdmins"))
        self.m = int(ini.GetSetting("Settings", "DontRenameMods"))
        self.DeleteIllegalCharsAdmins = int(ini.GetSetting("Settings", "DeleteIllegalCharsAdmins"))
        self.DeleteIllegalCharsMods = int(ini.GetSetting("Settings", "DeleteIllegalCharsMods"))
        self.maxl = int(ini.GetSetting("Settings", "NameLength"))
        self.KickInsteadOfRenaming = int(ini.GetSetting("Settings", "KickInsteadOfRenaming"))
        enum = ini.EnumSection("Restrict")
        for checkn in enum:
            get = ini.GetSetting("Restrict", checkn).lower()
            Restricted.append(get)
        Util.ConsoleLog("AAscii (ANA) by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def ANA(self):
        if not Plugin.IniExists("ANA"):
            ini = Plugin.CreateIni("ANA")
            ini.AddSetting("Settings", "KickInsteadOfRenaming", "0")
            ini.AddSetting("Settings", "DontRenameAdmins", "1")
            ini.AddSetting("Settings", "DontRenameMods", "1")
            ini.AddSetting("Settings", "DeleteIllegalCharsAdmins", "1")
            ini.AddSetting("Settings", "DeleteIllegalCharsMods", "1")
            ini.AddSetting("Settings", "NameLength", "17")
            ini.AddSetting("Restrict", "1", "DerpTeamNoob")
            ini.AddSetting("Restrict", "2", "Changeme")
            ini.Save()
        return Plugin.GetIni("ANA")

    def GetNum(self):
        for x in xrange(0, 1000):
            if x in RandNames:
                continue
            RandNames.append(x)
            return x

    def CutName(self, string):
        name = re.sub(r'[^\x00-\x7F]+', '', string)
        return name

    def Replace(self, Old, To, Text):
        return re.sub('(?i)' + re.escape(Old), lambda m: To, Text)

    def Rename(self, Player):
        name = Player.Name
        c = re.match(r'[^\x00-\x7F]+', name)
        if not c:
            if self.KickInsteadOfRenaming == 1:
                Player.Message(red + "You have illegal characters in your name! Rename yourself!")
                Player.Disconnect()
                return
            name = self.CutName(name)
        name = re.sub(' +', ' ', name)
        name = re.sub('[\t]+', '', name)
        starts = name.startswith(' ')
        ends = name.endswith(' ')
        if starts is True:
            name = name.replace(name[0], '')
        if ends is True:
            n = len(name)
            if n > 1:
                name = name.replace(name[n - 1], '')
        a = re.match('^[a-zA-Z0-9_!+?()<>/@#,. \[\]\\-]+$', name)
        if not a:
            if self.KickInsteadOfRenaming == 1:
                Player.Message(red + "You have illegal characters in your name! Rename yourself!")
                Player.Disconnect()
                return
            name = re.sub('^[a-zA-Z0-9_!+?()<>/@#,. \[\]\\-]+$', "", name)
        n = len(name)
        if n > self.maxl:
            n = 1
        if name.lower() in str.join(' ', Restricted).lower():
            n = 1
        if name.lower() in str.join(' ', Names).lower() and "stranger" not in name.lower():
            n = 1
        if n <= 1:
            name = "Stranger"
            rand = self.GetNum()
            name = name + str(rand)
        Player.Name = name
        Names.append(name)

    def On_PlayerConnected(self, Player):
        if Player.Admin and self.a == 1:
            if self.DeleteIllegalCharsAdmins == 1:
                name = Player.Name
                name = self.CutName(name)
                Player.Name = name
                Names.append(name)
            return
        if Player.Moderator and self.m == 1:
            if self.DeleteIllegalCharsMods == 1:
                name = Player.Name
                name = self.CutName(name)
                Player.Name = name
                Names.append(name)
            return
        self.Rename(Player)

    def On_PlayerDisconnected(self, Player):
        name = Player.Name
        if "Stranger" in name:
            ssw = [int(s) for s in name if s.isdigit()]
            ssw = int(''.join(str(e) for e in ssw))
            if ssw in RandNames:
                RandNames.remove(ssw)
        if name in Names:
            Names.remove(name)
