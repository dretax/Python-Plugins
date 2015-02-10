__author__ = 'DreTaX'
__version__ = '3.6'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import math
import System
from System import *
import re

red = "[color #FF0000]"
green = "[color #009900]"
white = "[color #FFFFFF]"
DStable = "TpTimer"

TpJobs = {'Name': 'TpFriend'}

"""
    Class
"""


class TpFriend:
    """
        Methods
    """

    def On_PluginInit(self):
        DataStore.Flush("TpTimer")
        DataStore.Flush("tpfriendautoban")
        DataStore.Flush("tpfriendpending")
        DataStore.Flush("tpfriendpending2")
        DataStore.Flush("tpfriendcooldown")
        Util.ConsoleLog(TpJobs['Name'] + " v" + __version__ + " by " + __author__ + " loaded.", True)

    def TpFriendConfig(self):
        if not Plugin.IniExists("TpFriendConfig"):
            loc = Plugin.CreateIni("TpFriendConfig")
            loc.Save()
        return Plugin.GetIni("TpFriendConfig")

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
        config = self.TpFriendConfig()
        systemname = config.GetSetting("Settings", "sysname")
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
            Player.MessageFrom(systemname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def Stringify(self, List):
        s = re.sub("[[\]\'\ ]", '', str(List))
        return str(s)

    def Parse(self, String):
        return String.split(',')

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

    def addJob(self, xtime, PlayerFrom, PlayerTo, callback):
        epoch = Plugin.GetTimestamp()
        exectime = int(epoch) + int(xtime)
        # Exectime, PlayerTo, Callback
        List = []
        List.append(str(exectime))
        List.append(str(PlayerTo))
        List.append(str(callback))
        DataStore.Add(DStable, PlayerFrom, self.Stringify(List))
        self.startTimer()

    def killJob(self, id):
        DataStore.Remove(DStable, id)

    def startTimer(self):
        config = self.TpFriendConfig()
        gfjfhg = int(config.GetSetting("Settings", "run_timer")) * 1000
        try:
            if not Plugin.GetTimer("TpJobTimer"):
                Plugin.CreateTimer("TpJobTimer", gfjfhg).Start()
        except:
            pass

    def stopTimer(self):
        #Plugin.KillTimer("TpJobTimer")
        timer = Plugin.GetTimer("TpJobTimer")
        if timer is None:
            return
        timer.Stop()
        Plugin.Timers.Remove("TpJobTimer")

    def getPlayer(self, d):
        try:
            id = str(d)
            pl = Server.FindPlayer(id)
            return pl
        except:
            return None

    def clearTimers(self):
        DataStore.Flush(DStable)
        self.stopTimer()

    def TpJobTimerCallback(self):
        epoch = int(Plugin.GetTimestamp())
        if DataStore.Count(DStable) >= 1:
            pending = DataStore.Keys(DStable)
            config = self.TpFriendConfig()
            sys = config.GetSetting("Settings", "sysname")
            for id in pending:
                if DataStore.Get(DStable, id) is None:
                    DataStore.Remove(DStable, id)
                    continue
                params = self.Parse(str(DataStore.Get(DStable, id)))
                if epoch >= int(params[0]):
                    DataStore.Add("tpfriendautoban", id, "using")
                    PlayerFrom = self.getPlayer(id)
                    PlayerTo = self.getPlayer(params[1])
                    callback = int(params[2])
                    self.killJob(id)
                    # Normal Teleport Callback
                    if callback == 1:
                        if PlayerFrom is None or PlayerTo is None:
                            DataStore.Add("tpfriendautoban", id, "none")
                            continue
                        check = int(config.GetSetting("Settings", "safetpcheck"))
                        PlayerFrom.TeleportTo(PlayerTo.Location)
                        PlayerFrom.MessageFrom(sys, "You have been teleported to your friend")
                        self.addJob(check, id, params[1], 3)
                    # AutoKill
                    elif callback == 2:
                        ispend = DataStore.Get("tpfriendpending", id)
                        ispend2 = DataStore.Get("tpfriendpending2", params[1])
                        if ispend is not None and ispend2 is not None:
                            DataStore.Remove("tpfriendpending", id)
                            DataStore.Remove("tpfriendpending2", params[1])
                            DataStore.Add("tpfriendcooldown", id, 7)
                            DataStore.Add("tpfriendautoban", id, "none")
                            if PlayerFrom is not None:
                                PlayerFrom.MessageFrom(sys, "Teleport request timed out")
                            if PlayerTo is not None:
                                PlayerTo.MessageFrom(sys, "Teleport request timed out")
                    elif callback == 3:
                        if PlayerFrom is None or PlayerTo is None:
                            DataStore.Add("tpfriendautoban", id, "none")
                            continue
                        PlayerFrom.TeleportTo(PlayerTo.Location)
                        PlayerFrom.MessageFrom(sys, "You have been teleported to your friend again.")
                        DataStore.Add("tpfriendy", id, str(PlayerTo.Y))
                        self.addJob(2, id, params[1], 5)
                    elif callback == 4:
                        DataStore.Add("tpfriendautoban", id, "none")
                    elif callback == 5:
                        y = float(PlayerFrom.Y)
                        oy = float(DataStore.Get("tpfriendy", id))
                        Server.Broadcast("Test: " + str(oy) + " | " + str(y) + " | " + str(oy-y))
                        if oy - y > 3.65:
                            Server.BroadcastFrom("TpFriend", PlayerFrom.Name + " tried to fall through a house via tpa. Kicked.")
                            PlayerFrom.TeleportTo(PlayerTo.Location)
                            PlayerFrom.Disconnect()
                        DataStore.Remove("tpfriendy", id)
                        self.addJob(2, id, params[1], 4)


        else:
            self.stopTimer()

    def On_PlayerDisconnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            return
        DataStore.Add("tpfriendautoban", id, "none")

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "cleartpatimers":
            if Player.Admin or self.isMod(id):
                self.clearTimers()
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                Player.MessageFrom(systemname, "Cleared!")

        elif cmd == "tpa":
            if len(args) == 0:
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                Player.MessageFrom(systemname, "Teleport Usage:")
                Player.MessageFrom(systemname, "TpFriend V3.6 by DreTaX")
                Player.MessageFrom(systemname, "\"/tpa [PlayerName]\" to request a teleport.")
                Player.MessageFrom(systemname, "\"/tpaccept\" to accept a requested teleport.")
                Player.MessageFrom(systemname, "\"/tpdeny\" to deny a request.")
                Player.MessageFrom(systemname, "\"/tpcount\" to see how many requests you have remaining.")
                Player.MessageFrom(systemname, "\"/tpcancel\" to cancel your own request.")
            else:
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                playertor = self.CheckV(Player, args)
                if playertor is None:
                    return
                if playertor == Player:
                    Player.MessageFrom(systemname, "Cannot teleport to yourself!")
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
                            Player.MessageFrom(systemname, "Reached max number of teleport requests!")
                            return
                    if DataStore.Get("tpfriendpending2", idt) is not None:
                        Player.MessageFrom(systemname, "This player is pending a request. Wait a bit.")
                        return
                    if DataStore.Get("tpfriendpending", id):
                        Player.MessageFrom(systemname, "You are pending a request. Wait a bit or cancel It")
                        return

                    DataStore.Add("tpfriendcooldown", id, System.Environment.TickCount)
                    playertor.MessageFrom(systemname, "Teleport request from " + name + " to accept write /tpaccept")
                    Player.MessageFrom(systemname, "Teleport request sent to " + namet)
                    DataStore.Add("tpfriendpending", id, idt)
                    DataStore.Add("tpfriendpending2", idt, id)
                    self.addJob(stuff, id, idt, 2)
                else:
                    Player.MessageFrom(systemname, "You have to wait before teleporting again!")
                    done = round((calc / 1000) / 60, 2)
                    done2 = round((cooldown / 1000) / 60, 2)
                    Player.MessageFrom(systemname, "Time Remaining: " + str(done) + "/" + str(done2) + " mins")

        elif cmd == "tpaccept":
            pending = DataStore.Get("tpfriendpending2", id)
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            if pending is not None:
                playerfromm = self.getPlayer(pending)
                if playerfromm is not None:
                    self.killJob(pending)
                    maxtpnumber = int(config.GetSetting("Settings", "Maxuses"))
                    playertpuse = int(DataStore.Get("tpfriendusedtp", pending))
                    tpdelayy = int(config.GetSetting("Settings", "tpdelay"))
                    if maxtpnumber > 0:
                        playertpuse = int(playertpuse) + 1
                        DataStore.Add("tpfriendusedtp", pending, playertpuse)
                        playerfromm.MessageFrom(systemname, "Teleport requests used " + str(playertpuse) + " / " + str(maxtpnumber))
                    else:
                        playerfromm.MessageFrom(systemname, "You have unlimited requests remaining!")

                    check = int(config.GetSetting("Settings", "safetpcheck"))
                    idt = playerfromm.SteamID
                    if tpdelayy > 0:
                        playerfromm.MessageFrom(systemname, "Teleporting you in: " + str(tpdelayy) + " second(s)")
                        self.addJob(tpdelayy, idt, id, 1)

                    else:
                        DataStore.Add("tpfriendautoban", idt, "using")
                        DataStore.Add("tpfriendy", idt, str(Player.Y))
                        playerfromm.TeleportTo(Player.Location)
                        playerfromm.MessageFrom(systemname, "Teleported!")
                        DataStore.Add("tpfriendautoban", idt, "none")
                        self.addJob(check, idt, id, 3)

                    DataStore.Remove("tpfriendpending", idt)
                    DataStore.Remove("tpfriendpending2", id)
                    Player.MessageFrom(systemname, "Teleport Request Accepted!")

                else:
                    Player.MessageFrom(systemname, "Player isn't online!")
            else:
                Player.MessageFrom(systemname, "Your request was timed out, or you don't have any.")

        elif cmd == "tpdeny":
            pending = DataStore.Get("tpfriendpending2", id)
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            if pending is not None:
                playerfromm = self.getPlayer(pending)
                if playerfromm is not None:
                    playerfromm.MessageFrom(systemname, "Your request was denied!")
                self.killJob(pending)
                DataStore.Remove("tpfriendpending", pending)
                DataStore.Add("tpfriendcooldown", pending, 7)
                DataStore.Remove("tpfriendpending2", id)
                Player.MessageFrom(systemname, "Request denied!")
            else:
                Player.MessageFrom(systemname, "No request to deny.")

        elif cmd == "tpcancel":
            pending = DataStore.Get("tpfriendpending", id)
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            if pending is not None:
                playerto = self.getPlayer(pending)
                if playerto is not None:
                    playerto.MessageFrom(systemname, Player.Name + " Cancelled the request!")
                self.killJob(id)
                DataStore.Remove("tpfriendpending", id)
                DataStore.Add("tpfriendcooldown", id, 7)
                DataStore.Remove("tpfriendpending2", pending)
                Player.MessageFrom(systemname, "Request Cancelled!")
            else:
                Player.MessageFrom(systemname, "There is nothing to cancel.")

        elif cmd == "tpcount":
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            maxuses = int(config.GetSetting("Settings", "Maxuses"))
            if maxuses > 0:
                uses = int(DataStore.Get("tpfriendusedtp", id))
                if uses is None:
                    uses = 0
                Player.MessageFrom(systemname, "Teleport requests used " + str(uses) + " / " + str(maxuses))
            else:
                Player.MessageFrom(systemname, "You have unlimited requests remaining!")

        elif cmd == "tpresettime":
            if Player.Admin or self.isMod(id):
                DataStore.Add("tpfriendcooldown", id, 7)
                Player.Message("Reset!")

        elif cmd == "clearuses":
            id = Player.SteamID
            if Player.Admin or self.isMod(id):
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                DataStore.Flush("tpfriendusedtp")
                Player.MessageFrom(systemname, "Flushed!")