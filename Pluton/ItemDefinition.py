__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""
import Rarity

class ItemDefinition:
    itemid = 0
    shortname = ""
    displayName = None
    displayDescription = None
    iconSprite = None
    category = None
    stackable = 0
    rarity = Rarity
    condition = None
    worldModel = None