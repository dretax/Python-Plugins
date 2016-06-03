# coding=utf-8
__author__ = 'Mike, Converted by DreTaX'
__version__ = '1.5'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

JZapDB = 'JZap'
"""
    Class
"""

emon = '[color#FFA500]'
noem = '[color#FFFFFF]'


class JZap:

    """
        Methods
    """

    def isMod(self, id):
        if DataStore.ContainsKey('Moderators', id):
            return True
        return False

    def AllStuff(self, OwnerID):
        arr = World.Entities.ToArray()
        return [e for e in arr if e.UOwnerID == OwnerID]

    """
        Events
    """

    def On_PluginInit(self):
        DataStore.Flush(JZapDB)
        Plugin.CommandList.Add(JZapDB.lower())

    def On_Command(self, Player, cmd, args):
        if cmd == JZapDB.lower():
            if not Player.Admin and not Player.Moderator:
                Player.Message("You aren't an admin.")
                return
            get = DataStore.Get(JZapDB, 'Active')
            if get is not None and get != Player.UID:
                Player.MessageFrom('☒ ', 'Wait a moment, someone else is zapping stuff.')
                return
            elif get != Player.UID:
                DataStore.Add(JZapDB, 'Active', Player.UID)
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
        if "NPC" in str(he.Attacker):
            return
        if he.Entity.Health > 0:
            if not he.Attacker.Admin and not he.Attacker.Moderator:
                return
            if not Server.HasRustPP:
                return
            dict = Server.GetRustPPAPI().Cache
            if not dict.ContainsKey(long(he.Entity.UOwnerID)):
                name = "UnKnown"
            else:
                name = dict[he.Entity.UOwnerID]
            if OwnerID is None and DataStore.Get(JZapDB, 'Active') == he.Attacker.UID:
                DataStore.Add(JZapDB, 'Target', he.Entity.UOwnerID)
                he.Attacker.MessageFrom('☑ ', 'This thing belongs to  ' + emon + str(name) +
                                        noem + ' (' + he.Entity.OwnerID + ').')
                he.Attacker.MessageFrom('☑ ☑ ', 'Hit it once more to zap  ' + emon + name + '\'s' +
                                        noem + '  stuff completely off the map.')
                return
            elif OwnerID == he.Entity.UOwnerID:
                DataStore.Flush(JZapDB)
                stuff = self.AllStuff(OwnerID)
                for e in stuff:
                    try:
                        e.Destroy()
                    except:
                        pass
                he.Attacker.MessageFrom('☑ ☑ ☑ ', emon + str(len(stuff)) + noem + '  objects were zapped.')
                he.Attacker.Notice('☠', name.upper() + '\'S RUST STUFF\'S DUST!', 10)
                he.Attacker.InventoryNotice(JZapDB + ' is de-activated!')
                return
