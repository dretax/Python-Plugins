__author__ = 'DreTaX & toffaste1337'
__version__ = '1.1'
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

    def On_PluginInit(self):
        Util.ConsoleLog("AdminDoors by " + __author__ + " Version: " + __version__ + " loaded.", False)

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

    def On_DoorUse(self, Player, DoorUseEvent):
        if Player.Admin or self.allowed(Player):
            if self.toggled(Player):
                DoorUseEvent.Open = True

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.0
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
        systemname = "AdminDoors"
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
            for pl in Server.ActivePlayers:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
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
                return
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