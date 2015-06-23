__author__ = 'DreTaX'
__version__ = '1.4'

import clr
import math
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System
from System import *

"""
	Class
"""


class FPSBoost:
    """
        Methods
    """

    name = None
    scooldown = None

    def On_PluginInit(self):
        Util.ConsoleLog("FPSBOOSTER by " + __author__ + " Version: " + __version__ + " loaded.", False)
        DataStore.Flush("FPSBoost")
        ini = self.FPSINI()
        self.name = ini.GetSetting("Settings", "name")
        self.cooldown = int(ini.GetSetting("Settings", "cd"))

    def FPSINI(self):
        if not Plugin.IniExists("FPSBoost"):
            ini = Plugin.CreateIni("FPSBoost")
            ini.AddSetting("Settings", "cd", "10000")
            ini.AddSetting("Settings", "name", "FPSBOOSTER")
            ini.Save()
        return Plugin.GetIni("FPSBoost")

    def SendGraph(self, Player):
        Player.SendCommand("grass.on true")
        Player.SendCommand("grass.forceredraw true")
        Player.SendCommand("grass.displacement false")
        Player.SendCommand("grass.disp_trail_seconds 10")
        Player.SendCommand("grass.shadowcast true")
        Player.SendCommand("grass.shadowreceive true")
        Player.SendCommand("render.level 1")
        Player.SendCommand("render.vsync true")
        Player.SendCommand("footsteps.quality 2")
        Player.SendCommand("gfx.grain true")
        Player.SendCommand("gfx.ssao true")
        Player.SendCommand("gfx.shafts true")
        Player.SendCommand("gfx.damage true")
        Player.SendCommand("gfx.tonemap true")
        Player.SendCommand("gfx.ssaa true")
        Player.SendCommand("gfx.bloom true")
        Player.MessageFrom(self.name, "You Switched to Graphics Mode!")


    def SendFPS(self, Player):
        Player.SendCommand("grass.on false")
        Player.SendCommand("grass.forceredraw False")
        Player.SendCommand("grass.displacement True")
        Player.SendCommand("grass.disp_trail_seconds 0")
        Player.SendCommand("grass.shadowcast False")
        Player.SendCommand("grass.shadowreceive False")
        Player.SendCommand("render.level 0")
        Player.SendCommand("render.vsync False")
        Player.SendCommand("footsteps.quality 2")
        Player.SendCommand("gfx.grain False")
        Player.SendCommand("gfx.ssao False")
        Player.SendCommand("gfx.shafts false")
        Player.SendCommand("gfx.damage false")
        Player.SendCommand("gfx.ssaa False")
        Player.SendCommand("gfx.bloom False")
        Player.SendCommand("gfx.tonemap False")
        Player.MessageFrom(self.name, "You Switched to FPS Mode!")

    def On_Command(self, Player, cmd, args):
        if cmd == "fps":
            time = DataStore.Get("FPSBoost", Player.SteamID)
            if time is None:
                DataStore.Add("FPSBoost", Player.SteamID, System.Environment.TickCount)
                time = 7
            if self.cooldown > 0:
                calc = System.Environment.TickCount - time
                if calc < 0 or math.isnan(calc):
                    DataStore.Add("FPSBoost", Player.SteamID, System.Environment.TickCount)
                    time = 7

                if calc >= self.cooldown or time == 7:
                    DataStore.Add("FPSBoost", Player.SteamID, System.Environment.TickCount)
                    self.SendFPS(Player)
                else:
                    Player.Notice("You have to wait before typing it again!")
                    next = (calc / 1000) / 60
                    last = (self.cooldown / 1000) / 60
                    Player.MessageFrom(self.name, "Time Remaining: " + str(round(next, 2)) + "/" + str(round(last, 2)))
            else:
                self.SendFPS(Player)
        elif cmd == "graph":
            time = DataStore.Get("FPSBoost", Player.SteamID)
            if time is None:
                DataStore.Add("FPSBoost", Player.SteamID, System.Environment.TickCount)
                time = 7
            if self.cooldown > 0:
                calc = System.Environment.TickCount - time
                if calc < 0 or math.isnan(calc):
                    DataStore.Add("FPSBoost", Player.SteamID, System.Environment.TickCount)
                    time = 7
                if calc >= self.cooldown or time == 7:
                    DataStore.Add("FPSBoost", Player.SteamID, System.Environment.TickCount)
                    self.SendGraph(Player)
                else:
                    Player.Notice("You have to wait before typing it again!")
                    next = (calc / 1000) / 60
                    last = (self.cooldown / 1000) / 60
                    Player.MessageFrom(self.name, "Time Remaining: " + str(round(next, 2)) + "/" + str(round(last, 2)))
            else:
                self.SendGraph(Player)

    def On_PlayerConnected(self, Player):
        ini = self.FPSINI()
        name = ini.GetSetting("Settings", "name")
        Player.MessageFrom(name, "Type /fps to increase /graph to decrease your fps.")