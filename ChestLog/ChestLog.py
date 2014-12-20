__author__ = 'DreTaX'
__version__ = '1.1'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

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
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            if HurtEvent.Entity.Name == "WoodBoxLarge" or HurtEvent.Entity.Name == "WoodBox" or HurtEvent.Entity.Name == "SmallStash":
                name = HurtEvent.Attacker.Name
                loc = str(HurtEvent.Attacker.Location)
                entityloc = Util.CreateVector(HurtEvent.Entity.X, HurtEvent.Entity.Y, HurtEvent.Entity.Z)
                Plugin.Log("ChestLog", str(entityloc) + " | " + HurtEvent.Entity.Name + "|" + id + "|" + name + "|" + loc)