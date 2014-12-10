__author__ = 'DreTaX'
__version__ = '1.1'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System

"""
    Class
"""

class DestroySystem:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("DestroySystem by " + __author__ + " Version: " + __version__ + " loaded.", False)
        self.DestroySys()

    def IsEligible(self, HurtEvent):
        try:
            Eligible = HurtEvent.Entity.Object._master.ComponentCarryingWeight(HurtEvent.Entity.Object)
            return not (Eligible)
        except:
            return True

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

    def DestroySys(self):
        if not Plugin.IniExists("DestroySys"):
            ini = Plugin.CreateIni("DestroySys")
            ini.AddSetting("options", "giveback", "1")
            ini.Save()
        return Plugin.GetIni("DestroySys")

    def On_Command(self, Player, cmd, args):
        if cmd == "destroy" or cmd == "crush" or cmd == "c":
            if not DataStore.ContainsKey("DestroySystem", Player.SteamID):
                DataStore.Add("DestroySystem", Player.SteamID, "true")
                Player.Message("---DestroySystem---")
                Player.Message("You are in Destroy mode")
                Player.Message("If you finished, don't forget to quit from It!")
                Player.Message("Shotgun cannot be used in destroy mode!")
            else:
                DataStore.Add("DestroySystem", Player.SteamID, "false")
                Player.Message("---DestroySystem---")
                Player.Message("You quit Destroy mode!")

    Items = {
        'WoodFoundation': 'Wood Foundation',
        'WoodDoorFrame': 'Wood Doorway',
        'WoodWall': 'Wood Wall',
        'WoodPillar': 'Wood Pillar',
        'WoodCeiling': 'Wood Ceiling',
        'MetalDoor': 'Metal Door',
        'WoodStairs': 'Wood Stairs',
        'WoodWindowFrame': 'Wood Window',
        'MetalFoundation': 'Metal Foundation',
        'MetalDoorFrame': 'Metal Doorway',
        'MetalWall': 'Metal Wall',
        'MetalPillar': 'Metal Pillar',
        'MetalCeiling': 'Metal Stairs',
        'MetalStairs': 'Metal Stairs',
        'MetalWindowFrame': 'Metal Window',
        'Wood_Shelter': 'Wood Shelter',
        'Barricade_Fence_Deployable': 'Wood Barricade',
        'Wood Box': 'Wood Storage Box',
        'Wood Box Large': 'Large Wood Storage',
        'Metal Bars Window': 'Metal Window Bars',
        'CampFire': 'Camp Fire',
        'Wood Spike Wall': 'Spike Wall',
        'Large Wood Spike Wall': 'Large Spike Wall'
    }


    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            #On Entity hurt the attacker is an NPC and a Player for somereason. We will try to grab his ID
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            gun = HurtEvent.WeaponName
            if gun == "Shotgun":
                return
            else:
                get = DataStore.Get("DestroySystem", str(id))
                #Dirty fucking hack against current bug. (Entity OWNERID request isn't working good yet, so hax it)
                OwnerID = self.GetIt(HurtEvent.Entity)
                if OwnerID is None:
                    return
                if str(id) == str(OwnerID) and get == "true":
                    if self.IsEligible(HurtEvent):
                        EntityName = HurtEvent.Entity.Name
                        HurtEvent.Entity.Destroy()
                        ini = self.DestroySys()
                        giveback = int(ini.GetSetting("options", "giveback"))
                        if giveback == 1:
                            item = self.Items.get(EntityName, None)
                            if item is None:
                                return
                            else:
                                HurtEvent.Attacker.Inventory.AddItem(item, 1)