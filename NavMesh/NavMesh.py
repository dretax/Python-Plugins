__author__ = 'DreTaX'
__version__ = '1.0'
import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("System.Core", "IronPythonModule")
import IronPythonModule
from IronPythonModule import Extensions
import Fougerite
import UnityEngine
from UnityEngine import *
import System
from System import Reflection


class NavMesh:

    def On_PluginInit(self):
        Plugin.CreateTimer("KillThem", 5000).Start()

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def KillEmAll(self):
        basicWildlifeAi = Util.TryFindReturnType("BasicWildLifeAI")
        takeDamage = Util.TryFindReturnType("TakeDamage")
        if basicWildlifeAi is None or takeDamage is None:
            return
        count = 0
        ailist = UnityEngine.Object.FindObjectsOfType[basicWildlifeAi]()
        for x in range(0, len(ailist)):
            current = ailist[x]
            takedmg = current.GetComponent[takeDamage]()
            idMain = takedmg.idMain # dafuq is wrong here ffs?
            alive = takedmg.alive
            try:
                movement = basicWildlifeAi.GetField("_wildMove", System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic).GetValue(current)
            except:
                continue

            if movement:
                try:
                    agent = movement._agent
                except:
                    continue
                if str(agent.pathStatus) in "PathInvalid" and alive:
                    takeDamage.KillSelf(idMain, None)
                    count += 1

        if count > 0:
            Plugin.Log("KilledNpcs", "Killed NPCs. Count: " + str(count))
        return count

    def KillThemCallback(self):
        timer = Plugin.GetTimer("KillThem")
        if timer is not None:
            timer.Stop()
            Plugin.Timers.Remove("KillThem")
        self.KillEmAll()
        Plugin.CreateTimer("KillThem", 5000).Start()

    def On_Command(self, Player, cmd, args):
        if cmd == "navmeshcheck":
            if Player.Admin or self.isMod(Player.SteamID):
                n = self.KillEmAll()
                Player.MessageFrom("Killed: " + str(n) + " animals.")