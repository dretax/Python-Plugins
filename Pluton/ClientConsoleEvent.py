__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

class ClientConsoleEvent:
    Internal = None
    User = None
    cmd = None
    Args = []
    Reply = None

    def ReplyWith(StringMessage):
        return