__author__ = 'DreTaX'
__version__ = '3.5.8'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import re

"""
    Class
"""

class DeathMSG:
    """
        Methods
    """
    red = "[color #FF0000]"
    green = "[color #009900]"
    deathmsgname = None
    bullet = None
    animal = None
    suicide = None
    huntingbow = None
    sleeper = None
    tpamsg = None
    banmsg = None
    spike = None
    explosion = None
    bleeding = None
    kl = None
    ean = None
    esn = None
    essn = None
    autoban = None

    def On_PluginInit(self):
        config = self.DeathMSGConfig()
        self.deathmsgname = config.GetSetting("Settings", "deathmsgname")
        self.bullet = config.GetSetting("Settings", "msg")
        self.kl = int(config.GetSetting("Settings", "killog"))
        self.ean = int(config.GetSetting("Settings", "enableanimalmsg"))
        self.animal = config.GetSetting("Settings", "animalkill")
        self.esn = int(config.GetSetting("Settings", "enablesuicidemsg"))
        self.suicide = config.GetSetting("Settings", "suicide")
        self.autoban = int(config.GetSetting("Settings", "autoban"))
        self.essn = int(config.GetSetting("Settings", "enablesleepermsg"))
        self.sleeper = config.GetSetting("Settings", "SleeperKill")
        self.huntingbow = config.GetSetting("Settings", "huntingbow")
        self.banmsg = config.GetSetting("Settings", "banmsg")
        self.tpamsg = config.GetSetting("Settings", "TpaMsg")
        self.spike = config.GetSetting("Settings", "spike")
        self.explosion = config.GetSetting("Settings", "explosionmsg")
        self.bleeding = config.GetSetting("Settings", "bmsg")
        Util.ConsoleLog("DeathMSG by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def On_Command(self, Player, cmd, args):
        if cmd == "uautoban":
            if len(args) == 0:
                Player.Message("---DeathMSG " + __version__ + "---")
                Player.Message("/uautoban name - Unbans player")
            else:
                if not Player.Admin and not Player.Moderator:
                    Player.MessageFrom(self.deathmsgname, "You aren't an admin!")
                    return
                pl = self.argsToText(args)
                b = Server.UnbanByName(pl, Player.Name)
                if not b:
                    Player.Message("Target: " + pl + " isn't in the database, or you misspelled It!")
                    return
                Player.MessageFrom(self.deathmsgname, "Player " + pl + " unbanned!")

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.DamageType is not None and DeathEvent.Victim is not None and DeathEvent.Attacker is not None:
            victim = str(DeathEvent.Victim.Name)
            try:
                killer = str(DeathEvent.Attacker.Name)
            except:
                return
            if self.IsAnimal(DeathEvent.Attacker):
                if self.ean == 1:
                    a = self.animal
                    a = a.replace("victim", victim)
                    a = a.replace("killer", killer)
                    Server.BroadcastFrom(self.deathmsgname, a)
                return
            id = self.TrytoGrabID(DeathEvent.Attacker)
            vid = self.TrytoGrabID(DeathEvent.Victim)
            if self.WasSuicide(id, vid):
                if self.esn == 1:
                    n = self.suicide
                    n = n.replace("victim", victim)
                    Server.BroadcastFrom(self.deathmsgname, n)
                return
            weapon = str(DeathEvent.WeaponName)
            bodyPart = self.BD(str(DeathEvent.DamageEvent.bodyPart))
            damage = round(DeathEvent.DamageAmount, 2)
            killerloc = DeathEvent.Attacker.Location
            location = DeathEvent.Victim.Location
            distance = round(Util.GetVectorsDistance(killerloc, location), 2)
            bleed = str(DeathEvent.DamageType)
            if bleed == "Bullet":
                if DeathEvent.Sleeper:
                    if not self.essn:
                        return
                    message = self.sleeper
                else:
                    message = self.bullet
                n = message.replace("victim", victim)
                n = n.replace("killer", killer)
                n = n.replace("weapon", weapon)
                n = n.replace("damage", str(damage))
                n = n.replace("number", str(distance))
                n = n.replace("bodyPart", str(bodyPart))
                Server.BroadcastFrom(self.deathmsgname, n)
                if self.autoban == 1:
                    if self.RangeOf(weapon) is None and "Spike" not in weapon:
                        Plugin.Log("Report This to DreTaX", "Null Weapon: " + weapon)
                        return
                    if distance > self.RangeOf(weapon) > 0:
                        tpfriendteleport = DataStore.Get("tpfriendautoban", id)
                        hometeleport = DataStore.Get("homesystemautoban", id)
                        if (tpfriendteleport == "none" or tpfriendteleport is None) and \
                                (hometeleport == "none" or hometeleport is None):
                            z = self.banmsg
                            z = z.replace("killer", killer)
                            if distance >= 1000:
                                return
                            Server.BroadcastFrom(self.deathmsgname, self.red + z)
                            self.Log(killer, weapon, distance, victim, bodyPart, damage, 1)
                            DataStore.Add("DeathMSGBAN", vid, str(location))
                            Server.BanPlayer(DeathEvent.Attacker, "Console", "Range Ban: " + str(distance) + " Gun: " +
                                             weapon)
                        else:
                            t = self.tpamsg
                            t = t.replace("killer", killer)
                            if distance >= 1000:
                                return
                            Server.BroadcastFrom(self.deathmsgname, t)
                            DataStore.Remove("tpfriendautoban", id)
                            DataStore.Remove("homesystemautoban", id)
                            if self.kl == 1:
                                self.Log(killer, weapon, distance, victim, bodyPart, damage, 1)
                        return
                if self.kl == 1:
                    self.Log(killer, weapon, distance, victim, bodyPart, damage, None)
            elif bleed == "Melee":
                if weapon == "Hunting Bow":
                    if DeathEvent.Sleeper:
                        if self.essn:
                            hn = self.sleeper
                        else:
                            return
                    else:
                        hn = self.huntingbow
                    hn = hn.replace("victim", victim)
                    hn = hn.replace("killer", killer)
                    hn = hn.replace("damage", str(damage))
                    hn = hn.replace("number", str(distance))
                    hn = hn.replace("bodyPart", str(bodyPart))
                    Server.BroadcastFrom(self.deathmsgname, hn)
                    if self.autoban == 1:
                        if distance > self.RangeOf(weapon) > 0:
                            tpfriendteleport = DataStore.Get("tpfriendautoban", id)
                            hometeleport = DataStore.Get("homesystemautoban", id)
                            if (tpfriendteleport == "none" or tpfriendteleport is None) and \
                                    (hometeleport == "none" or hometeleport is None):
                                z = self.banmsg
                                z = z.replace("killer", killer)
                                Server.BroadcastFrom(self.deathmsgname, self.red + z)
                                self.Log(killer, weapon, distance, victim, bodyPart, damage, 1)
                                DataStore.Add("DeathMSGBAN", vid, str(location))
                                Server.BanPlayer(DeathEvent.Attacker, "Console", "Range Ban: " + str(distance)
                                                 + " Gun: " + weapon)
                            else:
                                t = self.tpamsg
                                t = t.replace("killer", killer)
                                Server.BroadcastFrom(self.deathmsgname, t)
                                if self.kl == 1:
                                    self.Log(killer, "Hunting Bow", distance, victim, str(bodyPart), damage, 1)
                            return
                    if self.kl == 1:
                        self.Log(killer, "Hunting Bow", distance, victim, str(bodyPart), damage, None)
                elif weapon == "Spike Wall":
                    s = self.spike
                    s = s.replace("victim", victim)
                    s = s.replace("killer", killer)
                    s = s.replace("weapon", "Spike Wall")
                    Server.BroadcastFrom(self.deathmsgname, s)
                elif weapon == "Large Spike Wall":
                    s = self.spike
                    s = s.replace("victim", victim)
                    s = s.replace("killer", killer)
                    s = s.replace("weapon", "Large Spike Wall")
                    Server.BroadcastFrom(self.deathmsgname, s)
                else:
                    n = self.bullet
                    n = n.replace("victim", victim)
                    n = n.replace("killer", killer)
                    n = n.replace("weapon", weapon)
                    n = n.replace("damage", str(damage))
                    n = n.replace("number", str(distance))
                    n = n.replace("bodyPart", str(bodyPart))
                    Server.BroadcastFrom(self.deathmsgname, n)
            elif bleed == "Explosion":
                x = self.explosion
                x = x.replace("killer", killer)
                x = x.replace("victim", victim)
                if weapon == "F1 Grenade":
                    x = x.replace("weapon", "F1 Grenade")
                elif weapon == "Explosive Charge":
                    x = x.replace("weapon", "C4")
                Server.BroadcastFrom(self.deathmsgname, x)
            elif bleed == "Bleeding":
                n = self.bleeding
                n = n.replace("victim", victim)
                n = n.replace("killer", killer)
                Server.BroadcastFrom(self.deathmsgname, n)

    def On_PlayerSpawned(self, Player, SpawnEvent):
        id = Player.SteamID
        if DataStore.ContainsKey("DeathMSGBAN", id):
            get = DataStore.Get("DeathMSGBAN", id)
            loc = self.Replace(get)
            newloc = Util.CreateVector(float(loc[0]), float(loc[1]), float(loc[2]))
            Player.TeleportTo(newloc)
            Player.MessageFrom(self.deathmsgname, self.green + "You got teleported back where you died!")
            DataStore.Remove("DeathMSGBAN", id)

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def Log(self, killer, weapon, dist, victim, body, dmg, tp):
        if tp is None:
            Plugin.Log("KillLog", " Killer: " + killer + " Gun: " + weapon + " Dist: " + str(dist) + " Victim: " +
                       victim + " BodyP: " + str(body) + " DMG: " + str(dmg))
        else:
            Plugin.Log("KillLog", " Killer: " + killer + " Gun: " + weapon + " Dist: " + str(dist) + " Victim: " +
                       victim + " BodyP: " + str(body) + " DMG: " + str(dmg) + " WAS TELEPORTING")

    def IsAnimal(self, Entity):
        if "NPC" in str(Entity):
            return True
        return False

    def WasSuicide(self, killerid, victimid):
        if killerid == victimid:
            return True
        return False

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def BD(self, bodyp):
        ini = self.Bodies()
        bodyp = str(bodyp)
        name = ini.GetSetting("bodyparts", bodyp)
        return str(name)

    def Bodies(self):
        return Plugin.GetIni("bodyparts")

    def DeathMSGConfig(self):
        return Plugin.GetIni("DeathMSGConfig")

    def RangeOf(self, weapon):
        ini = Plugin.GetIni("range")
        range = ini.GetSetting("range", weapon)
        if range is None:
            return None
        return int(range)

    def Replace(self, s):
        s = re.sub('[(\)\]]', '', s)
        s = s.split(",")
        return s