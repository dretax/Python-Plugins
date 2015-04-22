__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

import NPC
import _info

class NPCDeathEvent:
    Victim = NPC
    _info = _info
    dropLoot = True
    HitBone = None
    DamageAmounts = []
    DamageType = None
    Attacker = None
    Weapon = None