__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

"""
    Class
"""

red = "[color #FF0000]"
class SteamProfiler:

    def Ini(self):
        if not Plugin.IniExists("Ini"):
            ini = Plugin.CreateIni("Ini")
            ini.AddSetting("Settings", "APIKey", "http://steamcommunity.com/dev/apikey")
            ini.AddSetting("Settings", "AllowShared", "0")
            ini.AddSetting("Settings", "AllowedVACBans", "2")
            ini.AddSetting("Settings", "MaximumDays", "300")
            ini.AddSetting("Settings", "Sys", "SteamProfiler")
            ini.AddSetting("Settings", "UsingShared", "You are using shared RUST. It's not allowed.")
            ini.AddSetting("Settings", "VacBans", "You reached the max number of VAC bans.")
            ini.Save()
        return Plugin.GetIni("Ini")

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def GetSteamDatas(self, page, num):
        if num == 1:
            p = page.replace('	"response": {', '')
            p = re.sub('[{\}\"\s\s+]', '', p)
            p = p.split(':')
            return p
        elif num == 2:
            p = page.replace('	"players": [', '')
            p = re.sub('[{\}\"\s\s+]', '', p)
            p = p.split(',')
            return p

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        ini = self.Ini()
        APIKey = ini.GetSetting("Settings", "APIKey")
        AllowShared = int(ini.GetSetting("Settings", "AllowShared"))
        AllowVACBanned = int(ini.GetSetting("Settings", "AllowVACBanned"))
        AllowedVACBans = int(ini.GetSetting("Settings", "AllowedVACBans"))
        MaximumDays = int(ini.GetSetting("Settings", "MaximumDays"))
        sys = ini.GetSetting("Settings", "Sys")
        if AllowShared == 0:
            url = Web.GET("http://api.steampowered.com/IPlayerService/IsPlayingSharedGame/v0001/?key=" + APIKey + "&steamid=" + id + "&appid_playing=252490")
            data = self.GetSteamDatas(url, 1)
            if int(data[1]) != 0:
                msg = ini.GetSetting("Settings", "UsingShared")
                Player.MessageFrom(sys, red + msg)
                Player.Disconnect()
                return
        if AllowVACBanned == 0:
            url = Web.GET("http://api.steampowered.com/ISteamUser/GetPlayerBans/v0001/?key=" + APIKey + "&steamids=" + id)
            data = self.GetSteamDatas(url, 2)
            numv = data[3].split(':')
            numv = int(numv[1])
            ldays = data[4].split(':')
            ldays = int(ldays[1])
            if (numv > AllowedVACBans and ldays < MaximumDays) or MaximumDays == 0:
                msg = ini.GetSetting("Settings", "VacBans")
                Player.MessageFrom(sys, red + msg)
                Player.Disconnect()
                return