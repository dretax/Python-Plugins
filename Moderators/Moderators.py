__author__ = 'DreTaX'
__version__ = '1.1'
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


    def GetPlayerName(self, name):
        try:
            name = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            Plugin.Log("Moderators", "Error caught at getPlayer method. Player was null.")
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

    # Method provided by Spoock. Converted to Python by DreTaX
    def CheckV(self, Player, args):
        systemname = "Moderators"
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

    def On_PluginInit(self):
        self.AddIdsToDS()

    def AddIdsToDS(self):
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
                    name = str(playerr.Name)
                    id = str(playerr.GameID)
                    ini = self.ModeratorsIni()
                    ini.AddSetting("Moderators", name, id)
                    ini.Save()
                    DataStore.Add("Moderators", id, name)
                    Player.Message(name + " was added to the moderators.")
        elif cmd == "delmoderator":
            if Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /delmoderator name")
                else:
                    Player.Message()
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