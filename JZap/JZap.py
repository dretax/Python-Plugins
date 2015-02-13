# coding=utf-8
__author__ = 'Mike, Converted by DreTaX'
__version__ = '1.2'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System

JZapDB = 'JZap'
"""
    Class
"""


class JZap:
    """
        Methods
    """

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def isMod(self, id):
        if DataStore.ContainsKey('Moderators', id):
            return True
        return False

    def Players(self):
        if not Plugin.IniExists('Players'):
            ini = Plugin.CreateIni('Players')
            ini.Save()
        return Plugin.GetIni('Players')

    def AllStuff(self, OwnerID):
        arr = World.Entities.ToArray()
        return [e for e in arr if long(e.OwnerID) == long(OwnerID)]

    """
        Events
    """

    def On_ServerShutdown(self):
        DataStore.Flush(JZapDB)


    def On_ServerInit(self):
        DataStore.Flush(JZapDB)


    def On_PluginInit(self):
        try:
            DataStore.Flush(JZapDB)
        except:
            pass


    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        ini = self.Players()
        if ini.GetSetting('List', id) is not None:
            ini.SetSetting('List', id, Player.Name)
            ini.Save()
            return
        ini.AddSetting('List', id, Player.Name)
        ini.Save()


    def On_Command(self, Player, cmd, args):
        if cmd.upper() == JZapDB.upper():
            if not Player.Admin and not self.isMod(Player.SteamID):
                Player.Message("You aren't an admin.")
                return
            get = DataStore.Get(JZapDB, 'Active')
            if get is not None and get != Player.SteamID:
                Player.MessageFrom('☒ ', 'Wait a moment, someone else is zapping stuff.')
                return
            elif get != Player.SteamID:
                DataStore.Add(JZapDB, 'Active', Player.SteamID)
                Player.InventoryNotice(JZapDB + ' is activated!')
            else:
                DataStore.Flush(JZapDB)
                Player.InventoryNotice(JZapDB + ' is de-activated!')



    def On_EntityHurt(self, he):
        if DataStore.Get(JZapDB, 'Active') is None:
            return
        if he.Attacker is None or he.Entity is None or he.IsDecay:
            return
        OwnerID = DataStore.Get(JZapDB, 'Target')
        emon = '[color#FFA500]'
        noem = '[color#FFFFFF]'
        id = self.TrytoGrabID(he.Attacker)
        if id is None:
            return
        if he.Entity.Health > 0:
            if not he.Attacker.Admin and not self.isMod(he.Attacker.SteamID):
                return
            ini = self.Players()
            name = ini.GetSetting('List', he.Entity.OwnerID)
            if name is None:
                name = "UnKnown"
            if OwnerID is None and long(DataStore.Get(JZapDB, 'Active')) == long(he.Attacker.SteamID):
                DataStore.Add(JZapDB, 'Target', he.Entity.OwnerID)
                he.Attacker.MessageFrom('☑ ', 'This thing belongs to  ' + emon + str(name) + noem + ' (' + he.Entity.OwnerID + ').')
                he.Attacker.MessageFrom('☑ ☑ ', 'Hit it once more to zap  ' + emon + name + '\'s' + noem + '  stuff completely off the map.')
                return
            elif long(OwnerID) == long(he.Entity.OwnerID):
                DataStore.Flush(JZapDB)
                stuff = self.AllStuff(OwnerID)
                for e in stuff:
                    try:
                        if e.Object.gameObject is not None and e.Health > 0:
                            if e.IsStructure():
                                e.Destroy()
                        else:
                            Util.DestroyObject(e.Object.gameObject)
                    except:
                        pass
                he.Attacker.MessageFrom('☑ ☑ ☑ ', emon + str(len(stuff)) + noem + '  objects were zapped.')
                he.Attacker.Notice('☠', name.upper() + '\'S RUST STUFF\'S DUST!', 10)
                he.Attacker.InventoryNotice(JZapDB + ' is de-activated!')
                return
            DataStore.Flush(JZapDB)  # just in case. should never reach this