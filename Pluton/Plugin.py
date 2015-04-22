__author__ = 'DreTaX'
__version__ = '1.0'

"""
    This file was created for plugin developers to be able to use the correct functions
    without looking at the wiki or the api.
    API showoff purposes only, and nothing else.
"""
import Ini
class Plugin:
    LibPath = None

    def Invoke(func, obj):
        """
        -Runs a method in another Plugin.
        :param func: String Function Name
        :param obj: Object Plugin
        :return: None
        """
        return

    def NormalizePath(StringPath):
        return

    def FormatException(Exception):
        return

    def ValidateRelativePath(StringPath):
        return

    def CreateDir(StringPath):
        return

    def DeleteLog(StringPath):
        return

    def Log(StringPath, StringText):
        return

    def GetIni(StringPath):
        return Ini

    def IniExists(StringPath):
        return

    def CreateIni(StringPathOrName):
        return

    def GetInis(StringPath):
        return

    def GetPlugin(StringName):
        return

    def GetDate(self):
        return

    def GetTicks(self):
        return

    def GetTime(self):
        return

    def GetTimestamp(self):
        return

    def CreateTimer(Name, timeoutDelay):
        return

    def CreateTimer(StringName, timeoutDelay, Dictionary):
        return

    def GetTimer(StringName):

        return

    def KillTimer(StringName):
        return

    def KillTimers(self):
        return

    def CreateParallelTimer(StringName, timeoutDelay, Dictionary):
        return

    def GetParallelTimer(StringName):
        return

    def KillParallelTimer(StringName):
        return

    def GET(StringUrl):
        return

    def POST(StringUrl, StringData):
        return

    def POSTJSON(StringUrl, StringJson):
        return

    def CreateDict(IntCapacity = 10):
        return