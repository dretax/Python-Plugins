__author__ = 'DreTaX'
__version__ = '1.7.1'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

"""
    Class
"""

green = "[color #009900]"
red = "[color #FF0000]"
rangeip = []
droped = []


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
        range = self.BannedPeopleRange()
        enum = range.EnumSection("RangeBan")
        for ip in enum:
            rangeip.append(ip)
        DataStore.Flush("DropTester")
        Util.ConsoleLog("BannedPeople by " + __author__ + " Version: " + __version__ + " loaded.", False)


    def BannedPeopleConfig(self):
        if not Plugin.IniExists("BannedPeopleConfig"):
            ini = Plugin.CreateIni("BannedPeopleConfig")
            ini.AddSetting("Main", "Name", "[Equinox-BanSystem]")
            ini.AddSetting("Main", "BannedDrop", "You were banned from this server.")
            ini.Save()
        return Plugin.GetIni("BannedPeopleConfig")

    def BannedPeopleRange(self):
        if not Plugin.IniExists("BannedPeople"):
            ini = Plugin.CreateIni("BannedPeople")
            ini.AddSetting("RangeBan", "46.16.", "1")
            ini.AddSetting("RangeBan", "199.188.", "1")
            ini.Save()
        return Plugin.GetIni("BannedPeople")

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
                    b = Server.IsBannedID(name)
                    if not b:
                        Server.BanPlayerID(name, "1", "You were banned.", "ConsoleOrRCON")
                        ConsoleEvent.ReplyWith("ID " + name + " banned!")
                    else:
                        ConsoleEvent.ReplyWith("ID " + name + " is already banned.")
                elif ipmatch:
                    b = Server.IsBannedIP(name)
                    if not b:
                        Server.BanPlayerIP(name, "1", "You were banned.", "ConsoleOrRCON")
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

                        checking = DataStore.Get("BanIp", Player.SteamID)
                        if checking == "true":
                            Server.BanPlayer(playerr, "Unknown", self.bannedreason, Player)
                        elif checking == "false" or checking is None:
                            Server.BanPlayer(playerr, Player.Name, self.bannedreason, Player)
                else:
                    Player.MessageFrom(self.sysname, "Specify a Name!")
            else:
                Player.MessageFrom(self.sysname, "You aren't an admin!")
        elif cmd == "unbanip":
            if Player.Admin or Player.Moderator:
                if len(args) > 0:
                    name = self.argsToText(args)
                    Server.UnbanByName(name, Player.Name, Player)
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
                        Server.BanPlayerIP(id, "1", "IP OfflineBanned", Player.Name + " | " + Player.SteamID)
                        Player.MessageFrom(self.sysname, "Player IP (" + id + ") was banned.")
                    else:
                        if Server.GetRustPPAPI().IsAdmin(long(id)):
                            Player.MessageFrom(self.sysname, "This owner of the ID is an Admin/Moderator.")
                            Player.MessageFrom(self.sysname, "You need to remove him from the list first.")
                            return
                        Server.BanPlayerID(id, "1", "ID OfflineBanned", Player.Name + " | " + Player.SteamID)
                        Player.MessageFrom(self.sysname, "Player ID (" + id + ") was banned.")
        elif cmd == "drop":
            if Player.Admin or Player.Moderator:
                p = self.CheckV(Player, args)
                if p is not None:
                    # self.recordInventory(p)
                    DataStore.Add("DropTester", p.SteamID, str(p.Location))
                    List = Plugin.CreateDict()
                    List["Health"] = p.Health
                    List["Player"] = p
                    List["Executor"] = Player
                    List["Location"] = p.Location
                    p.TeleportTo(float(p.X), float(p.Y) + float(55), float(p.Z), False)
                    Player.MessageFrom(self.sysname, p.Name + " was dropped.")
                    Plugin.CreateParallelTimer("hack", 3000, List).Start()

    def On_PlayerConnected(self, Player):
        ip = Player.IP
        split = ip.split(".", 4)
        nip = split[0] + "." + split[1] + "."
        if nip in rangeip and (not Server.IsBannedID(Player.SteamID) or not Server.IsBannedIP(ip)):
            Server.BanPlayer(Player, "Console", "Range Ban Connection")

    def On_PlayerDisconnected(self, Player):
        if DataStore.ContainsKey("DropTester", Player.SteamID):
            DataStore.Remove("DropTester", Player.SteamID)
        if Player.UID in droped:
            droped.remove(Player.UID)

    def On_PlayerSpawned(self, Player, SpawnEvent):
        if DataStore.ContainsKey("DropTester", Player.SteamID):
            l = self.Replace(DataStore.Get("DropTester", Player.SteamID))
            DataStore.Remove("DropTester", Player.SteamID)
            Player.TeleportTo(float(l[0]), float(l[1]), float(l[2]), False)
            # self.returnInventory(Player)
            Player.MessageFrom(self.sysname, green + "Teleported back to the same position!")

    def Replace(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(',')

    def recordInventory(self, Player):
        Inventory = []
        id = Player.SteamID
        for Item in Player.Inventory.Items:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in Player.Inventory.ArmorItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in Player.Inventory.BarItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)

        DataStore.Add("DropTester2", id, Inventory)
        DataStore.Save()
        Player.Inventory.ClearAll()

    def returnInventory(self, Player):
        id = Player.SteamID
        if DataStore.ContainsKey("DropTester2", id):
            Inventory = DataStore.Get("DropTester2", id)
            Player.Inventory.ClearAll()
            for dictionary in Inventory:
                if dictionary['name'] is not None:
                    Player.Inventory.AddItemTo(dictionary['name'], dictionary['slot'], dictionary['quantity'])
                else:
                    Player.MessageFrom(self.sysname, red + "No dictionary found in the for cycle?!")
            Player.MessageFrom(self.sysname, green + "Your have received your original inventory")
            DataStore.Remove("DropTester2", id)
        else:
            Player.MessageFrom(self.sysname, red + "No Items of your last inventory found!")

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.Victim is not None:
            if DataStore.ContainsKey("DropTester", DeathEvent.Victim.SteamID):
                droped.append(DeathEvent.Victim.UID)

    def hackCallback(self, timer):
        List = timer.Args
        timer.Kill()
        player = List["Player"]
        if player is None:
            List["Executor"].Notice(player.Name + " maybe disconnected.")
            return
        elif List["Location"] == player.Location:
            List["Executor"].Notice(player.Name + " has the same position, maybe bugged?")
            return
        elif player.UID in droped:
            droped.remove(player.UID)
            return
        if player.IsAlive:
            List["Executor"].Notice(player.Name + " failed the drop test.")
            if player.Admin or player.Moderator:
                return
            Server.BanPlayer(player, List["Executor"].Name, "Drop Failed", List["Executor"])
