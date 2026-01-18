__author__ = 'DreTaX'
__version__ = '1.0'
__about__ = 'This plugin re-spawns all sleepers during server load.'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

# Enable debug logging of failed sleeper spawns False/True
# Sleeper spawn may fail if the player is dead, or not existent, etc.
EnableSleeperSpawnLogging = False

class SleeperSpawner:

    """
        Methods
    """

    def On_ServerLoaded(self):
        sleeperSteamIds = PlayerCache.CachedPlayers.KeysCopy
        for i in xrange(len(sleeperSteamIds)):
            steamID = sleeperSteamIds[i]
            success = World.ManuallySpawnSleeper(steamID)
            if EnableSleeperSpawnLogging and not success:
                Plugin.Log("FailedSleepers.txt", "Failed to spawn sleeper for SteamID: " + str(steamID))