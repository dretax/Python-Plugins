__author__ = 'DreTaX'
__version__ = '1.5'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import math
import System
from System import *

"""
    Class
"""


class DeathMSG:
    BodyParts = {'2801294865': 'Head', '3847415609': 'Hand', '2881065196': 'Body', '3847102050': 'Legs', '2868606315': 'Foot'}

    def DeathMSGConfig(self):
        if not Plugin.IniExists("DeathMSGConfig"):
            loc = Plugin.CreateIni("DeathMSGConfig")
            loc.AddSetting("Settings", "SysName", "Equinox DeathMSG")
            loc.AddSetting("Settings", "NaturalDies", "1")
            loc.AddSetting("Settings", "KillLog", "1")
            loc.AddSetting("Settings", "SuicideMsg", "victim suicided...")
            loc.AddSetting("Settings", "NaturalMsg", "victim died because of (a) type")
            loc.AddSetting("Settings", "FallMsg", "victim died because he fell off from something")
            loc.AddSetting("Settings", "BledMsg", "victim bled out. He was killed by: killer")
            loc.AddSetting("Settings", "BledMsg2", "victim bled out.")
            loc.AddSetting("Settings", "DrownedMsg", "victim Drowned")
            loc.AddSetting("Settings", "ColdMsg", "victim Caught Cold, and died.")
            loc.AddSetting("Settings", "XyzMsg", "victim suicided....")
            loc.AddSetting("Settings", "KillMessage", "victim was killed by killer | Damage: dmg | Distance: dist | With: weapon | Part: bodypart")
            loc.Save()
        return Plugin.GetIni("DeathMSGConfig")

    def On_PluginInit(self):
        self.DeathMSGConfig()

    def IsNatural(self, type):
        if type == "Bite" or type == "BluntTrauma" or type == "Heat" or type == "Hunger" or type == "Radiation" or type == "Thirst":
            return True
        return False

    def On_PlayerDied(self, PlayerDeathEvent):
        if PlayerDeathEvent.Attacker.ToPlayer() is None:
            return

        attacker = PlayerDeathEvent.Attacker
        victim = PlayerDeathEvent.Victim
        attackername = str(attacker.displayName)
        victimname = str(victim.Name)
        if attackername == victimname:
            ini = self.DeathMSGConfig()
            NaturalDies = ini.GetSetting("Settings", "NaturalDies")
            sysname = ini.GetSetting("Settings", "SysName")
            if int(NaturalDies) == 1:
                type = str(PlayerDeathEvent.DamageType)
                if self.IsNatural(type):
                    ntrmsg = ini.GetSetting("Settings", "NaturalMsg")
                    ntrmsg = ntrmsg.replace("victim", victimname)
                    ntrmsg = ntrmsg.replace("type", type)
                    Server.BroadcastFrom(sysname, ntrmsg)
                elif type == "Generic":
                    cmsg = ini.GetSetting("Settings", "XyzMsg")
                    cmsg = cmsg.replace("victim", victimname)
                    Server.BroadcastFrom(sysname, cmsg)
                elif type == "Suicide":
                    smsg = ini.GetSetting("Settings", "SuicideMsg")
                    smsg = smsg.replace("victim", victimname)
                    Server.BroadcastFrom(sysname, smsg)
                elif type == "Fall":
                    fmsg = ini.GetSetting("Settings", "FallMsg")
                    fmsg = fmsg.replace("victim", victimname)
                    Server.BroadcastFrom(sysname, fmsg)
                elif type == "Drowned":
                    dmsg = ini.GetSetting("Settings", "DrownedMsg")
                    dmsg = dmsg.replace("victim", victimname)
                    Server.BroadcastFrom(sysname, dmsg)
                elif type == "Cold":
                    cmsg = ini.GetSetting("Settings", "ColdMsg")
                    cmsg = cmsg.replace("victim", victimname)
                    Server.BroadcastFrom(sysname, cmsg)
                elif type == "Bleeding":
                    bmsg = ini.GetSetting("Settings", "BledMsg2")
                    bmsg = bmsg.replace("victim", victimname)
                    Server.BroadcastFrom(sysname, bmsg)
        elif attackername != victimname:
            ini = self.DeathMSGConfig()
            sysname = ini.GetSetting("Settings", "SysName")
            dmgmsg = ini.GetSetting("Settings", "KillMessage")
            type = str(PlayerDeathEvent.DamageType)
            weapon = str(PlayerDeathEvent._info.Weapon.info.displayname)
            if type == "Bullet" or type == "Slash":
                if type == "Bullet":
                    bodypart = self.BodyParts[str(PlayerDeathEvent._info.HitPart)]
                else:
                    bodypart = "Body"
                vloc = victim.Location
                aloc = attacker.transform.position
                dist = round(Util.GetVectorsDistance(vloc, aloc), 2)
                damage = PlayerDeathEvent.DamageAmount
                dmgmsg = dmgmsg.replace("killer", attackername)
                dmgmsg = dmgmsg.replace("victim", victimname)
                dmgmsg = dmgmsg.replace("dmg", str(damage))
                dmgmsg = dmgmsg.replace("dist", str(dist))
                dmgmsg = dmgmsg.replace("weapon", weapon)
                dmgmsg = dmgmsg.replace("bodypart", bodypart)
                KillLog = ini.GetSetting("Settings", "KillLog")
                Server.BroadcastFrom(sysname, dmgmsg)
                if int(KillLog) == 1:
                    Plugin.Log("KillLog", str(System.DateTime.Now) + " " + dmgmsg)
            elif type == "Bleeding":
                bmsg = ini.GetSetting("Settings", "BledMsg")
                bmsg = bmsg.replace("victim", victimname)
                bmsg = bmsg.replace("killer", attackername)
                Server.BroadcastFrom(sysname, bmsg)