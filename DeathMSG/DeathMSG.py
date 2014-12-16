__author__ = 'DreTaX'
__version__ = '3.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System
from System import DateTime
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

    def On_PluginInit(self):
        Util.ConsoleLog("DeathMSG by" + __author__ + " Version: " + __version__ + " loaded.", False)

    def On_Command(self, Player, cmd, args):
        if cmd == "uautoban":
            if len(args) == 0:
                Player.Message("---DeathMSG 3.0---")
                Player.Message("/uautoban name - Unbans player")
            else:
                config = self.DeathMSGConfig()
                deathmsgname = config.GetSetting("Settings", "deathmsgname")
                if not Player.Admin and not self.isMod(Player.SteamID):
                    Player.MessageFrom(deathmsgname, "You aren't an admin!")
                    return
                ini = self.DMB()
                pl = self.argsToText(args)
                id = self.GetPlayerUnBannedID(pl)
                ip = self.GetPlayerUnBannedIP(pl)
                if id is None:
                    Player.Message("Target: " + pl + " isn't in the database, or you misspelled It!")
                    return
                iprq = ini.GetSetting("NameIps", ip)
                idrq = ini.GetSetting("NameIds", id)
                ini.DeleteSetting("Ips", iprq)
                ini.DeleteSetting("Ids", idrq)
                ini.DeleteSetting("NameIps", ip)
                ini.DeleteSetting("NameIds", id)
                ini.Save()
                Player.MessageFrom(deathmsgname, "Player " + pl + " unbanned!")

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.DamageType is not None and DeathEvent.Victim is not None and DeathEvent.Attacker is not None:
            config = self.DeathMSGConfig()
            killer = str(DeathEvent.Attacker.Name)
            victim = str(DeathEvent.Victim.Name)
            deathmsgname = config.GetSetting("Settings", "deathmsgname")
            if self.WasSuicide(killer, victim):
                e = int(config.GetSetting("Settings", "enablesuicidemsg"))
                if e == 1:
                    victim = DeathEvent.Victim.Name
                    n = config.GetSetting("Settings", "suicide")
                    n = n.replace("victim", victim)
                    Server.BroadcastFrom(deathmsgname, n)
                return
            if self.IsAnimal(killer):
                e = int(config.GetSetting("Settings", "enableanimalmsg"))
                if e == 1:
                    a = config.GetSetting("Settings", "animalkill")
                    a = a.replace("victim", victim)
                    a = a.replace("killer", killer)
                    Server.BroadcastFrom(deathmsgname, a)
            else:
                bodyPart = self.BD(DeathEvent.DamageEvent.bodyPart)
                weapon = DeathEvent.WeaponName
                damage = round(DeathEvent.DamageAmount, 2)
                killerloc = DeathEvent.Attacker.Location
                location = DeathEvent.Victim.Location
                distance = round(Util.GetVectorsDistance(killerloc, location), 2)
                bleed = DeathEvent.DamageType
                kl = int(config.GetSetting("Settings", "killog"))
                if bleed == "Bullet":
                    message = config.GetSetting("Settings", "msg")
                    n = message.replace("victim", victim)
                    n = n.replace("killer", killer)
                    n = n.replace("weapon", weapon)
                    n = n.replace("damage", str(damage))
                    n = n.replace("number", str(distance))
                    n = n.replace("bodyPart", str(bodyPart))
                    Server.BroadcastFrom(deathmsgname, n)
                    autoban = int(config.GetSetting("Settings", "autoban"))
                    if autoban == 1:
                        if distance > self.RangeOf(weapon) and self.RangeOf(weapon) > 0:
                            id = DeathEvent.Attacker.SteamID
                            tpfriendteleport = DataStore.Get("tpfriendautoban", id)
                            hometeleport = DataStore.Get("homesystemautoban", id)
                            if (tpfriendteleport == "none" or tpfriendteleport is None) and (hometeleport == "none" or hometeleport is None):
                                z = config.GetSetting("Settings", "banmsg")
                                z = z.replace("killer", killer)
                                DeathEvent.Attacker.Kill()
                                Server.BroadcastFrom(deathmsgname, self.red + z)
                                ini = self.DMB()
                                ip = DeathEvent.Attacker.IP
                                vid = DeathEvent.Victim.SteamID
                                ini.AddSetting("Ips", ip, "1")
                                ini.AddSetting("Ids", id, "1")
                                ini.AddSetting("NameIps", killer, ip)
                                ini.AddSetting("NameIds", killer, id)
                                ini.AddSetting("Logistical", killer, "Gun: " + weapon + " Dist: " + str(distance) + " BodyP: " + str(bodyPart) + " DMG: " + damage)
                                ini.Save()
                                DeathEvent.Attacker.Disconnect()
                                DataStore.Add("DeathMSGBAN", vid, str(location))
                            else:
                                t = config.GetSetting("Settings", "TpaMsg")
                                t = t.replace("killer", killer)
                                Server.BroadcastFrom(deathmsgname, t)
                                if kl == 1:
                                    self.Log(killer, weapon, distance, victim, str(bodyPart), damage, 1)
                            return
                    if kl == 1:
                        self.Log(killer, weapon, distance, victim, str(bodyPart), damage, None)
                elif bleed == "Melee":
                    if damage == 75:
                        hn = config.GetSetting("Settings", "huntingbow")
                        hn = hn.replace("victim", victim)
                        hn = hn.replace("killer", killer)
                        hn = hn.replace("damage", str(damage))
                        hn = hn.replace("number", str(distance))
                        hn = hn.replace("bodyPart", str(bodyPart))
                        Server.BroadcastFrom(deathmsgname, hn)
                        autoban = int(config.GetSetting("Settings", "autoban"))
                        if autoban == 1:
                            if distance > self.RangeOf(weapon) and self.RangeOf(weapon) > 0:
                                id = DeathEvent.Attacker.SteamID
                                tpfriendteleport = DataStore.Get("tpfriendautoban", id)
                                hometeleport = DataStore.Get("homesystemautoban", id)
                                if (tpfriendteleport == "none" or tpfriendteleport is None) and (hometeleport == "none" or hometeleport is None):
                                    z = config.GetSetting("Settings", "banmsg")
                                    z = z.replace("killer", killer)
                                    DeathEvent.Attacker.Kill()
                                    Server.BroadcastFrom(deathmsgname, self.red + z)
                                    ini = self.DMB()
                                    ip = DeathEvent.Attacker.IP
                                    vid = DeathEvent.Victim.SteamID
                                    ini.AddSetting("Ips", ip, "1")
                                    ini.AddSetting("Ids", id, "1")
                                    ini.AddSetting("NameIps", killer, ip)
                                    ini.AddSetting("NameIds", killer, id)
                                    ini.AddSetting("Logistical", killer, "Gun: Hunting Bow Dist: " + str(distance) + " BodyP: " + str(bodyPart) + " DMG: " + damage)
                                    ini.Save()
                                    DeathEvent.Attacker.Disconnect()
                                    DataStore.Add("DeathMSGBAN", vid, str(location))
                                else:
                                    t = config.GetSetting("Settings", "TpaMsg")
                                    t = t.replace("killer", killer)
                                    Server.BroadcastFrom(deathmsgname, t)
                                    if kl == 1:
                                        self.Log(killer, "Hunting Bow", distance, victim, str(bodyPart), damage, 1)
                                return
                        if kl == 1:
                            self.Log(killer, "Hunting Bow", distance, victim, str(bodyPart), damage, None)
                    elif damage == 10 or damage == 15:
                        s = config.GetSetting("Settings", "spike")
                        s = s.replace("victim", victim)
                        s = s.replace("killer", killer)
                        s = s.replace("weapon", "Spike Wall")
                        Server.BroadcastFrom(deathmsgname, s)
                    else:
                        n = config.GetSetting("Settings", "msg")
                        n = n.replace("victim", victim)
                        n = n.replace("killer", killer)
                        n = n.replace("weapon", weapon)
                        n = n.replace("damage", str(damage))
                        n = n.replace("number", str(distance))
                        n = n.replace("bodyPart", str(bodyPart))
                        Server.BroadcastFrom(deathmsgname, n)
                elif bleed == "Explosion":
                    x = config.GetSetting("Settings", "explosionmsg")
                    x = x.replace("killer", killer)
                    x = x.replace("victim", victim)
                    x = x.replace("weapon", "C4/F1 Grenade")
                    Server.BroadcastFrom(deathmsgname, x)
                elif bleed == "Bleeding":
                    n = config.GetSetting("Settings", "bmsg")
                    n = n.replace("victim", victim)
                    n = n.replace("killer", killer)
                    Server.BroadcastFrom(deathmsgname, n)

    def On_PlayerSpawned(self, Player, SpawnEvent):
        id = Player.SteamID
        if DataStore.ContainsKey("DeathMSGBAN", id):
            get = DataStore.Get("DeathMSGBAN", id)
            loc = self.Replace(get)
            newloc = Util.CreateVector(float(loc[0]), float(loc[1]), float(loc[2]))
            Player.TeleportTo(newloc)
            config = self.DeathMSGConfig()
            deathmsgname = config.GetSetting("Settings", "deathmsgname")
            Player.MessageFrom(deathmsgname, self.green + "You got teleported back where you died!")
            DataStore.Remove("DeathMSGBAN", id)

    def On_PlayerConnected(self, Player):
        ini = self.DMB()
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        config = self.DeathMSGConfig()
        deathmsgname = config.GetSetting("Settings", "deathmsgname")
        ip = Player.IP
        if ini.GetSetting("Ips", ip) is not None and int(ini.GetSetting("Ips", ip)) == 1:
            Player.MessageFrom(deathmsgname, "You are banned from this server")
            Player.Disconnect()
        elif ini.GetSetting("Ids", id) is not None and int(ini.GetSetting("Ids", id)) == 1:
            Player.MessageFrom(deathmsgname, "You are banned from this server")
            Player.Disconnect()

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
            Plugin.Log("KillLog", " Killer: " + killer + " Gun: " + weapon + " Dist: " + str(dist) + " Victim: " + victim + " BodyP: " + body + " DMG: " + str(dmg))
        else:
            Plugin.Log("KillLog", " Killer: " + killer + " Gun: " + weapon + " Dist: " + str(dist) + " Victim: " + victim + " BodyP: " + body + " DMG: " + str(dmg) + " WAS TELEPORTING")

    def IsAnimal(self, killer):
        if killer == 'Wolf' or killer == 'Bear' or killer == 'MutantWolf' or killer == 'MutantBear':
            return True
        return False

    def WasSuicide(self, killer, victim):
        if killer == victim:
            return True
        return False

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def BD(self, bodyp):
        ini = self.Bodies()
        name = ini.GetSetting("bodyparts", str(bodyp))
        return name

    def Bodies(self):
        return Plugin.GetIni("bodyparts")

    def DeathMSGConfig(self):
        return Plugin.GetIni("DeathMSGConfig")

    def DMB(self):
        return Plugin.GetIni("BannedPeopleDM")

    def GetPlayerUnBannedIP(self, name):
        ini = self.DMB()
        name = name.lower()
        checkdist = ini.EnumSection("NameIps")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIps", pl)
            if nameid is not None and pl.lower() == name:
                return pl
        return None

    def GetPlayerUnBannedID(self, name):
        ini = self.DMB()
        name = name.lower()
        checkdist = ini.EnumSection("NameIds")
        for pl in checkdist:
            nameid = ini.GetSetting("NameIds", pl)
            if nameid is not None and pl.lower() == name:
                return pl
        return None

    def RangeOf(self, weapon):
        ini = Plugin.GetIni("range")
        range = ini.GetSetting("range", weapon)
        return int(range)

    def Replace(self, s):
        s = re.sub('[(\)\]]', '', s)
        s = s.split(",")
        return s