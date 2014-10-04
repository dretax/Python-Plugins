__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System

"""
    Class
"""

class ChestLog:
    """
        Methods
    """
    def On_PluginInit(self):
        Util.ConsoleLog("ChestLog by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def ChestLog(self):
        if not Plugin.IniExists("ChestLog"):
            ChestLog = Plugin.CreateIni("ChestLog")
            ChestLog.Save()
        return Plugin.GetIni("ChestLog")

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker != None and HurtEvent.Entity != None and not HurtEvent.IsDecay:
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            entityname = HurtEvent.Entity.Name
            if entityname == "WoodBoxLarge" or entityname == "WoodBox" or entityname == "SmallStash":
                name = HurtEvent.Attacker.Name
                time = str(System.DateTime.Now)
                loc = str(HurtEvent.Attacker.Location)
                ini = self.ChestLog()
                entityloc = Util.CreateVector(HurtEvent.Entity.X, HurtEvent.Entity.Y, HurtEvent.Entity.Z)
                ini.AddSetting("ChestLog", str(entityloc), entityname + "|" + id + "|" + name + "|" + time + "|" + loc)
                ini.Save()