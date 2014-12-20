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
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay and HurtEvent.DamageType is not None:
            #On Entity hurt the attacker is an NPC and a Player for some reason. We will try to grab his ID
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            if HurtEvent.Entity.IsStructure() or HurtEvent.Entity.IsDeployableObject():
                if HurtEvent.DamageType == "Explosion":
                    if HurtEvent.WeaponName == "Explosive Charge":
                        Plugin.Log("C4", str(HurtEvent.Attacker.Location) + " | " + HurtEvent.Attacker.Name)
                    else:
                        Plugin.Log("Grenade", str(HurtEvent.Attacker.Location) + " | " +  HurtEvent.Attacker.Name)