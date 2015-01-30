__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

"""
    Class
"""

DStable = "DoorCloser"
class AutoDoorCloser:

    bd = None

    def On_PluginInit(self):
        self.bd = Util.TryFindReturnType("BasicDoor")
        if self.bd is None:
            Plugin.Log("Error", "Couldn't find return type.")

    def Stringify(self, List):
        s = re.sub("[[\]\'\ ]", '', str(List))
        return str(s)

    def Parse(self, String):
        return String.split(',')

    def ReplaceToDot(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(':')

    """
        Timer Functions
    """

    def addJob(self, id, xtime, location):
        epoch = Plugin.GetTimestamp()
        exectime = int(epoch) + int(xtime)
        # ID, EXECTIME : Location | Requires to be splited
        List = []
        List.append(str(exectime))
        List.append(str(location).replace(',', ':'))
        DataStore.Add(DStable, id, self.Stringify(List))
        self.startTimer()

    def killJob(self, id):
        DataStore.Remove(DStable, id)

    def startTimer(self):
        gfjfhg = 1700
        try:
            if not Plugin.GetTimer("AutoCloser"):
                Plugin.CreateTimer("AutoCloser", gfjfhg).Start()
        except:
            pass

    def stopTimer(self):
        timer = Plugin.GetTimer("AutoCloser")
        if timer is None:
            return
        timer.Stop()
        Plugin.Timers.Remove("AutoCloser")

    def getPlayer(self, d):
        try:
            id = str(d)
            pl = Server.FindPlayer(id)
            return pl
        except:
            return None

    def clearTimers(self):
        DataStore.Flush(DStable)
        self.stopTimer()

    def Find(self, x, y, z):
        objects = UnityEngine.Resources.FindObjectsOfTypeAll(self.bd)
        loc = Util.CreateVector(x, y, z)
        for door in objects:
            if door.transform.position == loc:
                return door
        return None

    def On_DoorUse(self, Player, DoorUseEvent):
        #if DoorUseEvent.Open:
        loc = Util.CreateVector(float(DoorUseEvent.Entity.X), float(DoorUseEvent.Entity.Y), float(DoorUseEvent.Entity.Z))
        self.addJob(Player.SteamID, 2, loc)

    def AutoCloserCallback(self):
        epoch = int(Plugin.GetTimestamp())
        if DataStore.Count(DStable) >= 1:
            pending = DataStore.Keys(DStable)
            for id in pending:
                if DataStore.Get(DStable, id) is None:
                    DataStore.Remove(DStable, id)
                    continue
                params = self.Parse(str(DataStore.Get(DStable, id)))
                if epoch >= int(params[0]):
                    self.killJob(id)
                    xto = self.ReplaceToDot(params[1])
                    door = self.Find(float(xto[0]), float(xto[1]), float(xto[2]))
                    if door is None:
                        continue
                    if self.bd is not None:
                        # Praise baluerino
                        self.bd.InvokeMember("ToggleStateServer", System.Reflection.BindingFlags.InvokeMethod | System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance, None, door, System.Linq.Enumerable.ToArray([None, Plugin.GetTimestamp().As[System.UInt64], None]))
        else:
            self.stopTimer()