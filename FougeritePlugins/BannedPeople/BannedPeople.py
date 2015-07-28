__author__ = 'DreTaX'
__version__ = '1.6.5'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

"""
    Class
"""


class BannedPeople:
    """
        Methods
    """

    sysname = None
    bannedreason = None

    def On_PluginInit(self):
        ini = self.BannedPeopleConfig()
        self.sysname = ini.GetSetting("Main", "Name")
        self.bannedreason = ini.GetSetting("Main", "BannedDrop")
        Util.ConsoleLog("BannedPeople by " + __author__ + " Version: " + __version__ + " loaded.", False)


    def BannedPeopleConfig(self):
        if not Plugin.IniExists("BannedPeopleConfig"):
            ini = Plugin.CreateIni("BannedPeopleConfig")
            ini.AddSetting("Main", "Name", "[Equinox-BanSystem]")
            ini.AddSetting("Main", "BannedDrop", "You were banned from this server.")
            ini.Save()
        return Plugin.GetIni("BannedPeopleConfig")

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
            if Player is not None:
                Player.MessageFrom(self.sysname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            if Player is not None:
                Player.MessageFrom(self.sysname, "Found [color#FF0000]" + str(count) +
                                   "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def On_Console(self, Player, ConsoleEvent):
        if Player is not None and not Player.Admin:
            ConsoleEvent.ReplyWith("You aren't an admin!")
            return
        if ConsoleEvent.Class == "fougerite":
            if "unban" in ConsoleEvent.Function:
                if len(ConsoleEvent.Args) == 0:
                    ConsoleEvent.ReplyWith("Specify a name!")
                    return
                name = str.join(' ', ConsoleEvent.Args)
                ipmatch = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", name))
                if name.isnumeric() and name.startswith("7656119"):
                    b = Server.UnbanByID(name)
                    if b:
                        ConsoleEvent.ReplyWith("ID " + name + " unbanned!")
                    else:
                        ConsoleEvent.ReplyWith("Couldn't find " + name)
                elif ipmatch:
                    b = Server.UnbanByIP(name)
                    if b:
                        ConsoleEvent.ReplyWith("IP " + name + " unbanned!")
                    else:
                        ConsoleEvent.ReplyWith("Couldn't find " + name)
                else:
                    b = Server.UnbanByName(name)
                    if not b:
                        ConsoleEvent.ReplyWith("Target: " + name + " isn't in the database, or you misspelled It!")
                    else:
                        ConsoleEvent.ReplyWith("Player " + name + " unbanned!")
            elif "ban" in ConsoleEvent.Function:
                if len(ConsoleEvent.Args) == 0:
                    ConsoleEvent.ReplyWith("Specify a name!")
                    return
                name = str.join(' ', ConsoleEvent.Args)
                ipmatch = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", name))
                if name.isnumeric() and name.startswith("7656119"):
                    if Server.GetRustPPAPI().IsAdmin(long(name)):
                        ConsoleEvent.ReplyWith("This owner of the ID is an Admin/Moderator.")
                        ConsoleEvent.ReplyWith("You need to remove him from the list first.")
                        return
                    b = Server.BanPlayerID(name, "Console ban")
                    if b:
                        ConsoleEvent.ReplyWith("ID " + name + " banned!")
                    else:
                        ConsoleEvent.ReplyWith("ID " + name + " is already banned.")
                elif ipmatch:
                    b = Server.BanPlayerIP(name, "Console ban")
                    if b:
                        ConsoleEvent.ReplyWith("IP " + name + " banned!")
                    else:
                        ConsoleEvent.ReplyWith("IP " + name + " is already banned.")
                else:
                    pl = self.CheckV(None, name)
                    if pl is None:
                        ConsoleEvent.ReplyWith("Target: " + name + " isn't online!")
                    else:
                        if pl.Admin or pl.Moderator:
                            ConsoleEvent.ReplyWith("You cannot ban admins!")
                            return
                        Server.BanPlayer(pl, "Console", self.bannedreason)

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def On_Command(self, Player, cmd, args):
        if cmd == "banip":
            if Player.Admin or Player.Moderator:
                if len(args) > 0:
                    playerr = self.CheckV(Player, args)
                    if playerr is None:
                        return
                    else:
                        if playerr.Admin or playerr.Moderator:
                            Player.MessageFrom(self.sysname, "You cannot ban admins!")
                            return

                        id = playerr.SteamID
                        ip = playerr.IP
                        name = playerr.Name
                        loc = str(playerr.Location)

                        Player.Message("You banned " + name)
                        Player.Message("Player's IP: " + ip)
                        Player.Message("Player's ID: " + id)
                        Player.Message("Player's Location: " + loc)

                        checking = DataStore.Get("BanIp", Player.SteamID)
                        if checking == "true":
                            Server.BanPlayer(playerr, "Unknown", self.bannedreason)
                        elif checking == "false" or checking is None:
                            Server.BanPlayer(playerr, Player.Name, self.bannedreason)
                else:
                    Player.MessageFrom(self.sysname, "Specify a Name!")
            else:
                Player.MessageFrom(self.sysname, "You aren't an admin!")
        elif cmd == "unbanip":
            if Player.Admin or Player.Moderator:
                if len(args) > 0:
                    name = self.argsToText(args)
                    b = Server.UnbanByName(name, Player.Name)
                    if not b:
                        Player.Message("Target: " + name + " isn't in the database, or you misspelled It!")
                    else:
                        Player.MessageFrom(self.sysname, "Player " + name + " unbanned!")
                else:
                    Player.MessageFrom(self.sysname, "Specify a Name!")
        elif cmd == "banhidename":
            if Player.Admin or Player.Moderator:
                if not DataStore.ContainsKey("BanIp", Player.SteamID):
                    DataStore.Add("BanIp", Player.SteamID, "true")
                    Player.MessageFrom(self.sysname, "Now hiding your name!")
                else:
                    DataStore.Remove("BanIp", Player.SteamID)
                    Player.MessageFrom(self.sysname, "Now displaying your name!")
        elif cmd == "munbanip":
            if Player.Admin or Player.Moderator:
                if len(args) == 0 or len(args) > 1:
                    Player.MessageFrom(self.sysname, "Usage: /munbanip IDorIP")
                    return
                v = str(args[0])
                ipmatch = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", v))
                if v.isnumeric() and v.startswith("7656119"):
                    b = Server.UnbanByID(v)
                    if b:
                        Player.MessageFrom(self.sysname, "Unbanned.")
                    else:
                        Player.MessageFrom(self.sysname, "Couldn't find " + v)
                elif ipmatch:
                    b = Server.UnbanByIP(v)
                    if b:
                        Player.MessageFrom(self.sysname, "Unbanned.")
                    else:
                        Player.MessageFrom(self.sysname, "Couldn't find " + v)
                else:
                    Player.MessageFrom(self.sysname, "Invalid value.")
        elif cmd == "offban":
            if len(args) == 0:
                Player.MessageFrom(self.sysname, "Specify an ID or IP")
            elif len(args) == 1:
                if Player.Admin or Player.Moderator:
                    id = str(args[0]).strip(' ')
                    if "." in id:
                        Server.BanPlayerIP(id, "IP OfflineBanned By " + Player.Name + " | " + Player.SteamID)
                        Player.MessageFrom(self.sysname, "Player IP (" + id + ") was banned.")
                    else:
                        if Server.GetRustPPAPI().IsAdmin(long(id)):
                            Player.MessageFrom(self.sysname, "This owner of the ID is an Admin/Moderator.")
                            Player.MessageFrom(self.sysname, "You need to remove him from the list first.")
                            return
                        Server.BanPlayerID(id, "ID OfflineBanned By " + Player.Name + " | " + Player.SteamID)
                        Player.MessageFrom(self.sysname, "Player ID (" + id + ") was banned.")
        elif cmd == "drop":
            if Player.Admin or Player.Moderator:
                p = self.CheckV(Player, args)
                if p is not None:
                    p.TeleportTo(float(p.X), float(p.Y) + float(30), float(p.Z), False)
                    Player.Message(p.Name + " was dropped.")

    def On_PlayerConnected(self, Player):
        ip = Player.IP
        if ip.startswith("46.16.") or ip.startswith("199.188.") or ip.startswith("198.144."):
            Player.Disconnect()