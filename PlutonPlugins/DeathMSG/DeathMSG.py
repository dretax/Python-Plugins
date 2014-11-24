__author__ = 'DreTaX'
__version__ = '1.8'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import DateTime

"""
    Class
"""


class DeathMSG:
    """
        Brought to you by XCorrosionX and DreTaX
    """
    BodyParts = {
        'l_upperarm': 'Upper Arm',
        'r_upperarm': 'Upper Arm',
        'head': 'Head',
        'jaw': 'Head',
        'l_knee': 'Knee',
        'r_knee': 'Knee',
        'spine1': 'Spine',
        'spine2': 'Spine',
        'spine3': 'Spine',
        'spine4': 'Spine',
        'l_hand': 'Hand',
        'r_hand': 'Hand',
        'r_hip': 'Hip',
        'l_hip': 'Hip',
        'l_eye': 'Eye',
        'r_eye': 'Eye',
        'l_toe': 'Toe',
        'r_toe': 'Toe',
        'pelvis': 'Pelvis',
        'l_clavicle': 'Clavicle',
        'r_clavicle': 'Clavicle',
        'r_forearm': 'Fore Arm',
        'l_forearm': 'Fore Arm',
        'r_ulna': 'Ulna',
        'l_ulna': 'Ulna',
        'r_foot': 'Foot',
        'l_foot': 'Foot',
        'neck': 'Neck'
    }

    def DeathMSGConfig(self):
        if not Plugin.IniExists("DeathMSGConfig"):
            loc = Plugin.CreateIni("DeathMSGConfig")
            loc.AddSetting("Settings", "SysName", "Equinox DeathMSG")
            loc.AddSetting("Settings", "NaturalDies", "1")
            loc.AddSetting("Settings", "KillLog", "1")
            loc.AddSetting("Settings", "AnimalKills", "1")
            loc.AddSetting("Settings", "Animal", "victim was killed by  a killer")
            loc.AddSetting("Settings", "Suicide", "victim suicided...")
            loc.AddSetting("Settings", "Bite", "victim was Bitten to Death")
            loc.AddSetting("Settings", "BluntTrauma", "victim died from a Blunt Trauma")
            loc.AddSetting("Settings", "Heat", "victim died from heat")
            loc.AddSetting("Settings", "Hunger", "victim died from starvation")
            loc.AddSetting("Settings", "Radiation", "victim died from radiation")
            loc.AddSetting("Settings", "Thirst", "victim died from dehydration")
            loc.AddSetting("Settings", "Fall", "victim died because he fell off from something")
            loc.AddSetting("Settings", "BledMsg", "victim bled out. He was killed by: killer")
            loc.AddSetting("Settings", "Bleeding", "victim bled out.")
            loc.AddSetting("Settings", "Drowned", "victim Drowned")
            loc.AddSetting("Settings", "Cold", "victim Caught Cold, and died.")
            loc.AddSetting("Settings", "Generic", "victim suicided....")
            loc.AddSetting("Settings", "Bullet", "killer shot through victim's bodypart, from dist, with: weapon & caused: dmg Damage")
            loc.AddSetting("Settings", "Slash", "killer slashed through victim's bodypart, from dist, with: weapon & caused: dmg Damage")
            loc.Save()
        return Plugin.GetIni("DeathMSGConfig")

    def On_PluginInit(self):
        self.DeathMSGConfig()

    def IsAnimal(self, String):
        s = String.replace('(Clone)', '')
        if s == 'stag' or s == 'wolf' or s == 'bear' or s == 'boar':
            return s
        return None

    def On_PlayerDied(self, PlayerDeathEvent):
        if PlayerDeathEvent.Attacker.ToPlayer() is None:
            #I'm unsure, so I just made this lol
            if not isinstance(PlayerDeathEvent.Attacker.displayName, str):
                return
            attacker = PlayerDeathEvent.Attacker
            attackername = str(attacker.name)
            ani = self.IsAnimal(attackername)
            if ani is None:
                return
            victim = PlayerDeathEvent.Victim
            victimname = str(victim.Name)
            ini = self.DeathMSGConfig()
            Animal = int(ini.GetSetting("Settings", "AnimalKills"))
            if Animal == 1:
                sysname = ini.GetSetting("Settings", "SysName")
                msg = ini.GetSetting("Settings", "Animal")
                msg = msg.replace("killer", ani)
                msg = msg.replace("victim", victimname)
                Server.BroadcastFrom(sysname, msg)
        else:
            attacker = PlayerDeathEvent.Attacker
            victim = PlayerDeathEvent.Victim
            attackername = str(attacker.displayName)
            victimname = str(victim.Name)
            if attacker.userID == victim.GameID:
                ini = self.DeathMSGConfig()
                NaturalDies = int(ini.GetSetting("Settings", "NaturalDies"))
                if NaturalDies == 1:
                    sysname = ini.GetSetting("Settings", "SysName")
                    type = str(PlayerDeathEvent.DamageType)
                    msg = ini.GetSetting("Settings", type)
                    msg = msg.replace("victim", victimname)
                    Server.BroadcastFrom(sysname, msg)
            elif attacker.userID != victim.GameID:
                ini = self.DeathMSGConfig()
                sysname = ini.GetSetting("Settings", "SysName")
                type = str(PlayerDeathEvent.DamageType)
                weapon = str(PlayerDeathEvent._info.Weapon.info.displayname)
                if type == "Bullet" or type == "Slash":
                    dmgmsg = ini.GetSetting("Settings", type)
                    bodypart = str(PlayerDeathEvent.HitBone)
                    bpart = self.BodyParts.get(bodypart, bodypart)
                    vloc = victim.Location
                    aloc = attacker.transform.position
                    dist = round(Util.GetVectorsDistance(vloc, aloc), 2)
                    damage = PlayerDeathEvent.DamageAmount
                    dmgmsg = dmgmsg.replace("killer", attackername)
                    dmgmsg = dmgmsg.replace("victim", victimname)
                    dmgmsg = dmgmsg.replace("dmg", str(damage))
                    dmgmsg = dmgmsg.replace("dist", str(dist))
                    dmgmsg = dmgmsg.replace("weapon", weapon)
                    dmgmsg = dmgmsg.replace("bodypart", bpart)
                    KillLog = int(ini.GetSetting("Settings", "KillLog"))
                    Server.BroadcastFrom(sysname, dmgmsg)
                    if KillLog == 1:
                        Plugin.Log("KillLog", str(System.DateTime.Now) + " " + dmgmsg)
                elif type == "Bleeding":
                    bmsg = ini.GetSetting("Settings", "BledMsg")
                    bmsg = bmsg.replace("victim", victimname)
                    bmsg = bmsg.replace("killer", attackername)
                    Server.BroadcastFrom(sysname, bmsg)