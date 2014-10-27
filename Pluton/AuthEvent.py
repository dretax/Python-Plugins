__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    This file is for API showoff only, and nothing else.
"""

class AuthEvent:

    GameID = None
    IP = None
    Name = None
    OS = None

    def Reject(StringReason = "no reason"):
        return