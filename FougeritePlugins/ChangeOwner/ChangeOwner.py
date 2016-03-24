__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""
green = "[color #009900]"
sysname = "ChangeOwner"


class ChangeOwner:
    """
        Methods
    """

    def On_PluginInit(self):
        Util.ConsoleLog("BannedPeople by " + __author__ + " Version: " + __version__ + " loaded.", False)

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
            if Player is not None:
                Player.MessageFrom(sysname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            if Player is not None:
                Player.MessageFrom(sysname, "Found [color#FF0000]" + str(count) +
                                   "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None


    def On_Command(self, Player, cmd, args):
        if cmd == "changeowner":
            if Player.Admin:
                if len(args) == 2:
                    player = self.CheckV(Player, args[0])
                    if player is not None:
                        if not args[1].isdigit():
                            Player.MessageFrom(sysname, "The id is only made of numbers")
                            return
                        c = 0
                        for x in World.Entities:
                            if x.OwnerID == args[1]:
                                x.ChangeOwner(player)
                                c += 1
                        Player.MessageFrom(sysname, "Successfully changed " + str(c) + " objects of " + player.Name)
                        player.MessageFrom(sysname, "You became an owner of " + str(c) + " objects")
                else:
                    Player.MessageFrom(sysname, "Usage: /changeowner TheNewOwnerPlayerName STEAMIDOfOldOwner")
        elif cmd == "changeowner2":
            if Player.Admin:
                if len(args) == 1:
                    player = self.CheckV(Player, args[0])
                    if player is not None:
                        DataStore.Add("ChangeOwner", Player.UID, player.UID)

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Entity is not None and HurtEvent.Attacker is not None:
            if HurtEvent.Attacker.Admin and DataStore.ContainsKey("ChangeOwner", HurtEvent.Attacker.UID):
                entity = HurtEvent.Entity
                player = Server.FindPlayer(DataStore.Get("ChangeOwner", HurtEvent.Attacker.UID))
                if player is not None:
                    c = 1
                    entity.ChangeOwner(player)
                    structs = entity.GetLinkedStructs()
                    for ent in structs:
                        ent.ChangeOwner(player)
                        c += 1
                    HurtEvent.Attacker.MessageFrom(sysname, "Successfully changed " + str(c) + " objects of "
                                                   + player.Name)
                    player.MessageFrom(sysname, "You became an owner of " + str(c) + " objects")
                    DataStore.Remove("ChangeOwner", HurtEvent.Attacker.UID)
