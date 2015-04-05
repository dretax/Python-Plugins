__author__ = 'DreTaX'
__version__ = '1.1'

import clr
clr.AddReferenceByPartialName("Pluton")
import Pluton, datetime
path = Util.GetPublicFolder()

class DestroyLog:

    def On_PluginInit(self):
        Plugin.CreateDir(path + "\\Plugins\\DestroyLog\\Logs")

    def On_CombatEntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None:
            attacker = str(HurtEvent.Attacker.Name)
            if HurtEvent.Weapon is not None:
                weapon = str(HurtEvent.Weapon.Name)
                id = HurtEvent.Attacker.SteamID
                ip = HurtEvent.Attacker.IP
                loc = str(HurtEvent.Attacker.Location)
            else:
                weapon = "Null Weapon"
                id = "None"
                ip = "None"
                loc = "None"
            type = str(HurtEvent.DamageType)
            if type == "Stab" or type == "Bullet" or type == "Slash" or type == "Explosion":
                try:
                    h = HurtEvent.Victim.Health
                except:
                    return
                for x in HurtEvent.DamageAmounts:
                    if x > h:
                        Plugin.Log(path + "\\Plugins\\DestroyLog\\Logs\\" + str(datetime.date.today()), HurtEvent.Victim.Name +
                            " | " + str(HurtEvent.Victim.Location) +
                            " | " + weapon + " | " + attacker +
                            " | " + loc + " | " + id + " | " + ip)
                        break