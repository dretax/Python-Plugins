__author__ = 'DreTaX'
__version__ = '1.0'
import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import Fougerite
import UnityEngine
from UnityEngine import *


class NavMeshRunner:

    char = None

    def On_PluginInit(self):
        self.char = Util.TryFindReturnType("Character")
        Plugin.CreateTimer("KillThem", 120000).Start()

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def Kill(self):
        if self.char is None:
            Plugin.Log("Failed", "Failed...")
            return
        number = 0
        navmeshes = UnityEngine.Object.FindObjectsOfType[UnityEngine.NavMeshAgent]()
        for agent in navmeshes:
            if str(agent.pathStatus) in "PathInvalid":
                char = agent.GetComponent[self.char]()
                char.takeDamage.health = 0
                number += 1
        return number

    def KillThemCallback(self):
        timer = Plugin.GetTimer("KillThem")
        if timer is not None:
            timer.Stop()
            Plugin.Timers.Remove("KillThem")
        self.Kill()
        Plugin.CreateTimer("KillThem", 120000).Start()

    def On_Command(self, Player, cmd, args):
        if cmd == "navmeshcheck":
            if Player.Admin or self.isMod(Player.SteamID):
                n = self.Kill()
                Player.MessageFrom("NavMesh", "Killed: " + str(n) + " animals.")