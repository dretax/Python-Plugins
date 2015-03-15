__author__ = 'DreTaX'
__version__ = '2.2'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import DateTime
import re
rgbstringtemplate = re.compile(r'#[a-fA-F0-9]{6}$')

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

    SysName = None
    SleepingKills = None
    NaturalDies = None
    KillLog = None
    AnimalKills = None
    AnimalDeaths = None
    #Messages.
    Animal = None
    AnimalDeath = None
    Beartrap = None
    Bow = None
    Bite = None
    Bullet = None
    Blunt = None
    Bleeding = None
    Cold = None
    Drowned = None
    Fall = None
    Generic = None
    Heat = None
    Hunger = None
    Radiation = None
    Thirst = None
    Suicide = None
    Stab = None
    Slash = None
    BiteSleep = None
    BluntSleep = None
    BleedingSleep = None
    StabSleep = None
    BowSleep = None
    BulletSleep = None
    Poison = None
    Explosion = None
    ExplosionSleep = None
    SlashSleep = None

    def On_PluginInit(self):
        ini = self.DeathMSGConfig()
        self.SysName = ini.GetSetting("Settings", "SysName")
        SysNameColor = ini.GetSetting("Settings", "SysNameColor")
        self.SysName = self.ColorText(SysNameColor, self.SysName)
        self.SleepingKills = bool(ini.GetSetting("Settings", "SleepingKills"))
        self.NaturalDies = bool(ini.GetSetting("Settings", "NaturalDies"))
        self.KillLog = bool(ini.GetSetting("Settings", "KillLog"))
        self.AnimalKills = bool(ini.GetSetting("Settings", "AnimalKills"))
        self.AnimalDeaths = bool(ini.GetSetting("Settings", "AnimalDeaths"))
        enum = ini.EnumSection("Messages")
        for Key in enum:
            if Key == "Message Settings" or Key == "Sleeping Types":
                continue
            v = ini.GetSetting("Messages", Key)
            self.ColorizeMessagesToMemory(Key, v)

    def DeathMSGConfig(self):
        if not Plugin.IniExists("DeathMSGConfig"):
            loc = Plugin.CreateIni("DeathMSGConfig")
            #Settings
            loc.AddSetting("Settings", "Plugin Settings", "-----------------------------")
            loc.AddSetting("Settings", "SysName", "Equinox DeathMSG")
            loc.AddSetting("Settings", "SysNameColor", "#55aaff")
            loc.AddSetting("Settings", "SleepingKills", "True")
            loc.AddSetting("Settings", "NaturalDies", "True")
            loc.AddSetting("Settings", "KillLog", "True")
            loc.AddSetting("Settings", "AnimalKills", "True")
            loc.AddSetting("Settings", "AnimalDeaths", "True")
            #Messages
            loc.AddSetting("Messages", "Message Settings", "-----------------------------")
            loc.AddSetting("Messages", "Animal", "COLOR#aaff55 victim was COLOR#55aaff killed by a COLOR#ff55aa killer")
            loc.AddSetting("Messages", "AnimalDeath", "killer killed animal using weapon")
            loc.AddSetting("Messages", "Beartrap", "victim ran into bear trap")
            loc.AddSetting("Messages", "Bite", "victim was Bitten to Death")
            loc.AddSetting("Messages", "Bow", "killer shot victim in bodypart, from dist m, with: weapon & caused: dmg Damage")
            loc.AddSetting("Messages", "Bullet", "killer shot through victim's bodypart, from dist m, with: weapon & caused: dmg Damage")
            loc.AddSetting("Messages", "Blunt", "killer hit victim in bodypart using weapon from dist m. Damage: dmg")
            loc.AddSetting("Messages", "Bleeding", "victim bled out.")
            loc.AddSetting("Messages", "Cold", "victim Caught Cold, and died.")
            loc.AddSetting("Messages", "Drowned", "victim Drowned")
            loc.AddSetting("Messages", "Fall", "victim died because he fell off from something")
            loc.AddSetting("Messages", "Generic", "victim suicided....")
            loc.AddSetting("Messages", "Heat", "victim died from heat")
            loc.AddSetting("Messages", "Hunger", "victim died from starvation")
            loc.AddSetting("Messages", "Radiation", "victim died from radiation")
            loc.AddSetting("Messages", "Thirst", "victim died from dehydration")
            loc.AddSetting("Messages", "Stab", "killer hit victim in bodypart using weapon. Damage: dmg")
            loc.AddSetting("Messages", "Poison", "victim got poisoned.")
            loc.AddSetting("Messages", "Explosion", "victim exploded.")
            loc.AddSetting("Messages", "Suicide", "COLOR#aaff55 victim COLOR#55aaff suicided COLOR#ff55aa...")
            loc.AddSetting("Messages", "Slash", "killer slashed through victim's bodypart, from dist m, with: weapon & caused: dmg Damage")
            #Sleeping Types, Stolen from Skully
            loc.AddSetting("Messages", "Sleeping Types", "-----------------------------")
            loc.AddSetting("Messages", "BiteSleep", "victim was bitten to death while he was sleeping")
            loc.AddSetting("Messages", "ExplosionSleep", "victim exploded while he was sleeping")
            loc.AddSetting("Messages", "BluntSleep", "killer hit victim while he was sleeping in bodypart using weapon from dist m. Damage: dmg")
            loc.AddSetting("Messages", "BleedingSleep", "victim bled out while he was sleeping")
            loc.AddSetting("Messages", "StabSleep", "killer hit victim while he was sleeping in bodypart using weapon. Damage: dmg")
            loc.AddSetting("Messages", "BowSleep", "killer shot victim while he was sleeping in bodypart, from dist m using weapon. Damage: dmg")
            loc.AddSetting("Messages", "BulletSleep", "killer shot victim while he was sleeping in bodypart, from dist m using weapon")
            loc.AddSetting("Messages", "SlashSleep", "killer slashed victim while he was sleeping in bodypart, from dist m using weapon. Damage: dmg")
            loc.Save()
        return Plugin.GetIni("DeathMSGConfig")

    def ColorizeMessagesToMemory(self, Key, String):
        s = String
        if "COLOR" in s:
            arr = []
            list = s.split('COLOR')
            for part in list:
                if part.isspace() or not part:
                    continue
                words = part.split(' ')
                for word in words:
                    strip = word.strip(' ')
                    if self.IsRGB(strip):
                        #Atleast iScripters realised that I should split here, since the logical REPLACE DIDNT WORK -.-
                        color = part.split(' ', 1)[0]
                        themsg = part.split(' ', 1)[1]
                        colorized = self.ColorText(color, themsg)
                        arr.append(colorized)
                        break
            s = ' '.join(arr)
        setattr(self, Key, s)

    def ColorText(self, color, part):
        return '<color=' + color + '>' + part + '</color>'

    def IsRGB(self, value):
        return bool(rgbstringtemplate.match(value))

    #Objects and IsAnimals were stolen from Skully
    Misc = {
        'autospawn/animals/bear': 'Bear',
        'autospawn/animals/wolf': 'Wolf',
        'campfire_deployed(Clone)': 'Fire',
        'beartrap(Clone)': 'BearTrap',
        'timed.explosive.deployed(Clone)': 'C4'
    }

    IsAnimal = {
        'autospawn/animals/bear': 'Bear',
        'autospawn/animals/wolf': 'Wolf',
        'autospawn/animals/stag': 'Stag',
        'autospawn/animals/boar': 'Boar',
        'autospawn/animals/chicken': 'Chicken'
    }

    def On_NPCKilled(self, NPCDeathEvent):
        #Skully
        if self.AnimalKills:
            Attacker = NPCDeathEvent.Attacker
            if Attacker.IsNPC():
                return
            Victim = NPCDeathEvent.Victim
            VictimName = self.IsAnimal.get(Victim.Name, Victim.Name)
            Attacker = Server.Players[Attacker.basePlayer.userID]
            AttackerName = Attacker.Name
            Weapon = NPCDeathEvent.Weapon.Name
            vloc = Victim.Location
            aloc = Attacker.Location
            dist = round(Util.GetVectorsDistance(vloc, aloc), 2)
            dmgmsg = self.AnimalDeath
            dmgmsg = dmgmsg.replace("killer", AttackerName)
            dmgmsg = dmgmsg.replace("animal", VictimName)
            dmgmsg = dmgmsg.replace("dist", str(dist))
            dmgmsg = dmgmsg.replace("weapon", Weapon)
            Server.BroadcastFrom(self.SysName, dmgmsg)

    def On_PlayerDied(self, PlayerDeathEvent):
        attacker = PlayerDeathEvent.Attacker
        victim = PlayerDeathEvent.Victim
        attackername = str(attacker.Name)
        victimname = str(victim.Name)
        Sleeping = False
        if victim.basePlayer.IsSleeping():
            Sleeping = True
        if attacker.ToPlayer() is None:
            atnn = self.Misc.get(attackername, None)
            if atnn is None or not atnn:
                return
            elif atnn == "fire":
                msg = self.Heat
                msg = msg.replace("victim", victimname)
                Server.BroadcastFrom(self.SysName, msg)
                return
            elif atnn == "beartrap":
                msg = self.Beartrap
                msg = msg.replace("victim", victimname)
                Server.BroadcastFrom(self.SysName, msg)
                return
            elif atnn == "C4":
                if Sleeping:
                    dmgmsg = self.ExplosionSleep
                else:
                    dmgmsg = self.Explosion
                msg = dmgmsg.replace("victim", victimname)
                Server.BroadcastFrom(self.SysName, msg)
            if self.AnimalKills and attacker.IsNPC():
                attackername = self.IsAnimal.get(attackername, attackername)
                msg = self.Animal
                msg = msg.replace("killer", attackername)
                msg = msg.replace("victim", victimname)
                Server.BroadcastFrom(self.SysName, msg)
        else:
            damage = round(PlayerDeathEvent.DamageAmounts[9], 2)
            type = str(PlayerDeathEvent.DamageType)
            weapon = PlayerDeathEvent.Weapon.Name
            if type == "Suicide":
                if self.NaturalDies:
                    msg = self.Suicide
                    msg = msg.replace("victim", victimname)
                    Server.BroadcastFrom(self.SysName, msg)
                    return
            elif type == "Bullet" or type == "Slash":
                dmgmsg = getattr(self, type)
                bodypart = str(PlayerDeathEvent.HitBone)
                bpart = self.BodyParts.get(bodypart, bodypart)
                vloc = victim.Location
                aloc = attacker.Location
                dist = round(Util.GetVectorsDistance(vloc, aloc), 2)
                dmgmsg = dmgmsg.replace("killer", attackername)
                dmgmsg = dmgmsg.replace("victim", victimname)
                dmgmsg = dmgmsg.replace("dmg", str(damage))
                dmgmsg = dmgmsg.replace("dist", str(dist))
                dmgmsg = dmgmsg.replace("weapon", weapon)
                dmgmsg = dmgmsg.replace("bodypart", bpart)
                Server.BroadcastFrom(self.SysName, dmgmsg)
                if self.KillLog:
                    Plugin.Log("KillLog", str(System.DateTime.Now) + " " + dmgmsg)
            elif type == "Bleeding":
                if Sleeping:
                    bmsg = self.BleedingSleep
                else:
                    bmsg = self.Bleeding
                bmsg = bmsg.replace("victim", victimname)
                bmsg = bmsg.replace("killer", attackername)
                Server.BroadcastFrom(self.SysName, bmsg)
            # Nono, mr.stolenfromskullysmodification isnt here
            elif type == "Blunt":
                if Sleeping:
                    dmgmsg = self.BluntSleep
                else:
                    dmgmsg = self.Blunt
                vloc = victim.Location
                aloc = attacker.Location
                dist = round(Util.GetVectorsDistance(vloc, aloc), 2)
                bodypart = str(PlayerDeathEvent.HitBone)
                bpart = self.BodyParts.get(bodypart, bodypart)
                dmgmsg = dmgmsg.replace("killer", attackername)
                dmgmsg = dmgmsg.replace("victim", victimname)
                dmgmsg = dmgmsg.replace("dist", str(dist))
                dmgmsg = dmgmsg.replace("dmg", str(damage))
                dmgmsg = dmgmsg.replace("weapon", weapon)
                dmgmsg = dmgmsg.replace("bodypart", bpart)
                if self.KillLog:
                    Plugin.Log("KillLog", str(System.DateTime.Now) + " " + dmgmsg)
            elif type == "Stab":
                if weapon == "Hunting Bow":
                    if Sleeping:
                        dmgmsg = self.BowSleep
                    else:
                        dmgmsg = self.Bow
                else:
                    if Sleeping:
                        dmgmsg = self.StabSleep
                    else:
                        dmgmsg = self.Stab
                bodypart = str(PlayerDeathEvent.HitBone)
                bpart = self.BodyParts.get(bodypart, bodypart)
                vloc = victim.Location
                aloc = attacker.Location
                dist = round(Util.GetVectorsDistance(vloc, aloc), 2)
                dmgmsg = dmgmsg.replace("killer", attackername)
                dmgmsg = dmgmsg.replace("victim", victimname)
                dmgmsg = dmgmsg.replace("dist", str(dist))
                dmgmsg = dmgmsg.replace("dmg", str(damage))
                dmgmsg = dmgmsg.replace("weapon", weapon)
                dmgmsg = dmgmsg.replace("bodypart", bpart)
                if self.KillLog:
                    Plugin.Log("KillLog", str(System.DateTime.Now) + " " + dmgmsg)
            else:
                if self.NaturalDies:
                    msg = getattr(self, type)
                    msg = msg.replace("victim", victimname)
                    Server.BroadcastFrom(self.SysName, msg)