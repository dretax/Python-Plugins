__author__ = 'DreTaX'
__version__ = '1.4'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

class Moderators:
    """
        Methods
    """

    def ModeratorsIni(self):
        if not Plugin.IniExists("Moderators"):
            ini = Plugin.CreateIni("Moderators")
            ini.AddSetting("Moderators", "ModNameHere", "76561197999999999")
            ini.Save()
        return Plugin.GetIni("Moderators")

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

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
        systemname = "Moderators"
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
            Player.MessageFrom(systemname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def On_PluginInit(self):
        self.AddIdsToDS()

    def AddIdsToDS(self):
        DataStore.Flush("Moderators")
        ini = self.ModeratorsIni()
        mods = ini.EnumSection("Moderators")
        for mod in mods:
            modid = ini.GetSetting("Moderators", mod)
            DataStore.Add("Moderators", modid, mod)

    def On_Command(self, Player, cmd, args):
        if cmd == "addmoderator":
            if Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /addmoderator name")
                else:
                    playerr = self.CheckV(Player, args)
                    if playerr is None:
                        return
                    name = playerr.Name
                    id = playerr.SteamID
                    ini = self.ModeratorsIni()
                    for x in ini.EnumSection("Moderators"):
                        if ini.GetSetting("Moderators", x) == id:
                            Player.Message(name + " is already a moderator.")
                            return
                    ini.AddSetting("Moderators", name, id)
                    ini.Save()
                    DataStore.Add("Moderators", id, name)
                    Player.Message(name + " was added to the moderators.")
        elif cmd == "delmoderator":
            if Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /delmoderator name")
                else:
                    name = self.argsToText(args)
                    name = name.lower()
                    ini = self.ModeratorsIni()
                    mods = ini.EnumSection("Moderators")
                    for mod in mods:
                        l = mod.lower()
                        if name in l or name == l:
                            id = ini.GetSetting("Moderators", mod)
                            ini.DeleteSetting("Moderators", mod)
                            ini.Save()
                            DataStore.Remove("Moderators", id)
                            Player.Message(mod + " was removed from the moderators.")
                            return
                    Player.Message("Couldn't find player. Use /listmods")
        elif cmd == "listmods":
            if Player.Admin:
                ini = self.ModeratorsIni()
                mods = ini.EnumSection("Moderators")
                Player.Message("Current Moderators:")
                for mod in mods:
                    Player.Message("- "+ str(mod))
        elif cmd == "modflush":
            if Player.Admin:
                self.AddIdsToDS()
                Player.Message("Flushed!")