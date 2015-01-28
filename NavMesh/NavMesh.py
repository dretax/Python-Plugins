__author__ = 'DreTaX'
__version__ = '1.0'
import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import Fougerite
import System
from System import Reflection
from UnityEngine import *


class NavMesh:

    def On_PluginInit(self):
        Plugin.CreateTimer("KillThem", 420000).Start()

    def KillEmAll(self):
        basicWildlifeAi = Util.TryFindReturnType("BasicWildLifeAI")
        takeDamage = Util.TryFindReturnType("TakeDamage")
        if basicWildlifeAi is None or takeDamage is None:
            return
        count = 0
        #ailist = Object.FindObjectsOfTypeAll[basicWildlifeAi]()
        ailist = UnityEngine.Resources.FindObjectsOfTypeAll(basicWildlifeAi)
        for x in range(0, len(ailist)):
            current = ailist[x]
            takedmg = current.GetComponent("TakeDamage")
            idmain = takedmg.idMain
            alive = takedmg.alive
            movement = basicWildlifeAi.GetField("_wildMove").GetValue(current)

            if movement:
                if str(movement._agent.pathStatus) in "PathInvalid" and alive:
                    takeDamage.KillSelf(idmain, None)
                    count += 1

        if count > 0:
            Plugin.Log("LogFile", "Killed NPCs. Count: " + str(count))

    def KillThemCallback(self):
        timer = Plugin.GetTimer("KillThem")
        if timer is not None:
            timer.Stop()
            Plugin.Timers.Remove("KillThem")
        self.KillEmAll()
        Plugin.CreateTimer("KillThem", 420000).Start()