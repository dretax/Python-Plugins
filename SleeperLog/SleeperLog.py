__author__ = 'DreTaX'
__version__ = '1.3'

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
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            #On Entity hurt the attacker is an NPC and a Player for some reason. We will try to grab his ID
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            entityname = HurtEvent.Entity.Name
            if entityname == "MaleSleeper":
                #Dirty fucking hack against current bug. (Entity OWNERID request isn't working good yet, so hax it)
                OwnerID = self.GetIt(HurtEvent.Entity)
                if OwnerID is None:
                    return
                entityloc = Util.CreateVector(HurtEvent.Entity.X, HurtEvent.Entity.Y, HurtEvent.Entity.Z)
                ini = self.SleeperId()
                name = ini.GetSetting("Sleeper", str(OwnerID))
                if name is not None:
                    attacker = HurtEvent.Attacker.Name
                    Plugin.Log("SleeperLog", str(entityloc) + "|" + attacker + "|<- Attacker|" + id + "|" + name)