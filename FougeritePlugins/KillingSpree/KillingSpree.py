__author__ = 'Converted By DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import time

"""
    Class
"""



class KillingSpree:

    def IsAnimal(self, killer):
        if killer == 'Wolf' or killer == 'Bear' or killer == 'MutantWolf' or killer == 'MutantBear':
            return True
        return False

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.Victim is not None and DeathEvent.Attacker is not None:
            id = self.TrytoGrabID(DeathEvent.Attacker)
            vid = self.TrytoGrabID(DeathEvent.Victim)
            try:
                killer = str(DeathEvent.Attacker.Name)
            except:
                return
            if self.IsAnimal(killer) and id is None:
                return
            if long(id) != long(vid):
                CurrentSpree = int(self.GetCurrentKillingSpree(id)) + 1
                self.SetKillingSpree(vid, 0)
                self.SetKillingSpree(id, CurrentSpree)
                self.ShowKillingSpreeNotification(killer, CurrentSpree)

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        LastSeen = self.GetLastSeen(id)
        TimeStamp = round(time.time())
        CurrentSpree = self.GetCurrentKillingSpree(id)

        if LastSeen is not None:
            if int(CurrentSpree) > 0 and (TimeStamp - int(LastSeen)) >= 900:
                self.SetKillingSpree(Player.SteamID, 0)
                Player.Message("Your killing spree has been reset.")

    def On_PlayerDisconnected(self, Player):
        TimeStamp = int(round(time.time()))
        self.SetLastSeen(Player.SteamID, TimeStamp)

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