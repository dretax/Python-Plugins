__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

import Player
import _info

class PlayerDeathEvent:
    _info = _info
    Victim = Player
    DamageAmounts = []
    DamageType = None
    Attacker = None
    Weapon = None