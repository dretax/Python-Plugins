__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

class Entity:
    Location = None
    Name = None
    X = None
    Y = None
    Z = None

    baseEntity = None
    Prefab = None
    PrefabID = None

    def Kill(self):
        return

    def IsBuildingPart(self):
        return

    def IsNPC(self):
        return

    def IsPlayer(self):
        return

    def ToBuildingPart(self):
        return

    def ToNPC(self):
        return

    def ToPlayer(self):
        return