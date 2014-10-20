__author__ = 'DreTaX'
__version__ = '1.2'

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

    def AutoKillCallback(self, timer):
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Settings", "sysname")
        autokill = timer.Args
        PlayerFrom = Server.FindPlayer(autokill["PlayerR"])
        PlayerTo = Server.FindPlayer(autokill["PlayerT"])
        if PlayerFrom is None or PlayerTo is None:
            timer.Kill()
            return
        DataStore.Remove("tpfriendpending", PlayerFrom.SteamID)
        DataStore.Add("tpfriendcooldown", PlayerFrom.SteamID, 7)
        DataStore.Remove("tpfriendpending2", PlayerTo.SteamID)
        PlayerFrom.MessageFrom(systemname, "Teleport request timed out.")
        PlayerTo.MessageFrom(systemname, "Teleport request timed out.")
        timer.Kill()

    def TpDelay(self, timer):
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Settings", "sysname")
        tpdelaytp = timer.Args
        PlayerFrom = Server.FindPlayer(tpdelaytp["PlayerR"])
        PlayerTo = Server.FindPlayer(tpdelaytp["PlayerT"])
        if PlayerFrom is None or PlayerTo is None:
            timer.Kill()
            return
        DataStore.Remove("tpfriendpending", PlayerFrom.SteamID)
        DataStore.Remove("tpfriendpending2", PlayerTo.SteamID)
        PlayerFrom.GroundTeleport(PlayerTo.Location)
        PlayerFrom.Teleport(PlayerTo.Location)
        PlayerFrom.MessageFrom(systemname, "Teleported!")
        PlayerTo.MessageFrom(systemname, str(PlayerFrom.Name) + " teleported to you!")
        timer.Kill()

    """
        Methods
    """
    def TpFriendConfig(self):
        if not Plugin.IniExists("TpFriendConfig"):
            loc = Plugin.CreateIni("TpFriendConfig")
            loc.Save()
        return Plugin.GetIni("TpFriendConfig")

    # method by Illuminati
    def CheckV(self, Player, args):
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Settings", "sysname")
        p = Server.FindPlayer(String.Join(" ", args))
        if p is not None:
            return p

        count = 0
        for pl in Server.ActivePlayers:
            for namePart in args:
                if namePart in pl.Name:
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, String.Format("Couldn't find {0}!", String.Join(" ", args)))
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, String.Format("Found {0} player with similar name. Use more correct name!"))
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
            elif len(args) == 1:
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                playertor = self.CheckV(Player, args)
                if playertor is None:
                    # Player.Message("Player " + playertor + " not found!")
                    return
                if playertor == Player:
                    Player.MessageFrom(systemname, "Cannot teleport to yourself!")
                    return
                maxuses = config.GetSetting("Settings", "Maxuses")
                cd = config.GetSetting("Settings", "cooldown")
                cooldown = int(cd)
                # checkn = config.GetSetting("Settings", "safetpcheck")
                stuff = config.GetSetting("Settings", "timeoutr")
                time = DataStore.Get("tpfriendcooldown", Player.SteamID)
                systick = System.Environment.TickCount
                usedtp = DataStore.Get("tpfriendusedtp", Player.SteamID)
                pending = DataStore.Get("tpfriendpending2", playertor.SteamID)
                if pending is not None:
                    Player.MessageFrom(systemname, "This player is already pending a request.")
                    Player.MessageFrom(systemname, "Try again later, or tell the player to deny his current request.")

                if time is None or (systick - time) < 0 or math.isnan(systick - time):
                    DataStore.Add("tpfriendcooldown", Player.SteamID, 7)

                calc = systick - time
                if calc >= cooldown or time == 7:
                    if usedtp is None:
                        DataStore.Add("tpfriendusedtp", Player.SteamID, 0)
                        usedtp = 0
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
                    autokill["PlayerR"] = Player.Name
                    autokill["PlayerT"] = playertor.Name
                    launchcalc = int(stuff * 1000)
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
                    # checkn = config.GetSetting("Settings", "safetpcheck")
                    usedtp = DataStore.Get("tpfriendusedtp", pending)
                    maxtpnumber = int(maxuses)
                    playertpuse = int(usedtp)
                    cd = config.GetSetting("Settings", "cooldown")
                    # cooldown = int(cd)
                    tpdelay = int(config.GetSetting("Settings", "tpdelay"))
                    if maxtpnumber > 0:
                        uses = playertpuse + 1
                        DataStore.Add("tpfriendusedtp", pending, uses)
                        playerfromm.MessageFrom(systemname, "Teleport requests used " + str(uses) + " / " + str(maxtpnumber))

                    else:
                        playerfromm.MessageFrom(systemname, "You have unlimited requests remaining!")

                    playerfromm.MessageFrom(systemname, "Teleported!")
                    DataStore.Add("tpfriendautoban", playerfromm.SteamID, "using")

                    DataStore.Remove("tpfriendpending", playerfromm.SteamID)
                    DataStore.Remove("tpfriendpending2", Player.SteamID)
                    Player.MessageFrom(systemname, "Teleport Request Accepted!")
                    if tpdelay > 0:
                        tpdelaytp = Plugin.CreateDict()
                        tpdelaytp["PlayerR"] = playerfromm.Name
                        tpdelaytp["PlayerT"] = Player.Name
                        launchcalc = tpdelay * 1000
                        Plugin.CreateParallelTimer("TpDelay", launchcalc, tpdelaytp).Start()
                        playerfromm.MessageFrom(systemname, "Teleporting you in: " + str(tpdelay) + " second(s)")
                    else:
                        playerfromm.GroundTeleport(Player.Location)
                        playerfromm.Teleport(Player.Location)
                        playerfromm.MessageFrom(systemname, "Teleported!")
                        Player.MessageFrom(systemname, str(playerfromm.Name) + " teleported to you!")

                else:
                    Player.MessageFrom(systemname, "Player isn't online!")

            else:
                Player.MessageFrom(systemname, "Your request timed out, or you don't have any.")
        elif cmd.cmd == "tpdeny":
            pending = DataStore.Get("tpfriendpending2", Player.SteamID)
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            if pending is not None:
                playerfromm = Server.Find(pending)
                if playerfromm is not None:
                    DataStore.Remove("tpfriendpending", pending)
                    DataStore.Add("tpfriendcooldown", pending, 7)
                    DataStore.Remove("tpfriendpending2", Player.SteamID)
                    Player.MessageFrom(systemname, "Request denied!")
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
            if Player.Moderator:
                DataStore.Add("tpfriendcooldown", Player.SteamID, 7)
                Player.Message("Time for you, Reset!")
            else:
                Player.Message("You aren't an admin!")