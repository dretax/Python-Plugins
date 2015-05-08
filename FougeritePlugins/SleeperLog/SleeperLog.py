__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""


class SleeperLog:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("SleeperLog by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def SleeperId(self):
        if not Plugin.IniExists("SleeperId"):
            ini = Plugin.CreateIni("SleeperId")
            ini.Save()
        return Plugin.GetIni("SleeperId")

    def IsAnimal(self, Entity):
        if "NPC" in str(Entity):
            return True
        return False

    def On_PlayerConnected(self, Player):
        name = Player.Name
        id = Player.SteamID
        ini = self.SleeperId()
        if ini.GetSetting("Sleeper", id) is None:
            ini.AddSetting("Sleeper", id, name)
            ini.Save()
        else:
            ini.SetSetting("Sleeper", id, name)
            ini.Save()

    def On_PlayerHurt(self, HurtEvent):
        if not self.IsAnimal(HurtEvent.Attacker) and HurtEvent.Sleeper:
            ini = self.SleeperId()
            n = ini.GetSetting("Sleeper", HurtEvent.Attacker.SteamID)
            n2 = ini.GetSetting("Sleeper", HurtEvent.Victim.OwnerID)
            Plugin.Log("SleeperLog", "Attacker: " + n + " | " + HurtEvent.Attacker.SteamID + " | " +
                       str(HurtEvent.Attacker.Location) + " Vic: " + HurtEvent.Victim.OwnerID + " | " + n2)