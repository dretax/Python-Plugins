__author__ = 'DreTaX'
__version__ = '1.1'

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
        Server.Broadcast("I guess this timer is running, isnt it?")
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Settings", "sysname")
        autokill = timer.Args
        PlayerFrom = Server.FindPlayer(autokill["PlayerR"])
        PlayerTo = Server.FindPlayer(autokill["PlayerT"])
        if PlayerFrom is None or PlayerTo is None:
            Plugin.KillParallelTimer("AutoKill")
            Server.Broadcast("Did it run fully?!!")
            return
        DataStore.Remove("tpfriendpending", PlayerFrom.SteamID)
        DataStore.Add("tpfriendcooldown", PlayerFrom.SteamID, 7)
        DataStore.Remove("tpfriendpending2", PlayerTo.SteamID)
        PlayerFrom.MessageFrom(systemname, "Teleport request timed out.")
        PlayerTo.MessageFrom(systemname, "Teleport request timed out.")
        timer.Kill()

    """
        Methods
    """

    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None

    # Method provided by Spoock. Converted to Python by DreTaX
    """def CheckV(self, Player, args):
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Settings", "sysname")
        Nickname = ""
        for i in xrange(-1, len(args)):
            i += 1
            Nickname = Nickname + args[i] + " "
            Nickname = Nickname.Substring(0, len(Nickname) - 1)
            target = Server.FindPlayer(Nickname)
            if target is not None:
                return target

            else:
                cc = 0
                found = None
                for all in Server.ActivePlayers:
                    name = all.Name.lower()
                    check = args[0].lower()
                    if check in name:
                        found = all.Name
                        cc += 1

                if cc == 1:
                    target = Server.FindPlayer(found)
                    return target
                elif cc > 1:
                    Player.MessageFrom(systemname, "Found " + cc + " players with similar names. Use more correct name !")
                    return None
                elif cc == 0:
                    Player.MessageFrom(systemname, "Player " + Nickname + " not found")
                    return None"""

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
                    #tpdelay = config.GetSetting("Settings", "tpdelay")
                    #tpdelayy = int(tpdelay)
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
                    playerfromm.GroundTeleport(Player.Location)
                    playerfromm.Teleport(Player.Location)

                else:
                    Player.MessageFrom(systemname, "Player isn't online!")

            else:
                Player.MessageFrom(systemname, "Your request timed out, or you don't have any.")
            # Uncommenting the delay, adding It later only.
            """if tpdelayy > 0:
            playerfromm.MessageFrom(systemname, "Teleporting you in: " + tpdelayy + " second(s)");
            var jobParams = [];
            jobParams.push(String(Player.SteamID));
            jobParams.push(String(playerfromm.SteamID));
            BZTJ.addJob('tpfirst', tpdelay, iJSON.stringify(jobParams));"""  # else
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