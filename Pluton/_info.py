__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""

class _info:

    DoHitEffects = True
    damageTypes = None
    Initiator = None
    Weapon = None
    IsPredicting = None
    Predicted = None
    DidHit = None
    HitEntity = None
    HitBone = None
    HitPart = None
    HitMaterial = None
    HitPositionWorld = None
    HitPositionLocal = None
    HitNormalWorld = None
    HitNormalLocal = None
    PointStart = None
    PointEnd = None
    ProjectileID = None
    HitVelocity = None
    material = None
    CanGather = None
    DidGather = None
    hasDamage = None
    isHeadshot = None
    boneName = None

    def LoadFromAttack(Attack, boolserverSide):
        return