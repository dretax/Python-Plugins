__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

import Entity
import Player
import ItemAmount

class GatherEvent:

    resourceDispenser = None
    Gatherer = Player
    Resource = Entity
    ItemAmount = ItemAmount
    Amount = 1
    origAmount = 1