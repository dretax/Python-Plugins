__author__ = 'DreTaX'
__version__ = '1.1'

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
            ini.AddSetting("Settings", "Broadcast", "True")
            ini.Save()
        return Plugin.GetIni("Settings")

    def Replace(self, String):
        if String.startswith("0"):
            n = String.replace(String[0], '')
            return n
        return String

    def On_ServerInit(self):
        self.GetIni()
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
            if ent.OwnerID not in enum:
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
                    else:
                        IdsToWipe.append(ent.OwnerID)
            if ent.OwnerID in IdsToWipe:
                ent.Destroy()
                c += 1
        for x in IdsToWipe:
            ini.DeleteSetting("Objects", x)
            Plugin.Log("WipedIds", str(x))
        ini.Save()
        del IdsToWipe[:]
        return c

    def WipeByID(self, id):
        c = 0
        for ent in World.Entities:
            if long(ent.OwnerID) == long(id):
                ent.Destroy()
                c += 1
        return c

    def WipeCallback(self):
        Plugin.KillTimer("Wipe")
        ini = self.GetIni()
        Broadcast = bool(ini.GetSetting("Settings", "Broadcast"))
        if Broadcast:
            Server.BroadcastFrom("Wiper", "Checking for Wipeable unused objects....")
        n = self.LaunchCheck()
        Plugin.Log("Log", "Wiped Objects: " + str(n))
        if Broadcast:
            Server.BroadcastFrom("Wiper", "Wiped " + str(n) + " unused objects!")
        Plugin.CreateTimer("Wipe", 3600000).Start()

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "wipehelp":
            if Player.Admin or self.isMod(id):
                Player.MessageFrom("Wiper", "Wiper Commands:")
                Player.MessageFrom("Wiper", "/wipecheck")
                Player.MessageFrom("Wiper", "/wipetimerreset")
                Player.MessageFrom("Wiper", "/wipeid")
                Player.MessageFrom("Wiper", "/wipebarr")
                Player.MessageFrom("Wiper", "/wipecampf")
        elif cmd == "wipecheck":
            if Player.Admin or self.isMod(id):
                ini = self.GetIni()
                Broadcast = bool(ini.GetSetting("Settings", "Broadcast"))
                if Broadcast:
                    Server.BroadcastFrom("Wiper", "Checking for Wipeable unused objects....")
                n = self.LaunchCheck()
                if Broadcast:
                    Server.BroadcastFrom("Wiper", "Wiped: " + str(n) + " objects.")
                else:
                    Player.MessageFrom("Wiper", "Wiped: " + str(n) + " objects.")
        elif cmd == "wipetimerreset":
            if Player.Admin or self.isMod(id):
                Plugin.KillTimer("Wipe")
                Plugin.CreateTimer("Wipe", 3600000).Start()
                Player.MessageFrom("Wiper", "Timer restarted.")
        elif cmd == "wipeid":
            if len(args) == 0 or len(args) > 1:
                Player.MessageFrom("Wiper", "Usage: /wipeid playerid")
                return
            if not args[0].isdigit():
                Player.MessageFrom("Wiper", "The id is only made of numbers")
                return
            if Player.Admin or self.isMod(id):
                num = self.WipeByID(args[0])
                Plugin.Log("Log", Player.Name + " wiped " + args[0] + "'s objects. Total: " + str(num))
                Player.MessageFrom("Wiper", "Wiped " + str(num) + " objects!")
        elif cmd == "wipebarr":
            if Player.Admin or self.isMod(id):
                c = 0
                for ent in World.Entities:
                    if "barricade" in ent.Name.lower():
                        ent.Destroy()
                        c += 1
                Player.MessageFrom("Wiper", "Wiped " + str(c) + " barricades.")
        elif cmd == "wipecampf":
            if Player.Admin or self.isMod(id):
                c = 0
                for ent in World.Entities:
                    if "camp" in ent.Name.lower():
                        ent.Destroy()
                        c += 1
                Player.MessageFrom("Wiper", "Wiped " + str(c) + " barricades.")