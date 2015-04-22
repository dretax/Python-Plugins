__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

import Player
class DoorCodeEvent:
    #todo needs fix in pluton
    codeLock = None
    msg = None
    doorCode = None
    Player = Player
    CodeEntered = None

    def IsCorrect(self):
        return

    def Deny(self):
        return