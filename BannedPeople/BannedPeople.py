__author__ = 'DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite


"""
    Class
"""


class BannedPeople:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("BannedPeople by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def GetPlayerName(self, name):
        try:
            namee = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == namee:
                    return pl
            return None
        except:
            Plugin.Log("BannedPeopleError", "Error caught at getPlayer method. Player was null.")
            return None

    def BannedPeopleConfig(self):
        if not Plugin.IniExists("BannedPeopleConfig"):
            ini = Plugin.CreateIni("BannedPeopleConfig")
            ini.AddSetting("Main", "Name", "[Equinox-BanSystem]")
            ini.AddSetting("Main", "BannedDrop", "You were banned from this server.")
            ini.Save()
        return Plugin.GetIni("BannedPeopleConfig")


    # Method provided by Spoock. Converted to Python by DreTaX
    def CheckV(self, Player, args):
        ini = self.BannedPeopleConfig()
        systemname = ini.GetSetting("Main", "Name")
        Nickname = ""
        for i in xrange(-1, len(args)):
            i += 1
            Nickname += args[i] + " "
            Nickname = Data.Substring(Nickname, 0, len(Nickname) - 1)
            target = self.GetPlayerName(Nickname)
            if target is not None:
                return target

            else:
                cc = 0
                found = None
                for all in Server.Players:
                    name = all.Name.lower()
                    check = args[0].lower()
                    if check in name:
                        found = all.Name
                        cc += 1

                if (cc == 1):
                    target = self.GetPlayerName(found)
                    return target
                elif cc > 1:
                    Player.MessageFrom(systemname, "Found [color#FF0000]" + cc + " players[/color] with similar names. [color#FF0000]Use more correct name !")
                    return None
                elif cc == 0:
                    Player.MessageFrom(systemname, "Player [color#00FF00]" + Nickname + "[/color] not found")
                    return None


    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            Plugin.Log("BannedPErr", "Error caught at TrytoGrabID method.")
            return None

    def argsToText(self, args):
        text = ""
        if len(args) == 1:
            text = args[0]
        else:
            for l in xrange(0, len(args)):
                l += 1
                if l == (len(args) - 1):
                    text += args[l]
                else:
                    text += args[l] + " "
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
            if nameid and lower == namee:
                return pl
        return None


    def GetPlayerUnBannedIP(self, name):
        namee = name.lower()
        ini = self.BannedPeopleIni()
        checkdist = ini.EnumSection("NameIps")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIps", pl)
            lower = pl.lower()
            if nameid and lower == namee:
                return pl
        return None

    def On_Command(self, Player, cmd, args):
        if cmd == "banip":
            if Player.Admin or self.isMod(Player.SteamID):
                ini = self.BannedPeopleConfig()
                sysname = ini.GetSetting("Main", "Name")
                if len(args) > 0:
                    playerr = self.CheckV(Player, args)
                    if playerr is None:
                        Player.MessageFrom(sysname, "No Player found with that name!")

                    else:
                        ini = self.BannedPeopleIni()
                        if playerr.Admin or self.isMod(Player.SteamID):
                            Player.MessageFrom(sysname, "You cannot ban admins!")
                            return

                        id = playerr.SteamID
                        ip = playerr.IP
                        name = playerr.Name
                        loc = str(playerr.Location)
                        for pl in Server.Players:
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
                        Player.Message("Player's Location: " + loc)
                        playerr.Message("You were banned from the server")
                        checking = DataStore.Get("BanIp", Player.SteamID)
                        if checking == "true":
                            playerr.MessageFrom(sysname, "Admin, who banned you: UNKNOWN - Admin in Casing mode")

                        elif checking == "false" or checking == None:
                            playerr.MessageFrom(sysname, "Admin, who banned you: " + Player.Name)

                        playerr.Disconnect()
                else:
                    Player.MessageFrom(sysname, "Specify a Name!")

        elif cmd == "unbanip":
            if Player.Admin or self.isMod(Player.SteamID):
                ini = self.BannedPeopleConfig()
                sysname = ini.GetSetting("Main", "Name")
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
                        for pl in Server.Players:
                            if pl.Admin:
                                pl.MessageFrom(sysname, name + " was unbanned by: " + Player.Name)

                        Player.MessageFrom(sysname, "Player " + name + " unbanned!")
                else:
                    Player.MessageFrom(sysname, "Specify a Name!")
        elif cmd == "banhidename":
            if Player.Admin or self.isMod(Player.SteamID):
                ini = self.BannedPeopleConfig()
                sysname = ini.GetSetting("Main", "Name")
                if not DataStore.ContainsKey("BanIp", Player.SteamID):
                    DataStore.Add("BanIp", Player.SteamID, "true")
                    Player.MessageFrom(sysname, "Now hiding your name!")
                else:
                    DataStore.Remove("BanIp", Player.SteamID)
                    Player.MessageFrom(sysname, "Now displaying your name!")

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            if Player is not None:
                try:
                    Player.Disconnect()
                except:
                    pass
            return
        ip = str(Player.IP)
        ini = self.BannedPeopleConfig()
        sysname = ini.GetSetting("Main", "Name")
        bannedreason = ini.GetSetting("Main", "BannedDrop")
        ini = self.BannedPeopleIni()
        if ini.GetSetting("Ips", ip) == "1":
            Player.MessageFrom(sysname, bannedreason)
            Player.Disconnect()
            return
        if ini.GetSetting("Ids", id) == "1":
            Player.MessageFrom(sysname, bannedreason)
            Player.Disconnect()