__author__ = 'DreTaX'
__version__ = '1.3.3'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import datetime
import sys
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

try:
    import os
except ImportError:
    Plugin.Log("Error", "Get the Extralibs!")
    raise ImportError("Get the Extralibs!")

"""
    Class
"""
IdsToWipe = []
EntityList = {

}

UserObj = {

}

class Wiper:

    DecayTimer = None
    WipeTimer = None
    Path = None
    Cooldown = None
    Broadcast = None

    def On_PluginInit(self):
        ini = self.GetIni()
        num = ini.GetSetting("Settings", "DecayTimer")
        num2 = ini.GetSetting("Settings", "WipeCheckTimer")
        self.Path = ini.GetSetting("Settings", "UserDataPath")
        self.Cooldown = int(ini.GetSetting("Settings", "MaxDays"))
        self.Broadcast = self.bool(ini.GetSetting("Settings", "Broadcast"))
        self.DecayTimer = int(num) * 60000
        self.WipeTimer = int(num2) * 60000
        today = datetime.date.today()
        if self.bool(ini.GetSetting("Settings", "UseDecay")):
            self.Assign()
            Plugin.CreateTimer("Decay", self.DecayTimer).Start()
        if not "REMOVETHISCAPSLOCKEDWORD" in self.Path:
            for id in os.listdir(path + self.Path):
                if int(id) == 0:
                    continue
                if ini.GetSetting("Objects", id) is None:
                    ini.AddSetting("Objects", id, str(today))
        if self.bool(ini.GetSetting("Settings", "UseDayLimit")):
            n = self.LaunchCheck()
            Plugin.Log("Log", "Wiped: " + str(n))
            Plugin.CreateTimer("Wipe", self.WipeTimer).Start()
        ini.Save()


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

    def bool(self, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            raise ValueError

    def Assign(self):
        ini = Plugin.GetIni("Health")
        EntityList['WoodFoundation'] = float(ini.GetSetting("Damage", "WoodFoundation"))
        EntityList['WoodDoorFrame'] = float(ini.GetSetting("Damage", "WoodDoorFrame"))
        EntityList['WoodPillar'] = float(ini.GetSetting("Damage", "WoodPillar"))
        EntityList['WoodWall'] = float(ini.GetSetting("Damage", "WoodWall"))
        EntityList['WoodCeiling'] = float(ini.GetSetting("Damage", "WoodCeiling"))
        EntityList['WoodWindowFrame'] = float(ini.GetSetting("Damage", "WoodWindowFrame"))
        EntityList['WoodStairs'] = float(ini.GetSetting("Damage", "WoodStairs"))
        EntityList['WoodRamp'] = float(ini.GetSetting("Damage", "WoodRamp"))
        EntityList['WoodSpikeWall'] = float(ini.GetSetting("Damage", "WoodSpikeWall"))
        EntityList['LargeWoodSpikeWall'] = float(ini.GetSetting("Damage", "LargeWoodSpikeWall"))
        EntityList['WoodBox'] = float(ini.GetSetting("Damage", "WoodBox"))
        EntityList['WoodBoxLarge'] = float(ini.GetSetting("Damage", "WoodBoxLarge"))
        EntityList['WoodGate'] = float(ini.GetSetting("Damage", "WoodGate"))
        EntityList['WoodGateway'] = float(ini.GetSetting("Damage", "WoodGateway"))
        EntityList['WoodenDoor'] = float(ini.GetSetting("Damage", "WoodenDoor"))
        EntityList['Wood_Shelter'] = float(ini.GetSetting("Damage", "Wood_Shelter"))
        EntityList['MetalWall'] = float(ini.GetSetting("Damage", "MetalWall"))
        EntityList['MetalCeiling'] = float(ini.GetSetting("Damage", "MetalCeiling"))
        EntityList['MetalDoorFrame'] = float(ini.GetSetting("Damage", "MetalDoorFrame"))
        EntityList['MetalPillar'] = float(ini.GetSetting("Damage", "MetalPillar"))
        EntityList['MetalFoundation'] = float(ini.GetSetting("Damage", "MetalFoundation"))
        EntityList['MetalStairs'] = float(ini.GetSetting("Damage", "MetalStairs"))
        EntityList['MetalRamp'] = float(ini.GetSetting("Damage", "MetalRamp"))
        EntityList['MetalWindowFrame'] = float(ini.GetSetting("Damage", "MetalWindowFrame"))
        EntityList['MetalDoor'] = float(ini.GetSetting("Damage", "MetalDoor"))
        EntityList['MetalBarsWindow'] = float(ini.GetSetting("Damage", "MetalBarsWindow"))
        EntityList['SmallStash'] = float(ini.GetSetting("Damage", "SmallStash"))
        EntityList['Campfire'] = float(ini.GetSetting("Damage", "Campfire"))
        EntityList['Furnace'] = float(ini.GetSetting("Damage", "Furnace"))
        EntityList['Workbench'] = float(ini.GetSetting("Damage", "Workbench"))
        EntityList['Barricade_Fence_Deployable'] = float(ini.GetSetting("Damage", "Barricade_Fence_Deployable"))
        EntityList['RepairBench'] = float(ini.GetSetting("Damage", "RepairBench"))
        EntityList['SleepingBagA'] = float(ini.GetSetting("Damage", "SleepingBagA"))
        EntityList['SingleBed'] = float(ini.GetSetting("Damage", "SingleBed"))

    def GetIni(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.AddSetting("Settings", "UseDayLimit", "True")
            ini.AddSetting("Settings", "MaxDays", "14")
            ini.AddSetting("Settings", "UseDecay", "True")
            ini.AddSetting("Settings", "DecayTimer", "180")
            ini.AddSetting("Settings", "WipeCheckTimer", "30")
            ini.AddSetting("Settings", "Broadcast", "True")
            ini.AddSetting("Settings", "UserDataPath", "REMOVETHISCAPSLOCKEDWORD\\rust_server_Data\\userdata\\")
            ini.Save()
        return Plugin.GetIni("Settings")

    def Replace(self, String):
        if String.startswith("0"):
            n = String.replace(String[0], '')
            return n
        return String

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
            if int(count) > self.Cooldown:
                IdsToWipe.append(long(id))
        for ent in World.Entities:
            if long(ent.OwnerID) in IdsToWipe:
                ent.Destroy()
                UserObj[long(ent.OwnerID)] = UserObj.get(long(ent.OwnerID), 0) + 1
                c += 1
        for x in IdsToWipe:
            pathtodir = path + self.Path + str(x)
            if os.path.exists(pathtodir):
                idlist = os.listdir(pathtodir)
                for file in idlist:
                    os.remove(path + self.Path + str(x) + "\\" + file)
                os.rmdir(path + self.Path + str(x))
            ini.DeleteSetting("Objects", str(x))
            Plugin.Log("WipedIds", str(x) + " Objects: " + str(UserObj[x]))
        Plugin.Log("WipedIds", "Total Objects: " + str(c))
        UserObj.clear()
        ini.Save()
        del IdsToWipe[:]
        return c

    def ForceDecay(self):
        for Entity in World.Entities:
            v = EntityList.get(Entity.Name, None)
            if v is None:
                continue
            Entity.Health = Entity.Health - v

    def WipeByID(self, id):
        c = 0
        for ent in World.Entities:
            if long(ent.OwnerID) == long(id):
                ent.Destroy()
                c += 1
        return c

    def WipeCallback(self, timer):
        timer.Kill()
        if self.Broadcast:
            Server.BroadcastFrom("Wiper", "Checking for Wipeable unused objects....")
        n = self.LaunchCheck()
        Plugin.Log("Log", "Wiped Objects: " + str(n))
        if self.Broadcast:
            Server.BroadcastFrom("Wiper", "Wiped " + str(n) + " unused objects!")
        Plugin.CreateTimer("Wipe", self.WipeTimer).Start()

    def DecayCallback(self, timer):
        timer.Kill()
        self.ForceDecay()
        Plugin.CreateTimer("Decay", self.DecayTimer).Start()

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "wipehelp":
            if Player.Admin or self.isMod(id):
                Player.MessageFrom("Wiper", "Wiper Commands:")
                Player.MessageFrom("Wiper", "/wipecheck - Checks for inactive objects")
                Player.MessageFrom("Wiper", "/wipetimerreset - Restarts the timer.")
                Player.MessageFrom("Wiper", "/wipeid playerid - Wipes All the objects of the ID")
                Player.MessageFrom("Wiper", "/wipebarr - Deletes all barricaes")
                Player.MessageFrom("Wiper", "/wipecampf - Deletes all camp fires")
                Player.MessageFrom("Wiper", "/wipeforced - Force a decay")
        elif cmd == "wipecheck":
            if Player.Admin or self.isMod(id):
                if self.Broadcast:
                    Server.BroadcastFrom("Wiper", "Checking for Wipeable unused objects....")
                n = self.LaunchCheck()
                if self.Broadcast:
                    Server.BroadcastFrom("Wiper", "Wiped: " + str(n) + " objects.")
                else:
                    Player.MessageFrom("Wiper", "Wiped: " + str(n) + " objects.")
        elif cmd == "wipetimerreset":
            if Player.Admin or self.isMod(id):
                Plugin.KillTimer("Wipe")
                Plugin.KillTimer("Decay")
                Plugin.CreateTimer("Wipe", self.WipeTimer).Start()
                Plugin.CreateTimer("Decay", self.DecayTimer).Start()
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
                Player.MessageFrom("Wiper", "Wiped " + str(c) + " camp fires.")
        elif cmd == "wipeforced":
            if Player.Admin or self.isMod(id):
                Player.MessageFrom("Wiper", "Forcing Decay...")
                self.ForceDecay()
                Player.MessageFrom("Wiper", "Force Decay Finished.")