__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""


class World:

    ResourceGatherMultiplier = 1.0
    freezeTimeTimer = None
    frozenTime = -1
    Time = None
    Timescale = None

    def AttachParachute(Player):
        return

    def AttachParachute(BaseEntity):
        return

    def AirDrop(self):
        return

    def AirDrop(FloatSpeed, FloatHeight = 400):
        return

    def AirDropAt(Vector3Position, FloatSpeed = 50, FloatHeight = 400):
        return

    def AirDropAt(FloatX, FloatY, FloatZ, FloatSpeed = 50, FloatHeight = 400):
        return

    def AirDropAtPlayer(Player, FloatSpeed = 50, FloatHeight = 400):
        return

    def GetGround(FloatX, FloatZ):
        return

    def GetGround(Vector3):
        return

    def GetPrefabNames(self):
        return

    def SpawnMapEntity(StringName, FloatX, FloatZ):
        return

    def SpawnMapEntity(StringName, Vector3):
        return

    def SpawnMapEntity(StringName, Vector3, Quaternion):
        return

    def SpawnMapEntity(StringName, FloatX, FloatY, FloatZ):
        return

    def SpawnAnimal(StringName, FloatX, FloatZ):
            return

    def SpawnAnimal(StringName, Vector3):
        return

    def SpawnEvent(StringEVT, FloatX, FloatZ):
        return

    def SpawnEvent(StringEVT, Vector3):
        return

    def SpawnEvent(StringEVT, FloatX, FloatY, FloatZ):
        return

    def SpawnAnimal(StringName, FloatX, FloatY, FloatZ):
        return

    def SpawnMapEntity(StringName, FloatX, FloatY, FloatZ, Quaternion):
        return

    def FreezeTime(self):
        return

    def Freeze(ObjectSender, ElapsedEventArgs):
        return

    def UnFreezeTime(self):
        frozenTime = -1

    def Initialize(self):
        return

    def CheckDependencies(self):
        return True

    def GetWorld(self):
        Instance = None
        return Instance

    list = None
    def PrintPrefabs(self):
        return