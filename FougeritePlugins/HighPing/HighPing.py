__author__ = 'DreTaX'
__version__ = '1.2'
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

    def On_PlayerConnected(self, Player):
        Players.append(Player)

    def On_PlayerDisconnected(self, Player):
        if Player in Players:
            Players.remove(Player)

    def PingCheckCallback(self, timer):
        timer.Kill()
        for pl in Players:
            if pl.IsOnline:
                if int(pl.Ping) >= self.MaxPing:
                    pl.MessageFrom("[High Ping Kicker]", "[color#FF2222]Your Ping: " + str(pl.Ping) +
                                   " Maximum you can have: " + str(self.MaxPing) + ".")
                    pl.Disconnect()
        Plugin.CreateTimer("PingCheck", self.Timer).Start()