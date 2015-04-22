__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""
import World

class Zone2D:

    zoneMesh = None
    zoneMeshFilter = None
    zoneCollider = None

    Name = "uninitalized"
    Verts = None

    min = -50.0
    max = World.Height

    Tris = None
    TrisCount = 0

    def ResetTris(self):
        return

    def ComputeAllTris(self):
        return

    def ComputeSideTris(self):
        return

    def ComputeTopTris(self):
        return

    def ComputeBottomTris(self):
        return

    def Awake(self):
        return

    def UpdateMesh(self):
        return

    def AddPoint(FloatX, FloatZ):
        return

    def AddPoint(FloatX, FloatY, FloatZ):
        return

    def AddPoint(Vector3):
        return

    def Clear(self):
        return

    def Contains(FloatX, FloatZ):
        return

    def Contains(FloatX, FloatY, FloatZ):
        return

    def Contains(Vector3):
        return

    def Draw(self):
        return

    def DrawLine(Vector3From, Vector3To, Color):
        return

    def Serialize(self):
        return