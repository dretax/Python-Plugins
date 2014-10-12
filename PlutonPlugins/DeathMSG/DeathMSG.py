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
            loc.AddSetting("Settings", "NaturalDies", "1")
            loc.AddSetting("Settings", "SuicideMsg", "victim suicided...")
            loc.AddSetting("Settings", "NaturalMsg", "victim died because of (a) type")
            loc.AddSetting("Settings", "FallMsg", "victim died because he fell off from something")
            loc.AddSetting("Settings", "BledMsg", "victim bled out. He was killed by: killer")
            loc.AddSetting("Settings", "DrownedMsg", "victim Drowned")
            loc.AddSetting("Settings", "ColdMsg", "victim Caught Cold, and died.")
            loc.AddSetting("Settings", "XyzMsg", "victim died by unknown type called Generic?!")
            loc.AddSetting("Settings", "KillMessage", "victim was killed by killer | Damage Caused: dmg | Distance: dist | Killed with: weapon")
            loc.Save()
        return Plugin.GetIni("DeathMSGConfig")

    def On_PluginInit(self):
        self.DeathMSGConfig()

    def IsNatural(self, type):
        if type == "Bite" or type == "BluntTrauma" or type == "Heat" or type == "Hunger" or type == "Radiation" or type == "Thirst":
            return True
        return False

    def On_PlayerDied(self, PlayerDeathEvent):
        attacker = PlayerDeathEvent.Attacker.ToPlayer()
        if PlayerDeathEvent.Victim is not None and attacker.displayName == PlayerDeathEvent.Victim.Name:
            ini = self.DeathMSGConfig()
            NaturalDies = int(ini.GetSetting("Settings", "NaturalDies"))
            sysname = ini.GetSetting("Settings", "SysName")
            if NaturalDies == 1:
                victim = PlayerDeathEvent.Victim
                type = str(PlayerDeathEvent.DamageType)
                if self.IsNatural(type):
                    ntrmsg = ini.GetSetting("Settings", "NaturalMsg")
                    ntrmsg = ntrmsg.replace("victim", victim.Name)
                    ntrmsg = ntrmsg.replace("type", type)
                    Server.BroadcastFrom(sysname, ntrmsg)
                elif type == "Generic":
                    cmsg = ini.GetSetting("Settings", "XyzMsg")
                    cmsg = cmsg.replace("victim", victim.Name)
                    Server.BroadcastFrom(sysname, cmsg)
                elif type == "Suicide":
                    smsg = ini.GetSetting("Settings", "SuicideMsg")
                    smsg = smsg.replace("victim", victim.Name)
                    Server.BroadcastFrom(sysname, smsg)
                elif type == "Fall":
                    fmsg = ini.GetSetting("Settings", "FallMsg")
                    fmsg = fmsg.replace("victim", victim.Name)
                    Server.BroadcastFrom(sysname, fmsg)
                elif type == "Drowned":
                    dmsg = ini.GetSetting("Settings", "DrownedMsg")
                    dmsg = dmsg.replace("victim", victim.Name)
                    Server.BroadcastFrom(sysname, dmsg)
                elif type == "Cold":
                    cmsg = ini.GetSetting("Settings", "ColdMsg")
                    cmsg = cmsg.replace("victim", victim.Name)
                    Server.BroadcastFrom(sysname, cmsg)

        if PlayerDeathEvent.Victim is not None and attacker.displayName != PlayerDeathEvent.Victim.Name:
            ini = self.DeathMSGConfig()
            sysname = ini.GetSetting("Settings", "SysName")
            dmgmsg = ini.GetSetting("Settings", "KillMessage")
            victim = PlayerDeathEvent.Victim
            type = str(PlayerDeathEvent.DamageType)
            if type == "Bullet" or type == "Slash":
                weapon = PlayerDeathEvent._info.Weapon.info.displayName
                #bodypart = PlayerDeathEvent._info.HitPart
                vloc = victim.Location
                aloc = attacker.transform.position
                dist = round(Util.GetVectorsDistance(vloc, aloc), 2)
                damage = PlayerDeathEvent.DamageAmount
                dmgmsg = dmgmsg.replace("killer", attacker.displayName)
                dmgmsg = dmgmsg.replace("victim", victim.Name)
                dmgmsg = dmgmsg.replace("dmg", str(damage))
                dmgmsg = dmgmsg.replace("dist", str(dist))
                dmgmsg = dmgmsg.replace("weapon", str(weapon))
                #TODO: Write a list of the body part numbers.
                #dmgmsg = dmgmsg.replace("bpart", str(bodypart))
                Server.BroadcastFrom(sysname, dmgmsg)
            elif type == "Bleeding":
                bmsg = ini.GetSetting("Settings", "BledMsg")
                bmsg = bmsg.replace("victim", victim.Name)
                bmsg = bmsg.replace("killer", attacker.displayName)
                Server.BroadcastFrom(sysname, bmsg)