__author__ = 'DreTaX'
__version__ = '1.1'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System

"""
    Class
"""

class C4Log:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("C4Log by" + __author__ + " Version: " + __version__ + " loaded.", False)


    def C4Log(self):
        if not Plugin.IniExists("C4Log"):
            ini = Plugin.CreateIni("C4Log")
            ini.AddSetting("C4Log")
            ini.Save()
        return Plugin.GetIni("C4Log")

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            #On Entity hurt the attacker is an NPC and a Player for some reason. We will try to grab his ID
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            if HurtEvent.Entity.IsStructure() or HurtEvent.Entity.IsDeployableObject():
                bleed = HurtEvent.DamageType
                if bleed == "Explosion":
                    ini = self.C4Log()
                    cexist = ini.GetSetting("C4Log", str(HurtEvent.Attacker.Location))
                    gexist = ini.GetSetting("GrenadeLog", str(HurtEvent.Attacker.Location))
                    if HurtEvent.DamageAmount == 600:
                        if cexist is not None:
                            return
                        ini.AddSetting("C4Log", str(HurtEvent.Attacker.Location), HurtEvent.Attacker.Name + "|" + str(System.DateTime.Now) + "| C4")
                        ini.Save()
                    elif HurtEvent.DamageAmount < 100 and HurtEvent.DamageAmount > 60:
                        if gexist is not None:
                            return
                        ini.AddSetting("GrenadeLog", str(HurtEvent.Attacker.Location) , HurtEvent.Attacker.Name + "|" + str(System.DateTime.Now) + "| Grenade")
                        ini.Save()