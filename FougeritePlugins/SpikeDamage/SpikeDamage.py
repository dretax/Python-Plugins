__author__ = 'DreTaX'
__version__ = '1.3'

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
        if check is not None:
            return True
        return False

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.1
    """

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        systemname = "[SpikeDamage]"
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Victim is not None:
            if self.TrytoGrabID(HurtEvent.Attacker) is None:
                return
            if HurtEvent.Attacker.SteamID == HurtEvent.Victim.SteamID:
                damage = HurtEvent.DamageAmount
                if damage == 10 or damage == 15:
                    HurtEvent.DamageAmount = 0
            else:
                if self.FriendOf(HurtEvent.Attacker.SteamID, HurtEvent.Victim.SteamID):
                    damage = HurtEvent.DamageAmount
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
                name = name.lower()
                for playerid in players:
                    nameof = ini.GetSetting(id, playerid)
                    if nameof.lower() == name:
                        ini.DeleteSetting(id, playerid)
                        ini.Save()
                        Player.Message("Player Removed from Whitelist")
                        return
                Player.Message("Player doesn't exist!")
        elif cmd == "spikedmgl":
            ini = self.SpikeL()
            id = Player.SteamID
            players = ini.EnumSection(id)
            for playerid in players:
                nameof = ini.GetSetting(id, playerid)
                Player.Message("Whitelisted: " + nameof)