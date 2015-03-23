__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

class AntiCheat:

    red = "[color #FF0000]"
    Players = []

    def On_PluginInit(self):
        DataStore.Flush("EquinoxAntiCheat")
        for p in Server.Players:
            self.Players.append(p)
        Plugin.CreateTimer("CheckLOC", 5000).Start()

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        DataStore.Remove("EquinoxAntiCheat", id)
        self.Players.append(Player)

    def On_PlayerDisconnected(self, Player):
        self.Players.remove(Player)
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        DataStore.Remove("EquinoxAntiCheat", id)

    def CheckLOCCallback(self):
        Plugin.KillTimer("CheckLOC")
        for player in self.Players:
            try:
                id = player.SteamID
                name = player.Name
            except:
                continue
            tpfriendteleport = DataStore.Get("tpfriendautoban", id)
            hometeleport = DataStore.Get("homesystemautoban", id)
            if not player.Admin and not self.isMod(id) and tpfriendteleport != "using" and hometeleport != "using":
                if player.X == 0.0 and player.Y == 0.0 and player.Z == 0.0:
                    continue
                loc = player.Location
                if DataStore.Get("EquinoxAntiCheat", id) is None:
                    DataStore.Add('EquinoxAntiCheat', id, str(player.X) + "," + str(player.Y) + "," + str(player.Z))
                    continue
                locl = DataStore.Get("EquinoxAntiCheat", id).split(",")
                vector = Util.CreateVector(float(locl[0]), float(locl[1]), float(locl[2]))
                fdist = Util.GetVectorsDistance(vector, loc)
                ndist = round(fdist, 2)
                ndistt = round(float(player.Y) - float(locl[1]), 2)
                if ndistt > 23:
                    player.Message(self.red + "You moved too fast!")
                    Server.Broadcast(self.red + str(name) + " was moving too fast. Kicked. (" + str(ndistt) + " m)")
                    player.Disconnect()
                    continue
                if ndist >= 43:
                    player.Message(self.red + "You moved too fast!")
                    Server.Broadcast(self.red + str(name) + " was moving too fast. Kicked. (" + str(ndist) + " m)")
                    player.Disconnect()
                    continue
                DataStore.Add('EquinoxAntiCheat', id, str(player.X) + "," + str(player.Y) + "," + str(player.Z))
        Plugin.CreateTimer("CheckLOC", 5000).Start()

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.Victim is not None and DeathEvent.Attacker is not None:
            DeathEvent.Victim.X = 0.0
            DeathEvent.Victim.Y = 0.0
            DeathEvent.Victim.Z = 0.0
            DataStore.Remove("EquinoxAntiCheat", DeathEvent.Victim.SteamID)

    def On_PlayerSpawned(self, Player, SpawnEvent):
        id = Player.SteamID
        DataStore.Remove("EquinoxAntiCheat", id)

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False