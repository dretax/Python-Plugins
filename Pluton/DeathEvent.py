__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

import _info
class DeathEvent:

    _info = _info
    dropLoot = True
    HitBone = ""

    """******************
    *                 *
    * Generic      0  *
    * Hunger       1  *
    * Thirst       2  *
    * Cold         3  *
    * Drowned      4  *
    * Heat         5  *
    * Bleeding     6  *
    * Poison       7  *
    * Suicide      8  *
    * Bullet       9  *
    * Slash        10 *
    * Blunt        11 *
    * Fall         12 *
    * Radiation    13 *
    * Bite         14 *
    * Stab         15 *
    *                 *
    ******************"""

    DamageAmounts = []
    DamageType = None
    Attacker = None
    Weapon = None