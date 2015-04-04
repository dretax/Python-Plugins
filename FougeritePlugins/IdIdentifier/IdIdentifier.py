__author__ = 'DreTaX'
__version__ = '1.4'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""


class IdIdentifier:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("IdIdentifier by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def PlayersIni(self):
        if not Plugin.IniExists("Players"):
            ini = Plugin.CreateIni("Players")
            ini.Save()
        return Plugin.GetIni("Players")

    #There is an error while converting ownerid to string in C#. Hax it.
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

    def ManualBan(self):
        if not Plugin.IniExists("ManualBan"):
            ini = Plugin.CreateIni("ManualBan")
            ini.Save()
        return Plugin.GetIni("ManualBan")

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def On_PlayerConnected(self, Player):
        sid = self.TrytoGrabID(Player)
        if sid is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        name = Player.Name
        ip = str(Player.IP)
        ini = self.PlayersIni()
        if ini.GetSetting("Track", sid) is not None:
            ini.SetSetting("Track", sid, name)
            ini.Save()
        else:
            ini.AddSetting("Track", sid, name)
            ini.Save()
        Plugin.Log("LastJoin", str(name) + "|" + sid + "|" + ip)


    def On_PlayerDisconnected(self, Player):
        name = Player.Name
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        location = str(Player.Location)
        Plugin.Log("LastQuit", str(name) + "|" + id + "|" + location)

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
            #On Entity hurt the attacker is an NPC and a Player for somereason. We will try to grab his ID
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            gun = HurtEvent.WeaponName
            if gun == "Shotgun":
                return
            else:
                #Dirty fucking hack against current bug. (Entity OWNERID request isn't working good yet, so hax it)
                OwnerID = self.GetIt(HurtEvent.Entity)
                if OwnerID is None:
                    return
                get = DataStore.Get("OwnerMode", HurtEvent.Attacker.SteamID)
                if get is not None and get == "true":
                    HurtEvent.DamageAmount = 0
                    OwnerID = HurtEvent.Entity.OwnerID
                    name = self.PlayersIni().GetSetting("Track", OwnerID)
                    if name is not None:
                        HurtEvent.Attacker.Notice(HurtEvent.Entity.Name + " is owned by " + name + ".")
                    else:
                        HurtEvent.Attacker.Notice(HurtEvent.Entity.Name + " is owned by " + OwnerID + ".")