__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

sysn = "Colors"


teal = "[color #00FFFF]"
gold = "[color #EEC900]"
silver = "[color #BFBFBF]"
bronze = "[color #A67D3D]"
yellow = "[color #EEEE00]"
red = "[color #FF0000]"

Colors = {

}

Selected = {

}

# Check if player is writing in color and if they do then remove it
NoPlayerColor = True


class Color:

    def On_PluginInit(self):
        cl = self.Colors()
        enum = cl.EnumSection("Colors")
        for name in enum:
            code = cl.GetSetting("Colors", name)
            Colors[name] = str(code)

    def On_PlayerConnected(self, Player):
        ini = self.Colors()
        if ini.GetSetting("ColorSet", Player.SteamID) is not None:
            Selected[Player] = ini.GetSetting("ColorSet", Player.SteamID)

    def Colors(self):
        if not Plugin.IniExists("Colors"):
            ini = Plugin.CreateIni("Colors")
            ini.AddSetting("Colors", "red", "#FF0000")
            ini.AddSetting("Colors", "teal", "#00FFFF")
            ini.AddSetting("Colors", "yellow", "#EEEE00")
            ini.AddSetting("Colors", "silver", "#BFBFBF")
            ini.AddSetting("Colors", "gold", "#EEC900")
            ini.AddSetting("Colors", "green", "#008B00")
            ini.AddSetting("Colors", "orange", "#A67D3D")
            ini.AddSetting("Colors", "bronze", "#EE9A00")
            ini.AddSetting("Colors", "black", "#000000")
            ini.AddSetting("Colors", "blue", "#0000FF")
            ini.AddSetting("Colors", "white", "#FFFFFF")
            ini.Save()
        return Plugin.GetIni("Colors")

    def On_Chat(self, Player, ChatEvent):
        if NoPlayerColor:
            if not Player.Admin and not Player.Moderator:
                Text = ChatEvent.OriginalMessage
                if "color" not in Text.lower():
                    return
                Text = re.sub(r'\[color\s*([^\]]+)\]', '', Text)
                Text = re.sub(r'\[/color\s*\]', '', Text)
                Text = Text.replace('"', '')
                ChatEvent.NewText = "          "
                Server.BroadcastFrom(Player.Name, Text)
                return
        if Player in Selected.keys():
            Text = ChatEvent.OriginalMessage
            ChatEvent.NewText = "          "
            c = "[color " + Selected[Player] + "] " + Text
            c = c.replace('"', '')
            Server.BroadcastFrom(Player.Name, c.strip(' '))

    def On_Command(self, Player, cmd, args):
        if cmd == "color":
            if Player.Admin or Player.Moderator:
                if len(args) == 0:
                    Player.MessageFrom(sysn, "List of colors: ")
                    Player.MessageFrom(sysn, str.join(', ', Colors.keys()))
                    return
                color = str.join(' ', args)
                if Colors.get(color) is None:
                    Player.MessageFrom(sysn, "Couldn't find color!")
                    Player.MessageFrom(sysn, "List of colors: ")
                    Player.MessageFrom(sysn, str.join(', ', Colors.keys()))
                    return
                Selected[Player] = Colors.get(color)
                ini = self.Colors()
                if ini.GetSetting("ColorSet", Player.SteamID) is not None:
                    ini.SetSetting("ColorSet", Player.SteamID, Colors.get(color))
                else:
                    ini.AddSetting("ColorSet", Player.SteamID, Colors.get(color))
                ini.Save()
                Player.MessageFrom(sysn, "Color set!")
