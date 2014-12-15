__author__ = 'DreTaX & toffaste1337'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

class AdminDoors:
    """
        Methods
    """
    red = "[color #FF0000]"
    green = "[color #009900]"

    def On_PluginInit(self):
        Util.ConsoleLog("AdminDoors by" + __author__ + " Version: " + __version__ + " loaded.", False)

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def Allows(self):
        if not Plugin.IniExists("allowed"):
            Plugin.CreateIni("allowed")
        return Plugin.GetIni("allowed")

    def Toggles(self):
        if not Plugin.IniExists("toggled"):
            Plugin.CreateIni("toggled")
        return Plugin.GetIni("toggled")

    def GetPlayerName(self, name):
        try:
            namee = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == namee:
                    return pl
            return None
        except:
            return None

    # Method provided by Spoock. Converted to Python by DreTaX
    def CheckV(self, Player, args):
        systemname = "AdminDoors"
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

                if cc == 1:
                    target = self.GetPlayerName(found)
                    return target
                elif cc > 1:
                    Player.MessageFrom(systemname, "Found [color#FF0000]" + cc + " players[/color] with similar names. [color#FF0000]Use more correct name !")
                    return None
                elif cc == 0:
                    Player.MessageFrom(systemname, "Player [color#00FF00]" + Nickname + "[/color] not found")
                    return None

    def allowed(self, target):
        ini = self.Allows()
        if ini.GetSetting("Players", target.SteamID) is not None:
            return True
        else:
            return False

    def allow(self, target, allowedBy):
        ini = self.Allows()
        ini.AddSetting("Players", target.SteamID, target.Name + " was allowed by " + allowedBy.Name)
        ini.Save()
        self.toggle(target)

    def unAllow(self, target):
        ini = self.Allows()
        ini2 = self.Toggles()
        ini.DeleteSetting("Players", target.SteamID)
        ini.DeleteSetting("Players", target.SteamID)
        ini.Save()
        ini2.Save()

    def toggle(self, target):
        ini = self.Toggles()
        if ini.GetSetting("Players", target.SteamID) is None:
            ini.AddSetting("Players", target.SteamID, target.Name)
            target.MessageFrom("AdminDoors", "Toggled on!")
            ini.Save()
        else:
            ini.DeleteSetting("Players", target.SteamID)
            target.MessageFrom("AdminDoors", "Toggled off!")
            ini.Save()

    def toggled(self, target):
        ini = self.Toggles()
        if ini.GetSetting("Players", target.SteamID) is not None:
            return True
        else:
            return False

    def On_Command(self, Player, cmd, args):
        if cmd == "admindoors" or cmd == "ad":
            if len(args) == 0:
                if Player.Admin or self.allowed(Player) and cmd != "ad":
                    Player.MessageFrom("AdminDoors", "/AdminDoors Allow  -  /AdminDoors UnAllow  -  /AdminDoors Toggle  -  /AdminDoors Info")
                    Player.MessageFrom("AdminDoors", "/AD can also be used.")
                else:
                    Player.MessageFrom("AdminDoors", "/AD Allow  -  /AD UnAllow  -  /AD toggle  -  /AD Info")
                    Player.MessageFrom("AdminDoors", "/AdminDoors can also be used.")
            if args[0] == "allow":
                if Player.Admin or self.allowed(Player):
                    if len(args) == 0:
                        Player.MessageFrom("AdminDoors", "/AdminDoors Allow <PlayerName>")
                        return
                    targetByArgs = self.CheckV(Player, args)
                    if targetByArgs is None:
                        Player.MessageFrom("AdminDoors", self.argsToText(args) + " was not found.")
                    else:
                        if self.allowed(targetByArgs) is False:
                            self.allow(targetByArgs, Player)
                            Player.MessageFrom("AdminDoors", targetByArgs.Name + " can now use all doors!")
                            targetByArgs.MessageFrom("AdminDoors", Player.Name + " allowed you to use all doors!")
                        else:
                            Player.MessageFrom("AdminDoors", targetByArgs.Name + " was allowed, nothing has been changed.")
                else:
                    Player.MessageFrom("AdminDoors", "You do not have permission for this.")
            elif args[0] == "unallow":
                if Player.Admin or self.allowed(Player):
                    if args.Length == 0:
                        Player.MessageFrom("AdminDoors", "/AdminDoors UnAllow <PlayerName>")
                        return
                    targetByArgs = self.CheckV(Player, args)
                    if targetByArgs is None:
                        Player.MessageFrom("AdminDoors", self.argsToText(args) + " was not found.")
                    else:
                        if self.allowed(targetByArgs):
                            self.unAllow(targetByArgs)
                            Player.MessageFrom("AdminDoors", targetByArgs.Name + " can no longer use all doors!")
                            targetByArgs.MessageFrom("AdminDoors", Player.Name + " took your powers to open all doors!")
                        else:
                            Player.MessageFrom("AdminDoors", targetByArgs.Name + " was not allowed, nothing has been changed.")
                else:
                    Player.MessageFrom("AdminDoors", "You do not have permission for this.")
            elif args[0] == "toggle":
                if Player.Admin or self.allowed(Player):
                    self.toggle(Player)
                else:
                    Player.MessageFrom("AdminDoors", "You do not have permission for this.")