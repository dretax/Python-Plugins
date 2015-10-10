__author__ = 'DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton

"""
    Class
"""


class Report:

    def Reports(self):
        if not Plugin.IniExists("Reports"):
            ini = Plugin.CreateIni("Reports")
            ini.Save()
        return Plugin.GetIni("Reports")

    """
        CheckV Assistants
    """

    def GetPlayerName(self, name, Mode=1):
        if Mode == 1 or Mode == 3:
            for pl in Server.ActivePlayers:
                if pl.Name.lower() == name:
                    return pl
        if Mode == 2 or Mode == 3:
            for pl in Server.OfflinePlayers.Values:
                if pl.Name.lower() == name:
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
        V6.0
    """

    def CheckV(self, Player, args, Mode=1):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.Join(" ", args).lower(), Mode)
            if p is not None:
                return p
            if Mode == 1 or Mode == 3:
                for pl in Server.ActivePlayers:
                    for namePart in args:
                        if namePart.lower() in pl.Name.lower():
                            p = pl
                            count += 1
            if Mode == 2 or Mode == 3:
                for offlineplayer in Server.OfflinePlayers.Values:
                    for namePart in args:
                        if namePart.lower() in offlineplayer.Name.lower():
                            p = offlineplayer
                            count += 1
        else:
            ag = str(args).lower()  # just incase
            p = self.GetPlayerName(ag, Mode)
            if p is not None:
                return p
            if Mode == 1 or Mode == 3:
                for pl in Server.ActivePlayers:
                    if ag in pl.Name.lower():
                        p = pl
                        count += 1
            if Mode == 2 or Mode == 3:
                for offlineplayer in Server.OfflinePlayers.Values:
                    if ag in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
        if count == 0:
            Player.MessageFrom("Reports", "Couldn't Find " + str.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom("Reports", "Found " + str(count) +
                               " player with similar name. Use more correct name!")
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
