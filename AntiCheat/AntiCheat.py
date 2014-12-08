__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

class AntiCheat:
    def On_PluginInit(self):
        DataStore.Flush("EquinoxAntiCheat")
        Plugin.CreateTimer("CheckLOC", 5000).Start()

    def CheckLOCCallback(self):
        Plugin.KillTimer("CheckLOC")
        currentlist = Server.Players
        for player in currentlist:
            try:
                id = player.SteamID
                name = player.Name
            except:
                continue
            tpfriendteleport = DataStore.Get("tpfriendautoban", id)
            hometeleport = DataStore.Get("homesystemautoban", id)
            if not player.Admin and not self.isMod(id) and tpfriendteleport != "using" and hometeleport != "using":
                loc = player.Location
                if DataStore.Get("EquinoxAntiCheat", id) == "undefined" or DataStore.Get("EquinoxAntiCheat", id) is None:
                    DataStore.Add('EquinoxAntiCheat', id, player.X+", "+player.Y+", "+player.Z)
                    continue
                locl = DataStore.Get("EquinoxAntiCheat", id).split(",")
                vector = Util.CreateVector(locl[0], locl[1], locl[2])
                ndist = round(Util.GetVectorsDistance(vector, loc), 2)
                ndistt = round(int(player.Y) - int(locl[1]), 2)
                if ndistt > 23 and ndistt > 0:
                    player.Message("You moved too fast!")
                    Server.Broadcast(name + " was moving too fast. Kicked.")
                    player.Disconnect()
                    continue
                if ndist >= 43 and ndistt > 0:
                    player.Message("You moved too fast!")
                    Server.Broadcast(name + " was moving too fast. Kicked.")
                    player.Disconnect()
                    continue
                DataStore.Add('EquinoxAntiCheat', id, player.X+", "+player.Y+", "+player.Z)
        Plugin.CreateTimer("CheckLOC", 5000).Start()

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False