__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton

"""
    Class
"""


class InstaBuild:
    def InstaBuild(self):
        if not Plugin.IniExists("InstaBuild"):
            ini = Plugin.CreateIni("InstaBuild")
            ini.AddSetting("Settings", "EnableforPublic", "0")
            ini.Save()
        return Plugin.GetIni("InstaBuild")

    def On_FrameDeployed(self, BuildingPart):
        ini = self.InstaBuild()
        get = int(ini.GetSetting("Settings", "EnableforPublic"))
        if get == 1:
            BuildingPart.health = BuildingPart.MaxHealth()
        else:
            Player = BuildingPart.Builder
            dsget = DataStore.ContainsKey("InstaBuild", Player.SteamID)
            if Player.Admin and dsget is True:
                BuildingPart.health = BuildingPart.MaxHealth()

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "instabuild":
            ini = self.InstaBuild()
            get = int(ini.GetSetting("Settings", "EnableforPublic"))
            if get == 1:
                Player.Message("InstaBuild is enabled for everyone.")
            else:
                if not Player.Admin:
                    Player.Message("Its only for admins. Sorry")
                    return
                dsget = DataStore.ContainsKey("InstaBuild", Player.SteamID)
                if dsget is True:
                    DataStore.Remove("InstaBuild", Player.SteamID)
                    Player.Message("You quit InstaBuild mode.")
                else:
                    DataStore.Add("InstaBuild", Player.SteamID)
                    Player.Message("You enabled InstaBuild mode.")