__title__ = 'KillingSpree'
__author__ = 'DreTaX'
__version__ = '1.2'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import time

"""
    Class
"""


class KillingSpree:

    def On_PluginInit(self):
        DataStore.Flush("Peak_KS_LastSeen")

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.Victim is not None and DeathEvent.Attacker is not None:
            if DeathEvent.VictimIsPlayer and DeathEvent.AttackerIsPlayer and DeathEvent.Victim.UID != DeathEvent.Attacker.UID:
                CurrentSpree = int(self.GetCurrentKillingSpree(DeathEvent.Attacker.UID)) + 1
                self.SetKillingSpree(DeathEvent.Victim.UID, 0)
                self.SetKillingSpree(DeathEvent.Attacker.UID, CurrentSpree)
                self.ShowKillingSpreeNotification(DeathEvent.Attacker, CurrentSpree)

    def On_PlayerConnected(self, Player):
        id = Player.UID
        LastSeen = self.GetLastSeen(id)
        TimeStamp = round(time.time())
        CurrentSpree = self.GetCurrentKillingSpree(id)

        if LastSeen is not None:
            if int(CurrentSpree) > 0 and (TimeStamp - int(LastSeen)) >= 900:
                self.SetKillingSpree(Player.UID, 0)
                Player.Message("Your killing spree has been reset.")

    def On_PlayerDisconnected(self, Player):
        TimeStamp = int(round(time.time()))
        self.SetLastSeen(Player.UID, TimeStamp)

    def GetLastSeen(self, SteamID):
        return DataStore.Get("Peak_KS_LastSeen", SteamID)

    def SetLastSeen(self, SteamID, LastSeen):
        DataStore.Add("Peak_KS_LastSeen", SteamID, int(LastSeen))

    def GetCurrentKillingSpree(self, SteamID):
        KillingSpree = DataStore.Get("Peak_KS_CurrentSpree", SteamID)
        if KillingSpree is None:
            return 0
        return int(KillingSpree)

    def SetKillingSpree(self, SteamID, Spree):
        DataStore.Add("Peak_KS_CurrentSpree", SteamID, Spree)

    def ShowKillingSpreeNotification(self, Name, CurrentSpree):
        CurrentSpree = int(CurrentSpree)
        if CurrentSpree == 5:
            Server.BroadcastNotice(Name + " is on a killing spree!")
        elif CurrentSpree == 10:
            Server.BroadcastNotice(Name + " is on a rampage!")
        elif CurrentSpree == 15:
            Server.BroadcastNotice(Name + " is dominating!")
        elif CurrentSpree == 20:
            Server.BroadcastNotice(Name + " is unstoppable!")
        elif CurrentSpree == 25:
            Server.BroadcastNotice(Name + " is godlike!")
