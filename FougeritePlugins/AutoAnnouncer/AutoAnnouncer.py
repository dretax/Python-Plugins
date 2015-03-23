__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

import sys
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

Lib = True
try:
    import random
except ImportError:
    Lib = False

"""
    Class
"""


class AutoAnnouncer:

    Timer = None
    AdvertNumber = None
    Sys = None

    def On_PluginInit(self):
        Util.ConsoleLog("AutoAnnouncer by " + __author__ + " Version: " + __version__ + " loaded.", False)
        ini = self.AutoAnnouncer()
        self.Timer = int(ini.GetSetting("Settings", "Timer"))
        self.AdvertNumber = int(ini.GetSetting("Settings", "AdvertNumber"))
        self.Sys = ini.GetSetting("Settings", "Sys")
        Plugin.CreateTimer("AutoAnnouncer", self.Timer).Start()

    def AutoAnnouncer(self):
        if not Plugin.IniExists("AutoAnnouncer"):
            ini = Plugin.CreateIni("AutoAnnouncer")
            ini.AddSetting("Settings", "Timer", "120000")
            ini.AddSetting("Settings", "AdvertNumber", "2")
            ini.AddSetting("Settings", "Sys", "[Advert]")
            ini.AddSetting("Announce1", "Message", "Welcome to Nigeria!")
            ini.AddSetting("Announce1", "Message2", "But I'm going to ban you now :P")
            ini.AddSetting("Announce2", "Message", "Welcome to Nigeria!")
            ini.AddSetting("Announce2", "Message2", "Hey you are lucky! You won't get banned.")
            ini.Save()
        return Plugin.GetIni("AutoAnnouncer")

    def AutoAnnouncerCallback(self):
        Plugin.KillTimer("AutoAnnouncer")
        r = random.randint(1, self.AdvertNumber)
        ini = self.AutoAnnouncer()
        sec = ini.EnumSection("Announce" + str(r))
        for msg in sec:
            val = ini.GetSetting("Announce" + str(r), msg)
            Server.BroadcastFrom(sys, val)
        Plugin.CreateTimer("AutoAnnouncer", self.Timer).Start()