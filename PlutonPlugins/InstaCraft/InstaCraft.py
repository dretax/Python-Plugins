__author__ = 'DreTaX'
__version__ = '1.1'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton

class InstaCraft:

    InstaCraft = None

    def On_PluginInit(self):
        if not Plugin.IniExists("Items"):
            x = Find.BluePrints()
            ini = Plugin.CreateIni("Items")
            ini.AddSetting("Config", "InstaCraft", "False")
            for y in x:
                ini.AddSetting("Items", str(y.name), str(y.time))
                ini.AddSetting("AllowCrafting", str(y.name), "True")
            ini.Save()
        ini = Plugin.GetIni("Items")
        self.InstaCraft = bool(ini.GetSetting("Config", "InstaCraft"))
        if self.InstaCraft:
            return
        for x in ini.EnumSection("Items"):
            v = ini.GetSetting("Items", x)
            setattr(self, x, float(v))
        for x in ini.EnumSection("AllowCrafting"):
            v = ini.GetSetting("AllowCrafting", x)
            setattr(self, x + "B", bool(v))

    def On_PlayerStartCrafting(self, CraftEvent):
        name = CraftEvent.bluePrint.name
        cb = getattr(self, name + "B")
        if not cb:
            CraftEvent.Stop("This item is banned.")
            return
        if InstaCraft:
            CraftEvent.CraftTime = float(0)
            return
        t = getattr(self, name)
        CraftEvent.CraftTime = float(t)