__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""
import Connection
import Player
class AuthEvent:

    GameID = None
    IP = None
    Name = None
    OS = None
    approved = None
    _reason = None
    Connection = Connection


    def Reject(StringReason = "no reason"):
        return