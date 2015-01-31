__author__ = 'DreTaX'
__version__ = '3.5'
import clr

clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import Fougerite
import UnityEngine
from UnityEngine import *
import math
import System
from System import *

"""
    Class
"""

import sys
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

Lib = True
try:
    import random
except ImportError:
    Lib = False

class HomeSystem3:
    """
        Methods
    """

    red = "[color #FF0000]"
    green = "[color #009900]"
    white = "[color #FFFFFF]"
    TimerStore = "HomeTimer"

    def On_PluginInit(self):
        Util.ConsoleLog("HomeSystem3 by " + __author__ + " Version: " + __version__ + " loaded.", False)
        self.Config()
        self.PlayersIni()
        DataStore.Flush("HomeSys3JCD")
        DataStore.Flush("HomeTimer")
        DataStore.Flush("HomeSys3CD")
        DataStore.Flush("homesystemautoban")

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def PlayersIni(self):
        if not Plugin.IniExists("Players"):
            ini = Plugin.CreateIni("Players")
            ini.Save()
        return Plugin.GetIni("Players")

    def Config(self):
        if not Plugin.IniExists("Config"):
            ini = Plugin.CreateIni("Config")
            ini.AddSetting("Settings", "Message", "No Derppassing ask the owner if you can live here")
            ini.AddSetting("Settings", "Distance", "25")
            ini.AddSetting("Settings", "SysName", "HomeSystem")
            ini.AddSetting("Settings", "EJoinCooldown", "1")
            ini.AddSetting("Settings", "JoinCooldown", "30")
            ini.AddSetting("Settings", "Cooldown", "300000")
            ini.AddSetting("Settings", "SendPlayertoHomeorRandom", "1")
            ini.AddSetting("Settings", "Randoms", "8156")
            ini.Save()
        return Plugin.GetIni("Config")

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def getPlayer(self, d):
        try:
            id = str(d)
            pl = Server.FindPlayer(id)
            return pl
        except:
            return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.0
    """

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        ini = self.Config()
        systemname = ini.GetSetting("Settings", "SysName")
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def DefaultLocations(self):
        if not Plugin.IniExists("DefaultLoc"):
            ini = Plugin.CreateIni("DefaultLoc")
            ini.Save()
        return Plugin.GetIni("DefaultLoc")

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def Replace(self, String):
        c = String.replace("(", "")
        c = c.replace(")", "")
        return c.split(",")

    def HasHome(self, id):
        beds = self.PlayersIni()
        if beds.GetSetting("Homes", id) and beds.GetSetting("Homes", id) is not None:
            return True
        return False

    def IsFriend(self, OwnerID, ID):
        beds = self.PlayersIni()
        if beds.GetSetting(OwnerID, ID):
            return True
        return False

    def On_Command(self, Player, cmd, args):
        ini = self.Config()
        sys = ini.GetSetting("Settings", "SysName")
        id = Player.SteamID
        beds = self.PlayersIni()
        if cmd == "home":
            Player.MessageFrom(sys, self.green + "HomeSystem3 " + self.white + " by " + __author__)
            Player.MessageFrom(sys, "/setdefaulthome - Sets home, If standing on a bed or bag.")
            Player.MessageFrom(sys, "/delhome - Deletes your Default Home")
            Player.MessageFrom(sys, "/addfriendh name - Adds Player To Foundation Whitelist")
            Player.MessageFrom(sys, "/delfriendh name - Removes Player From Foundation Whitelist")
            Player.MessageFrom(sys, "/listwlh - List Players On Distance Whitelist")
        elif cmd == "setdefaulthome":
            loc = Player.Location
            if not self.HasHome(id):
                type = Util.TryFindReturnType("DeployableObject")
                objects = UnityEngine.Object.FindObjectsOfType(type)
                for x in objects:
                    name = str(x.name).lower()
                    if "sleeping" in name:
                        dist = round(Util.GetVectorsDistance(loc, x.gameObject.transform.position), 2)
                        if dist < 2:
                            ownerid = long(x.ownerID)
                            if long(id) == ownerid:
                                beds.AddSetting("Homes", id, str(loc))
                                beds.Save()
                                Player.MessageFrom(sys, "Home Set.")
                                return
                    elif "single" in name:
                        dist = round(Util.GetVectorsDistance(loc, x.gameObject.transform.position), 2)
                        if dist < 3.5:
                            ownerid = long(x.ownerID)
                            if long(id) == ownerid:
                                beds.AddSetting("Homes", id, str(loc))
                                beds.Save()
                                Player.MessageFrom(sys, "Home Set.")
                                return
                Player.MessageFrom(sys, "Couldn't find a bed placed within 1m / 3.5m.")
                Player.MessageFrom(sys, "Stand on a bed or sleeping bag.")
                Player.MessageFrom(sys, self.red + "Make sure the bed is yours.")
            else:
                Player.MessageFrom(sys, "You already have a home. Delete It first.")
        elif cmd == "delhome":
            if self.HasHome(id):
                beds.DeleteSetting("Homes", id)
                beds.Save()
                Player.MessageFrom(sys, "Home Deleted")
            else:
                Player.MessageFrom(sys, "You don't have a home set.")
        elif cmd == "addfriendh":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage: /addfriendh playername")
            else:
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                if playerr == Player:
                    Player.MessageFrom(sys, "This is you...")
                    return
                idr = playerr.SteamID
                nrr = str(playerr.Name)
                if beds.GetSetting(id, idr) is not None:
                    Player.MessageFrom(sys, nrr + " is already on your list.")
                    return
                beds.AddSetting(id, idr, nrr)
                beds.Save()
                Player.MessageFrom(sys, nrr + " was added to your list.")
        elif cmd == "delfriendh":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage: /delfriendh playername")
                return
            elif len(args) > 0:
                name = self.argsToText(args)
                id = Player.SteamID
                players = beds.EnumSection(id)
                counted = len(players)
                if counted == 0:
                    Player.MessageFrom(sys, "You have never whitelisted anyone.")
                    return
                name = name.lower()
                for playerid in players:
                    nameof = beds.GetSetting(id, playerid)
                    lowered = nameof.lower()
                    if lowered == name or name in lowered:
                        beds.DeleteSetting(id, playerid)
                        beds.Save()
                        Player.MessageFrom(sys, str(nameof) + " Removed from Whitelist")
                        return
                Player.MessageFrom(sys, name + " is not on your list!")
        elif cmd == "listwlh":
            id = Player.SteamID
            players = beds.EnumSection(id)
            Player.MessageFrom(sys, self.green + " List of Whitelisted Friends:")
            for playerid in players:
                nameof = beds.GetSetting(id, playerid)
                if nameof:
                    Player.MessageFrom(sys, "- " + str(nameof))

    def HomeTimerCallback(self):
        epoch = Plugin.GetTimestamp()
        if DataStore.Count(self.TimerStore) >= 1:
            ids = DataStore.Keys(self.TimerStore)
            for id in ids:
                time = int(DataStore.Get(self.TimerStore, id))
                if epoch >= time:
                    if not self.HasHome(id):
                        Player = self.getPlayer(id)
                        if Player is None:
                            DataStore.Remove(self.TimerStore, id)
                            continue
                        self.SendRandom(Player)
                    else:
                        Player = self.getPlayer(id)
                        if Player is None:
                            DataStore.Remove(self.TimerStore, id)
                            continue
                        self.SendH(Player)
                    DataStore.Remove(self.TimerStore, id)
        else:
            Plugin.KillTimer("HomeTimer")

    def SendRandom(self, Player):
        ini = self.Config()
        sys = ini.GetSetting("Settings", "SysName")
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        randomloc = int(ini.GetSetting("Settings", "Randoms"))
        rand = random.randint(1, randomloc)
        deff = self.DefaultLocations()
        randp = deff.GetSetting("DefaultLoc", str(rand))
        randp = self.Replace(randp)
        location = Util.CreateVector(float(randp[0]), float(randp[1]), float(randp[2]))
        Player.TeleportTo(location)
        DataStore.Add("homesystemautoban", id, "none")
        Player.MessageFrom(sys, self.red + "Teleported to a random location.")
        Player.MessageFrom(sys, self.red + "Type /home to get the commands.")


    def SendH(self, Player):
        ini = self.Config()
        sys = ini.GetSetting("Settings", "SysName")
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        time = DataStore.Get("HomeSys3CD", id)
        cooldown = int(ini.GetSetting("Settings", "Cooldown"))
        if time is None:
            DataStore.Add("HomeSys3CD", id, 7)
            time = 7
        systick = System.Environment.TickCount
        if int(systick - int(time)) < 0 or math.isnan(int(systick - int(time))) or math.isnan(time):
            DataStore.Add("HomeSys3CD", id, 7)
            time = 7
        calc = systick - int(time)
        if calc >= cooldown or time == 7 or cooldown == 0:
            beds = self.PlayersIni()
            h = beds.GetSetting("Homes", id)
            h = self.Replace(h)
            home = Util.CreateVector(float(h[0]), float(h[1]), float(h[2]))
            Player.SafeTeleportTo(home)
            DataStore.Add("homesystemautoban", id, "none")
            Player.MessageFrom(sys, self.green + "Teleported to your home.")
            DataStore.Add("HomeSys3CD", id, System.Environment.TickCount)
        else:
            Player.MessageFrom(sys, self.green + "Your home teleportation is on cooldown.")
            done = round((calc / 1000) / 60, 2)
            done2 = round((cooldown / 1000) / 60, 2)
            Player.MessageFrom(sys, self.green + "Time: " + str(done) + "/" + str(done2))
            randomloc = int(ini.GetSetting("Settings", "Randoms"))
            rand = random.randint(1, randomloc)
            deff = self.DefaultLocations()
            randp = deff.GetSetting("DefaultLoc", str(rand))
            randp = self.Replace(randp)
            location = Util.CreateVector(float(randp[0]), float(randp[1]), float(randp[2]))
            Player.TeleportTo(location)
            DataStore.Add("homesystemautoban", id, "none")
            Player.MessageFrom(sys, self.green + "Teleported to a random location.")

    def SendPlayerToHome(self, id):
        DataStore.Remove("HomeSys3JCD", id)
        if not Plugin.GetTimer("HomeTimer"):
            Plugin.CreateTimer("HomeTimer", 2000).Start()
        epoch = Plugin.GetTimestamp()
        exectime = int(epoch) + 12
        DataStore.Add("homesystemautoban", id, "using")
        DataStore.Add(self.TimerStore, id, exectime)

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        jtime = DataStore.Get("HomeSys3JCD", id)
        ini = self.Config()
        sys = ini.GetSetting("Settings", "SysName")
        cooldown = int(ini.GetSetting("Settings", "JoinCooldown"))
        sendhome = int(ini.GetSetting("Settings", "SendPlayertoHomeorRandom"))
        ecooldown = int(ini.GetSetting("Settings", "EJoinCooldown"))
        if jtime is None:
            if sendhome == 1:
                self.SendPlayerToHome(id)
            return
        if int(System.Environment.TickCount - jtime) < 0 or math.isnan(int(System.Environment.TickCount - jtime)):
            if sendhome == 1:
                self.SendPlayerToHome(id)
            return
        if ecooldown == 1:
            calc = int(System.Environment.TickCount - (jtime + (cooldown * 1000)))
            if System.Environment.TickCount <= jtime + cooldown * 1000:
                calc2 = cooldown * 1000
                calc2 = round((calc2 - calc) / 1000 - cooldown, 2)
                Player.MessageFrom(sys, self.red + str(cooldown) + " seconds cooldown at join. You can't join till: " + str(calc2) + " more seconds.")
                Player.Disconnect()
                return
            elif System.Environment.TickCount > jtime + (cooldown * 1000):
                if sendhome == 1:
                    self.SendPlayerToHome(id)
        DataStore.Remove("HomeSys3JCD", id)


    def On_PlayerDisconnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        if Player.Admin or self.isMod(id):
            return
        if not DataStore.ContainsKey("HomeSys3JCD", id):
            DataStore.Add("HomeSys3JCD", id, System.Environment.TickCount)
        DataStore.Add("homesystemautoban", id, "none")

    def On_EntityDeployed(self, Player, Entity):
        if Entity is not None and Player is not None:
            if Entity.Name == "SleepingBagA" or Entity.Name == "SingleBed":
                id = Player.SteamID
                ini = self.Config()
                max = float(ini.GetSetting("Settings", "Distance"))
                loc = Util.CreateVector(Entity.X, Entity.Y, Entity.Z)
                sys = ini.GetSetting("Settings", "SysName")
                msg = ini.GetSetting("Settings", "Message")
                type = Util.TryFindReturnType("StructureComponent")
                objects = UnityEngine.Object.FindObjectsOfType(type)
                for x in objects:
                    if "Foundation" in x.name or "Ceiling" in x.name:
                        dist = round(Util.GetVectorsDistance(loc, x.gameObject.transform.position), 2)
                        if dist > max:
                            continue
                        ownerid = long(x._master.ownerID)
                        if ownerid == long(id):
                            continue
                        friends = self.IsFriend(str(ownerid), str(id))
                        if friends:
                            continue
                        else:
                            Entity.Destroy()
                            Player.MessageFrom(sys, msg)
                            return