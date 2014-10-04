__author__ = 'DreTaX'
__version__ = '1.0'

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
            Plugin.Log("SleeperErr", "Error caught at TrytoGrabID method.")
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


    def IsIn(self, EntityName):
        # Okay seriously DreTaX It's 0:03, It's about time to use something else and more logical
        if EntityName == 'WoodFoundation':
            return True
        elif EntityName == 'WoodDoorFrame':
            return True
        elif EntityName == 'WoodWall':
            return True
        elif EntityName == 'WoodPillar':
            return True
        elif EntityName == 'WoodCeiling':
            return True
        elif EntityName == 'MetalDoor':
            return True
        elif EntityName == 'WoodDoor':
            return True
        elif EntityName == 'WoodStairs':
            return True
        elif EntityName == 'WoodWindowFrame':
            return True
        elif EntityName == 'MetalFoundation':
            return True
        elif EntityName == 'MetalDoorFrame':
            return True
        elif EntityName == 'MetalWall':
            return True
        elif EntityName == 'MetalPillar':
            return True
        elif EntityName == 'MetalCeiling':
            return True
        elif EntityName == 'MetalStairs':
            return True
        elif EntityName == 'MetalWindowFrame':
            return True
        elif EntityName == 'Wood_Shelter':
            return True
        elif EntityName == 'Barricade_Fence_Deployable':
            return True
        elif EntityName == 'Metal Bars Window':
            return True
        elif EntityName == 'CampFire':
            return True
        elif EntityName == 'Wood Spike Wall':
            return True
        elif EntityName == 'WoodBoxLarge':
            return True
        elif EntityName == 'WoodBox':
            return True
        elif EntityName == 'SmallStash':
            return True
        elif EntityName == 'Campfire':
            return True
        elif EntityName == 'Furnace':
            return True
        elif EntityName == 'RepairBench':
            return True
        elif EntityName == 'Workbench':
            return True
        elif EntityName == 'Large Wood Spike Wall':
            return True
        elif EntityName == 'WoodGate':
            return True
        elif EntityName == 'WoodGateway':
            return True
        elif EntityName == 'MetalRamp':
            return True
        elif EntityName == 'WoodRamp':
            return True
        else:
            return False


    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id == None:
            return
        name = Player.Name
        ini = self.SleeperId()
        ini.AddSetting("Sleeper", id, name)
        ini.Save()


    def On_EntityHurt(self, HurtEvent):
        if (HurtEvent.Attacker != None and HurtEvent.Entity != None and not HurtEvent.IsDecay):
            #On Entity hurt the attacker is an NPC and a Player for some reason. We will try to grab his ID
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            entityname = HurtEvent.Entity.Name
            if self.IsIn(entityname):
                return
            else:
                #Dirty fucking hack against current bug. (Entity OWNERID request isn't working good yet, so hax it)
                OwnerID = self.GetIt(HurtEvent.Entity)
                if OwnerID is None:
                    return
                entityloc = Util.CreateVector(HurtEvent.Entity.X, HurtEvent.Entity.Y, HurtEvent.Entity.Z)
                ini = self.SleeperId()
                name = ini.GetSetting("Sleeper", str(OwnerID))
                exist = ini.GetSetting("SleeperLog", str(entityloc))
                if name != None and exist == None:
                    attacker = HurtEvent.Attacker.Name
                    time = str(System.DateTime.Now)
                    ini.AddSetting("SleeperLog", str(entityloc), attacker + "|<- Attacker|" + id + "|" + name + "|" + time)
                    ini.Save()