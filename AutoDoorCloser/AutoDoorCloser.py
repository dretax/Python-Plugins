__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("System.Core", "IronPythonModule")
import IronPythonModule
from IronPythonModule import Extensions
import Fougerite
import re
import UnityEngine
from UnityEngine import *
import System
from System import Reflection

"""
    Class
"""

DStable = "DoorCloser"
class AutoDoorCloser:

    bd = None
    flags = System.Reflection.BindingFlags.InvokeMethod | System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance
    params = System.Linq.Enumerable.ToArray[System.Object]([None, System.Convert.ToUInt64(Plugin.GetTimestamp()), None])

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

    def addJob(self, xtime, location):
        epoch = Plugin.GetTimestamp()
        exectime = int(epoch) + int(xtime)
        DataStore.Add(DStable, str(location).replace(',', ':'), exectime)
        self.startTimer()

    def killJob(self, loc):
        DataStore.Remove(DStable, loc)

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
            Distance = Util.GetVectorsDistance(loc, door.transform.position)
            if Distance < 1.5:
                return door
        return None

    def On_DoorUse(self, Player, DoorUseEvent):
        #if DoorUseEvent.Open:
        loc = Util.CreateVector(float(DoorUseEvent.Entity.X), float(DoorUseEvent.Entity.Y), float(DoorUseEvent.Entity.Z))
        self.addJob(2, loc)

    def AutoCloserCallback(self):
        epoch = int(Plugin.GetTimestamp())
        if DataStore.Count(DStable) >= 1:
            pending = DataStore.Keys(DStable)
            for location in pending:
                if DataStore.Get(DStable, location) is None:
                    DataStore.Remove(DStable, location)
                    continue
                time = DataStore.Get(DStable, location)
                if epoch >= int(time):
                    self.killJob(location)
                    xto = self.ReplaceToDot(location)
                    door = self.Find(float(xto[0]), float(xto[1]), float(xto[2]))
                    if door is None:
                        continue
                    if self.bd is not None:
                        # Praise baluerino
                        self.bd.InvokeMember("ToggleStateServer", self.flags, None, door, self.params)
        else:
            self.clearTimers()