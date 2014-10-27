__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

class Server:
        Players = None
        OfflinePlayers = None
        LoadOuts = None
        server_message_name = "Pluton"
        blueprints = None
        ActivePlayers = None
        SleepingPlayers = None

        def Broadcast(StringMessage):
            return

        def BroadcastFrom(StringName, StringMessage):
            return

        def BroadcastNotice(StringMessage):
            return


        def FindPlayer(StringName):
            return


        def FindPlayer(UlongSteamID):
            return


        def GetPlayer(BasePlayer):
            return

        def GetServer(self):
            return

        def CraftingTimeScale(self):
            return

        def ReloadBlueprints(self):
            return

        def LoadLoadouts(self):
            return

        def LoadOfflinePlayers(self):
            return

        def Save(self):
            return

        def SendCommand(StringCommand, BooleanWantsReply = True):
            return

        def OnShutdown(self):
            return