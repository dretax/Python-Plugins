__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

sysname = "SetHealth"
class SetHealth:

    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("SetHealth by " + __author__ + " Version: " + __version__ + " loaded.", False)


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
                Player.MessageFrom(sysname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            if Player is not None:
                Player.MessageFrom(sysname, "Found [color#FF0000]" + str(count) +
                                   "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def On_Command(self, Player, cmd, args):
        if cmd == "sethealth":
            if Player.Admin or Player.Moderator:
                if 1 >= len(args) or len(args) > 2:
                    Player.MessageFrom(sysname, "Usage: /sethealth playername amount")
                    return
                pl = self.CheckV(Player, args[0])
                if pl is None:
                    return
                if not args[1].isnumeric():
                    Player.MessageFrom(sysname, "Usage: /sethealth playername amount")
                    return
                pl.Health = float(args[1])