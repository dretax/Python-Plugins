__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

Players = []

class HighPing:

    Timer = None
    MaxPing = None

    def On_PluginInit(self):
        ini = self.PingConfig()
        self.Timer = int(ini.GetSetting("Settings", "Timer"))
        self.MaxPing = int(ini.GetSetting("Settings", "MaxPing"))
        Plugin.CreateTimer("PingCheck", self.Timer).Start()

    def PingConfig(self):
        if not Plugin.IniExists("PingConfig"):
            ini = Plugin.CreateIni("PingConfig")
            ini.AddSetting("Settings", "MaxPing", "250")
            ini.AddSetting("Settings", "Timer", "120000")
            ini.Save()
        return Plugin.GetIni("PingConfig")

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        Players.append(Player)

    def On_PlayerDisconnected(self, Player):
        try:
            Players.remove(Player)
        except:
            pass

    def PingCheckCallback(self):
        Plugin.KillTimer("PingCheck")
        for pl in Players:
            if int(pl.Ping) >= self.MaxPing:
                pl.MessageFrom("[High Ping Kicker]", "[color#FF2222]Your Ping: " + str(pl.Ping) + " Maximum you can have: " + str(self.MaxPing) +".")
                pl.Disconnect()
        Plugin.CreateTimer("PingCheck", self.Timer).Start()