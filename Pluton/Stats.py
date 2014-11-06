__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""


class Stats:
    Kills = None
    Deaths = None
    PlayerKills = None
    PlayerDeaths = None
    NPCKills = None
    NPCDeaths = None
    TotalDamageTaken = None
    TotalDamageDone = None
    DamageToPlayers = None
    DamageFromPlayers = None
    DamageToNPCs = None
    DamageFromNPCs = None
    DamageToEntities = None
    FallDamage = None

    def PlayerStats(StringSteamid):
        return

    def AddKill(BooleanPlayer, BooleanNpc):
        return

    def AddDeath(BooleanPlayer, BooleanNpc):
        return

    def AddDamageFrom(FloatDmgAmount, BooleanPlayer, BooleanNpc, BooleanFall):
        return

    def AddDamageTo(FloatDmgAmount, BooleanPlayer, BooleanNpc, BooleanEntity):
        return