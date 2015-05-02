__author__ = 'DreTaX'
__version__ = '1.6.2'

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

    red = "[color #FF0000]"
    green = "[color #009900]"
    white = "[color #FFFFFF]"


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
            ini = self.BannedPeopleIni()
            name = str.join(' ', ConsoleEvent.Args)
            if "unban" in ConsoleEvent.Function:
                if len(ConsoleEvent.Args) == 0:
                    ConsoleEvent.ReplyWith("Specify a name!")
                    return
                ipmatch = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", name))
                if name.isnumeric() and name.startswith("7656119"):
                    if ini.GetSetting("Ids", name) is not None:
                        ini.DeleteSetting("Ids", name)
                        ini.Save()
                        ConsoleEvent.ReplyWith("ID " + name + " unbanned!")
                    else:
                        ConsoleEvent.ReplyWith("Couldn't find " + name)
                elif ipmatch:
                    if ini.GetSetting("Ips", name) is not None:
                        ini.DeleteSetting("Ips", name)
                        ini.Save()
                        ConsoleEvent.ReplyWith("IP " + name + " unbanned!")
                    else:
                        ConsoleEvent.ReplyWith("Couldn't find " + name)
                else:
                    id = self.GetPlayerUnBannedID(name)
                    ip = self.GetPlayerUnBannedIP(name)
                    if id is None:
                        ConsoleEvent.ReplyWith("Target: " + name + " isn't in the database, or you misspelled It!")
                    else:
                        name = id
                        iprq = ini.GetSetting("NameIps", ip)
                        idrq = ini.GetSetting("NameIds", id)
                        ini.DeleteSetting("Ips", iprq)
                        ini.DeleteSetting("Ids", idrq)
                        ini.DeleteSetting("NameIps", name)
                        ini.DeleteSetting("NameIds", name)
                        ini.Save()
                        for pl in Server.Players:
                            if pl.Admin or self.isMod(pl.SteamID):
                                pl.MessageFrom(self.sysname, self.red + name + self.white + " was unbanned by: " +
                                               self.green + "Console!")
                    ConsoleEvent.ReplyWith("Player " + name + " unbanned!")
            elif "ban" in ConsoleEvent.Function:
                if len(ConsoleEvent.Args) == 0:
                    ConsoleEvent.ReplyWith("Specify a name!")
                    return
                ipmatch = bool(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", name))
                if name.isnumeric() and name.startswith("7656119"):
                    if not ini.GetSetting("Ids", name) is not None:
                        ini.AddSetting("Ids", name)
                        ini.Save()
                        ConsoleEvent.ReplyWith("ID " + name + " banned!")
                    else:
                        ConsoleEvent.ReplyWith("ID " + name + " is already banned.")
                elif ipmatch:
                    if not ini.GetSetting("Ips", name) is not None:
                        ini.AddSetting("Ips", name)
                        ini.Save()
                        ConsoleEvent.ReplyWith("IP " + name + " banned!")
                    else:
                        ConsoleEvent.ReplyWith("IP " + name + " is already banned.")
                else:
                    pl = self.CheckV(None, name)
                    if pl is None:
                        ConsoleEvent.ReplyWith("Target: " + name + " isn't online!")
                    else:
                        if pl.Admin or self.isMod(pl.SteamID):
                            ConsoleEvent.ReplyWith("You cannot ban admins!")
                            return

                        id = pl.SteamID
                        ip = pl.IP
                        name = pl.Name
                        for pl in Server.Players:
                            if pl.Admin or self.isMod(pl.SteamID):
                                pl.MessageFrom(self.sysname, "Message to Admins: " + self.red + name + self.white +
                                               " was banned by: Console")

                        ini.AddSetting("Ips", ip, "1")
                        ini.AddSetting("Ids", id, "1")
                        ini.AddSetting("NameIps", name, ip)
                        ini.AddSetting("NameIds", name, id)
                        ini.AddSetting("AdminWhoBanned", name, "Console")
                        ini.Save()
                        Server.Broadcast(name + " was banned by console.")
                        ConsoleEvent.ReplyWith("Player " + name + " banned!")
                        pl.Disconnect()

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def BannedPeopleIni(self):
        if not Plugin.IniExists("BannedPeople"):
            ini = Plugin.CreateIni("BannedPeople")
            ini.Save()
        return Plugin.GetIni("BannedPeople")

    def GetPlayerUnBannedID(self, name):
        namee = name.lower()
        ini = self.BannedPeopleIni()
        checkdist = ini.EnumSection("NameIds")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIds", pl)
            lower = pl.lower()
            if nameid is None:
                return
            if lower == namee:
                return pl
        return None


    def GetPlayerUnBannedIP(self, name):
        namee = name.lower()
        ini = self.BannedPeopleIni()
        checkdist = ini.EnumSection("NameIps")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIps", pl)
            lower = pl.lower()
            if nameid is None:
                return
            if lower == namee:
                return pl
        return None

    def On_Command(self, Player, cmd, args):
        ini = self.BannedPeopleIni()
        if cmd == "banip":
            if Player.Admin or self.isMod(Player.SteamID):
                if len(args) > 0:
                    playerr = self.CheckV(Player, args)
                    if playerr is None:
                        return

                    else:
                        if playerr.Admin or self.isMod(playerr.SteamID):
                            Player.MessageFrom(self.sysname, "You cannot ban admins!")
                            return

                        id = playerr.SteamID
                        ip = playerr.IP
                        name = playerr.Name
                        loc = str(playerr.Location)
                        for pl in Server.Players:
                            if pl.Admin or self.isMod(pl.SteamID):
                                pl.MessageFrom(self.sysname, "Message to Admins: " + self.red + name + self.white +
                                               " was banned by: " + Player.Name)

                        ini.AddSetting("Ips", ip, "1")
                        ini.AddSetting("Ids", id, "1")
                        ini.AddSetting("NameIps", name, ip)
                        ini.AddSetting("NameIds", name, id)
                        ini.AddSetting("AdminWhoBanned", name, Player.Name)
                        ini.Save()
                        Player.Message("You banned " + name)
                        Player.Message("Player's IP: " + ip)
                        Player.Message("Player's ID: " + id)
                        Player.Message("Player's Location: " + loc)
                        playerr.Message("You were banned from the server")
                        checking = DataStore.Get("BanIp", Player.SteamID)
                        if checking == "true":
                            playerr.MessageFrom(self.sysname, self.red + "Admin, who banned you: UNKNOWN - Admin in Casing mode")

                        elif checking == "false" or checking is None:
                            playerr.MessageFrom(self.sysname, self.red + "Admin, who banned you: " + Player.Name)

                        playerr.Disconnect()
                else:
                    Player.MessageFrom(self.sysname, "Specify a Name!")
            else:
                Player.MessageFrom(self.sysname, "You aren't an admin!")

        elif cmd == "unbanip":
            if Player.Admin or self.isMod(Player.SteamID):
                if len(args) > 0:
                    name = self.argsToText(args)
                    id = self.GetPlayerUnBannedID(name)
                    ip = self.GetPlayerUnBannedIP(name)
                    if id is None:
                        Player.Message("Target: " + name + " isn't in the database, or you misspelled It!")
                    else:
                        name = id
                        iprq = ini.GetSetting("NameIps", ip)
                        idrq = ini.GetSetting("NameIds", id)
                        ini.DeleteSetting("Ips", iprq)
                        ini.DeleteSetting("Ids", idrq)
                        ini.DeleteSetting("NameIps", name)
                        ini.DeleteSetting("NameIds", name)
                        ini.Save()
                        for pl in Server.Players:
                            if pl.Admin or self.isMod(pl.SteamID):
                                pl.MessageFrom(self.sysname, self.red + name + self.white + " was unbanned by: "
                                               + self.green + Player.Name)

                        Player.MessageFrom(self.sysname, "Player " + name + " unbanned!")
                else:
                    Player.MessageFrom(self.sysname, "Specify a Name!")
        elif cmd == "banhidename":
            if Player.Admin or self.isMod(Player.SteamID):
                if not DataStore.ContainsKey("BanIp", Player.SteamID):
                    DataStore.Add("BanIp", Player.SteamID, "true")
                    Player.MessageFrom(self.sysname, "Now hiding your name!")
                else:
                    DataStore.Remove("BanIp", Player.SteamID)
                    Player.MessageFrom(self.sysname, "Now displaying your name!")
        elif cmd == "bans":
            if Player.Admin or self.isMod(Player.SteamID):
                checkdist = ini.EnumSection("NameIds")
                Player.MessageFrom(self.sysname, self.red + "Current Bans:")
                for pl in checkdist:
                    Player.MessageFrom(self.sysname, str(pl))
        elif cmd == "munbanip":
            if Player.Admin or self.isMod(Player.SteamID):
                if len(args) == 0 or len(args) > 1:
                    Player.MessageFrom(self.sysname, "Usage: /munbanip IDorIP")
                    return
                v = str(args[0])
                if ini.GetSetting("Ips", v) is not None and ini.GetSetting("Ips", v):
                    ini.DeleteSetting("Ips", v)
                    ini.Save()
                    Player.MessageFrom(self.sysname, "Unbanned.")
                    return
                if ini.GetSetting("Ids", v) is not None and ini.GetSetting("Ids", v):
                    ini.DeleteSetting("Ids", v)
                    ini.Save()
                    Player.MessageFrom(self.sysname, "Unbanned.")
                    return
                Player.MessageFrom(self.sysname, "Couldn't find " + v)
        elif cmd == "offban":
            if len(args) == 0:
                Player.MessageFrom(self.sysname, "Specify an ID or IP")
            elif len(args) == 1:
                if Player.Admin or self.isMod(Player.SteamID):
                    id = str(args[0]).strip(' ')
                    if self.isMod(id):
                        Player.MessageFrom(self.sysname, "This owner of the ID is a moderator.")
                        Player.MessageFrom(self.sysname, "You need to remove him from the list first.")
                        return
                    if "." in id:
                        ini.AddSetting("Ips", id, "IP OfflineBanned By " + Player.Name + " | " + Player.SteamID)
                        Player.MessageFrom(self.sysname, "Player IP (" + id + ") was banned.")
                    else:
                        ini.AddSetting("Ids", id, "ID OfflineBanned By " + Player.Name + " | " + Player.SteamID)
                        Player.MessageFrom(self.sysname, "Player ID (" + id + ") was banned.")
                    ini.Save()


    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        ip = Player.IP
        ini = self.BannedPeopleIni()
        if ini.GetSetting("Ips", ip) is not None and ini.GetSetting("Ips", ip):
            if ini.GetSetting("Ids", id) is None:
                ini.AddSetting("Ids", id, Player.Name + " Connected from a banned IP: " + ip)
                ini.AddSetting("NameIps", Player.Name, ip)
                ini.AddSetting("NameIds", Player.Name, id)
                ini.Save()
            Player.MessageFrom(self.sysname, self.bannedreason)
            Player.Disconnect()
            return
        if ini.GetSetting("Ids", id) is not None and ini.GetSetting("Ids", id):
            if ini.GetSetting("Ips", ip) is None:
                ini.AddSetting("Ips", ip, Player.Name + " Connected from a banned ID " + id)
                ini.AddSetting("NameIps", Player.Name, ip)
                ini.AddSetting("NameIds", Player.Name, id)
                ini.Save()
            Player.MessageFrom(self.sysname, self.bannedreason)
            Player.Disconnect()