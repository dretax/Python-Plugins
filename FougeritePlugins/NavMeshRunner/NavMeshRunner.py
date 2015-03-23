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
    dmg = None

    def On_PluginInit(self):
        self.char = Util.TryFindReturnType("Character")
        self.dmg = Util.TryFindReturnType("DamageEvent")
        Plugin.CreateTimer("KillThem", 600000).Start()

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
                char.Signal_ServerCharacterDeath()
                try:
                    char.SendMessage("OnKilled", self.dmg(), SendMessageOptions.DontRequireReceiver)
                except:
                    pass
                number += 1
        return number

    def KillThemCallback(self, timer):
        timer.Kill()
        self.Kill()
        Plugin.CreateTimer("KillThem", 600000).Start()

    def On_Command(self, Player, cmd, args):
        if cmd == "navmeshcheck":
            if Player.Admin or self.isMod(Player.SteamID):
                n = self.Kill()
                Player.MessageFrom("NavMesh", "Killed: " + str(n) + " animals.")