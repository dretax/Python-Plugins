__author__ = 'DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""


class SpikeDamage:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("SpikeDamage by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def SpikeL(self):
        if not Plugin.IniExists("SpikeL"):
            SpikeL = Plugin.CreateIni("SpikeL")
            SpikeL.Save()
        return Plugin.GetIni("SpikeL")

    def FriendOf(self, id, selfid):
        ini = self.SpikeL()
        check = ini.GetSetting(id, selfid)
        if (check != None):
            return True
        return False

    def GetPlayerName(self, name):
        try:
            name = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            Plugin.Log("SpikeDamage", "Error caught at getPlayer method. Player was null.")
            return None

    # Method provided by Spoock. Converted to Python by DreTaX
    def CheckV(self, Player, args):
        systemname = "[SpikeDamage]"
        Nickname = ""
        for i in xrange(-1, len(args)):
            i += 1
            Nickname += args[i] + " "
            Nickname = Data.Substring(Nickname, 0, len(Nickname) - 1)
            target = self.GetPlayerName(Nickname)
            if target is not None:
                return target

            else:
                cc = 0
                found = None
                for all in Server.Players:
                    name = all.Name.lower()
                    check = args[0].lower()
                    if check in name:
                        found = all.Name
                        cc += 1

                if (cc == 1):
                    target = self.GetPlayerName(found)
                    return target
                elif cc > 1:
                    Player.MessageFrom(systemname, "Found [color#FF0000]" + cc + " players[/color] with similar names. [color#FF0000]Use more correct name !")
                    return None
                elif cc == 0:
                    Player.MessageFrom(systemname, "Player [color#00FF00]" + Nickname + "[/color] not found")
                    return None

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Victim is not None:
            if HurtEvent.Attacker.SteamID == HurtEvent.Victim.SteamID:
                bleed = HurtEvent.DamageType
                damage = HurtEvent.DamageAmount
                if bleed == "Melee":
                    if damage == 10 or damage == 15:
                        HurtEvent.DamageAmount = 0
            else:
                if self.FriendOf(HurtEvent.Attacker.SteamID, HurtEvent.Victim.SteamID):
                    bleed = HurtEvent.DamageType
                    damage = HurtEvent.DamageAmount
                    if (bleed == "Melee"):
                        if damage == 10 or damage == 15:
                            HurtEvent.DamageAmount = 0

    def On_Command(self, Player, cmd, args):
        if cmd == "spikedmg":
            if len(args) == 0:
                Player.Message("---SpikeDamage---")
                Player.Message("Makes ur friends not to get dmg from ur spikes")
                Player.Message("/spikedmg - List Commands")
                Player.Message("/spikedmga name - Adds friend to whitelist")
                Player.Message("/spikedmgd name - Deletes friend from whitelist")
                Player.Message("/spikedmgl - Lists Friends in Whitelist")
        elif cmd == "spikedmga":
            if len(args) == 0:
                Player.Message("/spikedmga name - Adds friend to whitelist")
            elif len(args) > 0:
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                idof = playerr.SteamID
                name = str(playerr.Name)
                ini = self.SpikeL()
                ini.AddSetting(Player.SteamID, idof, name)
                ini.Save()
        elif cmd == "spikedmgd":
            if len(args) == 0:
                Player.Message("Usage: /spikedmgd playername")
                return
            elif len(args) > 0:
                name = args[0]
                ini = self.SpikeL()
                id = Player.SteamID
                players = ini.EnumSection(id)
                i = 0
                counted = len(players)
                name = name.lower()
                for playerid in players:
                    i += 1
                    nameof = ini.GetSetting(id, playerid)
                    lowered = nameof.lower()
                    if lowered == name:
                        ini.DeleteSetting(id, playerid)
                        ini.Save()
                        Player.Message("Player Removed from Whitelist")
                        return
                    if i == counted:
                        Player.Message("Player doesn't exist!")
                        return
        elif cmd == "spikedmgl":
            ini = self.SpikeL()
            id = Player.SteamID
            players = ini.EnumSection(id)
            for playerid in players:
                nameof = ini.GetSetting(id, playerid)
                Player.Message("Whitelisted: " + nameof)