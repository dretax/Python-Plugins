__author__ = 'DreTaX'
__version__ = '1.0'

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

    def Players(self):
        if not Plugin.IniExists("Players"):
            ini = Plugin.CreateIni("Players")
            ini.Save()
        return Plugin.GetIni("Players")

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    #  There is an error while converting ownerid to string in C#. Hax it.
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
        ini = self.Players()
        name = Player.Name
        ip = str(Player.IP)
        if ini.GetSetting("Track", id) is not None:
            ini.SetSetting("Track", id, name)
            ini.Save()
        else:
            ini.AddSetting("Track", id, name)
            ini.Save()
        Plugin.Log("LastJoin", str(name) + "|" + id + "|" + ip)

    def On_PlayerHurt(self, HurtEvent):
        if not self.IsAnimal(HurtEvent.Attacker) and HurtEvent.Sleeper:
            ini = self.Players()
            n = ini.GetSetting("Track", HurtEvent.Attacker.SteamID)
            n2 = ini.GetSetting("Track", HurtEvent.Victim.OwnerID)
            Plugin.Log("SleeperLog", "Attacker: " + n + " | " + HurtEvent.Attacker.SteamID + " | " +
                       str(HurtEvent.Attacker.Location) + " Vic: " + HurtEvent.Victim.OwnerID + " | " + n2)

    def On_Command(self, Player, cmd, args):
        if cmd == "owner":
            if Player.Admin or self.isMod(Player.SteamID):
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
            if Player.Admin or self.isMod(Player.SteamID):
                id = Player.SteamID
                if not DataStore.ContainsKey("DecayOff", id):
                    Player.Message("---Decay---")
                    Player.Message("You are in Decay mode")
                    Player.Message("If you finished, don't forget to quit from It!")
                    Player.Message("Shotgun cannot be used in Owner mode!")
                    DataStore.Add("DecayOff", id, "true")
                else:
                    DataStore.Remove("DecayOff", id)
                    Player.Message("---Decay---")
                    Player.Message("You quit Decay mode!")
        elif cmd == "closedeployed":
            if Player.Admin or self.isMod(Player.SteamID):
                loc = Player.Location
                for x in World.Entities:
                    name = str(x.Name)
                    if not "barricade" in name.lower():
                        continue
                    dist = round(Util.GetVectorsDistance(loc, x.Location), 2)
                    if dist < 3.0:
                        Player.Message("Found: " + name + " OwnerID: " + x.OwnerID)

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            #  On Entity hurt the attacker is an NPC and a Player for somereason. We will try to grab his ID
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            #  Dirty fucking hack against current bug. (Entity OWNERID request isn't working good yet, so hax it)
            OwnerID = self.GetIt(HurtEvent.Entity)
            if OwnerID is None:
                return
            if DataStore.ContainsKey("OwnerMode", HurtEvent.Attacker.SteamID):
                gun = HurtEvent.WeaponName
                if gun == "Shotgun":
                    return
                HurtEvent.DamageAmount = 0
                OwnerID = HurtEvent.Entity.OwnerID
                name = self.Players().GetSetting("Track", OwnerID)
                if name is not None:
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