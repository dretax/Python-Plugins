__author__ = 'DreTaX'
__version__ = '1.8.2'

import clr

clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("Assembly-CSharp")
import Pluton
import System
from System import *
import math
import BasePlayer

"""
    Class
"""

Pending = []
class TpFriend:

    def On_PlayerConnected(self, Player):
        usedtp = DataStore.Get("tpfriendusedtp", Player.SteamID)
        if usedtp is None:
            DataStore.Add("tpfriendusedtp", Player.SteamID, 0)

    def On_PlayerDisconnected(self, Player):
        self.KillJob(Player)

    def On_PluginInit(self):
        DataStore.Flush("tpfriendpending")
        DataStore.Flush("tpfriendpending2")
        DataStore.Flush("tpfriendautoban")
        DataStore.Flush("tpfriendcooldown")

    """
        Timers
    """

    def TpDelayCallback(self, timer):
        timer.Kill()
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Settings", "sysname")
        tpdelaytp = timer.Args
        PlayerFrom = tpdelaytp["PlayerR"]
        PlayerTo = tpdelaytp["PlayerT"]
        callback = tpdelaytp["Call"]
        id = tpdelaytp["FromID"]
        id2 = tpdelaytp["ToID"]
        if PlayerFrom is None or PlayerTo is None:
            DataStore.Remove("tpfriendpending", id)
            DataStore.Add("tpfriendcooldown", id, 7)
            DataStore.Remove("tpfriendpending2", id2)
            return
        if callback == 1:
            if not PlayerTo.basePlayer.IsAlive():
                PlayerFrom.MessageFrom(systemname, "Your buddy died. Teleportation cancelled.")
                PlayerTo.MessageFrom(systemname, "You died. Teleportation cancelled.")
                DataStore.Add("tpfriendcooldown", id, 7)
                return
            if not PlayerFrom.basePlayer.IsAlive():
                PlayerTo.MessageFrom(systemname, "Your buddy died. His Teleportation cancelled.")
                PlayerFrom.MessageFrom(systemname, "You died. Teleportation cancelled.")
                DataStore.Add("tpfriendcooldown", id, 7)
                return
            DataStore.Remove("tpfriendpending", id)
            DataStore.Remove("tpfriendpending2", id2)
            PlayerFrom.Teleport(PlayerTo.Location)
            PlayerFrom.MessageFrom(systemname, "Teleported!")
            PlayerTo.MessageFrom(systemname, str(PlayerFrom.Name) + " teleported to you!")
        elif callback == 2:
            if not DataStore.ContainsKey("tpfriendpending", id) or not DataStore.ContainsKey("tpfriendpending2", id2):
                return
            if PlayerFrom not in Pending or PlayerTo not in Pending:
                return
            DataStore.Remove("tpfriendpending", id)
            DataStore.Add("tpfriendcooldown", id, 7)
            DataStore.Remove("tpfriendpending2", id2)
            PlayerFrom.MessageFrom(systemname, "Teleport request timed out.")
            PlayerTo.MessageFrom(systemname, "Teleport request timed out.")

    """
        Methods
    """

    def TpFriendConfig(self):
        if not Plugin.IniExists("TpFriendConfig"):
            loc = Plugin.CreateIni("TpFriendConfig")
            loc.Save()
        return Plugin.GetIni("TpFriendConfig")

    def addJob(self, xtime, PlayerFrom, PlayerTo, callback, id, id2):
        List = Plugin.CreateDict()
        List["PlayerR"] = PlayerFrom
        List["PlayerT"] = PlayerTo
        List["Call"] = callback
        List["FromID"] = id
        List["ToID"] = id2
        Plugin.CreateParallelTimer("TpDelay", xtime * 1000, List).Start()

    def KillJob(self, Player):
        if Player in Pending:
            Pending.remove(Player)

    """
        CheckV Assistants
    """

    def GetPlayerName(self, name, Mode=1):
        if Mode == 1 or Mode == 3:
            for pl in Server.ActivePlayers:
                if pl.Name.lower() == name:
                    return pl
        if Mode == 2 or Mode == 3:
            for pl in Server.OfflinePlayers.Values:
                if pl.Name.lower() == name:
                    return pl
        return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        Mode: Search mode (Default: 1)
            1 = Search Online Players
            2 = Search Offline Players
            3 = Both
        V6.0
    """

    def CheckV(self, Player, args, Mode=1):
        config = self.TpFriendConfig()
        systemname = config.GetSetting("Settings", "sysname")
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.Join(" ", args).lower(), Mode)
            if p is not None:
                return p
            if Mode == 1 or Mode == 3:
                for pl in Server.ActivePlayers:
                    for namePart in args:
                        if namePart.lower() in pl.Name.lower():
                            p = pl
                            count += 1
            if Mode == 2 or Mode == 3:
                for offlineplayer in Server.OfflinePlayers.Values:
                    for namePart in args:
                        if namePart.lower() in offlineplayer.Name.lower():
                            p = offlineplayer
                            count += 1
        else:
            ag = str(args).lower()  # just incase
            p = self.GetPlayerName(ag, Mode)
            if p is not None:
                return p
            if Mode == 1 or Mode == 3:
                for pl in Server.ActivePlayers:
                    if ag in pl.Name.lower():
                        p = pl
                        count += 1
            if Mode == 2 or Mode == 3:
                for offlineplayer in Server.OfflinePlayers.Values:
                    if ag in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find " + str.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found " + str(count) +
                               " player with similar name. Use more correct name!")
            return None

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        id = Player.SteamID
        if cmd.cmd == "tpa":
            if len(args) == 0:
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                Player.MessageFrom(systemname, "Teleport Usage:")
                Player.MessageFrom(systemname, "\"/tpa [PlayerName]\" to request a teleport.")
                Player.MessageFrom(systemname, "\"/tpaccept\" to accept a requested teleport.")
                Player.MessageFrom(systemname, "\"/tpdeny\" to deny a request.")
                Player.MessageFrom(systemname, "\"/tpcancel\" to cancel your request.")
                Player.MessageFrom(systemname, "\"/tpcount\" to see how many requests you have remaining.")
            elif len(args) > 0:
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                playertor = self.CheckV(Player, args)
                if playertor is None:
                    return
                if playertor.Name == Player.Name:
                    Player.MessageFrom(systemname, "Cannot teleport to yourself!")
                    return
                maxuses = config.GetSetting("Settings", "Maxuses")
                cd = config.GetSetting("Settings", "cooldown")
                cooldown = int(cd)
                stuff = int(config.GetSetting("Settings", "timeoutr"))
                if DataStore.Get("tpfriendcooldown", id) is None:
                    DataStore.Add("tpfriendcooldown", id, 7)
                time = DataStore.Get("tpfriendcooldown", id)
                systick = System.Environment.TickCount
                pending = DataStore.Get("tpfriendpending2", playertor.SteamID)
                if pending is not None:
                    Player.MessageFrom(systemname, "This player is already pending a request.")
                    Player.MessageFrom(systemname, "Try again later, or tell the player to deny his current request.")
                    return

                if (systick - time) < 0 or math.isnan(systick - time):
                    DataStore.Add("tpfriendcooldown", id, 7)
                    time = 7

                calc = systick - time
                if calc >= cooldown or time == 7:
                    if DataStore.Get("tpfriendusedtp", id) is None:
                        DataStore.Add("tpfriendusedtp", id, 0)
                    usedtp = DataStore.Get("tpfriendusedtp", id)
                    maxtpnumber = int(maxuses)
                    playertpuse = int(usedtp)
                    if maxtpnumber > 0:
                        if maxtpnumber >= playertpuse:
                            Player.MessageFrom(systemname, "Reached max number of teleport requests!")
                            return

                    DataStore.Add("tpfriendcooldown", id, System.Environment.TickCount)
                    playertor.MessageFrom(systemname, "Teleport request from " + Player.Name + " to accept type /tpaccept")
                    playertor.MessageFrom(systemname, "Teleport request from " + Player.Name + " to deny type /tpdeny")
                    Player.MessageFrom(systemname, "Teleport request sent to " + playertor.Name)
                    DataStore.Add("tpfriendpending", id, playertor.SteamID)
                    DataStore.Add("tpfriendpending2", playertor.SteamID, id)
                    self.KillJob(Player)
                    self.KillJob(playertor)
                    Pending.append(Player)
                    Pending.append(playertor)
                    self.addJob(stuff, Player, playertor, 2, id, playertor.SteamID)
                else:
                    Player.MessageFrom(systemname, "You have to wait before teleporting again!")
                    done = round((calc / 1000) / 60, 2)
                    done2 = round((cooldown / 1000) / 60, 2)
                    Player.MessageFrom(systemname, "Time Remaining: " + str(done) + "/" + str(done2))
        elif cmd.cmd == "tpaccept":
            pending = DataStore.Get("tpfriendpending2", id)
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            if pending is not None:
                playerfromm = Server.FindPlayer(pending)
                if playerfromm is not None:
                    self.KillJob(Player)
                    self.KillJob(playerfromm)
                    maxuses = config.GetSetting("Settings", "Maxuses")
                    usedtp = DataStore.Get("tpfriendusedtp", pending)
                    maxtpnumber = int(maxuses)
                    playertpuse = int(usedtp)
                    tpdelay = int(config.GetSetting("Settings", "tpdelay"))
                    if maxtpnumber > 0:
                        uses = playertpuse + 1
                        DataStore.Add("tpfriendusedtp", pending, uses)
                        playerfromm.MessageFrom(systemname, "Teleport requests used " + str(uses) + " / " + str(maxtpnumber))

                    else:
                        playerfromm.MessageFrom(systemname, "You have unlimited requests remaining!")
                    DataStore.Add("tpfriendautoban", playerfromm.SteamID, "using")

                    DataStore.Remove("tpfriendpending", playerfromm.SteamID)
                    DataStore.Remove("tpfriendpending2", id)
                    Player.MessageFrom(systemname, "Teleport Request Accepted!")
                    if tpdelay > 0:
                        self.addJob(tpdelay, playerfromm, Player, 1, pending, id)
                        playerfromm.MessageFrom(systemname, "Teleporting you in: " + str(tpdelay) + " second(s)")
                    else:
                        playerfromm.Teleport(Player.Location)
                        playerfromm.MessageFrom(systemname, "Teleported!")
                        Player.MessageFrom(systemname, playerfromm.Name + " teleported to you!")
                else:
                    Player.MessageFrom(systemname, "Player isn't online!")
                    self.KillJob(Player)

            else:
                Player.MessageFrom(systemname, "Your request timed out, or you don't have any.")
        elif cmd.cmd == "tpdeny":
            pending = DataStore.Get("tpfriendpending2", id)
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            if pending is not None:
                playerfromm = Server.FindPlayer(pending)
                DataStore.Remove("tpfriendpending", playerfromm.SteamID)
                DataStore.Add("tpfriendcooldown", playerfromm.SteamID, 7)
                DataStore.Remove("tpfriendpending2", id)
                Player.MessageFrom(systemname, "Request denied!")
                if playerfromm is not None:
                    playerfromm.MessageFrom(systemname, "Your request was denied!")
                    self.KillJob(playerfromm)
                self.KillJob(Player)
            else:
                Player.MessageFrom(systemname, "No request to deny.")
        elif cmd == "tpcancel":
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            pending = DataStore.Get("tpfriendpending", id)
            if pending is not None:
                playerto = Server.FindPlayer(pending)
                if playerto is not None:
                    playerto.MessageFrom(systemname, Player.Name + " Cancelled the request!")
                    self.KillJob(playerto)
                self.KillJob(Player)
                DataStore.Remove("tpfriendpending", id)
                DataStore.Add("tpfriendcooldown", id, 7)
                DataStore.Remove("tpfriendpending2", pending)
                Player.MessageFrom(systemname, "Request Cancelled!")
            else:
                Player.MessageFrom(systemname, "There is nothing to cancel.")
        elif cmd.cmd == "tpcount":
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            maxuses = config.GetSetting("Settings", "Maxuses")
            if int(maxuses) > 0:
                uses = DataStore.Get("tpfriendusedtp", Player.Name)
                if uses is None:
                    uses = 0

                Player.MessageFrom(systemname, "Teleport requests used " + str(uses) + " / " + str(maxuses))
            else:
                Player.MessageFrom(systemname, "You have unlimited requests remaining!")
        elif cmd.cmd == "tpresettime":
            if Player.Admin:
                DataStore.Add("tpfriendcooldown", id, 7)
                Player.Message("Time for you, Reset!")
            else:
                Player.Message("You aren't an admin!")
        elif cmd.cmd == "flushcount":
            if Player.Admin:
                DataStore.Flush("tpfriendusedtp")
                Player.Message("Done!")
            else:
                Player.Message("You aren't an admin!")