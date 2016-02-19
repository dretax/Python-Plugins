__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

warps = {

}

OnlyAdminWarp = {

}

CanModsUseAdminWarp = {

}

# Little config here
SysName = "Warps"
AllowModsSetWarp = True
AllowModsDeleteWarp = True

EnableTeleportDelay = False
TeleportDelay = 10

# EAC will check if the player glitched at TP. This may not be Necessary
AllowEACToCheckTeleport = True


class Warps:

    def On_PluginInit(self):
        ini = self.Warps()
        enum = ini.EnumSection("Warps")
        enum2 = ini.EnumSection("AdminWarps")
        enum3 = ini.EnumSection("CanModsUse")
        for x in enum:
            s = ini.GetSetting("Warps", x)
            s = s.split(',')
            vector = Util.CreateVector(float(s[0]), float(s[1]), float(s[2]))
            warps[x.lower()] = vector
        for x in enum2:
            bl = self.bool(ini.GetSetting("AdminWarps", x))
            if bl is None:
                bl = False
            OnlyAdminWarp[x.lower()] = bl
        for x in enum3:
            bl = self.bool(ini.GetSetting("CanModsUse", x))
            if bl is None:
                bl = False
            CanModsUseAdminWarp[x.lower()] = bl

    def bool(self, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        return None

    def On_Command(self, Player, cmd, args):
        if cmd == "setwarp":
            if Player.Admin or (Player.Moderator and AllowModsSetWarp):
                if len(args) != 3:
                    Player.MessageFrom(SysName,
                                       "Usage: /setwarp name OnlyAdminWarp?(True/False) CanModsUseIfAdmin?(True/False)")
                    return
                if args[0].lower() in warps.keys():
                    Player.MessageFrom(SysName, "This warp already exists!")
                    return
                warps[args[0].lower()] = Player.Location
                onlyadmin = self.bool(args[1])
                canmodsuse = self.bool(args[2])
                if onlyadmin is None:
                    Player.MessageFrom(SysName, "Invalid OnlyAdminWarp parameter! Type TRUE OR FALSE !")
                    return
                if canmodsuse is None:
                    Player.MessageFrom(SysName, "Invalid CanModsUseIfAdmin parameter! Type TRUE OR FALSE !")
                    return

                ini = self.Warps()
                ini.AddSetting("Warps", args[0], str(Player.X) + "," + str(Player.Y) + "," + str(Player.Z))
                if onlyadmin:
                    ini.AddSetting("AdminWarps", args[0], str(onlyadmin))
                    ini.AddSetting("CanModsUse", args[0], str(canmodsuse))
                    OnlyAdminWarp[args[0]] = onlyadmin
                    CanModsUseAdminWarp[args[0]] = canmodsuse
                ini.Save()
                Player.MessageFrom(SysName, "Warp " + args[0] + " set!")
        elif cmd == "warp":
            if len(args) == 0:
                Player.MessageFrom(SysName, "Usage: /warp name")
                return
            warpname = args[0].lower()
            if warpname in warps.keys():
                Teleport = False
                if warpname in OnlyAdminWarp.keys():
                    if Player.Admin:
                        Teleport = True
                    elif Player.Moderator and warpname in CanModsUseAdminWarp.keys():
                        Teleport = True
                else:
                    Teleport = True
                if Teleport:
                    if not EnableTeleportDelay:
                        Player.TeleportTo(warps[warpname], AllowEACToCheckTeleport)
                        Player.MessageFrom(SysName, "Teleported to " + warpname + "!")
                    else:
                        List = Plugin.CreateDict()
                        List["Player"] = Player
                        List["Location"] = warps[warpname]
                        List["Name"] = warpname
                        Plugin.CreateParallelTimer("WarpDelay", TeleportDelay * 1000, List).Start()
                        Player.MessageFrom(SysName, "Teleporting in " + str(TeleportDelay) + " seconds!")
                else:
                    Player.MessageFrom(SysName, warpname + " is only for admins!")
            else:
                Player.MessageFrom(SysName, "Couldn't find warp " + warpname + "!")
        elif cmd == "deletewarp":
            if len(args) == 0:
                Player.MessageFrom(SysName, "Usage: /deletewarp name")
                return
            if Player.Admin or (Player.Moderator and AllowModsDeleteWarp):
                warpname = args[0].lower()
                warp = None
                if warpname not in warps.keys():
                    Player.MessageFrom(SysName, "Couldn't find " + warpname + "!")
                    return
                ini = self.Warps()
                enum = ini.EnumSection("Warps")
                for x in enum:
                    if x.lower() == warpname:
                        warp = x
                        break
                if warp is not None:
                    warps.pop(warp.lower())
                    OnlyAdminWarp.pop(warp.lower())
                    CanModsUseAdminWarp.pop(warp.lower())
                    ini.DeleteSetting("Warps", warp)
                    ini.DeleteSetting("AdminWarps", warp)
                    ini.DeleteSetting("CanModsUse", warp)
                    ini.Save()
                    Player.MessageFrom(SysName, warpname + " removed!")
                else:
                    Player.MessageFrom(SysName, "Couldn't find " + warpname + "!")
        elif cmd == "warps":
            warpns = ""
            for x in warps:
                warpns = warpns + x + ", "
            Player.MessageFrom(SysName, "===Warps===")
            Player.MessageFrom(SysName, warpns)

    def WarpDelayCallback(self, timer):
        timer.Kill()
        List = timer.Args
        Player = List["Player"]
        if not Player.IsOnline:
            return
        Location = List["Location"]
        name = List["Name"]
        Player.TeleportTo(Location, AllowEACToCheckTeleport)
        Player.MessageFrom(SysName, "Teleported to " + name + "!")

    def Warps(self):
        if not Plugin.IniExists("Warps"):
            homes = Plugin.CreateIni("Warps")
            homes.Save()
        return Plugin.GetIni("Warps")
