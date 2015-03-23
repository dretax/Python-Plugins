__author__ = 'DreTaX'
__version__ = '1.4'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System

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

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    #There is an error while converting ownerid to string in C#. Hax it.
    def GetIt(self, Entity):
        try:
            if Entity.IsDeployableObject():
                return Entity.Object.ownerID
            if Entity.IsStructure():
                return Entity.Object._master.ownerID
        except:
            return None

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        name = Player.Name
        ini = self.SleeperId()
        if ini.GetSetting("Sleeper", id) is None:
            ini.AddSetting("Sleeper", id, name)
            ini.Save()
        else:
            ini.SetSetting("Sleeper", id, name)
            ini.Save()

    def On_EntityHurt(self, HurtEvent):
        Server.Broadcast("EntityHurt")
        if self.TrytoGrabID(HurtEvent.Attacker):
            HurtEvent.Attacker.Message("Ran")
            if HurtEvent.Victim:
                HurtEvent.Attacker.Message(HurtEvent.Victim.Name)
            if HurtEvent.Entity:
                HurtEvent.Attacker.Message(HurtEvent.Entity.Name)

    def On_PlayerHurt(self, HurtEvent):
        Server.Broadcast("EntityHurt")
        if self.TrytoGrabID(HurtEvent.Attacker):
            HurtEvent.Attacker.Message("Ran")
            if HurtEvent.Victim:
                HurtEvent.Attacker.Message(HurtEvent.Victim.Name)
            if HurtEvent.Entity:
                HurtEvent.Attacker.Message(HurtEvent.Entity.Name)