__author__ = 'DreTaX'
__version__ = '3.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
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
            ini.AddSetting("Settings", "JoinCooldown", "30")
            ini.AddSetting("Settings", "Cooldown", "300000")
            ini.AddSetting("Settings", "Randoms", "8156")
            ini.Save()
        return Plugin.GetIni("Config")

    def argsToText(self, args):
        text = String.Join(" ", args)
        return text

    def GetPlayerName(self, name):
        try:
            name = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            Plugin.Log("SpikeDamage", "Error caught at getPlayer method. Player was null.")
            return None

    # Method provided by Spoock. Converted to Python by DreTaX
    def CheckV(self, Player, args):
        ini = self.Config()
        systemname = ini.GetSetting("Settings", "SysName")
        Nickname = ""
        for i in xrange(-1, len(args)):
            i += 1
            Nickname += args[i] + " "
            Nickname = Data.Substring(Nickname, 0, len(Nickname) - 1)
            target = self.GetPlayerName(Nickname)
            if target is not None:
                return target

            else:
                cc = 0
                found = None
                for all in Server.Players:
                    name = all.Name.lower()
                    check = args[0].lower()
                    if check in name:
                        found = all.Name
                        cc += 1

                if cc == 1:
                    target = self.GetPlayerName(found)
                    return target
                elif cc > 1:
                    Player.MessageFrom(systemname, "Found [color#FF0000]" + cc + " players[/color] with similar names. [color#FF0000]Use more correct name !")
                    return None
                elif cc == 0:
                    Player.MessageFrom(systemname, "Player [color#00FF00]" + Nickname + "[/color] not found")
                    return None

    def DefaultLocations(self):
        if not Plugin.IniExists("DefaultLoc"):
            ini = Plugin.CreateIni("DefaultLoc")
            ini.Save()
        return Plugin.GetIni("DefaultLoc")

    #There is an error while converting ownerid to string in C#. Hax it.
    def GetIt(self, Entity):
        try:
            if Entity.IsDeployableObject():
                return Entity.Object.ownerID
            if Entity.IsStructure():
                return Entity.Object._master.ownerID
        except:
            return None

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
        if beds.GetSetting("Homes", id):
            return True
        return False

    def FriendOf(self, Owner, Id):
        beds = self.PlayersIni()
        if beds.GetSetting(Owner, Id):
            return True
        return False

    def On_Command(self, Player, cmd, args):
        ini = self.Config()
        sys = ini.GetSetting("Settings", "SysName")
        id = Player.SteamID
        beds = self.PlayersIni()
        if cmd == "home":
            Player.MessageFrom(sys, self.green + "HomeSystem3" + self.white + " by " + __author__)
            Player.MessageFrom(sys, "/setdefaulthome - Sets home, If standing on a bed or bag.")
            Player.MessageFrom(sys, "/delhome - Deletes your Default Home")
            Player.MessageFrom(sys, "/addfriendh name - Adds Player To Foundation Whitelist")
            Player.MessageFrom(sys, "/delfriendh name - Removes Player From Foundation Whitelist")
            Player.MessageFrom(sys, "/listwlh - List Players On Distance Whitelist")
        elif cmd == "setdefaulthome":
            loc = Player.Location
            if not self.HasHome(id):
                for x in World.Entities:
                    if x.Name == "SleepingBagA" or x.Name == "SingleBed":
                        eloc = Util.CreateVector(x.X, x.Y, x.Z)
                        dist = round(Util.GetVectorsDistance(loc, eloc), 2)
                        if dist <= 2:
                            beds.AddSetting("Homes", id, str(loc))
                            beds.Save()
                            Player.MessageFrom(sys, "Home Set.")
                            return
                Player.MessageFrom(sys, "Couldn't find a bed placed within 1m.")
                Player.MessageFrom(sys, "Stand on a bed or sleeping bag.")
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
                i = 0
                counted = len(players)
                name = name.lower()
                for playerid in players:
                    i += 1
                    nameof = beds.GetSetting(id, playerid)
                    lowered = nameof.lower()
                    if lowered == name:
                        ini.DeleteSetting(id, playerid)
                        ini.Save()
                        Player.MessageFrom(sys, "Player Removed from Whitelist")
                        return
                    if i == counted:
                        Player.MessageFrom(sys, "Player doesn't exist!")
                        return
        elif cmd == "listwlh":
            id = Player.SteamID
            players = beds.EnumSection(id)
            Player.MessageFrom(sys, self.green + " List of Whitelisted Friends:")
            for playerid in players:
                nameof = beds.GetSetting(id, playerid)
                if nameof:
                    Player.MesssageFrom(sys, "- " + str(nameof))

    def HomeTimerCallback(self):
        epoch = Plugin.GetTimestamp()
        if DataStore.Count(self.TimerStore) >= 1:
            ids = DataStore.Keys(self.TimerStore)
            for id in ids:
                time = int(DataStore.Get(self.TimerStore, id))
                if epoch >= time:
                    if not self.HasHome(id):
                        Player = Server.FindPlayer(id)
                        if Player is None:
                            DataStore.Remove(self.TimerStore, id)
                            continue
                        self.SendRandom(Player)
                    else:
                        Player = Server.FindPlayer(id)
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
        randomloc = int(ini.GetSetting("Settings", "Randoms"))
        rand = random.randrange(0, randomloc)
        deff = self.DefaultLocations()
        randp = deff.GetSetting("DefaultLoc", str(rand))
        randp = self.Replace(randp)
        location = Util.CreateVector(float(randp[0]), float(randp[1]), float(randp[2]))
        Player.TeleportTo(location)
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
            beds= self.PlayersIni()
            h = beds.GetSetting("Homes", id)
            h = self.Replace(h)
            home = Util.CreateVector(float(h[0]), float(h[1]), float(h[2]))
            Player.SafeTeleportTo(home)
            Player.MessageFrom(sys, self.green + "Teleported to your home.")
            DataStore.Add("HomeSys3CD", id, System.Environment.TickCount)
        else:
            Player.MessageFrom(sys, self.green + "Your home teleportation is on cooldown.")
            done = round((calc / 1000) / 60, 2)
            done2 = round((cooldown / 1000) / 60, 2)
            Player.MessageFrom(sys, self.green + "Time: " + str(done) + "/" + str(done2))
            randomloc = int(ini.GetSetting("Settings", "Randoms"))
            rand = random.randrange(0, randomloc)
            deff = self.DefaultLocations()
            randp = deff.GetSetting("DefaultLoc", str(rand))
            randp = self.Replace(randp)
            location = Util.CreateVector(float(randp[0]), float(randp[1]), float(randp[2]))
            Player.TeleportTo(location)
            Player.MessageFrom(sys, self.green + "Teleported to a random location.")

    def SendPlayerToHome(self, Player, id):
        DataStore.Remove("HomeSys3JCD", id)
        if not Plugin.GetTimer("HomeTimer"):
            Plugin.CreateTimer("HomeTimer", 2000).Start()
        epoch = Plugin.GetTimestamp()
        exectime = int(epoch) + 10
        DataStore.Add(self.TimerStore, id, exectime)

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        jtime = DataStore.Get("HomeSys3JCD", id)
        ini = self.Config()
        sys = ini.GetSetting("Settings", "SysName")
        cooldown = int(ini.GetSetting("Settings", "JoinCooldown"))
        if jtime is None:
            self.SendPlayerToHome(Player, id)
            return
        if int(System.Environment.TickCount - jtime) < 0 or math.isnan(int(System.Environment.TickCount - jtime)):
            DataStore.Remove("HomeSys3JCD", id)
            self.SendPlayerToHome(Player, id)
            return
        calc = int(System.Environment.TickCount - (jtime + (cooldown * 1000)))
        if System.Environment.TickCount <= jtime + cooldown * 1000:
            calc2 = cooldown * 1000
            calc2 = round((calc2 - calc) / 1000 - cooldown, 2)
            Player.MessageFrom(sys, self.red + str(cooldown) + " seconds cooldown at join. You can't join till: " + str(calc2) + " more seconds.")
            Player.Disconnect()
            return
        elif System.Environment.TickCount > jtime + (cooldown * 1000):
            self.SendPlayerToHome(Player, id)


    def On_PlayerDisconnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        if Player.Admin or self.isMod(id):
            return
        if not DataStore.ContainsKey("HomeSys3JCD", id):
            DataStore.Add("HomeSys3JCD", id, System.Environment.TickCount)

    def On_EntityDeployed(self, Player, Entity):
        if Entity is not None and Player is not None:
            if Entity.Name == "SleepingBagA" or Entity.Name == "SingleBed":
                id = Player.SteamID
                ini = self.Config()
                max = float(ini.GetSetting("Settings", "Distance"))
                loc = Util.CreateVector(Entity.X, Entity.Y, Entity.Z)
                sys = ini.GetSetting("Settings", "SysName")
                msg = ini.GetSetting("Settings", "Message")
                for x in World.Entities:
                    if x.Name == "WoodFoundation" or x.Name == "MetalFoundation":
                        eloc = Util.CreateVector(x.X, x.Y, x.Z)
                        dist = round(Util.GetVectorsDistance(loc, eloc), 2)
                        if dist >= max:
                            ownerid = self.GetIt(x)
                            if ownerid is None:
                                try:
                                    Plugin.Log("HomeSystem3Error", str(eloc) + " | " + str(x.Name))
                                except:
                                    pass
                                continue
                            if ownerid == id:
                                continue
                            if not self.FriendOf(ownerid, id):
                                Player.MessageFrom(sys, msg)
                                return