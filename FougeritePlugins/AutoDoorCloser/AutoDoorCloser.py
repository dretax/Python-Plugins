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
from System import *

"""
    Class
"""

DStable = "DoorCloser"
class AutoDoorCloser:

    bd = None
    params = System.Linq.Enumerable.ToArray[System.Object]([None, System.Convert.ToUInt64(Plugin.GetTimestamp()), None])

    def On_PluginInit(self):
        self.bd = Util.TryFindReturnType("BasicDoor")
        DataStore.Flush(DStable)

    def On_Command(self, Player, cmd, args):
        if cmd == "doorcloser":
            string = str.join(' ', args)
            if not string.isnumeric():
                Player.Message("Usage: /doorcloser number")
                return
            string = int(string)
            if 5 <= string <= 30:
                DataStore.Add(DStable, Player.UID, string)
            else:
                Player.Message("Number must be between 5-30")

    def On_DoorUse(self, Player, DoorUseEvent):
        if str(DoorUseEvent.BasicDoor.state) != "Closed: 3":
            return
        if DataStore.ContainsKey(DStable, Player.UID):
            n = DataStore.Get(DStable, Player.UID)
            List = Plugin.CreateDict()
            List["BasicDoor"] = DoorUseEvent.BasicDoor
            Plugin.CreateParallelTimer("AutoCloser", n * 1000, List).Start()

    def AutoCloserCallback(self, timer):
        timer.Kill()
        List = timer.Args
        BasicDoor = List["BasicDoor"]
        if str(BasicDoor.state) == "Opened: 1":
            self.bd.ToggleStateServer(BasicDoor, self.params)