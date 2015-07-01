__author__ = 'DreTaX'
__version__ = '1.3'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton

"""
    Class
"""


class BannedPeople:
    """
        Methods
    """
    sysname = None
    bannedreason = None

    def BannedPeopleConfig(self):
        if not Plugin.IniExists("BannedPeopleConfig"):
            ini = Plugin.CreateIni("BannedPeopleConfig")
            ini.AddSetting("Main", "Name", "[Equinox-BanSystem]")
            ini.AddSetting("Main", "BannedDrop", "You were banned from this server.")
            ini.Save()
        return Plugin.GetIni("BannedPeopleConfig")

    def BannedPeopleIni(self):
        if not Plugin.IniExists("BannedPeople"):
            ini = Plugin.CreateIni("BannedPeople")
            ini.Save()
        return Plugin.GetIni("BannedPeople")

    def On_PluginInit(self):
        ini = self.BannedPeopleConfig()
        self.sysname = ini.GetSetting("Main", "Name")
        self.bannedreason = ini.GetSetting("Main", "BannedDrop")
        Commands.Register("banip")\
            .setCallback("banip")\
            .setDescription("Allow admin to ban an IP")\
            .setUsage("/banip IP")
        Commands.Register("unbanip")\
            .setCallback("unbanip")\
            .setDescription("Allow admin to unban an IP")\
            .setUsage("/unbanip IP")
        Commands.Register("banhidename")\
            .setCallback("banhidename")\
            .setDescription("Hides name of player being banned.")\
            .setUsage("/banhidename true/false")

    def argsToText(self, args):
        text = str.Join(" ", args)
        return text

    def GetPlayerUnBannedID(self, namee):
        name = namee.lower()
        ini = self.BannedPeopleIni()
        checkdist = ini.EnumSection("NameIds")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIds", pl)
            lower = pl.lower()
            if nameid and lower == name:
                return pl
        return None

    def GetPlayerUnBannedIP(self, namee):
        name = namee.lower()
        ini = self.BannedPeopleIni()
        checkdist = ini.EnumSection("NameIps")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIps", pl)
            lower = pl.lower()
            if nameid and lower == name:
                return pl
        return None

    """
        CheckV Assistants
    """

    def GetPlayerName(self, name, Mode=1):
        Name = name.lower()
        if Mode == 1:
            for pl in Server.ActivePlayers:
                if pl.Name.lower() == Name:
                    return pl
        elif Mode == 2:
            for pl in Server.OfflinePlayers.Values:
                if pl.Name.lower() == Name:
                    return pl
        else:
            for pl in Server.ActivePlayers:
                if pl.Name.lower() == Name:
                    return pl
            for pl in Server.OfflinePlayers.Values:
                if pl.Name.lower() == Name:
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
        V5.0
    """

    def CheckV(self, args, Player, Mode=1):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.Join(" ", args), Mode)
            if p is not None:
                return p
            if Mode == 1:
                for pl in Server.ActivePlayers:
                    for namePart in args:
                        if namePart.lower() in pl.Name.lower():
                            p = pl
                            count += 1
            elif Mode == 2:
                for offlineplayer in Server.OfflinePlayers.Values:
                    for namePart in args:
                        if namePart.lower() in offlineplayer.Name.lower():
                            p = offlineplayer
                            count += 1
            else:
                for pl in Server.ActivePlayers:
                    for namePart in args:
                        if namePart.lower() in pl.Name.lower():
                            p = pl
                            count += 1
                for offlineplayer in Server.OfflinePlayers.Values:
                    for namePart in args:
                        if namePart.lower() in offlineplayer.Name.lower():
                            p = offlineplayer
                            count += 1
        else:
            p = self.GetPlayerName(str(args), Mode)
            if p is not None:
                return p
            if Mode == 1:
                for pl in Server.ActivePlayers:
                    if str(args).lower() in pl.Name.lower():
                        p = pl
                        count += 1
            elif Mode == 2:
                for offlineplayer in Server.OfflinePlayers.Values:
                    if str(args).lower() in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
            else:
                for pl in Server.ActivePlayers:
                    if str(args).lower() in pl.Name.lower():
                        p = pl
                        count += 1
                for offlineplayer in Server.OfflinePlayers.Values:
                    if str(args).lower() in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
        if count == 0:
            Player.MessageFrom(self.sysname, "Couldn't find " + str.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(self.sysname, "Found " + str(count) + " player with similar name. Use more correct name!")
            return None

    def banip(self, args, Player):
        if Player.Admin:
            if len(args) > 0:
                playerr = self.CheckV(args, Player, 3)
                if playerr is None:
                    return

                else:
                    ini = self.BannedPeopleIni()
                    if playerr.Admin and Player.Moderator:
                        Player.MessageFrom(self.sysname, "You cannot ban admins!")
                        return

                    id = playerr.SteamID
                    ip = playerr.IP
                    name = playerr.Name
                    for pl in Server.ActivePlayers:
                        if pl.Admin: pl.MessageFrom(self.sysname, "Message to Admins: " + name + " was banned by: " + Player.Name)

                    ini.AddSetting("Ips", ip, "1")
                    ini.AddSetting("Ids", id, "1")
                    ini.AddSetting("NameIps", name, ip)
                    ini.AddSetting("NameIds", name, id)
                    ini.AddSetting("AdminWhoBanned", name, Player.Name)
                    ini.Save()
                    Player.Message("You banned " + name)
                    Player.Message("Player's IP: " + ip)
                    Player.Message("Player's ID: " + id)
                    if not "offlineplayer" in str(playerr).lower():
                        playerr.Message("You were banned from the server")
                        checking = DataStore.Get("BanIp", Player.SteamID)
                        if checking == "true":
                            playerr.MessageFrom(self.sysname, "Admin, who banned you: UNKNOWN - Admin in Casing mode")

                        elif checking == "false" or checking == None:
                            playerr.MessageFrom(self.sysname, "Admin, who banned you: " + Player.Name)
                        playerr.Kick(self.bannedreason)
            else:
                Player.MessageFrom(self.sysname, "Specify a Name!")

    def unbanip(self, args, Player):
        if Player.Admin:
            if len(args) > 0:
                name = self.argsToText(args)
                id = self.GetPlayerUnBannedID(name)
                ip = self.GetPlayerUnBannedIP(name)
                if id is None:
                    Player.Message("Target: " + name + " isn't in the database, or you misspelled It!")

                else:
                    ini = self.BannedPeopleIni()
                    name = id
                    iprq = ini.GetSetting("NameIps", ip)
                    idrq = ini.GetSetting("NameIds", id)
                    ini.DeleteSetting("Ips", iprq)
                    ini.DeleteSetting("Ids", idrq)
                    ini.DeleteSetting("NameIps", name)
                    ini.DeleteSetting("NameIds", name)
                    ini.Save()
                    for pl in Server.ActivePlayers:
                        if pl.Admin: pl.MessageFrom(self.sysname, name + " was unbanned by: " + Player.Name)

                    Player.MessageFrom(self.sysname, "Player " + name + " unbanned!")
            else:
                Player.MessageFrom(self.sysname, "Specify a Name!")

    def banhidename(self, args, Player):
        if Player.Admin:
            if len(args) == 0:
                Player.MessageFrom(self.sysname, "BanIp HideName")
                Player.MessageFrom(self.sysname, "To activate use the command \"/banhidename true\"")
                Player.MessageFrom(self.sysname, "To deactivate use the command \"/banhidename false\"")

            elif len(args) == 1:
                if args[0] == "true":
                    DataStore.Add("BanIp", Player.SteamID, "true")
                    Player.MessageFrom(self.sysname, "Now hiding your name!")

                elif args[0] == "false":
                    DataStore.Add("BanIp", Player.SteamID, "false")
                    Player.MessageFrom(self.sysname, "Now displaying your name!")

    def On_PlayerConnected(self, Player):
        id = Player.SteamID
        ip = Player.IP
        ini = self.BannedPeopleIni()
        if ini.GetSetting("Ips", ip) == "1" and ini.GetSetting("Ips", ip):
            if ini.GetSetting("Ids", id) is None:
                ini.AddSetting("Ids", id, "1")
                ini.AddSetting("NameIps", Player.Name, ip)
                ini.AddSetting("NameIds", Player.Name, id)
            Player.Kick(self.bannedreason)
            return
        if ini.GetSetting("Ids", id) == "1" and ini.GetSetting("Ids", id):
            if ini.GetSetting("Ips", ip) is None:
                ini.AddSetting("Ips", ip, "1")
                ini.AddSetting("NameIps", Player.Name, ip)
                ini.AddSetting("NameIds", Player.Name, id)
            Player.Kick(self.bannedreason)
