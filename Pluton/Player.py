__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

import BasePlayer
class Player:
    GameID = None

    def OnPlayerDeserialized(StreamingContext):
        return

    def Find(stringnameOrSteamidOrIP):
        return

    def FindByGameID(ulongsteamID):
        return

    def FindBySteamID(stringsteamID):
        return

    def Ban(stringreason = "no reason"):
        return

    def Kick(stringreason = "no reason"):
        return

    def Reject(stringreason = "no reason"):
        return

    def GetLookPoint(FloatMaxDist = 500):
        return

    def GetLookHit(FloatMaxDist = 500, intLayers = ""):
        return

    def GetLookPlayer(FloatMaxDist = 500):
        return

    def GetLookBuildingPart(FloatMaxDist = 500):
        return

    def Kill(self):
        return

    def KnowsBlueprint(intItemID):
        return

    def KnowsBlueprint(ItemBlueprint):
        return

    def KnowsBlueprint(ItemDefinition):
        return

    def KnowsBlueprints(itemIDs):
        return

    def KnowsBlueprints(itemBPs):
        return

    def KnowsBlueprints(itemdefs):
        return

    def KnownBlueprints(self):
        return

    def LearnBlueprint(intItemID):
        return

    def LearnBlueprint(ItemBlueprint):
        return

    def LearnBlueprint(ItemDefinition):
        return

    def LearnBlueprints(itemIDs):
        return

    def LearnBlueprints(itembps):
        return

    def LearnBlueprints(itemdefs):
        return

    def MakeNone(stringreason = "no reason"):
        return

    def MakeModerator(stringreason = "no reason"):
        return

    def MakeOwner(stringreason = "no reason"):
        return

    def Message(stringmsg):
        return

    def MessageFrom(stringfrom, stringmsg):
        return

    def ConsoleMessage(stringmsg):
        return

    def IsPlayer(self):
        return True

    def SendConsoleCommand(stringcmd):
        return

    def GroundTeleport(floatX, floatY, floatZ):
        return

    def GroundTeleport(Vector3):
        return

    def Teleport(Vector3):
        return

    worldSizeHalf = None
    firstLocations = []

    def Teleport(floatX, floatY, floatZ):
        return


    Admin = None
    AuthStatus = None
    basePlayer = BasePlayer
    Health = None
    Inventory = None
    IP = None
    IsWounded = None
    Location = None
    Moderator = None
    Name = None
    Offline = None
    Owner = None
    OS = None
    Ping = None
    Stats = None
    SteamID = None
    TimeOnline = None
    Teleporting = None