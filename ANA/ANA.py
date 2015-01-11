__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

RandNames = []

import sys
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

Lib = True
try:
    import random
except ImportError:
    Lib = False


class ANA:

    def On_PluginInit(self):
        Util.ConsoleLog("Anti Non ASCII by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def GetRand(self):
        d = random.randrange(0, 550)
        while d in RandNames:
            d = random.randrange(0, 550)
        RandNames.append(d)
        return d

    def CutName(self, string):
        name = re.sub(r'[^\x00-\x7F]+', '', string)
        return name

    def Replace(self, Old, To, Text):
        return re.sub('(?i)' + re.escape(Old), lambda m: To, Text)

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        name = Player.Name
        name = re.sub(' +',' ', name)
        name = re.sub('[\t]+','', name)
        starts = name.startswith(' ')
        ends = name.endswith(' ')
        if starts is True:
            name = name.replace(name[0], '')
        if ends is True:
            n = len(name)
            name = name.replace(name[n-1], '')
        a = re.match('^[a-zA-Z0-9_!+?()<>/@#,. \[\]\\-]+$', name)
        if not a:
            name = re.sub('^[a-zA-Z0-9_!+?()<>/@#,. \[\]\\-]+$', "", name)
        n = len(name)
        if n <= 1:
            name = "Stranger"
            if Lib:
                rand = self.GetRand()
                name = name + str(rand)
        Player.Name = name