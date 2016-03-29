__author__ = 'DreTaX'
__version__ = '1.7.3'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System

"""
    Class
"""

EntityList = {

}

class DestroySystem:
    """
        Methods
    """

    giveback = None
    TurnOfAfterATime = None
    Time = None

    def On_PluginInit(self):
        Util.ConsoleLog("DestroySystem by " + __author__ + " Version: " + __version__ + " loaded.", False)
        ini = self.DestroySys()
        self.giveback = int(ini.GetSetting("options", "giveback"))
        self.TurnOfAfterATime = int(ini.GetSetting("options", "TurnOfAfterATime"))
        self.Time = int(ini.GetSetting("options", "Time")) * 1000
        DataStore.Flush("DestroySystem")
        DataStore.Flush("DestroySystem2")
        EntityList['WoodFoundation'] = "Wood Foundation"
        EntityList['WoodDoorFrame'] = "Wood Doorway"
        EntityList['WoodDoor'] = "Wood Door"
        EntityList['WoodPillar'] = "Wood Pillar"
        EntityList['WoodWall'] = "Wood Wall"
        EntityList['WoodCeiling'] = "Wood Ceiling"
        EntityList['WoodWindowFrame'] = "Wood Window"
        EntityList['WoodStairs'] = "Wood Stairs"
        EntityList['WoodRamp'] = "Wood Ramp"
        EntityList['WoodSpikeWall'] = "Spike Wall"
        EntityList['LargeWoodSpikeWall'] = "Large Spike Wall"
        EntityList['WoodBox'] = "Wood Storage Box"
        EntityList['WoodBoxLarge'] = "Large Wood Storage"
        EntityList['WoodGate'] = "Wood Gate"
        EntityList['WoodGateway'] = "Wood Gateway"
        EntityList['WoodenDoor'] = "Wood Door"
        EntityList['Wood_Shelter'] = "Wood Shelter"
        EntityList['MetalWall'] = "Metal Wall"
        EntityList['MetalCeiling'] = "Metal Ceiling"
        EntityList['MetalDoorFrame'] = "Metal Doorway"
        EntityList['MetalPillar'] = "Metal Pillar"
        EntityList['MetalFoundation'] = "Metal Foundation"
        EntityList['MetalStairs'] = "Metal Stairs"
        EntityList['MetalRamp'] = "Metal Ramp"
        EntityList['MetalWindowFrame'] = "Metal Window"
        EntityList['MetalDoor'] = "Metal Door"
        # EntityList['MetalBarsWindow'] = "Metal Window Bars"
        EntityList['SmallStash'] = "Small Stash"
        EntityList['Campfire'] = "Camp fire"
        EntityList['Furnace'] = "Furnace"
        EntityList['Workbench'] = "Workbench"
        EntityList['Wood Barricade'] = "Wood Barricade"
        EntityList['RepairBench'] = "Repair Bench"
        EntityList['SleepingBagA'] = "Sleeping Bag"
        EntityList['SingleBed'] = "Bed"

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.1
    """

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom("DestroySystem", "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom("DestroySystem", "Found [color#FF0000]" + str(count)
                               + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def IsEligible(self, HurtEvent):
        try:
            Eligible = HurtEvent.Entity.Object._master.ComponentCarryingWeight(HurtEvent.Entity.Object)
            return not (Eligible)
        except:
            return True

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
            ini.AddSetting("options", "TurnOfAfterATime", "1")
            ini.AddSetting("options", "Time", "60")
            ini.Save()
        return Plugin.GetIni("DestroySys")

    def Foundation(self):
        if not Plugin.IniExists("Foundation"):
            ini = Plugin.CreateIni("Foundation")
            ini.Save()
        return Plugin.GetIni("Foundation")

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def IsFriend(self, id, tid):
        ini = self.Foundation()
        if ini.GetSetting(str(id), str(tid)) is not None:
            return True
        return False

    def DestroyTimeoutCallback(self, timer):
        timer.Kill()
        List = timer.Args
        Player = List["Player"]
        if not Player.IsOnline:
            return
        id = Player.SteamID
        if DataStore.Get("DestroySystem", id) is not None:
            Player.Message("---DestroySystem---")
            Player.Message("You quit Destroy mode!")
        elif DataStore.Get("DestroySystem2", id) is not None:
            Player.Message("---DestroySystem---")
            Player.Message("You quit Destroy ALL mode!")

    def On_Command(self, Player, cmd, args):
        ini = self.Foundation()
        if cmd == "destroy" or cmd == "crush" or cmd == "c":
            if not DataStore.ContainsKey("DestroySystem", Player.SteamID):
                DataStore.Add("DestroySystem", Player.SteamID, True)
                Player.Message("---DestroySystem---")
                Player.Message("You are in Destroy mode")
                Player.Message("If you finished, don't forget to quit from It!")
                Player.Message("Shotgun cannot be used in destroy mode!")
                if self.TurnOfAfterATime == 1:
                    List = Plugin.CreateDict()
                    List["Player"] = Player
                    Plugin.CreateParallelTimer("DestroyTimeout", self.Time, List).Start()
            else:
                DataStore.Remove("DestroySystem", Player.SteamID)
                Player.Message("---DestroySystem---")
                Player.Message("You quit Destroy mode!")
        elif cmd == "destroyall":
            if not DataStore.ContainsKey("DestroySystem2", Player.SteamID):
                DataStore.Add("DestroySystem2", Player.SteamID, True)
                Player.Message("---DestroySystem---")
                Player.Message("You are in Destroy ALL mode")
                Player.Message("If you finished, don't forget to quit from It!")
                Player.Message("Shotgun cannot be used in Destroy ALL mode!")
                if self.TurnOfAfterATime == 1:
                    List = Plugin.CreateDict()
                    List["Player"] = Player
                    Plugin.CreateParallelTimer("DestroyTimeout", self.Time, List).Start()
            else:
                DataStore.Remove("DestroySystem2", Player.SteamID)
                Player.Message("---DestroySystem---")
                Player.Message("You quit Destroy ALL mode!")
        elif cmd == "sharefoundation":
            if len(args) == 0:
                Player.Message("Usage: /sharefoundation name")
                return
            playerr = self.CheckV(Player, args)
            if playerr is None:
                return
            ini.AddSetting(Player.SteamID, playerr.SteamID, playerr.Name)
            ini.Save()
            Player.Message("Sharing Foundations with: " + playerr.Name)
        elif cmd == "lfoundation":
            enum = ini.EnumSection(Player.SteamID)
            Player.Message("Foundation List:")
            for id in enum:
                Player.Message("- " + ini.GetSetting(Player.SteamID, id))
        elif cmd == "delfoundation":
            if len(args) == 0:
                Player.Message("Usage: /delfoundation name")
                return
            enum = ini.EnumSection(Player.SteamID)
            text = self.argsToText(args)
            for id in enum:
                n = ini.GetSetting(Player.SteamID, id)
                if n in text or n == text:
                    ini.DeleteSetting(Player.SteamID, id)
                    ini.Save()
                    Player.Message("Deleted " + n + " from foundation whitelist.")
                    return
            Player.Message("Couldn't find: " + text)

    def On_EntityHurt(self, HurtEvent):
        if not HurtEvent.AttackerIsPlayer:
            return
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            gun = HurtEvent.WeaponName
            if gun == "Shotgun":
                return
            OwnerID = self.GetIt(HurtEvent.Entity)
            if OwnerID is None:
                return
            id = HurtEvent.Attacker.SteamID
            if long(id) == long(OwnerID) or self.IsFriend(OwnerID, id):
                EntityName = HurtEvent.Entity.Name
                if DataStore.ContainsKey("DestroySystem", id):
                    if self.IsEligible(HurtEvent):
                        HurtEvent.Entity.Destroy()
                        if self.giveback == 1:
                            if EntityName in EntityList.keys():
                                HurtEvent.Attacker.Inventory.AddItem(EntityList[EntityName])
                elif DataStore.ContainsKey("DestroySystem2", id):
                    structs = HurtEvent.Entity.GetLinkedStructs()
                    if self.giveback == 1:
                        if EntityName in EntityList.keys():
                            HurtEvent.Attacker.Inventory.AddItem(EntityList[EntityName])
                    for ent in structs:
                        if self.giveback == 1:
                            namef = ent.Name
                            if namef in EntityList.keys():
                                HurtEvent.Attacker.Inventory.AddItem(EntityList[namef])
                        ent.Destroy()
                    HurtEvent.Entity.Destroy()
