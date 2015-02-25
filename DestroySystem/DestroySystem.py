__author__ = 'DreTaX'
__version__ = '1.4'
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
        DataStore.Flush("DestroySystem")

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
            Player.MessageFrom("DestroySystem", "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

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

    def On_Command(self, Player, cmd, args):
        ini = self.Foundation()
        if cmd == "destroy" or cmd == "crush" or cmd == "c":
            if not DataStore.ContainsKey("DestroySystem", Player.SteamID):
                DataStore.Add("DestroySystem", Player.SteamID, "True")
                Player.Message("---DestroySystem---")
                Player.Message("You are in Destroy mode")
                Player.Message("If you finished, don't forget to quit from It!")
                Player.Message("Shotgun cannot be used in destroy mode!")
            else:
                DataStore.Add("DestroySystem", Player.SteamID, "False")
                Player.Message("---DestroySystem---")
                Player.Message("You quit Destroy mode!")
        elif cmd == "sharefoundation":
            if len(args) == 0:
                Player.Message("Usage: /sharefoundation name")
                return
            playerr = self.CheckV(Player, args)
            if playerr is None:
                return
            ini.AddSetting(Player.SteamID, playerr.SteamID, playerr.Name)
            ini.Save()
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

    Items = {
        'WoodFoundation': 'Wood Foundation',
        'WoodDoorFrame': 'Wood Doorway',
        'WoodDoor': 'Wood Door',
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
        'MetalCeiling': 'Metal Ceiling',
        'MetalStairs': 'Metal Stairs',
        'MetalWindowFrame': 'Metal Window',
        'Wood_Shelter': 'Wood Shelter',
        'Barricade_Fence_Deployable': 'Wood Barricade',
        'Wood Box': 'Wood Storage Box',
        'Wood Box Large': 'Large Wood Storage',
        'Metal Bars Window': 'Metal Window Bars',
        'CampFire': 'Camp Fire',
        'Wood Spike Wall': 'Spike Wall',
        'Large Wood Spike Wall': 'Large Spike Wall',
        'Workbench': 'Workbench',
        'WoodGate': 'Wood Gate',
        'WoodGateway': 'Wood Gateway',
        'RepairBench': 'Repair Bench',
        'Furnace': 'Furnace'
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
            get = DataStore.Get("DestroySystem", str(id))
            OwnerID = self.GetIt(HurtEvent.Entity)
            if OwnerID is None:
                return
            if (long(id) == long(OwnerID) or self.IsFriend(OwnerID, id)) and bool(get):
                if self.IsEligible(HurtEvent):
                    EntityName = HurtEvent.Entity.Name
                    HurtEvent.Entity.Destroy()
                    ini = self.DestroySys()
                    giveback = int(ini.GetSetting("options", "giveback"))
                    if giveback == 1:
                        item = self.Items.get(EntityName, None)
                        if item is None:
                            return
                        HurtEvent.Attacker.Inventory.AddItem(item)