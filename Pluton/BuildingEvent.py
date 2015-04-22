__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

import Player
import BuildingPart

class BuildingEvent:
    BuildingPart = BuildingPart
    Builder = Player
    Construction = None
    Target = None
    NeedsValidPlacement = None

    DestroyReason = ""
    DoDestroy = False

    def Destroy(reason = "Plugin blocks building!"):
        return