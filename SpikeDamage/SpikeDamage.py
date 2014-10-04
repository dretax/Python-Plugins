__author__ = 'DreTaX'
__version__ = '1.0'

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

    def GetPlayer(self, name):
        name = Data.ToLower(name)
        for pl in Server.Players:
            if (Data.ToLower(pl.Name) == name):
                return pl
        return None

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Attacker != None and HurtEvent.Victim != None:
            if (HurtEvent.Attacker == HurtEvent.Victim):
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
        elif cmd == "spikedmgd":
            if len(args) == 0:
                Player.Message("Usage: /spikedmgd playername")
                return
            elif len(args) == 1:
                name = args[0]
                ini = self.SpikeL()
                id = Player.SteamID
                players = ini.EnumSection(id)
                i = 0
                counted = players.Length
                name = Data.ToLower(name)
                for playerid in players:
                    i += 1
                    nameof = ini.GetSetting(id, playerid)
                    lowered = Data.ToLower(nameof)
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