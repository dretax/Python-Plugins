__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    This file is for API showoff only, and nothing else.
"""

import Player

class PlayerHurtEvent:
    Victim = Player
    DamageAmount = None
    DamageType = None
    Attacker = None
    Weapon = None


    def PlayerHurtEvent(Player, HitInfo):
       return