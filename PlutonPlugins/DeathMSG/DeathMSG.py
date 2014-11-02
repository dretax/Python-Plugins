__author__ = 'DreTaX'
__version__ = '1.6'

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
    """
        Brought to you by XCorrosionX and DreTaX
    """
    BodyParts = {
        '2801294865': 'Head',
        '4040387367': 'Head',
        '1607781229': 'Head',
        '2910575312': 'Head',
        '2341211393': 'Head',
        '2881065196': 'Body',
        '405856008': 'Body',
        '497750834': 'Body',
        '2107788330': 'Body',
        '998083258': 'Body',
        '1469249236': 'Body',
        '3856158477': 'Body',
        '487549081': 'Body',
        '1819052778': 'Legs',
        '3428008992': 'Legs',
        '3847102050': 'Legs',
        '2868606315': 'Foot',
        '2590633211': 'Foot',
        '1020274123': 'Foot',
        '935136153': 'Hand',
        '3847415609': 'Hand',
        '1286581443': 'Hand'
    }

    def DeathMSGConfig(self):
        if not Plugin.IniExists("DeathMSGConfig"):
            loc = Plugin.CreateIni("DeathMSGConfig")
            loc.AddSetting("Settings", "SysName", "Equinox DeathMSG")
            loc.AddSetting("Settings", "NaturalDies", "1")
            loc.AddSetting("Settings", "KillLog", "1")
            loc.AddSetting("Settings", "SuicideMsg", "victim suicided...")
            loc.AddSetting("Settings", "Bite", "victim was Bitten to Death")
            loc.AddSetting("Settings", "BluntTrauma", "victim died from a Blunt Trauma")
            loc.AddSetting("Settings", "Heat", "victim died from heat")
            loc.AddSetting("Settings", "Hunger", "victim died from starvation")
            loc.AddSetting("Settings", "Radiation", "victim died from radiation")
            loc.AddSetting("Settings", "Thirst", "victim died from dehydration")
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
        ini = self.DeathMSGConfig()
        msg = ini.GetSetting("Settings", type)
        if type == "Bite":
            return msg
        elif type == "BluntTrauma":
            return msg
        elif type == "Heat":
            return msg
        elif type == "Hunger":
            return msg
        elif type == "Radiation":
            return msg
        elif type == "Thirst":
            return msg
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
                if self.IsNatural(type) and self.IsNatural(type) is not False:
                    ntrmsg = ini.GetSetting("Settings", "NaturalMsg")
                    ntrmsg = ntrmsg.replace("victim", victimname)
                    #ntrmsg = ntrmsg.replace("type", type)
                    Server.BroadcastFrom(sysname, ntrmsg)
                if type == "Generic":
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
                bodypart = str(PlayerDeathEvent._info.HitPart)
                vloc = victim.Location
                aloc = attacker.transform.position
                dist = round(Util.GetVectorsDistance(vloc, aloc), 2)
                damage = PlayerDeathEvent.DamageAmount
                dmgmsg = dmgmsg.replace("killer", attackername)
                dmgmsg = dmgmsg.replace("victim", victimname)
                dmgmsg = dmgmsg.replace("dmg", str(damage))
                dmgmsg = dmgmsg.replace("dist", str(dist))
                dmgmsg = dmgmsg.replace("weapon", weapon)
                dmgmsg = dmgmsg.replace("bodypart", self.BodyParts[bodypart])
                KillLog = ini.GetSetting("Settings", "KillLog")
                Server.BroadcastFrom(sysname, dmgmsg)
                if int(KillLog) == 1:
                    Plugin.Log("KillLog", str(System.DateTime.Now) + " " + dmgmsg)
            elif type == "Bleeding":
                bmsg = ini.GetSetting("Settings", "BledMsg")
                bmsg = bmsg.replace("victim", victimname)
                bmsg = bmsg.replace("killer", attackername)
                Server.BroadcastFrom(sysname, bmsg)