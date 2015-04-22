__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

class CraftEvent:
    Crafter = None
    Target = None
    itemCrafter = None
    bluePrint = None
    Cancel = False
    cancelReason = "A plugin stops you from crafting that!"


    def Stop(stringreason = "A plugin stops you from crafting that!"):
        return

    CraftTime = None
    FreeCraft = None