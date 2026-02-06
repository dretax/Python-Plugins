__author__ = 'DreTaX'
__version__ = '1.4.1'

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
        location = str(Player.DisconnectLocation)
        Plugin.Log("LastQuit", str(name) + "|" + id + "|" + location)

    def On_ItemRemoved(self, InventoryModEvent):
        if InventoryModEvent.Player is not None and InventoryModEvent.InventoryItem is not None:
            en = InventoryModEvent.Inventory.name
            if "woodbox" in en.lower() or "stash" in en.lower():
                n = InventoryModEvent.Player.Name
                d = InventoryModEvent.Player.SteamID
                loc = str(InventoryModEvent.Player.Location)
                el = str(InventoryModEvent.Inventory.transform.position)
                Plugin.Log("InventoryRemove", "New: " + n + "|" + d + "|" + en + "| C: " + el + "| P: " + loc)
                if InventoryModEvent.InventoryItem is not None:
                    inn = str(InventoryModEvent.ItemName)
                    q = str(InventoryModEvent.InventoryItem.uses)
                    Plugin.Log("InventoryRemove", inn + " " + q)
                else:
                    Plugin.Log("InventoryRemove", "Inventory item was null?! " + str(InventoryModEvent.InventoryItem))

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Attacker is None or HurtEvent.Victim is None:
            return
        if not HurtEvent.AttackerIsPlayer:
            return

        if not self.IsAnimal(HurtEvent.Attacker) and HurtEvent.VictimIsSleeper:
            n = HurtEvent.Attacker.Name

            victim_cp = PlayerCache.GetPlayerBySteamId(HurtEvent.Victim.UID)
            n2 = "Unknown"
            if victim_cp is not None:
                n2 = victim_cp.Name

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
            if not HurtEvent.AttackerIsPlayer:
                return
            id = HurtEvent.Attacker.SteamID
            OwnerID = HurtEvent.Entity.UOwnerID
            if DataStore.ContainsKey("OwnerMode", HurtEvent.Attacker.SteamID):
                gun = HurtEvent.WeaponName
                if gun == "Shotgun":
                    return
                HurtEvent.DamageAmount = 0

                cached_owner = PlayerCache.GetPlayerBySteamId(OwnerID)
                if cached_owner:
                    name = cached_owner.Name
                    HurtEvent.Attacker.Notice(HurtEvent.Entity.Name + " is owned by " + name + ".")
                else:
                    HurtEvent.Attacker.Notice(HurtEvent.Entity.Name + " is owned by " + str(OwnerID) + ".")
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
                        entityid = HurtEvent.Entity.OwnerID
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
                        entityid = HurtEvent.Entity.OwnerID
                        entityloc = Util.CreateVector(HurtEvent.Entity.X, HurtEvent.Entity.Y, HurtEvent.Entity.Z)
                        Plugin.Log("ChestLog", str(entityloc) + " | " + HurtEvent.Entity.Name + " | " + entityid
                                   + " | PlayerDatas: " + id + "|" + name + "|" + loc)