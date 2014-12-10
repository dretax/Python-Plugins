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
                            if EntityName == "WoodFoundation":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Foundation", 1)

                            elif EntityName == "WoodDoorFrame":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Doorway", 1)

                            elif EntityName == "WoodWall":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Wall", 1)

                            elif EntityName == "WoodPillar":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Pillar", 1)

                            elif EntityName == "WoodCeiling":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Ceiling", 1)

                            elif EntityName == "MetalDoor":
                                HurtEvent.Attacker.Inventory.AddItem("Metal Door", 1)

                            elif EntityName == "WoodStairs":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Stairs", 1)

                            elif EntityName == "WoodWindowFrame":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Window", 1)

                            elif EntityName == "MetalFoundation":
                                HurtEvent.Attacker.Inventory.AddItem("Metal Foundation", 1)

                            elif EntityName == "MetalDoorFrame":
                                HurtEvent.Attacker.Inventory.AddItem("Metal Doorway", 1)

                            elif EntityName == "MetalWall":
                                HurtEvent.Attacker.Inventory.AddItem("Metal Wall", 1)

                            elif EntityName == "MetalPillar":
                                HurtEvent.Attacker.Inventory.AddItem("Metal Pillar", 1)

                            elif EntityName == "MetalCeiling":
                                HurtEvent.Attacker.Inventory.AddItem("Metal Ceiling", 1)

                            elif EntityName == "MetalStairs":
                                HurtEvent.Attacker.Inventory.AddItem("Metal Stairs", 1)

                            elif EntityName == "MetalWindowFrame":
                                HurtEvent.Attacker.Inventory.AddItem("Metal Window", 1)

                            elif EntityName == "Wood_Shelter":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Shelter", 1)

                            elif EntityName == "Barricade_Fence_Deployable":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Barricade", 1)

                            elif EntityName == "Wood Box":
                                HurtEvent.Attacker.Inventory.AddItem("Wood Storage Box", 1)

                            elif EntityName == "Wood Box Large":
                                HurtEvent.Attacker.Inventory.AddItem("Large Wood Storage", 1)

                            elif EntityName == "Metal Bars Window":
                                HurtEvent.Attacker.Inventory.AddItem("Metal Window Bars", 1)

                            elif EntityName == "CampFire":
                                HurtEvent.Attacker.Inventory.AddItem("Camp Fire", 1)

                            elif EntityName == "Wood Spike Wall":
                                HurtEvent.Attacker.Inventory.AddItem("Spike Wall", 1)

                            elif EntityName == "Large Wood Spike Wall":
                                HurtEvent.Attacker.Inventory.AddItem("Large Spike Wall", 1)