__author__ = 'DreTaX'
__version__ = '1.1'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System
from System import *
import math
import sys

path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

try:
    import random
except ImportError:
    raise ImportError("Failed to import random!")

"""
    Config Starts from here
"""

# Enable timer for airdrop False/True
TimedAirdrop = True
# Airdrop time, 1000 = 1 second | 1800000 = 30 minutes
AirdropTime = 1800000
# Minimum Players
MinPlayers = 15
# Allow commands for mods?
Mods = True
# Whitelisted SteamIDs
WLS = ["SteamIDHere", "SteamID2Here", "SteamID3Here"]
# Cooldown time? 0 to disable | 300000 = 5 minutes
Cooldown = 300000
# Chance for a drop? 0 to disable (1-100)
Chance = 25

#  Colors
blue = "[color #0099FF]"
red = "[color #FF0000]"
pink = "[color #CC66FF]"
teal = "[color #00FFFF]"
green = "[color #009900]"
purple = "[color #6600CC]"
white = "[color #FFFFFF]"
yellow = "[color #FFFF00]"

"""
    End of Config
"""


class Airdrops:

    d = {
        "Hacker Valley South": "5907,-1848",
        "Hacker Mountain South": "5268,-1961",
        "Hacker Valley Middle": "5268,-2700",
        "Hacker Mountain North": "4529,-2274",
        "Hacker Valley North": "4416,-2813",
        "Wasteland North": "3208,-4191",
        "Wasteland South": "6433,-2374",
        "Wasteland East": "4942,-2061",
        "Wasteland West": "3827,-5682",
        "Sweden": "3677,-4617",
        "Everust Mountain": "5005,-3226",
        "North Everust Mountain": "4316,-3439",
        "South Everust Mountain": "5907,-2700",
        "Metal Valley": "6825,-3038",
        "Metal Mountain": "7185,-3339",
        "Metal Hill": "5055,-5256",
        "Resource Mountain": "5268,-3665",
        "Resource Valley": "5531,-3552",
        "Resource Hole": "6942,-3502",
        "Resource Road": "6659,-3527",
        "Beach": "5494,-5770",
        "Beach Mountain": "5108,-5875",
        "Coast Valley": "5501,-5286",
        "Coast Mountain": "5750,-4677",
        "Coast Resource": "6120,-4930",
        "Secret Mountain": "6709,-4730",
        "Secret Valley": "7085,-4617",
        "Factory Radtown": "6446,-4667",
        "Small Radtown": "6120,-3452",
        "Big Radtown": "5218,-4800",
        "Hangar": "6809,-4304",
        "Tanks": "6859,-3865",
        "Civilian Forest": "6659,-4028",
        "Civilian Mountain": "6346,-4028",
        "Civilian Road": "6120,-4404",
        "Ballzack Mountain": "4316,-5682",
        "Ballzack Valley": "4720,-5660",
        "Spain Valley": "4742,-5143",
        "Portugal Mountain": "4203,-4570",
        "Portugal": "4579,-4637",
        "Lone Tree Mountain": "4842,-4354",
        "Forest": "5368,-4434",
        "Rad-Town Valley": "5907,-3400",
        "Next Valley": "4955,-3900",
        "Silk Valley": "5674,-4048",
        "French Valley": "5995,-3978",
        "Ecko Valley": "7085,-3815",
        "Ecko Mountain": "7348,-4100",
        "Zombie Hill": "6396,-3428"
    }

    Vector2s = {

    }

    def On_PluginInit(self):
        DataStore.Flush("AirdropCD")
        for x in self.d.keys():
            v = self.d[x].split(',')
            self.Vector2s[Util.CreateVector2(float(v[0]), float(v[1]))] = x
        self.d.clear()

        if TimedAirdrop:
            Plugin.CreateTimer("AirdropTimer", AirdropTime).Start()

    def AirdropTimerCallback(self, timer):
        timer.Kill()
        if len(Server.Players) >= MinPlayers:
            r = random.randint(1, 100)
            if r <= Chance or Chance == 0:
                World.Airdrop()
            else:
                Server.BroadcastFrom("Military", red + "We failed to drop the Airdrop at a location!")
        else:
            Server.BroadcastFrom("Military", red + "HQ needs atleast " + white + str(MinPlayers) + red
                                 + " soldiers on the ground!")
            Server.BroadcastFrom("Military", red + "We will check back in after " + white + str(AirdropTime / 60000)
                                 + red + " minutes!")
        Plugin.CreateTimer("AirdropTimer", AirdropTime).Start()

    def On_Airdrop(self, Vector3):
        closest = float(999999999)
        loc = Util.CreateVector2(Vector3.x, Vector3.z)
        v = None
        for x in self.Vector2s.keys():
            dist = Util.GetVector2sDistance(loc, x)
            if dist < closest:
                v = x
                closest = dist
        Server.BroadcastFrom("Military", green + "==========================")
        Server.BroadcastFrom("Military", green + "Airdrop is headed to: " + teal + self.Vector2s[v])
        Server.BroadcastFrom("Military", green + "==========================")

    def On_Command(self, Player, cmd, args):
        if cmd == "airdrop":
            if Player.Admin or (Player.Moderator and Mods) or Player.SteamID in WLS:
                if len(args) == 0:
                    Player.Message("Usage: /airdrop here/random")
                    return
                time = DataStore.Get("AirdropCD", "CD")
                if time is None:
                    DataStore.Add("AirdropCD", "CD", 0)
                    time = 0
                calc = System.Environment.TickCount - time
                if calc < 0 or math.isnan(calc) or math.isnan(time):
                    DataStore.Add("AirdropCD", "CD", 0)
                    time = 0
                if calc >= Cooldown or time == 0 or Cooldown == 0:
                    if args[0] == "here":
                        World.AirdropAtPlayer(Player)
                        Player.Notice("\u2708", "Airdrop has been spawned!", 3)
                        DataStore.Add("AirdropCD", "CD", System.Environment.TickCount)
                    elif args[0] == "random":
                        World.Airdrop()
                        Player.Notice("\u2708", "Airdrop has been spawned!", 3)
                        DataStore.Add("AirdropCD", "CD", System.Environment.TickCount)
                else:
                    done = round((calc / 1000) / 60, 2)
                    done2 = round((Cooldown / 1000) / 60, 2)
                    Player.Notice("\u2708", "Cooldown: " + str(done) + "/" + str(done2))
