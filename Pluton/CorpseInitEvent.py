__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""
import BaseCorpse
import Entity
class CorpseInitEvent:
    Corpse = BaseCorpse
    Parent = Entity
    def CorpseInitEvent(BaseCorpse, BaseEntity):
        return