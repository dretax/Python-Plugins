__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite

"""
    Class
"""

class Give:

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

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
        systemname = "Give"
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

    def On_Command(self, Player, cmd, args):
        if cmd == "give":
            if Player.Admin or self.isMod(Player.SteamID):
                if len(args) == 0:
                    Player.MessageFrom('Give', 'Usage: /give "PlayerName" "ItemName" "Amount"')
                    Player.MessageFrom('Give', 'Quote signs (") are required.')
                    return
                text = str.join(" ", args)
                n = ['"'.join(text[i:i+2]).replace('"', '').strip(' ') for i in range(0, len(text), 2)]
                if n[0] and n[1] and n[2]:
                    playerr = self.CheckV(Player, n[0])
                    if playerr is None:
                        return
                    if not n[2].isdigit():
                        Player.MessageFrom('Give', 'You must specify a quantity...')
                        return
                    inventory = Player.Inventory
                    inventory.AddItem(n[1], int(n[2]))
                    Player.MessageFrom('Give', 'Given ' + str(n[1]) + " " + str(n[2]) + " to " + playerr.Name)
                else:
                    Player.MessageFrom('Give', 'Usage: /give "PlayerName" "ItemName" "Amount"')
                    Player.MessageFrom('Give', 'Quote signs (") are required.')