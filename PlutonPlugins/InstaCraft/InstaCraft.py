__author__ = 'DreTaX'
__version__ = '1.2'

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
        self.InstaCraft = self.bool(ini.GetSetting("Config", "InstaCraft"))
        if self.InstaCraft is True:
            return
        for x in ini.EnumSection("Items"):
            v = ini.GetSetting("Items", x)
            setattr(self, x, float(v))
        for x in ini.EnumSection("AllowCrafting"):
            v = ini.GetSetting("AllowCrafting", x)
            n = x + "Bool"
            setattr(self, n, self.bool(v))

    def bool(self, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            raise ValueError

    def On_PlayerStartCrafting(self, CraftEvent):
        name = str(CraftEvent.bluePrint.targetItem.name)
        cb = getattr(self, name + "Bool")
        if not cb:
            CraftEvent.Stop("This item is banned.")
            return
        if InstaCraft is True:
            CraftEvent.CraftTime = float(0)
            return
        t = getattr(self, name)
        CraftEvent.CraftTime = float(t)