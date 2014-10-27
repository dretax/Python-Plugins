__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

import Entity
class EntityLootEvent:
    Target = Entity

    def EntityLootEvent(PlayerLoot, PlayerLooter, LootedEntity):
        return