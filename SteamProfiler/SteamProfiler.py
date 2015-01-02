__author__ = 'DreTaX'
__version__ = '1.1'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

"""
    Class
"""

red = "[color #FF0000]"
class SteamProfiler:

    APIKey = None
    AllowShared = None
    AllowVACBanned = None
    AllowedVACBans = None
    MinimumDays = None
    CheckOnlyRust = None
    CheckForPrivate = None
    CheckForNoProfile = None
    sys = None
    Debug = None

    def On_PluginInit(self):
        Util.ConsoleLog("SteamProfiler by " + __author__ + " Version: " + __version__ + " loaded.", False)
        ini = self.Ini()
        self.APIKey = ini.GetSetting("Settings", "APIKey")
        self.AllowShared = int(ini.GetSetting("Settings", "AllowShared"))
        self.AllowVACBanned = int(ini.GetSetting("Settings", "AllowVACBanned"))
        self.AllowedVACBans = int(ini.GetSetting("Settings", "AllowedVACBans"))
        self.MinimumDays = int(ini.GetSetting("Settings", "MinimumDays"))
        self.CheckOnlyRust = int(ini.GetSetting("Settings", "CheckForOnlyRust"))
        self.CheckForPrivate = int(ini.GetSetting("Settings", "CheckForPrivate"))
        self.CheckForNoProfile = int(ini.GetSetting("Settings", "CheckForNoProfile"))
        self.sys = ini.GetSetting("Settings", "Sys")
        self.Debug = int(ini.GetSetting("Settings", "Debug"))

    def Ini(self):
        if not Plugin.IniExists("Ini"):
            ini = Plugin.CreateIni("Ini")
            ini.AddSetting("Settings", "APIKey", "http://steamcommunity.com/dev/apikey")
            ini.AddSetting("Settings", "AllowShared", "0")
            ini.AddSetting("Settings", "AllowVACBanned", "0")
            ini.AddSetting("Settings", "AllowedVACBans", "2")
            ini.AddSetting("Settings", "MinimumDays", "300")
            ini.AddSetting("Settings", "CheckForOnlyRust", "1")
            ini.AddSetting("Settings", "CheckForPrivate", "1")
            ini.AddSetting("Settings", "CheckForNoProfile", "1")
            ini.AddSetting("Settings", "Sys", "SteamProfiler")
            ini.AddSetting("Settings", "UsingShared", "You are using shared RUST. It's not allowed.")
            ini.AddSetting("Settings", "VacBans", "You reached the max number of VAC bans.")
            ini.AddSetting("Settings", "OnlyRust", "People only having Rust are not allowed to join.")
            ini.AddSetting("Settings", "NoProfile", "Only People who have setup their community profile can join.")
            ini.AddSetting("Settings", "Private", "Only People who are having public profile can join.")
            ini.AddSetting("Settings", "Debug", "1")
            ini.Save()
        return Plugin.GetIni("Ini")

    def Log(self, String):
        if self.Debug == 0:
            return
        Plugin.Log("Debug", str(String))

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

    def RunRequest(self, Player, id):
        ini = self.Ini()
        self.Log("ID: " + str(id) + " Name: " + str(Player.Name))
        if self.AllowShared == 0:
            t = True
            try:
                url = Web.GET("http://api.steampowered.com/IPlayerService/IsPlayingSharedGame/v0001/?key=" + self.APIKey + "&steamid=" + id + "&appid_playing=252490")
            except:
                t = False
            if t:
                data = self.GetSteamDatas(url, 1)
                self.Log("Data: " + str(data) + " Number which should be NOT 0, so It would kick players: " +str(data[1]))
                if int(data[1]) != 0:
                    msg = ini.GetSetting("Settings", "UsingShared")
                    Player.MessageFrom(self.sys, red + msg)
                    Player.Disconnect()
                    return
        if self.AllowVACBanned == 0:
            t = True
            try:
                url = Web.GET("http://api.steampowered.com/ISteamUser/GetPlayerBans/v0001/?key=" + self.APIKey + "&steamids=" + id)
            except:
                t = False
            if t:
                data = self.GetSteamDatas(url, 2)
                numv = data[3].split(':')
                numv = int(numv[1])
                ldays = data[4].split(':')
                ldays = int(ldays[1])
                self.Log("Data2: " + str(data) + " | " + str(numv) + " | " + str(ldays))
                if (numv > self.AllowedVACBans and ldays < self.MinimumDays) or self.MinimumDays == 0:
                    msg = ini.GetSetting("Settings", "VacBans")
                    Player.MessageFrom(self.sys, red + msg)
                    Player.Disconnect()
                    return
        if self.CheckOnlyRust == 1:
            t = True
            try:
                url = Web.GET("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + self.APIKey + "&steamid=" + id)
            except:
                t = False

            if t:
                listofappids = re.findall(r'"appid":.*,', url)
                gamecount = re.findall(r'"game_count":.*,', url)
                gamecount = re.sub('["\,\ \'\[\]]', '', str(gamecount)).split(':')
                self.Log("Data3: " + str(listofappids) + " | " + str(gamecount) + " | " + str(gamecount[1]))
                if int(gamecount[1]) == 1 and "252490" in listofappids:
                    msg = ini.GetSetting("Settings", "OnlyRust")
                    Player.MessageFrom(self.sys, red + msg)
                    Player.Disconnect()
                    return
        if self.CheckForPrivate == 1 or self.CheckForNoProfile == 1:
            t = True
            try:
                url = Web.GET("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + self.APIKey + "&steamids=" + id)
            except:
                t = False
            if not t:
                return
            if self.CheckForNoProfile == 1:
                comm = re.findall(r'"profilestate":.*,', url)
                comm = re.sub('["\,\ \'\[\]]', '', str(comm)).split(':')
                self.Log("Data4: " + str(comm))
                if int(comm[1]) != 1:
                    msg = ini.GetSetting("Settings", "NoProfile")
                    Player.MessageFrom(self.sys, red + msg)
                    Player.Disconnect()
                    return
            if self.CheckForPrivate == 1:
                comm = re.findall(r'"communityvisibilitystate":.*,', url)
                comm = re.sub('["\,\ \'\[\]]', '', str(comm)).split(':')
                self.Log("Data5: " + str(comm) + " | " + str(comm[1]))
                if int(comm[1]) == 1:
                    Plugin.Log("Check", Player.Name + "'s  void went forward at the check. He should be disconnected?!")
                    msg = ini.GetSetting("Settings", "Private")
                    Player.MessageFrom(self.sys, red + msg)
                    Player.Disconnect()
                    return

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        if self.APIKey == "http://steamcommunity.com/dev/apikey":
            return
        self.RunRequest(Player, id)