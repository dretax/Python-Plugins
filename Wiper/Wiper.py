__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import datetime

"""
    Class
"""
IdsToWipe = []
class Wiper:

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def GetIni(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "MaxDays", "14")
            ini.Save()
        return Plugin.GetIni("Settings")

    def Replace(self, String):
        if String.startswith("0"):
            n = String.replace(String[0], '')
            return n
        return String

    def On_ServerInit(self):
        n = self.LaunchCheck()
        Plugin.Log("Log", "Wiped: " + str(n))
        Plugin.CreateTimer("Wipe", 3600000).Start()

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        today = datetime.date.today()
        ini = self.GetIni()
        if ini.GetSetting("Objects", id) is None:
            ini.AddSetting("Objects", id, str(today))
            ini.Save()
        else:
            ini.SetSetting("Objects", id, str(today))
            ini.Save()

    def On_PlayerDisconnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        today = datetime.date.today()
        ini = self.GetIni()
        if ini.GetSetting("Objects", id) is None:
            ini.AddSetting("Objects", id, str(today))
            ini.Save()
        else:
            ini.SetSetting("Objects", id, str(today))
            ini.Save()

    def LaunchCheck(self):
        ini = self.GetIni()
        enum = ini.EnumSection("Objects")
        c = 0
        cooldown = int(ini.GetSetting("Settings", "MaxDays"))
        today = datetime.date.today()
        for id in enum:
            v = str(ini.GetSetting("Objects", id)).split('-')
            lastseen = datetime.datetime(int(v[0]), int(self.Replace(v[1])), int(self.Replace(v[02])))
            count = str(today - lastseen)
            if "day" not in count:
                continue
            count = count.split(',')
            # Yeah, this is sucky don't even ask.
            count = str(count[0]).replace(' days', '')
            count = count.replace(' day', '')
            count = count.replace('days', '')
            count = count.replace('day', '')
            if int(count) > cooldown:
                IdsToWipe.append(id)
        for ent in World.Entities:
            if ent.OwnerID not in enum and ent.OwnerID not in IdsToWipe:
                if ini.GetSetting("Objects", ent.OwnerID) is None and not ini.GetSetting("Objects", ent.OwnerID):
                    ini.AddSetting("Objects", ent.OwnerID, str(today))
                    ini.Save()
                else:
                    v = str(ini.GetSetting("Objects", ent.OwnerID))
                    if v[1] == "0":
                        continue
                    lastseen = datetime.datetime(int(v[0]), int(self.Replace(v[1])), int(self.Replace(v[02])))
                    count = str(today - lastseen)
                    count = count.split(',')
                    count = str(count[0]).replace(' days', '')
                    count = count.replace(' day', '')
                    count = count.replace('days', '')
                    count = count.replace('day', '')
                    if int(count) < cooldown:
                        continue
            if ent.OwnerID in IdsToWipe:
                ent.Destroy()
                c = c + 1
        for x in IdsToWipe:
            ini.DeleteSetting("Objects", x)
            Plugin.Log("WipedIds", str(x))
        ini.Save()
        del IdsToWipe[:]
        return c

    def WipeCallback(self):
        Plugin.KillTimer("Wipe")
        n = self.LaunchCheck()
        Plugin.Log("Log", "Wiped Objects: " + str(n))
        Plugin.CreateTimer("Wipe", 3600000).Start()

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "wipecheck":
            if Player.Admin or self.isMod(id):
                check = self.LaunchCheck()
                Player.MessageFrom("Wiper", "Wiped: " + str(check) + " objects.")