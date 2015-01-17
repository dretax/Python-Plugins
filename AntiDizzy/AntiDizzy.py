__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

"""
    Class
"""

DStable = 'AntiDizzy'
class AntiDizzy:

    """
        Timer Functions
    """

    def addJob(self, id, xtime):
        epoch = Plugin.GetTimestamp()
        exectime = int(epoch) + int(xtime)
        DataStore.Add(DStable, id, exectime)
        self.startTimer()

    def killJob(self, id):
        DataStore.Remove(DStable, id)

    def startTimer(self):
        gfjfhg = 2000
        try:
            if not Plugin.GetTimer("AntiDizzy"):
                Plugin.CreateTimer("AntiDizzy", gfjfhg).Start()
        except:
            pass

    def stopTimer(self):
        Plugin.KillTimer("AntiDizzy")

    def getPlayer(self, d):
        try:
            pl = Server.FindPlayer(d)
            return pl
        except:
            return None

    def clearTimers(self):
        DataStore.Flush(DStable)
        self.stopTimer()


    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def Replace(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(',')

    def On_PlayerSpawned(self, Player, SpawnEvent):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.SteamID
            except:
                pass
            return
        if DataStore.Get("LastLoc", id) is not None:
            loc = DataStore.Get("LastLoc", id)
            loc = self.Replace(loc)
            Player.TeleportTo(float(loc[0]), float(loc[1]) + float(2.5), float(loc[2]))
            self.addJob(id, 4)
            Server.Broadcast("Tp1")

    def AntiDizzyCallback(self):
        epoch = int(Plugin.GetTimestamp())
        if DataStore.Count(DStable) >= 1:
            pending = DataStore.Keys(DStable)
            for id in pending:
                if DataStore.Get(DStable, id) is None:
                    DataStore.Remove(DStable, id)
                    continue
                param = DataStore.Get(DStable, id)
                if epoch >= int(param):
                    Player = self.getPlayer(id)
                    self.killJob(id)
                    if Player is None:
                        continue
                    loc = DataStore.Get("LastLoc", id)
                    if loc is None:
                        continue
                    loc = self.Replace(loc)
                    #Player.TeleportTo(float(loc[0]), float(loc[1]) + float(2.5), float(loc[2]))
                    vec = Util.CreateVector(float(loc[0]), float(loc[1]), float(loc[2]))
                    Server.Broadcast("Current: " + str(float(Player.Y)) + " Last: " + str(float(loc[1])))
                    Server.Broadcast("Y dist: " + str(float(Player.Y) - float(loc[1])))
                    d = float(Player.Y) - float(loc[1])
                    if d < (0 - float(3.8)) and d < 0.0:
                        Server.Broadcast("This fag had dizzy.")
                    DataStore.Remove("LastLoc", id)
                    Server.Broadcast("Tp2")

    def On_PlayerDisconnected(self, Player):
        id = Player.SteamID
        loc = Player.Location
        DataStore.Add("LastLoc", id, str(loc))