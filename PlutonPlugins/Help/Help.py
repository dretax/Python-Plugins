__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton

"""
    Class
"""

class Help:

    def On_PluginInit(self):
        self.HelpCfg()

    def HelpCfg(self):
        if not Plugin.IniExists("Help"):
            loc = Plugin.CreateIni("Help")
            loc.AddSetting("Settings", "SysName", "Help")
            loc.AddSetting("AdminCommands", "/god", "Gives You godmode!")
            loc.AddSetting("AdminCommands", "/tphere playername", "Teleports Player to you!")
            loc.AddSetting("PlayerCommands", "/playerlist", "Lists Current Players!")
            loc.Save()
        return Plugin.GetIni("Help")

    def SendAdminCommands(self, Player):
        ini = self.HelpCfg()
        sys = ini.GetSetting("Settings", "SysName")
        enum = ini.EnumSection("AdminCommands")
        Player.MessageFrom(sys, "Admin Commands")
        for com in enum:
            get = ini.GetSetting("AdminCommands", com)
            Player.MessageFrom(sys, com + " - " + get)

    def SendPlayerCommands(self, Player):
        ini = self.HelpCfg()
        sys = ini.GetSetting("Settings", "SysName")
        enum = ini.EnumSection("PlayerCommands")
        Player.MessageFrom(sys, "Player Commands")
        for com in enum:
            get = ini.GetSetting("PlayerCommands", com)
            Player.MessageFrom(sys, com + " - " + get)

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "playerlist":
            all = ""
            for pl in Server.ActivePlayers:
                all = all + str(pl.Name) + ", "
            Player.MessageFrom("Online Players", all)
        elif cmd.cmd == "help":
            if len(args) == 0:
                ini = self.HelpCfg()
                sys = ini.GetSetting("Settings", "SysName")
                Player.MessageFrom(sys, "Lists you the commands of Admins or Players")
                Player.MessageFrom(sys, "Usage: /help player or /help admin")
            else:
                if args[0] == "admin":
                    if not Player.Admin:
                        self.SendPlayerCommands(Player)
                        return
                    self.SendAdminCommands(Player)
                else:
                    self.SendPlayerCommands(Player)