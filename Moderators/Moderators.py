__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite


"""
    Class
"""

class Moderators:
    """
        Methods
    """

    def ModeratorsIni(self):
        if not Plugin.IniExists("Moderators"):
            ini = Plugin.CreateIni("Moderators")
            ini.AddSetting("Moderators", "ModNameHere", "76561197999999999")
            ini.Save()
        return Plugin.GetIni("Moderators")

    def On_PluginInit(self):
        ini = self.ModeratorsIni()
        mods = ini.EnumSection("Moderators")
        counted = len(mods)
        i = 0
        for mod in mods:
            i += 1
            if (i <= counted):
                modid = ini.GetSetting("Moderators", mod)
                DataStore.Add("Moderators", modid, mod)