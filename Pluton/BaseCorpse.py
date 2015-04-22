__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""
import BaseEntity
class BaseCorpse:
    ragdollPrefab = None
    parentEnt = BaseEntity

    def ServerInit(self):
        return

    def InitCorpse(BaseEntity):
        return

    def CanRemove(self):
        return

    def RemoveCorpse(self):
        return

    def ResetRemovalTime(FloatDur):
        return

    def ResetRemovalTime(self):
        return

    def Save(BaseNetworkableSaveInfo):
        return

    def Load(BaseNetworkableLoadInfo):
        return

    def OnAttacked(HitInfo):
        return