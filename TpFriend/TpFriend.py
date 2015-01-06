__author__ = 'DreTaX'
__version__ = '3.0'
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

TpJobs = {'Name': 'TpFriend', 'Author': 'DreTaX', 'Version': '3.0'}

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
        DataStore.Flush("homesystemautoban")
        DataStore.Flush("home_cooldown")
        Util.ConsoleLog(TpJobs['Name'] + " v" + TpJobs['Version'] + " by " + TpJobs['Author'] + " loaded.", True)

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
        systemname = "[TpFriend]"
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
        Plugin.KillTimer("TpJobTimer")

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
                DataStore.Add("tpfriendautoban", id, "using")
                params = self.Parse(str(DataStore.Get(DStable, id)))
                if epoch >= int(params[0]):
                    PlayerFrom = self.getPlayer(id)
                    PlayerTo = self.getPlayer(params[1])
                    callback = int(params[2])
                    self.killJob(id)
                    # Normal Teleport Callback
                    if callback == 1:
                        if PlayerFrom is None or PlayerTo is None:
                            DataStore.Add("tpfriendautoban", id, "none")
                            self.killJob(id)
                            continue
                        PlayerFrom.SafeTeleportTo(PlayerTo.Location)
                        PlayerFrom.MessageFrom(sys, "You have been teleported to your home")
                    elif callback == 2:
                        ispend = DataStore.Get("tpfriendpending", params[0])
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

    def On_Command(self, Player, cmd, args):
        if cmd == "cleartpatimers":
            if Player.Admin and self.isMod(Player.SteamID):
                self.clearTimers()
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                Player.MessageFrom(systemname, "Cleared!")
        #todo:..................................