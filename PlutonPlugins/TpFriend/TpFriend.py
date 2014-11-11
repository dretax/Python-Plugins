__author__ = 'DreTaX'
__version__ = '1.6'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import *
import math

"""
    Class
"""


class TpFriend:

    """
        Timers
    """

    def On_PlayerConnected(self, Player):
        usedtp = DataStore.Get("tpfriendusedtp", Player.SteamID)
        if usedtp is None:
            DataStore.Add("tpfriendusedtp", Player.SteamID, 0)

    def AutoKillCallback(self, timer):
        timer.Kill()
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Settings", "sysname")
        autokill = timer.Args
        PlayerFrom = Server.FindPlayer(autokill["PlayerR"])
        PlayerTo = Server.FindPlayer(autokill["PlayerT"])
        if PlayerFrom is None or PlayerTo is None:
            DataStore.Remove("tpfriendpending", autokill["PlayerR"])
            DataStore.Add("tpfriendcooldown", autokill["PlayerR"], 7)
            DataStore.Remove("tpfriendpending2", autokill["PlayerT"])
            return
        if not DataStore.ContainsKey("tpfriendpending", PlayerFrom.SteamID) or not DataStore.ContainsKey("tpfriendpending2", PlayerTo.SteamID):
            return
        DataStore.Remove("tpfriendpending", PlayerFrom.SteamID)
        DataStore.Add("tpfriendcooldown", PlayerFrom.SteamID, 7)
        DataStore.Remove("tpfriendpending2", PlayerTo.SteamID)
        PlayerFrom.MessageFrom(systemname, "Teleport request timed out.")
        PlayerTo.MessageFrom(systemname, "Teleport request timed out.")
        return

    def TpDelayCallback(self, timer):
        timer.Kill()
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Settings", "sysname")
        tpsec = int(ini.GetSetting("Settings", "tpsec"))
        tpdelaytp = timer.Args
        PlayerFrom = Server.FindPlayer(tpdelaytp["PlayerR"])
        PlayerTo = Server.FindPlayer(tpdelaytp["PlayerT"])
        if PlayerFrom is None or PlayerTo is None:
            DataStore.Remove("tpfriendpending", tpdelaytp["PlayerR"])
            DataStore.Remove("tpfriendpending2", tpdelaytp["PlayerT"])
            return
        DataStore.Remove("tpfriendpending", PlayerFrom.SteamID)
        DataStore.Remove("tpfriendpending2", PlayerTo.SteamID)
        PlayerFrom.GroundTeleport(PlayerTo.Location)
        PlayerFrom.Teleport(PlayerTo.Location)
        PlayerFrom.MessageFrom(systemname, "Teleported!")
        PlayerTo.MessageFrom(systemname, str(PlayerFrom.Name) + " teleported to you!")
        if tpsec > 0:
            Plugin.CreateParallelTimer("TpSafeTy", tpsec * 1000, tpdelaytp).Start()
        return

    def TpSafeTyCallback(self, timer):
        timer.Kill()
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Settings", "sysname")
        tpdelaytp = timer.Args
        PlayerFrom = Server.FindPlayer(tpdelaytp["PlayerR"])
        if PlayerFrom is None:
            return
        PlayerFrom.basePlayer.supressSnapshots = True
        PlayerFrom.basePlayer.UpdateNetworkGroup()
        PlayerFrom.basePlayer.UpdatePlayerCollider(True, False)
        PlayerFrom.basePlayer.SendFullSnapshot()
        PlayerFrom.basePlayer.inventory.SendSnapshot()
        PlayerFrom.MessageFrom(systemname, "Updated You.")
        return

    """
        Methods
    """
    def On_PluginInit(self):
        DataStore.Flush("tpfriendpending")
        DataStore.Flush("tpfriendpending2")
        DataStore.Flush("tpfriendautoban")

    def TpFriendConfig(self):
        if not Plugin.IniExists("TpFriendConfig"):
            loc = Plugin.CreateIni("TpFriendConfig")
            loc.Save()
        return Plugin.GetIni("TpFriendConfig")

    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        V3.1
    """
    def CheckV(self, Player, args):
        systemname = "TpFriend"
        p = self.GetPlayerName(String.Join(" ", args))
        if p is not None:
            return p

        count = 0
        for pl in Server.ActivePlayers:
            for namePart in args:
                if namePart.lower() in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find " + String.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found " + str(count) + " player with similar name. Use more correct name!")
            return None

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "tpa":
            if len(args) == 0:
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                Player.MessageFrom(systemname, "Teleport Usage:")
                Player.MessageFrom(systemname, "\"/tpa [PlayerName]\" to request a teleport.")
                Player.MessageFrom(systemname, "\"/tpaccept\" to accept a requested teleport.")
                Player.MessageFrom(systemname, "\"/tpdeny\" to deny a request.")
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
                if DataStore.Get("tpfriendcooldown", Player.SteamID) is None:
                    DataStore.Add("tpfriendcooldown", Player.SteamID, 7)
                time = DataStore.Get("tpfriendcooldown", Player.SteamID)
                systick = System.Environment.TickCount
                pending = DataStore.Get("tpfriendpending2", playertor.SteamID)
                if pending is not None:
                    Player.MessageFrom(systemname, "This player is already pending a request.")
                    Player.MessageFrom(systemname, "Try again later, or tell the player to deny his current request.")
                    return

                if (systick - time) < 0 or math.isnan(systick - time):
                    DataStore.Add("tpfriendcooldown", Player.SteamID, 7)
                    time = 7

                calc = systick - time
                if calc >= cooldown or time == 7:
                    if DataStore.Get("tpfriendusedtp", Player.SteamID) is None:
                        DataStore.Add("tpfriendusedtp", Player.SteamID, 0)
                    usedtp = DataStore.Get("tpfriendusedtp", Player.SteamID)
                    maxtpnumber = int(maxuses)
                    playertpuse = int(usedtp)
                    if maxtpnumber > 0:
                        if maxtpnumber >= playertpuse:
                            Player.MessageFrom(systemname, "Reached max number of teleport requests!")
                            return

                    DataStore.Add("tpfriendcooldown", Player.SteamID, System.Environment.TickCount)
                    playertor.MessageFrom(systemname, "Teleport request from " + Player.Name + " to accept type /tpaccept")
                    playertor.MessageFrom(systemname, "Teleport request from " + Player.Name + " to deny type /tpdeny")
                    Player.MessageFrom(systemname, "Teleport request sent to " + playertor.Name)
                    DataStore.Add("tpfriendpending", Player.SteamID, playertor.SteamID)
                    DataStore.Add("tpfriendpending2", playertor.SteamID, Player.SteamID)
                    autokill = Plugin.CreateDict()
                    autokill["PlayerR"] = Player.SteamID
                    autokill["PlayerT"] = playertor.SteamID
                    launchcalc = stuff * 1000
                    Plugin.CreateParallelTimer("AutoKill", launchcalc, autokill).Start()

                else:
                    Player.MessageFrom(systemname, "You have to wait before teleporting again!")
                    done = round((calc / 1000) / 60, 2)
                    done2 = round((cooldown / 1000) / 60, 2)
                    Player.MessageFrom(systemname, "Time Remaining: " + str(done) + "/" + str(done2))
        elif cmd.cmd == "tpaccept":
            pending = DataStore.Get("tpfriendpending2", Player.SteamID)
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            if pending is not None:
                playerfromm = Server.FindPlayer(pending)
                if playerfromm is not None:
                    maxuses = config.GetSetting("Settings", "Maxuses")
                    tpsec = int(config.GetSetting("Settings", "tpsec"))
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
                    DataStore.Remove("tpfriendpending2", Player.SteamID)
                    Player.MessageFrom(systemname, "Teleport Request Accepted!")
                    if tpdelay > 0:
                        tpdelaytp = Plugin.CreateDict()
                        tpdelaytp["PlayerR"] = playerfromm.SteamID
                        tpdelaytp["PlayerT"] = Player.SteamID
                        launchcalc = tpdelay * 1000
                        Plugin.CreateParallelTimer("TpDelay", launchcalc, tpdelaytp).Start()
                        playerfromm.MessageFrom(systemname, "Teleporting you in: " + str(tpdelay) + " second(s)")
                    else:
                        playerfromm.GroundTeleport(Player.Location)
                        playerfromm.Teleport(Player.Location)
                        playerfromm.MessageFrom(systemname, "Teleported!")
                        Player.MessageFrom(systemname, str(playerfromm.Name) + " teleported to you!")
                        tpdelaytp = Plugin.CreateDict()
                        tpdelaytp["PlayerR"] = playerfromm.SteamID
                        tpdelaytp["PlayerT"] = Player.SteamID
                        if tpsec > 0:
                            Plugin.CreateParallelTimer("TpSafeTy", tpsec * 1000, tpdelaytp).Start()

                else:
                    Player.MessageFrom(systemname, "Player isn't online!")

            else:
                Player.MessageFrom(systemname, "Your request timed out, or you don't have any.")
        elif cmd.cmd == "tpdeny":
            pending = DataStore.Get("tpfriendpending2", Player.SteamID)
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            if pending is not None:
                playerfromm = Server.FindPlayer(pending)
                DataStore.Remove("tpfriendpending", playerfromm.SteamID)
                DataStore.Add("tpfriendcooldown", playerfromm.SteamID, 7)
                DataStore.Remove("tpfriendpending2", Player.SteamID)
                Player.MessageFrom(systemname, "Request denied!")
                if playerfromm is not None:
                    playerfromm.MessageFrom(systemname, "Your request was denied!")
            else:
                Player.MessageFrom(systemname, "No request to deny.")
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
                DataStore.Add("tpfriendcooldown", Player.SteamID, 7)
                Player.Message("Time for you, Reset!")
            else:
                Player.Message("You aren't an admin!")
        elif cmd.cmd == "flushcount":
            if Player.Admin:
                DataStore.Flush("tpfriendusedtp")
                Player.Message("Done!")
            else:
                Player.Message("You aren't an admin!")