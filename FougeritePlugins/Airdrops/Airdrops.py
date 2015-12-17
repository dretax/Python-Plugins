__author__ = 'DreTaX'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

# Enable timer for airdrop False/True
TimedAirdrop = True
# Airdrop time, 1000 = 1 second | 1800000 = 30 minutes
AirdropTime = 1800000
# Minimum Players
MinPlayers = 15


class Airdrops:

    def On_PluginInit(self):
        if TimedAirdrop:
            Plugin.CreateTimer("AirdropTimer", AirdropTime).Start()

    def AirdropTimerCallback(self, timer):
        timer.Kill()
        if len(Server.Players) >= MinPlayers:
            Server.BroadcastFrom("Military", "==========================")
            Server.BroadcastFrom("Military", "Airdrop is on the way!")
            Server.BroadcastFrom("Military", "==========================")
            World.Airdrop()
        else:
            Server.BroadcastFrom("Military", "HQ needs atleast " + str(MinPlayers) + " soldiers on the ground!")
            Server.BroadcastFrom("Military", "We will check back in after " + str(AirdropTime / 60000) + " minutes!")
        Plugin.CreateTimer("AirdropTimer", AirdropTime).Start()

    def On_Command(self, Player, cmd, args):
        if cmd == "airdrop":
            if Player.Admin or Player.Moderator:
                if len(args) == 0:
                    return
                if args[0] == "here":
                    World.AirdropAtPlayer(Player)
                    Player.Notice("\u2708", "Airdrop has been spawned!", 3)
                elif args[0] == "random":
                    World.Airdrop()
                    Player.Notice("\u2708", "Airdrop has been spawned!", 3)
