__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
from System import *
import math

"""
    Class
"""


class TpFriend:
    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None

    # Method provided by Spoock. Converted to Python by DreTaX
    def CheckV(self, Player, args):
        ini = self.TpFriendConfig()
        systemname = ini.GetSetting("Main", "Name")
        Nickname = ""
        for i in xrange(-1, len(args)):
            i += 1
            Nickname += args[i] + " "
            Nickname = Nickname.Substring(0, len(Nickname) - 1)
            target = self.GetPlayerName(Nickname)
            if target != None:
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
                    target = self.GetPlayerName(found)
                    return target
                elif cc > 1:
                    Player.MessageFrom(systemname, "Found " + cc + " players with similar names. Use more correct name !")
                    return None
                elif cc == 0:
                    Player.MessageFrom(systemname, "Player " + Nickname + " not found")
                    return None

    def TpFriendConfig(self):
        if not Plugin.IniExists("TpFriendConfig"):
            loc = Plugin.CreateIni("TpFriendConfig")
            loc.Save()
        return Plugin.GetIni("TpFriendConfig")

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "tpa":
            if len(args) == 0:
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                Player.MessageFrom(systemname, "Teleport Usage:")
                Player.MessageFrom(systemname, "This will teleport you to another player.")
                Player.MessageFrom(systemname, "\"/tpa [PlayerName]\" to request a teleport.")
                Player.MessageFrom(systemname, "\"/tpaccept\" to accept a requested teleport.")
                Player.MessageFrom(systemname, "\"/tpdeny\" to deny a request.")
                Player.MessageFrom(systemname, "\"/tpcount\" to see how many requests you have remaining.")
            elif len(args) == 1:
                config = self.TpFriendConfig()
                systemname = config.GetSetting("Settings", "sysname")
                playertor = self.CheckV(Player, args)
                if playertor == None:
                    # Player.Message("Player " + playertor + " not found!")
                    return
                if playertor == Player:
                    Player.MessageFrom(systemname, "Cannot teleport to yourself!")
                    return
                maxuses = config.GetSetting("Settings", "Maxuses")
                cd = config.GetSetting("Settings", "cooldown")
                cooldown = int(cd)
                # checkn = config.GetSetting("Settings", "safetpcheck")
                #stuff = config.GetSetting("Settings", "timeoutr")
                time = DataStore.Get("tpfriendcooldown", Player.SteamID)
                usedtp = DataStore.Get("tpfriendusedtp", Player.SteamID)
                calc = System.Environment.TickCount - time
                if time == None or calc < 0 or math.isnan(calc):
                    time = DataStore.Add("tpfriendcooldown", Player.SteamID, System.Environment.TickCount)
                if calc >= cooldown or time == 7:
                    if usedtp == None:
                        DataStore.Add("tpfriendusedtp", Player.SteamID, 0)
                        usedtp = 0
                    maxtpnumber = int(maxuses)
                    playertpuse = int(usedtp)
                    if maxtpnumber > 0:
                        if maxtpnumber >= playertpuse:
                            Player.MessageFrom(systemname, "Reached max number of teleport requests!")
                            return

                    DataStore.Add("tpfriendcooldown", Player.SteamID, System.Environment.TickCount)
                    playertor.MessageFrom(systemname,
                                          "Teleport request from " + Player.Name + " to accept write /tpaccept")
                    Player.MessageFrom(systemname, "Teleport request sent to " + playertor.Name)
                    DataStore.Add("tpfriendpending", Player.SteamID, playertor.SteamID)
                    DataStore.Add("tpfriendpending2", playertor.SteamID, Player.SteamID)
                else:
                    Player.MessageFrom(systemname, "You have to wait before teleporting again!")
                    next2 = (calc / 1000) / 60
                    def2 = (cooldown / 1000) / 60
                    done = round(next2, 2)
                    done2 = round(def2, 2)
                    Player.MessageFrom(systemname, "Time Remaining: " + done + "/" + done2)
        elif cmd.cmd == "tpaccept":
            pending = DataStore.Get("tpfriendpending2", Player.SteamID)
            config = self.TpFriendConfig()
            systemname = config.GetSetting("Settings", "sysname")
            if pending != None:
                playerfromm = Server.Find(pending)
                if playerfromm != None:
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
                    playerfromm.SafeTeleportTo(Player.Location)
                    DataStore.Add("tpfriendautoban", playerfromm.SteamID, "using")

                    DataStore.Add("tpfriendpending", playerfromm.SteamID, None)
                    DataStore.Add("tpfriendpending2", Player.SteamID, None)
                    Player.MessageFrom(systemname, "Teleport Request Accepted!")

                else:
                    Player.MessageFrom(systemname, "Player isn't online!")

            else:
                Player.MessageFrom(systemname, "Your request was timed out, or you don't have any.")
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
            if pending != None:
                playerfromm = Server.Find(pending)
                if playerfromm != None:
                    DataStore.Add("tpfriendpending", pending, None)
                    DataStore.Add("tpfriendcooldown", pending, 7)
                    DataStore.Add("tpfriendpending2", Player.SteamID, None)
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
                if uses == None:
                    uses = 0

                Player.MessageFrom(systemname, "Teleport requests used " + str(uses) + " / " + str(maxuses))
            else:
                Player.MessageFrom(systemname, "You have unlimited requests remaining!")
        elif cmd.cmd == "tpresettime":
            if Player.Admin:
                DataStore.Add("tpfriendcooldown", Player.SteamID, 7)
                Player.Message("Time for you, Reset!")