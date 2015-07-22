__author__ = 'DreTaX'
__version__ = '1.2b'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""


class AdminTools:
    """
        Methods
    """

    def On_PluginInit(self):
        DataStore.Flush("OwnerMode")
        DataStore.Flush("DecayOff")
        Util.ConsoleLog("AdminTools by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def GetIt(self, Entity):
        try:
            if Entity.IsDeployableObject():
                return Entity.Object.ownerID
            if Entity.IsStructure():
                return Entity.Object._master.ownerID
        except:
            return None

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def IsAnimal(self, Entity):
        if "NPC" in str(Entity):
            return True
        return False

    def On_PlayerConnected(self, Player):
        id = Player.SteamID
        name = Player.Name
        ip = str(Player.IP)
        Plugin.Log("LastJoin", str(name) + "|" + id + "|" + ip)

    def On_PlayerDisconnected(self, Player):
        name = Player.Name
        id = Player.SteamID
        location = str(Player.Location)
        Plugin.Log("LastQuit", str(name) + "|" + id + "|" + location)

    def On_ItemRemoved(self, InventoryModEvent):
        if InventoryModEvent.Player is not None:
            en = InventoryModEvent.Inventory.name
            if "woodbox" in en.lower() or "stash" in en.lower():
                n = InventoryModEvent.Player.Name
                d = InventoryModEvent.Player.SteamID
                loc = str(InventoryModEvent.Player.Location)
                el = str(InventoryModEvent.Inventory.transform.position)
                inn = InventoryModEvent.InventoryItem.datablock.name
                q = str(InventoryModEvent.InventoryItem.uses)
                Plugin.Log("InventoryRemove", "New: " + n + "|" + d + "|" + en + "| C: " + el + "| P: " + loc)
                Plugin.Log("InventoryRemove", inn + " " + q)

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Attacker is None or HurtEvent.Victim is None:
            return
        if not self.IsAnimal(HurtEvent.Attacker) and HurtEvent.Sleeper:
            if not Server.HasRustPP:
                return
            dict = Server.GetRustPPAPI().Cache
            if long(HurtEvent.Attacker.SteamID) in dict.Keys:
                n = dict[long(HurtEvent.Attacker.SteamID)]
            else:
                n = "Unknown"
            if long(HurtEvent.Victim.SteamID) in dict.Keys:
                n2 = dict[long(HurtEvent.Victim.SteamID)]
            else:
                n2 = "Unknown"
            if DataStore.ContainsKey("OwnerMode", HurtEvent.Attacker.SteamID):
                HurtEvent.DamageAmount = 0
                HurtEvent.Attacker.Notice("Owner: " + n2)
                return
            Plugin.Log("SleeperLog", "Attacker: " + n + " | " + HurtEvent.Attacker.SteamID + " | " +
                       str(HurtEvent.Attacker.Location) + " Vic: " + HurtEvent.Victim.OwnerID + " | " + n2)

    def On_Command(self, Player, cmd, args):
        if cmd == "owner":
            if Player.Admin or Player.Moderator:
                id = Player.SteamID
                if not DataStore.ContainsKey("OwnerMode", id):
                    Player.Message("---Owner---")
                    Player.Message("You are in Owner mode")
                    Player.Message("If you finished, don't forget to quit from It!")
                    Player.Message("Shotgun cannot be used in Owner mode!")
                    DataStore.Add("OwnerMode", id, "true")
                else:
                    DataStore.Remove("OwnerMode", id)
                    Player.Message("---Owner---")
                    Player.Message("You quit Owner mode!")
        elif cmd == "decayoff":
            if Player.Admin or Player.Moderator:
                id = Player.SteamID
                if not DataStore.ContainsKey("DecayOff", id):
                    Player.Message("---Decay---")
                    Player.Message("You are in Decay mode")
                    Player.Message("If you finished, don't forget to quit from It!")
                    Player.Message("Shotgun cannot be used in Decay mode!")
                    DataStore.Add("DecayOff", id, "true")
                else:
                    DataStore.Remove("DecayOff", id)
                    Player.Message("---Decay---")
                    Player.Message("You quit Decay mode!")
        elif cmd == "decayoffdeploy":
            if Player.Admin or Player.Moderator:
                loc = Player.Location
                c = 0
                for entity in World.Entities:
                    if "spike" in entity.Name.lower() or "box" in entity.Name.lower():
                        if Util.GetVectorsDistance(loc, entity.Location) < 400:
                            entity.SetDecayEnabled(False)
                            c += 1
                Player.Message("Decay is disabled on " + str(c) + " objects.")

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            OwnerID = HurtEvent.Entity.OwnerID
            if DataStore.ContainsKey("OwnerMode", HurtEvent.Attacker.SteamID):
                gun = HurtEvent.WeaponName
                if gun == "Shotgun":
                    return
                HurtEvent.DamageAmount = 0
                if not Server.HasRustPP:
                    return
                dict = Server.GetRustPPAPI().Cache
                if dict.ContainsKey(long(OwnerID)):
                    name = dict[long(OwnerID)]
                    HurtEvent.Attacker.Notice(HurtEvent.Entity.Name + " is owned by " + name + ".")
                else:
                    HurtEvent.Attacker.Notice(HurtEvent.Entity.Name + " is owned by " + OwnerID + ".")
            elif DataStore.ContainsKey("DecayOff", id):
                gun = HurtEvent.WeaponName
                if gun == "Shotgun":
                    return
                HurtEvent.DamageAmount = 0
                if HurtEvent.Entity.IsDeployableObject():
                    HurtEvent.Entity.SetDecayEnabled(False)
                    HurtEvent.Attacker.Message("Decay is now off!")
                else:
                    HurtEvent.Attacker.Message("This isn't a deployable object.")
            else:
                if HurtEvent.Entity.IsStructure() or HurtEvent.Entity.IsDeployableObject():
                    if HurtEvent.DamageType == "Explosion":
                        entityloc = str(Util.CreateVector(HurtEvent.Entity.X, HurtEvent.Entity.Y, HurtEvent.Entity.Z))
                        entityid = str(self.GetIt(HurtEvent.Entity))
                        if HurtEvent.WeaponName == "Explosive Charge":
                            Plugin.Log("C4", str(HurtEvent.Attacker.Location) + " | " + HurtEvent.Attacker.Name
                                       + " | " + id + " | Entity: " + HurtEvent.Entity.Name + " | "
                                       + entityloc + " | " + entityid)
                        else:
                            Plugin.Log("Grenade", str(HurtEvent.Attacker.Location) + " | "
                                       + HurtEvent.Attacker.Name + " | " + id + " | Entity: " + HurtEvent.Entity.Name
                                       + " | " + entityloc + " | " + entityid)
                    if HurtEvent.Entity.Name == "WoodBoxLarge" or HurtEvent.Entity.Name == "WoodBox" \
                            or HurtEvent.Entity.Name == "SmallStash":
                        name = HurtEvent.Attacker.Name
                        loc = str(HurtEvent.Attacker.Location)
                        entityid = str(self.GetIt(HurtEvent.Entity))
                        entityloc = Util.CreateVector(HurtEvent.Entity.X, HurtEvent.Entity.Y, HurtEvent.Entity.Z)
                        Plugin.Log("ChestLog", str(entityloc) + " | " + HurtEvent.Entity.Name + " | " + entityid
                                   + " | PlayerDatas: " + id + "|" + name + "|" + loc)