__author__ = 'DreTaX'
__version__ = '3.7'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import math
import System
from System import *
import re
import sys

path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

try:
    import random
except ImportError:
    pass

red = "[color #FF0000]"
green = "[color #009900]"
white = "[color #FFFFFF]"
"""
    Class
"""

Pending = []
class TpFriend:

    """
        Methods
    """

    sys = None

    def On_PluginInit(self):
        DataStore.Flush("TpTimer")
        DataStore.Flush("tpfriendautoban")
        DataStore.Flush("tpfriendpending")
        DataStore.Flush("tpfriendpending2")
        DataStore.Flush("tpfriendcooldown")
        DataStore.Flush("tpfriendy")
        config = self.TpFriendConfig()
        self.sys = config.GetSetting("Settings", "sysname")
        Util.ConsoleLog("TpFriend v" + __version__ + " by " + __author__ + " loaded.", True)

    def TpFriendConfig(self):
        if not Plugin.IniExists("TpFriendConfig"):
            loc = Plugin.CreateIni("TpFriendConfig")
            loc.Save()
        return Plugin.GetIni("TpFriendConfig")

    def DefaultLoc(self):
        if not Plugin.IniExists("DefaultLoc"):
            loc = Plugin.CreateIni("DefaultLoc")
            loc.Save()
        return Plugin.GetIni("DefaultLoc")

    def KillJob(self, Player):
        if Player in Pending:
            Pending.remove(Player)

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.1
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
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(self.sys, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(self.sys, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def getPlayer(self, d):
        try:
            pl = Server.FindPlayer(d)
            return pl
        except:
            return None

    def Replace(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(',')

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    """
        Timer Functions
    """

    def addJob(self, xtime, PlayerFrom, PlayerTo, callback, id=None, tid=None):
        List = Plugin.CreateDict()
        List["PlayerF"] = PlayerFrom
        List["PlayerT"] = PlayerTo
        # Let's make sure we have the steamid all the time.
        if id is None:
            List["PlayerFID"] = PlayerFrom.SteamID
            List["PlayerTID"] = PlayerTo.SteamID
        else:
            List["PlayerFID"] = id
            List["PlayerTID"] = tid
        List["Call"] = callback
        Plugin.CreateParallelTimer("TpJobTimer", xtime * 1000, List).Start()


    def clearTimers(self):
        Plugin.KillParallelTimer("TpJobTimer")


    def TpJobTimerCallback(self, timer):
        timer.Kill()
        List = timer.Args
        PlayerFrom = List["PlayerF"]
        PlayerTo = List["PlayerT"]
        callback = List["Call"]
        id = List["PlayerFID"]
        tid = List["PlayerTID"]
        if self.TrytoGrabID(PlayerFrom) is None or self.TrytoGrabID(PlayerTo) is None:
            DataStore.Add("tpfriendautoban", id, "none")
            self.KillJob(PlayerFrom)
            self.KillJob(PlayerTo)
            return
        DataStore.Add("tpfriendautoban", id, "using")
        # Normal Teleport Callback
        if callback == 1:
            PlayerFrom.TeleportTo(PlayerTo.Location)
            PlayerFrom.MessageFrom(self.sys, "You have been teleported to your friend")
            self.addJob(2, PlayerFrom, PlayerTo, 3, id, tid)
        # AutoKill
        elif callback == 2:
            if PlayerFrom not in Pending or PlayerTo not in Pending:
                return
            self.KillJob(PlayerFrom)
            self.KillJob(PlayerTo)
            ispend = DataStore.Get("tpfriendpending", id)
            ispend2 = DataStore.Get("tpfriendpending2", tid)
            if ispend is not None and ispend2 is not None:
                DataStore.Remove("tpfriendpending", id)
                DataStore.Remove("tpfriendpending2", tid)
                DataStore.Add("tpfriendcooldown", id, 7)
                DataStore.Add("tpfriendautoban", id, "none")
                if PlayerFrom is not None:
                    PlayerFrom.MessageFrom(self.sys, "Teleport request timed out")
                if PlayerTo is not None:
                    PlayerTo.MessageFrom(self.sys, "Teleport request timed out")
        elif callback == 3:
            PlayerFrom.TeleportTo(PlayerTo.Location)
            PlayerFrom.MessageFrom(self.sys, "You have been teleported to your friend again.")
            DataStore.Add("tpfriendy", id, str(PlayerTo.Y))
            self.addJob(2, PlayerFrom, PlayerTo, 5, id, tid)
        elif callback == 4:
            DataStore.Add("tpfriendautoban", id, "none")
        elif callback == 5:
            y = float(PlayerFrom.Y)
            oy = float(DataStore.Get("tpfriendy", id))
            if oy - y > 2.6:
                Server.BroadcastFrom(self.sys, PlayerFrom.Name + red + " tried to fall through a house via tpa. Kicked.")
                Plugin.Log("DizzyHackBypass", PlayerFrom.Name + " - " + PlayerFrom.SteamID + " - " + PlayerFrom.IP + " - " + str(PlayerFrom.Location))
                rand = self.DefaultLoc()
                num = random.randrange(1, 8155)
                loc = rand.GetSetting("DefaultLoc", str(num))
                loc = self.Replace(loc)
                loc = Util.CreateVector(float(loc[0]), float(loc[1]), float(loc[2]))
                PlayerFrom.TeleportTo(loc)
                DataStore.Remove("tpfriendy", id)
                self.addJob(2, PlayerFrom, PlayerTo, 6, id, tid)
                return
            self.addJob(2, PlayerFrom, PlayerTo, 4, id, tid)
        elif callback == 6:
            try:
                PlayerFrom.Disconnect()
            except:
                pass

    def On_PlayerDisconnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        self.KillJob(Player)
        DataStore.Add("tpfriendautoban", id, "none")

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "cleartpatimers":
            if Player.Admin or self.isMod(id):
                self.clearTimers()
                Player.MessageFrom(self.sys, "Cleared!")

        elif cmd == "tpa":
            if len(args) == 0:
                Player.MessageFrom(self.sys, "Teleport Usage:")
                Player.MessageFrom(self.sys, "TpFriend V" + __version__ + " by DreTaX")
                Player.MessageFrom(self.sys, "\"/tpa [PlayerName]\" to request a teleport.")
                Player.MessageFrom(self.sys, "\"/tpaccept\" to accept a requested teleport.")
                Player.MessageFrom(self.sys, "\"/tpdeny\" to deny a request.")
                Player.MessageFrom(self.sys, "\"/tpcount\" to see how many requests you have remaining.")
                Player.MessageFrom(self.sys, "\"/tpcancel\" to cancel your own request.")
            else:
                config = self.TpFriendConfig()
                playertor = self.CheckV(Player, args)
                if playertor is None:
                    return
                if playertor == Player:
                    Player.MessageFrom(self.sys, "Cannot teleport to yourself!")
                    return
                name = Player.Name
                id = Player.SteamID
                idt = playertor.SteamID
                namet = playertor.Name
                maxuses = int(config.GetSetting("Settings", "Maxuses"))
                cooldown = int(config.GetSetting("Settings", "cooldown"))
                stuff = int(config.GetSetting("Settings", "timeoutr"))
                time = DataStore.Get("tpfriendcooldown", id)
                usedtp = DataStore.Get("tpfriendusedtp", id)
                if time is None:
                    DataStore.Add("tpfriendcooldown", id, 7)
                    time = 7
                calc = System.Environment.TickCount - time
                if calc < 0 or math.isnan(calc):
                    DataStore.Add("tpfriendcooldown", id, 7)
                    time = 7
                if calc >= cooldown or time == 7:
                    if usedtp is None:
                        DataStore.Add("tpfriendusedtp", id, 0)
                        usedtp = 0
                    if maxuses > 0:
                        if maxuses >= int(usedtp):
                            Player.MessageFrom(self.sys, "Reached max number of teleport requests!")
                            return
                    if DataStore.Get("tpfriendpending2", idt) is not None:
                        Player.MessageFrom(self.sys, "This player is pending a request. Wait a bit.")
                        return
                    if DataStore.Get("tpfriendpending", id):
                        Player.MessageFrom(self.sys, "You are pending a request. Wait a bit or cancel It")
                        return

                    DataStore.Add("tpfriendcooldown", id, System.Environment.TickCount)
                    playertor.MessageFrom(self.sys, "Teleport request from " + name + " to accept write /tpaccept")
                    Player.MessageFrom(self.sys, "Teleport request sent to " + namet)
                    DataStore.Add("tpfriendpending", id, idt)
                    DataStore.Add("tpfriendpending2", idt, id)
                    self.KillJob(Player)
                    self.KillJob(playertor)
                    self.addJob(stuff, id, idt, 2)
                else:
                    Player.MessageFrom(self.sys, "You have to wait before teleporting again!")
                    done = round((calc / 1000) / 60, 2)
                    done2 = round((cooldown / 1000) / 60, 2)
                    Player.MessageFrom(self.sys, "Time Remaining: " + str(done) + "/" + str(done2) + " mins")

        elif cmd == "tpaccept":
            pending = DataStore.Get("tpfriendpending2", id)
            config = self.TpFriendConfig()
            if pending is not None:
                playerfromm = self.getPlayer(pending)
                if playerfromm is not None:
                    self.KillJob(Player)
                    self.KillJob(playerfromm)
                    maxtpnumber = int(config.GetSetting("Settings", "Maxuses"))
                    playertpuse = int(DataStore.Get("tpfriendusedtp", pending))
                    tpdelayy = int(config.GetSetting("Settings", "tpdelay"))
                    if maxtpnumber > 0:
                        playertpuse = int(playertpuse) + 1
                        DataStore.Add("tpfriendusedtp", pending, playertpuse)
                        playerfromm.MessageFrom(self.sys, "Teleport requests used " + str(playertpuse) + " / " + str(maxtpnumber))
                    else:
                        playerfromm.MessageFrom(self.sys, "You have unlimited requests remaining!")

                    check = int(config.GetSetting("Settings", "safetpcheck"))
                    idt = playerfromm.SteamID
                    if tpdelayy > 0:
                        playerfromm.MessageFrom(self.sys, "Teleporting you in: " + str(tpdelayy) + " second(s)")
                        self.addJob(tpdelayy, idt, id, 1)

                    else:
                        DataStore.Add("tpfriendautoban", idt, "using")
                        DataStore.Add("tpfriendy", idt, str(Player.Y))
                        playerfromm.TeleportTo(Player.Location)
                        playerfromm.MessageFrom(self.sys, "Teleported!")
                        DataStore.Add("tpfriendautoban", idt, "none")
                        self.addJob(check, idt, id, 3)

                    DataStore.Remove("tpfriendpending", idt)
                    DataStore.Remove("tpfriendpending2", id)
                    Player.MessageFrom(self.sys, "Teleport Request Accepted!")

                else:
                    self.KillJob(Player)
                    Player.MessageFrom(self.sys, "Player isn't online!")
            else:
                Player.MessageFrom(self.sys, "Your request was timed out, or you don't have any.")

        elif cmd == "tpdeny":
            pending = DataStore.Get("tpfriendpending2", id)
            if pending is not None:
                playerfromm = self.getPlayer(pending)
                if playerfromm is not None:
                    playerfromm.MessageFrom(self.sys, "Your request was denied!")
                    self.KillJob(playerfromm)
                self.KillJob(Player)
                DataStore.Remove("tpfriendpending", pending)
                DataStore.Add("tpfriendcooldown", pending, 7)
                DataStore.Remove("tpfriendpending2", id)
                Player.MessageFrom(self.sys, "Request denied!")
            else:
                Player.MessageFrom(self.sys, "No request to deny.")

        elif cmd == "tpcancel":
            pending = DataStore.Get("tpfriendpending", id)
            if pending is not None:
                playerto = self.getPlayer(pending)
                if playerto is not None:
                    playerto.MessageFrom(self.sys, Player.Name + " Cancelled the request!")
                    self.KillJob(playerto)
                self.KillJob(Player)
                DataStore.Remove("tpfriendpending", id)
                DataStore.Add("tpfriendcooldown", id, 7)
                DataStore.Remove("tpfriendpending2", pending)
                Player.MessageFrom(self.sys, "Request Cancelled!")
            else:
                Player.MessageFrom(self.sys, "There is nothing to cancel.")

        elif cmd == "tpcount":
            config = self.TpFriendConfig()
            maxuses = int(config.GetSetting("Settings", "Maxuses"))
            if maxuses > 0:
                uses = int(DataStore.Get("tpfriendusedtp", id))
                if uses is None:
                    uses = 0
                Player.MessageFrom(self.sys, "Teleport requests used " + str(uses) + " / " + str(maxuses))
            else:
                Player.MessageFrom(self.sys, "You have unlimited requests remaining!")

        elif cmd == "tpresettime":
            if Player.Admin or self.isMod(id):
                DataStore.Add("tpfriendcooldown", id, 7)
                Player.Message("Reset!")

        elif cmd == "clearuses":
            id = Player.SteamID
            if Player.Admin or self.isMod(id):
                DataStore.Flush("tpfriendusedtp")
                Player.MessageFrom(self.sys, "Flushed!")