__author__ = 'DreTaX'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

GlobalChatCommands = []


class CommandRestrict:

    def Commands(self):
        if not Plugin.IniExists("Commands"):
            loc = Plugin.CreateIni("Commands")
            loc.AddSetting("ConsoleCommands", "1", "suicide")
            loc.AddSetting("ConsoleCommands", "2", "allahakbar")
            loc.AddSetting("ChatCommands", "1", "yell")
            loc.Save()
        return Plugin.GetIni("Commands")

    def On_PluginInit(self):
        ini = self.Commands()
        for x in ini.EnumSection("ConsoleCommands"):
            Server.RestrictConsoleCommand(ini.GetSetting("ConsoleCommands", x))
        for x in ini.EnumSection("ChatCommands"):
            GlobalChatCommands.append(ini.GetSetting("ConsoleCommands", x))

    def On_PlayerConnected(self, Player):
        for x in GlobalChatCommands:
            Player.RestrictCommand(x)

    def On_Command(self, Player, cmd, args):
        # Todo: Make Player type Console Restriction instead of global in Fougerite
        if cmd == "restrict":
            if Player.Admin:
                if len(args) == 0:
                    Player.MessageFrom("Restrict", "Usage: /restrict name commandname")
                elif len(args) == 2:
                    name = args[0]
                    command = args[1].lower()
                    pl = self.CheckV(Player, name)
                    if pl is not None:
                        pl.RestrictCommand(command)
                        Player.MessageFrom("Restrict", pl.Name + " is now not able to use " + command)
        elif cmd == "unrestrict":
            if Player.Admin:
                if len(args) == 0:
                    Player.MessageFrom("Restrict", "Usage: /restrict name commandname")
                elif len(args) == 2:
                    name = args[0]
                    command = args[1].lower()
                    pl = self.CheckV(Player, name)
                    if pl is not None:
                        pl.UnRestrictCommand(command)
                        Player.MessageFrom("Restrict", pl.Name + " now has access to " + command)


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
            Player.MessageFrom("Restrict", "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom("Restrict", "Found [color#FF0000]" + str(count)
                               + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None
