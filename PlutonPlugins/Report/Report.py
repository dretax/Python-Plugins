__author__ = 'DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import *

"""
    Class
"""


class Report:

    def Reports(self):
        if not Plugin.IniExists("Reports"):
            ini = Plugin.CreateIni("Reports")
            ini.Save()
        return Plugin.GetIni("Reports")

    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.0
    """
    def CheckV(self, Player, args):
        systemname = "[Report System]"
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(String.Join(" ", args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            p = self.GetPlayerName(str(args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                if str(args).lower() in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find " + String.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found " + str(count) + " player with similar name. Use more correct name!")
            return None

    def On_Chat(self, ChatEvent):
        if DataStore.ContainsKey("Reports", ChatEvent.User.SteamID):
            reason = ChatEvent.OriginalText
            systemname = "[Report System]"
            Player = ChatEvent.User
            # Avoid null players.
            bpl = str(DataStore.Get("Reports", Player.SteamID)).split(":")
            dt = str(System.DateTime.Now)
            ini = self.Reports()
            ini.AddSetting(bpl[0], dt + " | Reported: " + bpl[1] + " | Report By: " + Player.Name)
            ini.AddSetting(bpl[0], dt + " | Reason: " + reason)
            ini.Save()
            Player.MessageFrom(systemname, "Report Submitted!")
            for admin in Server.ActivePlayers:
                if admin.Admin:
                    admin.MessageFrom(systemname, "Complaint From Player: " + Player.Name + " about " + bpl[1])
                    admin.MessageFrom(systemname, "Reason: " + reason)
            DataStore.Remove("Reports", Player.SteamID)
            ChatEvent.FinalText = ""

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        systemname = "[Report System]"
        if cmd.cmd == "report":
            if len(args) == 0:
                Player.MessageFrom(systemname, "Usage: /report username")
            elif len(args) > 0:
                if DataStore.ContainsKey("Reports", Player.SteamID):
                    Player.MessageFrom(systemname, "You are already pending to submit a report atm.")
                    Player.MessageFrom(systemname, "Type the reason in the chat without /")
                    return
                else:
                    pl = self.CheckV(Player, args)
                    if pl is None:
                        return
                    DataStore.Add("Reports", Player.SteamID, pl.SteamID + ":" + pl.Name)
                    Player.MessageFrom(systemname, "Type the reason in the chat to report the player.")