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

    def On_PluginInit(self):
        Util.ConsoleLog("SteamProfiler by" + __author__ + " Version: " + __version__ + " loaded.", False)
        self.Ini()

    def Ini(self):
        if not Plugin.IniExists("Ini"):
            ini = Plugin.CreateIni("Ini")
            ini.AddSetting("Settings", "APIKey", "http://steamcommunity.com/dev/apikey")
            ini.AddSetting("Settings", "AllowShared", "0")
            ini.AddSetting("Settings", "AllowedVACBans", "2")
            ini.AddSetting("Settings", "MaximumDays", "300")
            ini.AddSetting("Settings", "CheckForOnlyRust", "1")
            ini.AddSetting("Settings", "CheckForPrivate", "1")
            ini.AddSetting("Settings", "CheckForNoProfile", "1")
            ini.AddSetting("Settings", "Sys", "SteamProfiler")
            ini.AddSetting("Settings", "UsingShared", "You are using shared RUST. It's not allowed.")
            ini.AddSetting("Settings", "VacBans", "You reached the max number of VAC bans.")
            ini.AddSetting("Settings", "OnlyRust", "People only having Rust are not allowed to join.")
            ini.AddSetting("Settings", "NoProfile", "Only People who have setup their community profile can join.")
            ini.AddSetting("Settings", "Private", "Only People who are having public profile can join.")
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
        CheckOnlyRust = int(ini.GetSetting("Settings", "CheckForOnlyRust"))
        CheckForPrivate = int(ini.GetSetting("Settings", "CheckForPrivate"))
        CheckForNoProfile = int(ini.GetSetting("Settings", "CheckForNoProfile"))
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
            url = Web.GET("http://api.steampowered.com/ISteamUser/GetPlayerBans/v0001/?key=" + APIKey + "&steamid=" + id)
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
        if CheckOnlyRust == 1:
            url = Web.GET("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + APIKey + "&steamid=" + id)
            listofappids = re.findall(r'"appid":.*,', url)
            gamecount = re.findall(r'"game_count":.*,', url)
            gamecount = re.sub('["\,\ \'\[\]]', '', str(gamecount)).split(':')
            if int(gamecount[1]) == 1 and "252490" in listofappids:
                msg = ini.GetSetting("Settings", "OnlyRust")
                Player.MessageFrom(sys, red + msg)
                Player.Disconnect()
                return
        if CheckForPrivate == 1 or CheckForNoProfile == 1:
            url = Web.GET("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + APIKey + "&steamid=" + id)
            if CheckForNoProfile == 1:
                comm = re.findall(r'"profilestate":.*,', url)
                comm = re.sub('["\,\ \'\[\]]', '', str(comm)).split(':')
                if int(comm[1]) != 1:
                    msg = ini.GetSetting("Settings", "NoProfile")
                    Player.MessageFrom(sys, red + msg)
                    Player.Disconnect()
                    return
            if CheckForPrivate == 1:
                comm = re.findall(r'"communityvisibilitystate":.*,', url)
                comm = re.sub('["\,\ \'\[\]]', '', str(comm)).split(':')
                if int(comm[1]) == 1:
                    msg = ini.GetSetting("Settings", "Private")
                    Player.MessageFrom(sys, red + msg)
                    Player.Disconnect()
                    return