__author__ = 'DreTaX'
__version__ = '1.0'

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
        self.BannedPeopleConfig()


    def argsToText(self, args):
        text = String.Join(" ", args)
        return text

    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None

    def GetPlayerUnBannedID(self, namee):
        name = namee.lower()
        ini = self.BannedPeopleIni()
        checkdist = ini.EnumSection("NameIds")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIds", pl)
            lower = pl.lower()
            if nameid != None and lower == name:
                return pl
        return None


    def GetPlayerUnBannedIP(self, namee):
        name = namee.lower()
        ini = self.BannedPeopleIni()
        checkdist = ini.EnumSection("NameIps")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIps", pl)
            lower = pl.lower()
            if nameid != None and lower == name:
                return pl
        return None

    # Method provided by Spoock. Converted to Python by DreTaX
    """def CheckV(self, Player, args):
        ini = self.BannedPeopleConfig()
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
                    return None"""
    # method by Illuminati
    def CheckV(self, Player, args):
        ini = self.BannedPeopleConfig()
        systemname = ini.GetSetting("Main", "Name")
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
        if Player.Admin:
            if cmd.cmd == "banip":
                ini = self.BannedPeopleConfig()
                sysname = ini.GetSetting("Main", "Name")
                bannedreason = ini.GetSetting("Main", "BannedDrop")
                if len(args) > 0:
                    playerr = self.CheckV(Player, args)
                    if playerr == None:
                        Player.MessageFrom(sysname, "No Player found with that name!")

                    else:
                        ini = self.BannedPeopleIni()
                        #todo: Be sure to check later here for the admin mod and owner rights, so owner can ban an admin maybe?!
                        if playerr.Admin:
                            Player.MessageFrom(sysname, "You cannot ban admins!")
                            return

                        id = playerr.SteamID
                        ip = playerr.IP
                        name = playerr.Name
                        for pl in Server.ActivePlayers:
                            if pl.Admin: pl.MessageFrom(sysname, "Message to Admins: " + name + " was banned by: " + Player.Name)

                        ini.AddSetting("Ips", ip, "1")
                        ini.AddSetting("Ids", id, "1")
                        ini.AddSetting("NameIps", name, ip)
                        ini.AddSetting("NameIds", name, id)
                        ini.AddSetting("AdminWhoBanned", name, Player.Name)
                        ini.Save()
                        Player.Message("You banned " + name)
                        Player.Message("Player's IP: " + ip)
                        Player.Message("Player's ID: " + id)
                        playerr.Message("You were banned from the server")
                        checking = DataStore.Get("BanIp", Player.SteamID)
                        if checking == "true":
                            playerr.MessageFrom(sysname, "Admin, who banned you: UNKNOWN - Admin in Casing mode")

                        elif checking == "false" or checking == None:
                            playerr.MessageFrom(sysname, "Admin, who banned you: " + Player.Name)

                        #todo: Make sure to add a kick reason arg crap here
                        playerr.Kick(bannedreason)
                else:
                    Player.MessageFrom(sysname, "Specify a Name!")
        elif cmd.cmd == "unbanip":
            if Player.Admin:
                ini = self.BannedPeopleConfig()
                sysname = ini.GetSetting("Main", "Name")
                if len(args) > 0:
                    name = self.argsToText(args)
                    id = self.GetPlayerUnBannedID(name)
                    ip = self.GetPlayerUnBannedIP(name)
                    if id == None:
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
                            if pl.Admin: pl.MessageFrom(sysname, name + " was unbanned by: " + Player.Name)

                        Player.MessageFrom(sysname, "Player " + name + " unbanned!")
                else:
                    Player.MessageFrom(sysname, "Specify a Name!")
        elif cmd.cmd == "banhidename":
            if Player.Admin:
                ini = self.BannedPeopleConfig()
                sysname = ini.GetSetting("Main", "Name")
                if len(args) == 0:
                    Player.MessageFrom(sysname, "BanIp HideName")
                    Player.MessageFrom(sysname, "To activate use the command \"/banhidename true\"")
                    Player.MessageFrom(sysname, "To deactivate use the command \"/banhidename false\"")

                elif len(args) == 1:
                    if args[0] == "true":
                        DataStore.Add("BanIp", Player.SteamID, "true")
                        Player.MessageFrom(sysname, "Now hiding your name!")

                    elif args[0] == "false":
                        DataStore.Add("BanIp", Player.SteamID, "false")
                        Player.MessageFrom(sysname, "Now displaying your name!")

    def On_PlayerConnected(self, Player):
        id = Player.SteamID
        ip = Player.IP
        ini = self.BannedPeopleConfig()
        bannedreason = ini.GetSetting("Main", "BannedDrop")
        ini = self.BannedPeopleIni()
        if ini.GetSetting("Ips", ip) == "1":
            Player.Kick(bannedreason)
            return
        if ini.GetSetting("Ids", id) == "1":
            Player.Kick(bannedreason)