__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import math

"""
    Class
"""


class DeathMSG:

    def DeathMSGConfig(self):
        if not Plugin.IniExists("DeathMSGConfig"):
            loc = Plugin.CreateIni("DeathMSGConfig")
            loc.AddSetting("Settings", "SysName", "Equinox DeathMSG")
            loc.AddSetting("Settings", "SuicideMsgs", "1")
            loc.AddSetting("Settings", "KillMessage", "victim was killed by killer , Damage Caused: dmg , Distance: dist")
            loc.Save()
        return Plugin.GetIni("DeathMSGConfig")

    def On_PlayerDied(self, PlayerDeathEvent):
        attacker = PlayerDeathEvent.Attacker.ToPlayer()
        if PlayerDeathEvent.Victim is not None and attacker.displayName == PlayerDeathEvent.Victim.Name:
            ini = self.DeathMSGConfig()
            suicidemsg = int(ini.GetSetting("Settings", "SuicideMsgs"))
            sysname = ini.GetSetting("Settings", "SysName")
            if suicidemsg == 1:
                victim = PlayerDeathEvent.Victim
                Server.BroadcastFrom(sysname, victim.Name + " suicided...")

        if PlayerDeathEvent.Victim is not None and attacker.displayName != PlayerDeathEvent.Victim.Name:
            ini = self.DeathMSGConfig()
            sysname = ini.GetSetting("Settings", "SysName")
            dmgmsg = ini.GetSetting("Settings", "KillMessage")
            victim = PlayerDeathEvent.Victim
            vloc = victim.Location
            aloc = attacker.transform.position
            dist = round(Util.GetVectorsDistance(vloc, aloc), 2)
            damage = PlayerDeathEvent.DamageAmount
            dmgmsg = dmgmsg.replace("killer", attacker.displayName)
            dmgmsg = dmgmsg.replace("victim", victim.Name)
            dmgmsg = dmgmsg.replace("dmg", str(damage))
            dmgmsg = dmgmsg.replace("dist", str(dist))
            # = dmgmsg.replace("weapon", WEAPONMISSINGOMG)
            Server.BroadcastFrom(sysname, dmgmsg)